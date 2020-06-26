# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.http import Headers
from scrapy.utils.project import get_project_settings

import re

import json

from huaban.items import BoardItem
from huaban.items import PinItem


class UserboardsspiderSpider(Spider):
    name = 'UserBoardSpider'
    allowed_domains = ['huaban.com']

    def __init__(self):
        settings = get_project_settings()
        self.username = settings.get('USERNAME')
        self.hostname = 'http://huaban.com'
        self.start_urls = ['{0}/{1}/'.format(self.hostname, self.username)]

    def parse(self, response):
        '''Get boards info from home page of user'''
        # Enable below comments need disable huabanDownloaderMiddleware
        # data = response.xpath('body/script[1]').extract_first()
        # user_page = re.search('app\.page\["user"\]\s*=\s*({.*});', data)[1]
        # info = json.loads(user_page, encoding='utf-8')
        # boards = info.get('boards')

        info = json.loads(response.text, encoding='utf-8')
        boards = info['user'].get('boards')

        if not boards:
            return

        # Get BoardItem and capture all boards
        for board in boards:
            item = BoardItem()
            item['title'] = board['title']
            item['board_id'] = board['board_id']
            item['category_id'] = board['category_id']
            item['pin_count'] = board['pin_count']
            item['follow_count'] = board['follow_count']
            item['like_count'] = board['like_count']
            yield item

            board_url = '{0}/boards/{1}'.format(self.hostname,
                                                board['board_id'])
            yield Request(board_url, meta={'board_title': board['title']}, callback=self.parse_pins)

        # Get more boards info
        # Request parameters:
        #   max: the last board_id get from boards
        #   limit: default 10, it's the limit number of boards, can be modified
        board_req = '{0}/{1}/?jg0gcj0&max={2}&limit={3}&wfl=1'.format(self.hostname,
                                                                      self.username, boards[-1]['board_id'], 10)
        yield Request(board_req, callback=self.parse)

    def parse_pins(self, response):
        board_data = json.loads(response.text, encoding='utf-8')
        pins = board_data['board'].get('pins')
        board_title = response.meta['board_title']

        if not pins:
            return

        for pin in pins:
            item = PinItem()
            item['pin_id'] = pin['pin_id']
            item['board_id'] = pin['board_id']
            item['board_title'] = board_title
            item['file_id'] = pin['file_id']
            item['file_key'] = pin['file']['key']
            item['source'] = pin['source']
            item['tags'] = pin['tags']
            yield item

        # Get more pins info
        # Request parameters:
        #   max: the last pin_id get from pins
        #   limit: default 20, it's the limit number of pins, can be modified
        pin_req = '{0}/boards/{1}/?jg6nr2rm&max={2}&limit={3}&wfl=1'.format(
            self.hostname, pins[-1]['board_id'], pins[-1]['pin_id'], 20)
        yield Request(pin_req, meta={'board_title': board_title}, callback=self.parse_pins)
