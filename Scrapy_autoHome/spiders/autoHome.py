# -*- coding: utf-8 -*-
import scrapy
from Scrapy_autoHome.items import ScrapyAutohomeItem

class AutohomeSpider(scrapy.Spider):
    name = 'autoHome'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/3704.html']

    def parse(self, response):
        # SelectorList类型 -> list
        uiboxs = response.xpath("//div[@class='uibox']")[1:]  # 第一个不需要去除掉
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()  #get()操作只会取到一份
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()  #getall()操作提取所有的东西
            # for url in urls:
            #     # url = "https:"+url
            #     url = response.urljoin(url)
            #     print(url)
            # map()方法 可以去遍历列表，将列表中的每一项都执行某一个函数，再把函数的返回值当作一个新的列表返回回来
            # 将列表中的每一项进行遍历传递给lambda表达式，并执行函数中的代码，再以返回值以列表形式进行返回，结果为map对象，接着使用list转换为列表
            urls = list(map(lambda url:response.urljoin(url),urls))
            item = ScrapyAutohomeItem(category=category,image_urls=urls)
            yield item