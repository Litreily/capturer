#!/usr/bin/python3
# author: litreily
# date: 2018.02.05
# description: capture pictures from sina

import re
import urllib.request
import urllib
import os
import platform
from bs4 import BeautifulSoup

def getRootPath(uid):
    rootPath = {
        'Windows': 'D:/litreily/Pictures/python/sina/%s' % uid,
        'Linux': '/mnt/d/litreily/Pictures/python/sina/%s' % uid
    }.get(platform.system())
    if not os.path.isdir(rootPath):
        os.makedirs(rootPath)
    return rootPath

def getHtml(url, headers):
    try:
        req = urllib.request.Request(url, headers = headers)
        page = urllib.request.urlopen(req)
        html = page.read().decode('UTF-8')
    except Exception:
        print("get "+ url + " failed")
        return None
    return html

def getImgFromSina(uid, headers, path):
    filterMode = 1      # 0-all 1-original 2-pictures
    numOfPage = 1
    numOfBlog = 0
    numOfImg = 0

    # regular expression of imgList and img
    imgListReg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imgListPattern = re.compile(imgListReg)
    imgReg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/.{32,33}.(jpg|gif))"'
    imgPattern = re.compile(imgReg)
    
    print('start capture picture of uid:' + str(uid))
    while True:
        # https://weibo.cn/3261134763/profile?filter=1&page=1
        url = r'https://weibo.cn/'+ str(uid) +'/profile?filter='+ str(filterMode)  +'&page=' + str(numOfPage)

        # 1. get html of each page url
        html = getHtml(url, headers)
        
        # 2. parse the html and find all the imgList Url of each page
        soup = BeautifulSoup(html, "html.parser")
        # <div class="c" id="M_G4gb5pY8t"><div>
        blogs = soup.body.find_all(attrs={"id":re.compile(r"^M_")}, recursive=False)
        numOfBlog += len(blogs)
        imgUrls = []        
        for blog in blogs:
            blog = str(blog)
            imgListUrl = imgListPattern.findall(blog)
            if not imgListUrl:
                # 2.1 get img-url from blog that have only one pic
                imgUrls += imgPattern.findall(blog)
            else:
                # 2.2 get img-urls from blog that have group pics
                html = getHtml(imgListUrl[0], headers)
                imgUrls += imgPattern.findall(html)

        if not imgUrls:
            print('capture complete!')
            print('captured pages: %d, blogs: %d, imgs: %d' % (numOfPage, numOfBlog, numOfImg))
            print('directory: ' + path)
            break

        # 3. download all the imgs from each imgList
        print('PAGE '+ str(numOfPage) + ' with ' + str(len(imgUrls)) + ' images')
        for img in imgUrls:
            imgUrl = img[0].replace(img[1], 'large')
            numOfImg += 1
            try:
                urllib.request.urlretrieve(imgUrl, '{}/{}.{}'.format(path, numOfImg, img[2]))
                # display the raw url of images
                print('\t%d\t%s' % (numOfImg, imgUrl))
            except Exception as err:
                print(err)
                print('\t%d\t%s failed' % (numOfImg, imgUrl))
        numOfPage += 1
        print('')

def main():
    # uids = ['2657006573','2173752092','3261134763','2174219060']
    uid = '6128705439'
    path = getRootPath(uid)

    # cookie is form the above url->network->request headers
    cookies = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}

    # capture imgs from sina
    getImgFromSina(uid, headers, path)

if __name__ == '__main__':
    main()