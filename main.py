#!/usr/bin/python3
# author: litreily
# date: 2018.03.06
# description: capture pictures from webs

import sina.sina_spider as sina
import lofter.lofter_spider as lofter
import toutiao.toutiao_spider as toutiao
import qqzone.qqzone_spider as qqzone

if __name__ == '__main__':
    webs = {
        '1': sina,
        '2': lofter,
        '3': toutiao,
        '4': qqzone
    }

    tips = '''please select web you want to caputer(1-4, default=1)
    1 - sina
    2 - lofter
    3 - toutiao
    4 - qqzone
You want to captuer from:'''

    select = input(tips)
    if select not in webs:
        select = '1'
    webs.get(select).main()
