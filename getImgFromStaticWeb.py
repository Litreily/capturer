#!/usr/bin/python3
# get images from static web

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

# capture imgs from static web page
#dir = '/home/litreily/web/www/html/images'
dir = '/mnt/d/litreily/Pictures/python'
url = r"http://blog.csdn.net/ben_ben_niao/article/details/40677869"
html = getStaticHtml(url)
saveHtml(html)
saveImgFromStaticWeb(html,dir + '/static')
