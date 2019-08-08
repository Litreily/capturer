# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

from vmgirls.items import VmgirlsItem
from vmgirls.items import VmgirlsImagesItem

import os


class VmgirlsPipeline(object):
    '''Pipeline for every url of one theme, save theme info to json file'''
    def __init__(self, user_data_dir):
        '''Open file to save the exported Items'''
        self.user_data_dir = user_data_dir

        if not os.path.isdir(self.user_data_dir):
            os.makedirs(self.user_data_dir)

        self.girls_info = open(os.path.join(self.user_data_dir, 'vmgirls.json'), 'w+b')
        self.girls_exporter = JsonLinesItemExporter(self.girls_info, encoding='utf-8', indent=4)

    @classmethod
    def from_crawler(cls, crawler):
        '''Get user dir from global settings.py'''
        settings = crawler.settings
        return cls(settings.get('USER_DATA_DIR'))

    def open_spider(self, spider):
        '''Start exporting VmgirlsItem'''
        self.girls_exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, VmgirlsItem):
            self.girls_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.girls_exporter.finish_exporting()
        self.girls_info.close()


class VmgirlsImagesPipeline(ImagesPipeline):
    '''Get images from one theme'''
    def get_media_requests(self, item, info):
        if isinstance(item, VmgirlsImagesItem):
            for image_url in item['image_urls']:
                yield Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        url = request.url
        item = request.meta['item']
        path = os.path.join(item['title'], url.split('/')[-1])
        return path

    def item_completed(self, results, item, info):
        if isinstance(item, VmgirlsImagesItem):
            image_paths = [x['path'] for ok, x in results if ok]

            if not image_paths:
                raise DropItem("Item contains no images")
            return item
