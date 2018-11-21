# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BntoengItem(scrapy.Item):
    bangla_word = scrapy.Field()
    word_type = scrapy.Field()
    translation = scrapy.Field()
