# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from scrapy.exporters import JsonLinesItemExporter

from huaban.items import BoardItem
from huaban.items import PinItem


class HuabanPipeline(object):
    def __init__(self):
        '''Open file to save the exported Items'''
        # save info of BoardItem
        self.board_info = open('D:/litreily/Pictures/python/huaban/boards.json', 'w+b')
        self.board_exporter = JsonItemExporter(self.board_info, encoding='utf-8', indent=4)

        # save info of PinItem
        self.pin_info = open('D:/litreily/Pictures/python/huaban/pins.json', 'w+b')
        self.pin_exporter = JsonLinesItemExporter(self.pin_info, encoding='utf-8', indent=4)

    def open_spider(self, spider):
        '''Start exporting BoardItem'''
        self.board_exporter.start_exporting()
        self.pin_exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, BoardItem):
            self.board_exporter.export_item(item)
        elif isinstance(item, PinItem):
            self.pin_exporter.export_item(item)

        return item

    def close_spider(self, spider):
        '''finish exporting and close files'''
        self.board_exporter.finish_exporting()
        self.pin_exporter.finish_exporting()
        self.board_info.close()
        self.pin_info.close()
