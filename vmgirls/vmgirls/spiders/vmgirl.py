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
        urls = response.xpath('//*[@id="content"][1]/ul/li/a/@href').extract()
        titles = response.xpath(
            '//*[@id="content"][1]/ul/li/a/text()').extract()

        item = VmgirlsItem()
        item['theme_urls'] = urls
        item['theme_titles'] = titles
        yield item

        for url, title in zip(urls, titles):
            save_path = os.path.join(self.user_data_dir, title)
            if not os.path.isdir(save_path):
                os.makedirs(save_path)

            yield Request(url, meta={'title': title}, callback=self.parse_page)

    def parse_page(self, response):
        '''Parse each page of girls'''
        urls = response.xpath(
            '//*[@class="post-content"]//img/@data-src').extract()
        item = VmgirlsImagesItem()
        item['image_urls'] = urls
        item['title'] = response.meta['title']
        yield item
