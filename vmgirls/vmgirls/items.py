# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field


class VmgirlsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    title = Field()
    pass

class VmgirlsImagesItem(Item):
    image_urls = Field()
    title = Field()
    pass
