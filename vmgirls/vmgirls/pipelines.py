# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter

from vmgirls.items import VmgirlsItem

import os

class VmgirlsPipeline(object):
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

