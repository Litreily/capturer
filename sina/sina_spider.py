#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: litreily
# date: 2018.02.05
"""Capture pictures from sina-weibo with user_id."""

import re
import os

import socket
import urllib.request

from bs4 import BeautifulSoup


def _get_path(uid):
    home_path = os.path.expanduser('~')
    path = os.path.join(home_path, 'Pictures/python/sina', uid)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def _get_html(url, headers):
    try:
        req = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(req)
        html = page.read().decode('UTF-8')
    except Exception as e:
        print("get %s failed" % url)
        return None
    return html


def _capture_images(uid, headers, path):
    filter_mode = 1      # 0-all 1-original 2-pictures
    num_pages = 1
    num_blogs = 0
    num_imgs = 0

    # regular expression of imgList and img
    imglist_reg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imglist_pattern = re.compile(imglist_reg)
    img_reg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/.{32,33}.(jpg|gif))"'
    img_pattern = re.compile(img_reg)

    print('start capture picture of uid:' + uid)
    while True:
        url = 'https://weibo.cn/%s/profile?filter=%s&page=%d' % (
            uid, filter_mode, num_pages)

        # 1. get html of each page url
        html = _get_html(url, headers)
        if html == None:
            print('\nPlease check your cookies in sina/sina_spider.py!\n')
            break

        # 2. parse the html and find all the imgList Url of each page
        soup = BeautifulSoup(html, "lxml")
        # <div class="c" id="M_G4gb5pY8t"><div>
        blogs = soup.body.find_all(
            attrs={'id': re.compile(r'^M_')}, recursive=False)
        num_blogs += len(blogs)

        if num_pages == 1:
            # get number of pages
            max_pages = soup.find('input', attrs={'name': 'mp'}).attrs['value']

        imgurls = []
        for blog in blogs:
            blog = str(blog)
            imglist_url = imglist_pattern.findall(blog)
            if not imglist_url:
                # 2.1 get img-url from blog that have only one pic
                imgurls += img_pattern.findall(blog)
            else:
                # 2.2 get img-urls from blog that have group pics
                html = _get_html(imglist_url[0], headers)
                imgurls += img_pattern.findall(html)

        if num_pages > int(max_pages):
            print('capture complete!')
            print('captured pages:%d, blogs:%d, imgs:%d' %
                  (num_pages - 1, num_blogs, num_imgs))
            print('directory:' + path)
            break

        # 3. download all the imgs from each imgList
        print('PAGE {}/{} with {} images'.format(num_pages, max_pages, len(imgurls)))
        for img in imgurls:
            imgurl = img[0].replace(img[1], 'large')
            num_imgs += 1
            count = 1
            try:
                urllib.request.urlretrieve(
                    imgurl, '{}/{}.{}'.format(path, num_imgs, img[2]))
            except socket.timeout:
                while count <= 3:
                    try:
                        urllib.request.urlretrieve(
                            imgurl, '{}/{}.{}'.format(path, num_imgs, img[2]))
                        break
                    except socket.timeout:
                        count += 1
            finally:
                # display the raw url of images
                print('\t%d\t%s' % (num_imgs, imgurl))
                if count > 3:
                    print('\t%d\t%s failed' % (num_imgs, imgurl))
                pass
        num_pages += 1
        print('')


def main():
    uids = ['3261134763', '2173752092']
    uid = uids[0]
    path = _get_path(uid)
    socket.setdefaulttimeout(20)

    # cookie is form the above url->network->request headers
    cookies = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Cookie': cookies}

    # capture imgs from sina
    _capture_images(uid, headers, path)


if __name__ == '__main__':
    main()
