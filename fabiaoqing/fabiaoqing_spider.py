#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: litreily
# date: 2019.09.15
'''按关键词爬取发表情网fabiaoqing.com的表情包'''

import requests
import os
import sys
from lxml import html


base_url = 'https://fabiaoqing.com/search/search/keyword/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}


def get_path(keyword):
    '''生成指定关键词对应的表情包存储路径'''
    home_path = os.path.expanduser('~')
    path = os.path.join(home_path, 'Pictures/python/表情包/' + keyword)
    if not os.path.isdir(path):
        os.makedirs(path)

    return os.path.realpath(path)


def get_imgs(keyword):
    '''爬取某一个关键词相关的所有表情包

    Args:
        keyword: 表情包关键词
    '''
    page_index = 0
    img_cnts = 0
    save_dir = get_path(keyword)
    while True:
        page_index = page_index + 1
        # https://fabiaoqing.com/search/search/keyword/抱抱/type/bq/page/1.html
        url = '{}{}/type/bq/page/{}.html'.format(base_url, keyword, page_index)
        response = requests.get(url, headers=headers).content
        page = html.fromstring(response)
        imgs = page.xpath(
            '//div[@class="searchbqppdiv tagbqppdiv"]//img/@data-original')

        print('爬取 "{}" 相关表情包第 {} 页:'.format(keyword, page_index))
        img_cnts = download_imgs(imgs, img_cnts, save_dir)

        if page_index == 20 or len(imgs) == 0:
            break

    return img_cnts, save_dir


def download_imgs(img_urls, starti, save_dir):
    '''下载单个页面内所有图片

    Args:
        img_urls: 关键词相关表情包某一分页的所有图片链接
        starti: 当前页面首个图片命名id
        save_dir: 图片存储路径
    '''
    fid = starti
    for img in img_urls:
        print('\t' + img)
        fid = fid + 1
        file_name = '{}.{}'.format(fid, os.path.basename(img).split('.')[-1])
        save_path = os.path.join(save_dir, file_name)

        try:
            with open(save_path, 'wb') as f:
                f.write(requests.get(img, headers=headers, timeout=20).content)
        except requests.exceptions.ConnectionError as ce:
            print(ce.strerror())
        except requests.exceptions.MissingSchema:
            print(img + ' missing schema')
        except requests.exceptions.ReadTimeout:
            print('get {} timeout, skip this item.'.format(img))
        finally:
            pass

    return fid


def usage():
    print('Usage:\n\t' + os.path.basename(sys.argv[0]) +
          ' [key1] [key2] [key3] ...\n')


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    print('============================================')
    for keyword in sys.argv[1:]:
        print('开始爬取关键词为 "{}" 的表情包:'.format(keyword))
        count, save_dir = get_imgs(keyword)
        print('共爬取 "{}" 表情包 {} 个'.format(keyword, count))
        print('文件存储于"{}"'.format(save_dir))
    print('\n爬取完成！')
    print('============================================')

if __name__ == "__main__":
    main()
