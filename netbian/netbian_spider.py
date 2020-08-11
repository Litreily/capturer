#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from lxml import html
from multiprocessing import Pool, cpu_count


class NetbianSpider(object):
    def __init__(self):
        self.index = 'http://pic.netbian.com'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }

    def get_path(self, name):
        home_path = os.path.expanduser('~')
        path = os.path.join(home_path, 'Pictures/python/netbian/' + name)
        if not os.path.isdir(path):
            os.makedirs(path)

        return os.path.realpath(path)

    def get_categories(self):
        '''get categories of website'''
        res = requests.get(self.index, headers=self.headers)
        doc = html.fromstring(res.content)
        categories = doc.xpath('//div[contains(@class, "classify")]/a')

        for category in categories:
            name = category.xpath('text()')[0]
            url = category.xpath('@href')[0]
            yield name, url

    def spider_by_category(self, category, url):
        '''Process function which use to capture images base on category'''
        path_category = self.get_path(category)
        detail_pages, page_cnt = self.parse_thumb_page(url, first_page=True)

        img_cnt = 0
        page_num = 1
        while True:
            for page in detail_pages:
                img_cnt += 1

                print('[{} page-{} img-{}] Parsing page {}'.format(
                    category, page_num, img_cnt, page))
                img_url = self.parse_detail_page(page)
                self.download_image(img_url, path_category)

            page_num += 1
            if page_num > page_cnt:
                break
            detail_pages = self.parse_thumb_page(
                '{}index_{}.html'.format(url, page_num))

    def parse_thumb_page(self, url, first_page=False):
        '''parse thumbnail page and get all the detail pages url'''
        res = requests.get(self.index + url, headers=self.headers)
        doc = html.fromstring(res.content)
        detail_pages = doc.xpath('//div[@class="slist"]//a/@href')

        if first_page:
            page_cnt = doc.xpath(
                '//span[@class="slh"]/following-sibling::a[1]/text()')[0]
            return detail_pages, int(page_cnt)
        else:
            return detail_pages

    def parse_detail_page(self, url):
        '''parse detail page and get source image url'''
        res = requests.get(self.index + url, headers=self.headers)
        doc = html.fromstring(res.content)
        img_url = doc.xpath('//*[@id="img"]/img/@src')[0]

        return img_url

    def download_image(self, url, path):
        img_name = url.split('/')[-1]
        save_path = os.path.join(path, img_name)

        res = requests.get(self.index + url, headers=self.headers, timeout=20)
        if res.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(res.content)


def main():
    spider = NetbianSpider()
    categories = spider.get_categories()

    p = Pool(cpu_count())
    for name, url in categories:
        p.apply_async(spider.spider_by_category, args=(name, url))

    p.close()
    p.join()
    print('All Done!')


if __name__ == "__main__":
    main()
