# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from scrapy.exporters import JsonLinesItemExporter

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

from huaban.items import BoardItem
from huaban.items import PinItem

import os


class HuabanPipeline(object):
    def __init__(self, user_data_dir):
        '''Open file to save the exported Items'''
        self.user_data_dir = user_data_dir

        if not os.path.isdir(self.user_data_dir):
            os.makedirs(self.user_data_dir)

        # save info of BoardItem
        self.board_info = open(self.user_data_dir + 'boards.json', 'w+b')
        self.board_exporter = JsonItemExporter(self.board_info, encoding='utf-8', indent=4)

        # save info of PinItem
        self.pin_info = open(self.user_data_dir + 'pins.json', 'w+b')
        self.pin_exporter = JsonLinesItemExporter(self.pin_info, encoding='utf-8', indent=4)
    
    @classmethod
    def from_crawler(cls, crawler):
        '''get some global settings from settings.py'''
        settings = crawler.settings
        return cls(settings.get('USER_DATA_DIR'))

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


class HuabanImagesPipeline(ImagesPipeline):
    '''Implement image downloader by inherit class ImagesPipeline'''
    def get_media_requests(self, item, info):
        if isinstance(item, PinItem):
            image_url = 'http://img.hb.aicdn.com/' + item['file_key']
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
