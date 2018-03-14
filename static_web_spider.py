#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""Get images from static web."""

import re
import os

import urllib
import urllib.request


def _get_static_html(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('UTF-8')
    return html


def _save_html(html):
    txt='result.html'
    f = open(txt,"w+")  
    f.write(html)


def _download_images(html, path): 
    imgurls = re.findall(r'src="(http.+?\.jpg)"', html)
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path+'/'

    x = 0
    for imgurl in imgurls:
        x = x + 1
        urllib.request.urlretrieve(imgurl,'{}{}.jpg'.format(paths,x))
        print(str(x) + '.jpg')


def main():
    """capture imgs from static web page"""
    dir = '/mnt/d/litreily/Pictures/python'
    url = r'http://blog.csdn.net/ben_ben_niao/article/details/40677869'
    html = _get_static_html(url)
    _save_html(html)
    _download_images(html, dir + '/static')


if __name__ == '__main__':
    main()