# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter

from huaban.items import BoardItem
from huaban.items import PinItem


class HuabanPipeline(object):
    def __init__(self):
        '''Open file to save the exported BoardItem'''
        self.file = open('D:/litreily/Pictures/python/huaban/boards.json', 'w+b')
        self.item_exporter = JsonItemExporter(self.file, encoding='utf-8', indent=4)

    def open_spider(self, spider):
        '''Start exporting BoardItem'''
        self.item_exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, BoardItem):
            self.item_exporter.export_item(item)
        elif isinstance(item, PinItem):
            pass

        return item

    def close_spider(self, spider):
        '''finish exporting and close files'''
        self.item_exporter.finish_exporting()
        self.file.close()
