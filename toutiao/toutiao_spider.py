#!/usr/bin/env python3
"""
Description: Get pisture collections from www.toutiao.com
Tip:  This script comes from https://github.com/smslit/spider-collection/tree/master/ttpic
Link: https://www.smslit.top/2018/06/21/spider-practice-pic-dog/
"""
__author__ = '5km(smslit)'
__date__ = '20180627'

import os
import requests
from hashlib import md5
from functools import partial
from urllib.parse import urlencode
from multiprocessing.pool import Pool

PAGE_NUM = 5

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_page_json(offset, keyword):
    '''生成ajax请求，发出get请求，并获取响应结果，以字典的形式返回json数据
    :param offset: 页面请求偏移值
    :type offset: 能被20整除的整数
    :param keyword: 图片搜索的关键词
    :type keyword: unicode字符串
    :return: 响应数据
    :rtype: dict
    '''
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery'
    }

    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e)

def parse_images_url(json):
    '''解析json字典，获得对应条目标题和图片链接
    :param json: 页面请求响应结果对应的字典数据
    :type json: dict
    '''
    data = json['data']
    if data:
        for item in data:
            title = item['title']
            images = item['image_list']
            if images:
                for image in images:
                    yield {
                        'image': 'http:' + image['url'].replace('list', 'origin'),
                        'title': title
                    }

def save_image_from(image_info, to_dir=''):
    '''根据链接获取图片，保存到标题命名的目录中，图片以md5码命名
    :param image_info: 包含标题和链接信息的字典数据
    :type image_info: dict
    :param to_dir: 要保存到的目录，默认值是空字符串，可指定目录，格式如: '狗狗'
    :type to_dir: unicode 字符串
    '''
    if image_info:
        print(image_info)
        image_dir = to_dir + '/' + image_info['title']
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        try:
            response = requests.get(image_info['image'])
            if response.status_code == 200:
                image_path = '{0}/{1}.{2}'.format(image_dir, md5(response.content).hexdigest(), 'jpg')
                print(image_path)
                if not os.path.exists(image_path):
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print('图片下载完成！')
                else:
                    print('图片已下载 -> ', image_path)
        except requests.ConnectionError as e:
            print('图片下载失败！')
        except:
            print('出现异常！')

def get_images_of(offset, keyword):
    '''主函数，用于多进程调度
    :param offset: 页面链接offset参数的值
    :type offset: 能被20整除的整数
    :param keyword: 图片搜索关键词
    :type keyword: unicode字符串
    '''
    print('获取第', offset + 1, '～', offset + 20, '个条目...')
    json = get_page_json(offset, keyword)
    for image in parse_images_url(json):
        path = os.path.join(os.path.expanduser('~'), 'Pictures/python/toutiao', keyword)
        save_image_from(image, path)

def main():
    print('\nWelcome here to get pictures from www.toutiao.com!')
    keyword = input('Please input your search keywords > ')
    count = None
    while count == None:
        number_str = input('Please input count of picture collection that you want(Divisible by 20 ) > ')
        try:
            count = int(number_str)
        except ValueError:
            print('Please input a valid number!')

    if count > 0:
        print('Getting %s pictures...' % keyword)
        page_num = count // 20 + (0 if count % 20 == 0 else 1)
        offset_list = [x * 20 for x in range(0, page_num)]
        pool = Pool()
        partial_getter = partial(get_images_of, keyword=keyword)
        pool.map(partial_getter, offset_list)
        pool.close()
        pool.join()
    else:
        print('Get Cancel!')

if __name__ == '__main__':
    main()

