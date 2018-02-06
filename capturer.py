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

def getHtml(url):
    global webType
    global encodeType

    page = urllib.request.urlopen(url)
    html = page.read().decode(encodeType[webType])
    return html
     
def saveHtml(html):
    txt='result.html'  
    f = open(txt,"w+")  
    f.write(html)

def saveImg(html): 
    reg = r'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)
    x = 0
    path = '/home/litreily/capturer.git/download'
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path+'/'
    for imgurl in imglist:
        urllib.request.urlretrieve(imgurl,'{}{}.jpg'.format(paths,x))
        x = x + 1
                                                               
url = r"http://blog.csdn.net/ben_ben_niao/article/details/40677869"
#url = r"https://weibo.com/p/1005052657006573/photos?from=page_100505&mod=TAB#place"
html = getHtml(url)
saveHtml(html)
saveImg(html)
