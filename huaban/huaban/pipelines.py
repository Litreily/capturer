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
from os.path import join, basename

from urllib.parse import urlparse

from PIL import Image

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

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
            yield Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        url_path = urlparse(request.url).path
        item = request.meta['item']
        board_title = item['board_title']
        # file path: IMAGE_STORE/images/[BOARD_TITLE]/[URL_PATH].jpg
        return join('images', board_title.replace(':', '-'), basename(url_path))

    def check_gif(self, image):
        if image.format == 'GIF':
            return True
        else:
            return image.info.get('version') in ['GIF89a', 'GIF87a']

    def get_images(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(BytesIO(response.body))

        if self.check_gif(orig_image):
            path += '.gif'
            abs_path = self.store._get_filesystem_path(path)
            self.store._mkdir(os.path.dirname(abs_path), info)

            # save gif image from reponse
            with open(abs_path, 'wb') as f:
                f.write(response.body)
            return None
        else:
            path += '.jpg'
            image, buf = self.convert_image(orig_image)

        yield path, image, buf

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
