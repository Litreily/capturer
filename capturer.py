#!/usr/bin/python3.5
# author: litreily
# date: 2018:02:05
# description: capture web pages or pictures

import re
import urllib.request
import urllib
import os
  
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('UTF-8')
    #print(html)
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
                                                               
html = getHtml(r"http://blog.csdn.net/ben_ben_niao/article/details/40677869")
saveHtml(html)
saveImg(html)
