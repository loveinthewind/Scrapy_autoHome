# -*- coding: utf-8 -*-
import scrapy
from Scrapy_autoHome.items import ScrapyAutohomeItem

class AutohomeSpider(scrapy.Spider):
    name = 'autoHome'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/3704.html']

    def parse(self, response):
        # SelectorList -> list
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            #以上最后get()操作只会取到一份
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            #以上最后getall()操作提取所有的东西
            # for url in urls:
            #     # url = "https:"+url
            #     url = response.urljoin(url)
            #     print(url)
            # map()方法 可以去遍历列表，将列表中的每一项都执行某一个函数，再把函数的返回值当作一个新的列表返回回来
            urls = list(map(lambda url:response.urljoin(url),urls))
            item = ScrapyAutohomeItem(category=category,image_urls=urls)
            yield item