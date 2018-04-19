# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field


class HuabanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BoardItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    board_id = Field()
    category_id = Field()
    pin_count = Field()
    follow_count = Field()
    like_count = Field()
    pass


class PinItem(Item):
    pin_id = Field()
    board_id = Field()
    file_id = Field()
    file_key = Field()
    source = Field()
    tags = Field()
    pass
