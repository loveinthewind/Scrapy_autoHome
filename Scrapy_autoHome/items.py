# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAutohomeItem(scrapy.Item):
    category = scrapy.Field()
    # 定义两个属性：image_urls和images
    image_urls = scrapy.Field()
    images = scrapy.Field()
