#!/usr/bin/python3
# author: litreily
# date: 2018.03.06
# description: capture pictures from webs

import sina_spider as sina
import lofter_spider as lofter

if __name__ == '__main__':
    webs = {
        '1': sina,
        '2': lofter
    }

    tips = '''please select web you want to caputer(1-2, default=1)
    1 - sina
    2 - lofter
You want to captuer from:'''

    select = input(tips)
    if select not in webs:
        select = '1'
    webs.get(select).main()