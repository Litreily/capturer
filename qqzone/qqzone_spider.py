#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""一个用于下载QQ空间相册内所有照片的爬虫"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os
import re
import sys
import time
import logging
import requests
from json import loads


class qqzone(object):
    """QQ空间相册爬虫"""
    def __init__(self, user):
        self.username = user['username']
        self.password = user['password']
    
    @staticmethod
    def get_path(album_name):
        home_path = os.path.expanduser('~')
        path = os.path.join(home_path, 'Pictures/python/qqzone', album_name)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
    
    def _login_and_get_args(self):
        """登录QQ，获取Cookies和g_tk"""
        opt = webdriver.ChromeOptions()
        opt.set_headless()

        driver = webdriver.Chrome(chrome_options=opt)
        driver.get('https://i.qq.com/')

        logging.info('User {} login...'.format(self.username))
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(self.username)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(self.password)
        driver.find_element_by_id('login_button').click()

        time.sleep(1)
        driver.get('https://user.qzone.qq.com/{}'.format(self.username))

        try:
            logging.info('Getting g_tk...')
            self.g_tk = driver.execute_script('return QZONE.FP.getACSRFToken()')
            logging.debug('g_tk: {}'.format(self.g_tk))
        except WebDriverException:
            logging.error('Getting g_tk failed, please check your QQ number and password')
            driver.close()
            driver.quit()
            sys.exit(1)

        logging.info('Getting Cookies...')
        self.cookies = driver.get_cookies()

        driver.close()
        driver.quit()
    
    def _init_session(self):
        self.session = requests.Session()
        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        self.session.headers = {
            'Referer': 'https://qzs.qq.com/qzone/photo/v7/page/photo.html?init=photo.v7/module/albumList/index&navBar=1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
    
    def _get_query_for_request(self, topicId=None, pageStart=0, pageNum=100):
        """获取请求相册信息或照片信息所需的参数
        
        Args:
            topicId: 每个相册对应的唯一标识符
            pageStart: 请求某个相册的照片列表信息所需的起始页码
            pageNum: 单次请求某个相册的照片数量

        Returns:
            一个组合好所有请求参数的字符串
        """
        query = {
            'g_tk': self.g_tk,
            'hostUin': self.username,
            'uin': self.username,
            'appid': 4,
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'source': 'qzone',
            'plat': 'qzone',
            'format': 'jsonp'
        }
        if topicId:
            query['topicId'] = topicId
            query['pageStart'] = pageStart
            query['pageNum'] = pageNum
        return '&'.join('{}={}'.format(key, val) for key, val in query.items())
    
    def _load_callback_data(self, resp):
        """以json格式解析返回的jsonp数据"""
        try:
            resp.encoding = 'utf-8'
            data = loads(re.search(r'.*?\(({.*}).*?\).*', resp.text, re.S)[1])
            return data
        except ValueError:
            logging.error('Invalid input')

    def _get_ablum_list(self):
        """获取相册的列表信息"""
        album_url = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?' + self._get_query_for_request()

        logging.info('Getting ablum list id...')
        resp = self.session.get(album_url)
        data = self._load_callback_data(resp)

        album_list = {}
        for item in data['data']['albumListModeSort']:
            album_list[item['name']] = item['id']

        return album_list

    def _get_photo(self, album_name, album_id):
        """获取单个相册的照片列表信息，并下载该相册所有照片"""
        photo_list_url = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?' + self._get_query_for_request(topicId=album_id)

        logging.info('Getting photo list for album {}...'.format(album_name))
        resp = self.session.get(photo_list_url)
        data = self._load_callback_data(resp)
        if data['data']['totalInPage'] == 0:
            return None

        file_dir = self.get_path(album_name)
        for item in data['data']['photoList']:
            path = '{}/{}.jpg'.format(file_dir, item['name'])
            logging.info('Downloading {}-{}'.format(album_name, item['name']))
            self._download_image(item['url'], path)
    
    def _download_image(self, url, path):
        """下载单张照片"""
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                open(path, 'wb').write(resp.content)
        except requests.exceptions.Timeout:
            logging.warning('get {} timeout'.format(url))
        except requests.exceptions.ConnectionError as e:
            logging.error(e.__str__)
        finally:
            pass

    def start(self):
        """爬虫的入口函数"""
        self._login_and_get_args()
        self._init_session()
        album_list = self._get_ablum_list()
        for name, id in album_list.items():
            self._get_photo(name, id)


def get_user():
    """从终端获取用户输入的QQ号及密码"""
    username = input('please input QQ number: ').strip()
    if not re.match(r'^[1-9][0-9]{4,9}$', username):
        logging.error('\033[31mQQ number is wrong!\033[0m')
        sys.exit(1)

    import getpass
    password = getpass.getpass('password: ')
    
    return {
        'username': username,
        'password': password
    }


def main():
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    # 默认QQ账户信息
    user = {
        'username': '123456789',
        'password': '*********'
    }
    
    # 加 -d 参数可以使用上面的默认账户，默认信息请自行修改
    if not (len(sys.argv) > 1 and sys.argv[1] == '-d'):
        user = get_user()

    qz = qqzone(user)
    qz.start()


if __name__ == '__main__':
    main()

