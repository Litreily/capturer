#!/usr/bin/python3
# author: litreily
# date: 2018.03.07
# description: capture pictures from lofter

import requests
import random
import time
import re
import os

def getRootPath(username, sysType):
    if sysType == 'windows':
        rootPath = 'D:/litreily/Pictures/python/lofter/%s' % username
    else:
        rootPath = '/mnt/d/litreily/Pictures/python/lofter/%s' % username
    if not os.path.isdir(rootPath):
        os.makedirs(rootPath)
    return rootPath

def getHtml(url, data, headers):
    try:
        html = requests.post(url, data, headers = headers)
    except Exception as e:
        print("get "+ url + " failed\n" + str(e))
        return None
    return html

def getUserID(username):
    try:
        html = requests.get('http://' + username + '.lofter.com')
        idReg = r'src="http://www.lofter.com/control\?blogId=(.*)"'
        blogID = re.search(idReg, html.text).group(1)
        print('The blogID of %s is: %s' % (username, blogID))
        return blogID
    except Exception as e:
        print('get blogID from http://' +username + '.lofter.com failed\n' + str(e))
        return None

def getNextTimeStamp(html, timePattern):
    if not html:
        nextTimeStamp = round(time.time() * 1000)  # first timeStamp(ms)
    else:
        nextTimeStamp = timePattern.search(html).group(1)
    return str(nextTimeStamp)

def getImgUrlsFromBlog(username, blog, headers):
    imgUrls = []
    blogUrl = 'http://%s.lofter.com/post/%s' % (username, blog)
    blogHtml = requests.get(blogUrl, headers = headers).text
    imgUrls.extend(re.findall(r'bigimgsrc="(.*?)"', blogHtml))
    print('Blog\t%s\twith %d\tpictures' % (blogUrl, len(imgUrls)))
    return imgUrls

def downloadImg(imgUrl, path):
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    for i in range(1,2):
        try:
            imgRequest = requests.get(imgUrl, timeout=10)
            if imgRequest.status_code == 200:
                open(path, 'wb').write(imgRequest.content)
                break
        except requests.exceptions.ConnectionError as e:
            print('\tGet ' + imgUrl + ' error: Connection aborted')
            if i == 1:
                imgUrl = re.sub('^http://img.*?\.','http://img.',imgUrl)
                print('\tRetry ' + imgUrl)
            else:
                print('\tRetry fail')
        except Exception as e:
            print(e)
        finally:
            pass

def createQueryData(blogID, timeStamp, queryNumber):
    data = {'callCount':'1',
    'scriptSessionId':'${scriptSessionId}187',
    'httpSessionId':'',
    'c0-scriptName':'ArchiveBean',
    'c0-methodName':'getArchivePostByTime',
    'c0-id':'0',
    'c0-param0':'number:' + blogID,
    'c0-param1':'number:' + timeStamp,
    'c0-param2':'number:' + queryNumber,
    'c0-param3':'boolean:false',
    'batchId':'123456'}
    return data

def main():
    # prepare paramters
    username = 'litreily'
    blogID = getUserID(username)
    queryNumber = 20
    timePattern = re.compile('s%s\.time=(.*);s.*type' % (queryNumber-1))
    blogUrlPattern = re.compile(r's[\d]*\.permalink="([\w_]*)"') 
    
    # creat path to save imgs
    sysType = 'windows'
    rootPath = getRootPath(username, sysType)

    # parameters of post packet
    url = 'http://'+ username + '.lofter.com/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr'
    data = createQueryData(blogID, getNextTimeStamp(None, timePattern), str(queryNumber))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host': username + '.lofter.com',
        'Referer': 'http://' + username + '.lofter.com/view',
        'Accept-Encoding': 'gzip, deflate'
    }

    numOfBlogs = 0
    numOfImgs = 0
    indexOfImg = 0
    print('------------------------------- start line ------------------------------')
    while True:
        html = getHtml(url, data, headers).text
        # get urls of blogs: s3.permalink="44fbca_19a6b1b"
        newBlogs = blogUrlPattern.findall(html)
        numOfNewBlogs = len(newBlogs)
        numOfBlogs += numOfNewBlogs 

        if numOfNewBlogs != 0:
            print('NewBlogs:%d\tTotalBolgs:%d' % (numOfNewBlogs, numOfBlogs))
            # get imgUrls from newBlogs
            imgUrls = []
            for blog in newBlogs:
                imgUrls.extend(getImgUrlsFromBlog(username, blog, headers))
            numOfImgs += len(imgUrls)

            # download imgs
            for imgUrl in imgUrls:
                indexOfImg += 1
                path = '%s/%d.%s' % (rootPath, indexOfImg, re.search(r'(jpg|png|gif)', imgUrl).group(0))
                print('{}\t{}'.format(indexOfImg, path))
                downloadImg(imgUrl, path)
        
        if numOfNewBlogs != queryNumber:
            print('------------------------------- stop line -------------------------------')
            print('capture complete!')
            print('captured blogs:%d images:%d' % (numOfBlogs, numOfImgs))
            print('download path:' + rootPath)
            print('-------------------------------------------------------------------------')
            break

        data['c0-param1'] = 'number:' + getNextTimeStamp(html, timePattern)
        print('The next TimeStamp is : %s\n' % data['c0-param1'].split(':')[1])
        # wait a few second
        time.sleep(random.randint(2,5))

if __name__ == '__main__':
    main()