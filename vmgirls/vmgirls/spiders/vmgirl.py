# -*- coding: utf-8 -*-
import scrapy

from vmgirls.items import VmgirlsItem
from vmgirls.items import VmgirlsImagesItem

from scrapy.http import Request
from scrapy.utils.project import get_project_settings

import os

class VmgirlSpider(scrapy.Spider):
    name = 'vmgirl'
    allowed_domains = ['vmgirls.com']
    start_urls = ['https://www.vmgirls.com/sitemap.shtml/']

    def __init__(self):
        settings = get_project_settings()
        self.user_data_dir = settings.get('USER_DATA_DIR')

    def parse(self, response):
        '''Parse sitemap'''
        urls = response.xpath('//*[@id="content"][1]/ul/li')
        for url in urls:
            item = VmgirlsItem()

            item['url'] = url.xpath('a/@href').extract_first()
            item['title'] = url.xpath('a/text()').extract_first()
            yield item

            save_path = os.path.join(self.user_data_dir, item['title'])
            if not os.path.isdir(save_path):
                os.makedirs(save_path)

            yield Request(item['url'], meta={'title': item['title']},
                          callback=self.parse_page)

    def parse_page(self, response):
        '''Parse each page of girls'''
        urls = response.xpath('//*[@class="post-content"]//img/@data-src').extract()
        item = VmgirlsImagesItem()
        item['image_urls'] = urls
        item['title'] = response.meta['title']
        yield item
