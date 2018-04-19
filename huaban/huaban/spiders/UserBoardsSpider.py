# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.http import Headers

import re

import json

from huaban.items import BoardItem
from huaban.items import PinItem


class UserboardsspiderSpider(Spider):
    name = 'UserBoardSpider'
    # user_name = 'meirijingxuan'
    # user_name = 'dsk1985'
    user_name = 'litreily'
    host_name = 'http://huaban.com'

    allowed_domains = ['huaban.com']
    start_urls = ['{0}/{1}/'.format(host_name, user_name)]

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

            board_url = '{0}/boards/{1}'.format(self.host_name, board['board_id'])
            yield Request(board_url, callback=self.parse_pins)
        
        # Get more boards info
        # Request parameters:
        #   max: the last board_id get from boards
        #   limit: default 10, it's the limit number of boards, can be modified
        board_req = '{0}/{1}/?jg0gcj0&max={2}&limit={3}&wfl=1'.format(self.host_name, 
        self.user_name, boards[-1]['board_id'], 10)
        yield Request(board_req, callback=self.parse)

    def parse_pins(self, response):
        board_data = json.loads(response.text, encoding='utf-8')
        pins = board_data['board'].get('pins')

        if not pins:
            return

        for pin in pins:
            item = PinItem()
            item['pin_id'] = pin['pin_id']
            item['board_id'] = pin['board_id']
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
            self.host_name, pins[-1]['board_id'], pins[-1]['pin_id'], 20)
        yield Request(pin_req, callback=self.parse_pins)

        pass
