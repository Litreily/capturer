#!/usr/bin/python3
# author: litreily
# date: 2018:02:05
# description: capture web pages or pictures

import re
import urllib.request
import urllib
import os

webType = 'default'
encodeType = {'default':'UTF-8', 'sina':'gb2312'}

def getStaticHtml(url):
    global webType
    global encodeType

    page = urllib.request.urlopen(url)
    html = page.read().decode(encodeType[webType])
    return html

def getDynamicHtml(url, headers):
    global webType
    global encodeType

    req = urllib.request.Request(url, headers = headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode(encodeType[webType])
    return html

def saveHtml(html):
    txt='result.html'  
    f = open(txt,"w+")  
    f.write(html)

def saveImgFromStaticWeb(html, path): 
    reg = r'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imgUrls = imgre.findall(html)
    x = 0
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path+'/'

    for imgUrl in imgUrls:
        x = x + 1
        urllib.request.urlretrieve(imgUrl,'{}{}.jpg'.format(paths,x))
        print("%d.jpg" % (x))
                                                               
def saveImgFromSina(uid, dir):
    count = 0
    page = 1

    print('start capture picture of uid:' + str(uid))
    while True:
        reg = r'src="http://w(.{2})\.sinaimg.cn/(wap180|square)/(.{32,33}.(jpg|gif))" alt'
        imgre = re.compile(reg)
        url = r'http://weibo.cn/album/albummblog/?rl=11&fuid='+ str(uid) + '&page='+ str(page)
        # cookie is form the above url->network->request headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                   'Cookie': 'YOUR COOKIES IN THE ABOVE URL'}
        html = getDynamicHtml(url, headers)
        saveHtml(html)
        imgIds = imgre.findall(html)
        if len(imgIds) == 0:
            print("capture complete!")
            break;

        imgUrls = []
        for id in imgIds:
            imgUrl = 'http://w' + id[0] + '.sinaimg.cn/large/' + id[2]
            imgUrls.append(imgUrl)
        imgUrls.reverse()

        path = str(dir) + '/' + str(uid)
        if not os.path.isdir(path):
            os.makedirs(path)
        paths = path+'/'
        
        print('page '+ str(page))
        for imgUrl in imgUrls:
            count += 1
            # display the raw url of images
            print('%d\t%s' % (count, imgUrl))
            urllib.request.urlretrieve(imgUrl, '{}{}.{}'.format(paths, count, imgUrl[-3:]))
        page += 1
        print('')


dir = '/home/litreily/web/www/html/images'

# capture imgs from static web page
'''
url = r"http://blog.csdn.net/ben_ben_niao/article/details/40677869"
html = getStaticHtml(url)
saveHtml(html)
saveImgFromStaticWeb(html,dir + '/static')
'''

# capture imgs from sina
uids = ['2173752092', '2657006573']
uid = uids[1]
saveImgFromSina(uid, dir)
