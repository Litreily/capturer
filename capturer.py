#!/usr/bin/python3
# author: litreily
# date: 2018:02:05
# description: capture web pages or pictures

import re
import urllib.request
import urllib
import os

def getHtml(url, headers):
    req = urllib.request.Request(url, headers = headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('UTF-8')
    return html

def saveHtml(path, name, html):
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path + '/' + name
    f = open(paths,"w")
    f.write(html)
                                                              
def getImgFromSina(uid, headers, path):
    filterMode = 1      # 0-all 1-original 2-pictures
    numOfPage = 1
    numOfBlog = 0
    numOfImg = 0
    
    path = str(path) + '/' + str(uid)
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path+'/'

    # regular expression of imgList and img
    imgListReg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imgReg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/.{32,33}.(jpg|gif))" alt'
    imgListre = re.compile(imgListReg)
    imgre = re.compile(imgReg)
    
    print('start capture picture of uid:' + str(uid))
    while True:
        url = r'https://weibo.cn/'+ str(uid) +'/profile?filter='+ str(filterMode)  +'&page=' + str(numOfPage)

        # 1. get html of each page url
        html = getHtml(url, headers)
        saveHtml(paths + 'html', 'page_' + str(numOfPage) +'.html', html)
        
        # 2. parse the html and find all the imgList Url of each page
        imgListUrls = imgListre.findall(html)
        if not imgListUrls:
            print('capture complete!')
            print('captured pages: %d, blogs: %d, imgs: %d' % (numOfPage, numOfBlog, numOfImg))
            print('directory: ' + path)
            break

        # 3. download all the imgs from each imgList
        print('PAGE '+ str(numOfPage))
        imgUrls = []
        for imglist in imgListUrls:
            # 3.1 get html of imglist
            numOfBlog += 1
            print('blog_'+ str(numOfBlog)+ '\t' + imglist)
            html = getHtml(imglist, headers)
            
            # 3.2 parse the html and find all the img url of each imglist
            imgs = imgre.findall(html)
            
            # 3.3 download imgs from each imglist
            for img in imgs:
                imgUrl = img[0].replace(img[1], 'large')
                numOfImg += 1
                # display the raw url of images
                print('\t%d\t%s' % (numOfImg, imgUrl))
                urllib.request.urlretrieve(imgUrl, '{}{}.{}'.format(paths, numOfImg, img[2]))

        numOfPage += 1
        print('')


#path = '/home/litreily/web/www/html/images'
path = '/mnt/d/litreily/Pictures/python'

# user id
uids = ['2657006573','2173752092','3261134763','6101208662','5688659894','2174219060']
uid = uids[5]

# cookie is form the above url->network->request headers
cookies = ''
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Cookie': cookies}

# capture imgs from sina
getImgFromSina(uid, headers, path + '/sina')
