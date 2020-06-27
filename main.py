#!/usr/bin/env python3
# author: litreily
# date: 2018.03.06
# description: capture pictures from webs

from importlib import import_module

if __name__ == '__main__':
    webs = {
        '1': "sina",
        '2': "lofter",
        '3': "toutiao",
        '4': "qqzone",
        '5': 'telegram'
    }

    tips = 'please select web you want to caputer(1-{0}, default=1)\n'.format(len(webs)) + \
           ''.join(["\t{0} - {1}\n".format(i, webs.get(i)) for i in webs]) + \
           'You want to captuer from: '

    select = input(tips)
    if select not in webs:
        select = '1'

    module = "{0}.{0}_spider".format(webs.get(select))
    spider = import_module(module)
    spider.main()
