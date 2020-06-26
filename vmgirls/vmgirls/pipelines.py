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

    @classmethod
    def from_crawler(cls, crawler):
        '''Get user dir from global settings.py'''
        settings = crawler.settings
        return cls(settings.get('USER_DATA_DIR'))

    def process_item(self, item, spider):
        '''Save item info to loacl file'''
        if isinstance(item, VmgirlsItem):
            self.girls_info = open(
                os.path.join(self.user_data_dir, 'vmgirls.json'), 'w+b')
            self.girls_exporter = JsonLinesItemExporter(
                self.girls_info, encoding='utf-8', indent=4)

            self.girls_exporter.start_exporting()

            for url, title in zip(item['theme_urls'], item['theme_titles']):
                single_item = {'theme_url': url, 'title': title}
                self.girls_exporter.export_item(single_item)

            self.girls_exporter.finish_exporting()
            self.girls_info.close()
        return item


class VmgirlsImagesPipeline(ImagesPipeline):
    '''Get images from one theme'''

    def get_media_requests(self, item, info):
        if isinstance(item, VmgirlsImagesItem):
            for image_url in item['image_urls']:
                yield Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        '''Set image dir to IMAGES_STORE/title/base_url'''
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
