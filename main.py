#!/usr/bin/python3
# author: litreily
# date: 2018:03:06
# description: capture pictures from sina

import getImgFromSina as sina

if __name__ == '__main__':
    path = '/mnt/d/litreily/Pictures/python'
    # user id
    uids = ['2657006573','2173752092','3261134763','2174219060']
    uid = uids[3]

    # cookie is form the above url->network->request headers
    cookies = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}

    # capture imgs from sina
    sina.getImgFromSina(uid, headers, path + '/sina')