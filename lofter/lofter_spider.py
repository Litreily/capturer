#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: litreily
# date: 2018.03.07
"""Capture pictures from lofter with username."""

import re
import os
import sys

import requests

import time
import random


def _get_path(uid):
    home_path = os.path.expanduser('~')
    path = os.path.join(home_path, 'Pictures/python/lofter', uid)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def _get_html(url, data, headers):
    try:
        html = requests.post(url, data, headers = headers)
    except Exception as e:
        print("get %s failed\n%s" % (url, str(e)))
        return None
    finally:
        pass
    return html


def _get_blogid(username):
    try:
        html = requests.get('http://%s.lofter.com' % username)
        id_reg = r'src="//www.lofter.com/control\?blogId=(.*)"'
        blogid = re.search(id_reg, html.text).group(1)
        print('The blogid of %s is: %s' % (username, blogid))
        return blogid
    except Exception as e:
        print('get blogid from http://%s.lofter.com failed' % username)
        print('please check your username.')
        exit(1)


def _get_timestamp(html, time_pattern):
    if not html:
        timestamp = round(time.time() * 1000)  # first timestamp(ms)
    else:
        timestamp = time_pattern.search(html).group(1)
    return str(timestamp)


def _get_imgurls(username, blog, headers):
    blog_url = 'http://%s.lofter.com/post/%s' % (username, blog)
    blog_html = requests.get(blog_url, headers = headers).text
    imgurls = re.findall(r'bigimgsrc="(.*?)"', blog_html)
    print('Blog\t%s\twith %d\tpictures' % (blog_url, len(imgurls)))
    return imgurls


def _capture_images(imgurl, path):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    for i in range(1,3):
        try:
            image_request = requests.get(imgurl, headers = headers, timeout = 20)
            if image_request.status_code == 200:
                open(path, 'wb').write(image_request.content)
                break
        except requests.exceptions.ConnectionError as e:
            print('\tGet %s failed\n\terror:%s' % (imgurl, e))
            if i == 1:
                imgurl = re.sub(r'^http://img.*?\.','http://img.',imgurl)
                print('\tRetry ' + imgurl)
            else:
                print('\tRetry fail')
        except Exception as e:
            print(e)
        finally:
            pass


def _create_query_data(blogid, timestamp, query_number):
    data = {'callCount':'1',
    'scriptSessionId':'${scriptSessionId}187',
    'httpSessionId':'',
    'c0-scriptName':'ArchiveBean',
    'c0-methodName':'getArchivePostByTime',
    'c0-id':'0',
    'c0-param0':'boolean:false',
    'c0-param1':'number:' + blogid,
    'c0-param2':'number:' + timestamp,
    'c0-param3':'number:' + query_number,
    'c0-param4':'boolean:false',
    'batchId':'123456'}
    return data


def main(argv):
    # prepare paramters
    if len(argv) < 2:
        print(os.path.basename(argv[0]) + ' username')
        exit(1)
    username = argv[1]
    blogid = _get_blogid(username)
    query_number = 40
    time_pattern = re.compile(r's%d\.time=(.*);s.*type' % (query_number-1))
    blog_url_pattern = re.compile(r's[\d]*\.permalink="([\w_]*)"')

    # creat path to save imgs
    path = _get_path(username)

    # parameters of post packet
    url = 'http://%s.lofter.com/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr' % username
    data = _create_query_data(blogid, _get_timestamp(None, time_pattern), str(query_number))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'Host': username + '.lofter.com',
        'Referer': 'http://%s.lofter.com/view' % username,
        'Accept-Encoding': 'gzip, deflate'
    }

    num_blogs = 0
    num_imgs = 0
    index_img = 0
    print('------------------------------- start line ------------------------------')
    while True:
        html = _get_html(url, data, headers).text
        # get urls of blogs: s3.permalink="44fbca_19a6b1b"
        new_blogs = blog_url_pattern.findall(html)
        num_new_blogs = len(new_blogs)
        num_blogs += num_new_blogs

        if num_new_blogs != 0:
            print('NewBlogs:%d\tTotalBolgs:%d' % (num_new_blogs, num_blogs))
            # get imgurls from new_blogs
            imgurls = []
            for blog in new_blogs:
                imgurls.extend(_get_imgurls(username, blog, headers))
            num_imgs += len(imgurls)

            # download imgs
            for imgurl in imgurls:
                index_img += 1
                paths = '%s/%d.%s' % (path, index_img, re.search(r'(jpg|png|gif)', imgurl).group(0))
                print('{}\t{}'.format(index_img, paths))
                _capture_images(imgurl, paths)

        if num_new_blogs != query_number:
            print('------------------------------- stop line -------------------------------')
            print('capture complete!')
            print('captured blogs:%d images:%d' % (num_blogs, num_imgs))
            print('download path:' + path)
            print('-------------------------------------------------------------------------')
            break

        data['c0-param2'] = 'number:' + _get_timestamp(html, time_pattern)
        print('The next TimeStamp is : %s\n' % data['c0-param2'].split(':')[1])
        # wait a few second
        time.sleep(random.randint(5,10))


if __name__ == '__main__':
    main(sys.argv)
