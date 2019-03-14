# -*- coding: utf-8 -*-

# 说明：
# 通过分析缩略图和高清图的url，我们可以发现规律
# 缩略图url：https://car2.autoimg.cn/cardfs/product/g27/M00/61/3C/t_autohomecar__ChcCQFuw5z2ALnJmAAikSrj7qzw385.jpg
# 高清图url：https://car2.autoimg.cn/cardfs/product/g27/M00/61/3C/800x0_1_q87_autohomecar__ChcCQFuw5z2ALnJmAAikSrj7qzw385.jpg

# https://car3.autoimg.cn/cardfs/product/g27/M08/5D/61/800x0_1_q87_autohomecar__ChsEnVuw5zyASx0nAAdUKPZVVzY707.jpg
# https://car3.autoimg.cn/cardfs/product/g27/M08/5D/61/t_autohomecar__ChsEnVuw5zyASx0nAAdUKPZVVzY707.jpg
#
# https://car2.autoimg.cn/cardfs/product/g28/M09/C7/CE/800x0_1_q87_autohomecar__ChcCR1xhb7-AfHdmAAbYzH3AHVA666.jpg
# https://car2.autoimg.cn/cardfs/product/g28/M09/C7/CE/t_autohomecar__ChcCR1xhb7-AfHdmAAbYzH3AHVA666.jpg

# 获取所有高清图片
# 传统思路如下：找到更多获取接口的url，进入详情页--找到分页接口
# （显然这种情况会大大增加工作量，下面用Scrapy框架中的CrawlSpider进行爬取
# 因为CrawlSpider只要指定响应的规则，爬虫会自动爬取，省时省力）

# 分析url规律：
# “更多图片”的第一页url：https://car.autohome.com.cn/pic/series/3862-1.html
# ”更多图片“的第二页url：https://car.autohome.com.cn/pic/series/3862-1-p2.html


import scrapy
from scrapy.spiders import CrawlSpider, Rule  # 导入CrawlSpider模块  需改写原来的def parse(self, response)方法
from scrapy.linkextractors import LinkExtractor  # 导入链接提取模块
from Scrapy_autoHome.items import ScrapyAutohomeItem

class AutohomeHdSpider(CrawlSpider):
    name = 'autoHome_HD'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/172.html']

    rules = {
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/172.+'), callback='parse_page', follow=True)
        # 如果需要进行页面解释则使用callback回调函数
        # 因为有下一页，所以需要跟进，这里follow需要改为True
    }

    # 页面解析函数
    def parse_page(self, response):
    #     # SelectorList类型 -> list
    #     uiboxs = response.xpath("//div[@class='uibox']")[1:]  # 第一个不需要去除掉
    #     for uibox in uiboxs:
    #         category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()  # get()操作只会取到一份
    #         urls = uibox.xpath(".//ul/li/a/img/@src").getall()  # getall()操作提取所有的东西
    #         urls = list(map(lambda x:x.replace('t_','800x0_1_q87_'),urls))
    #         # for url in urls:
    #         #     # url = "https:"+url
    #         #     url = response.urljoin(url)
    #         #     print(url)
    #         # map()方法 可以去遍历列表，将列表中的每一项都执行某一个函数，再把函数的返回值当作一个新的列表返回回来
    #         # 将列表中的每一项进行遍历传递给lambda表达式，并执行函数中的代码，再以返回值以列表形式进行返回，结果为map对象，接着使用list转换为列表
    #         urls = list(map(lambda url: response.urljoin(url), urls))
    #         item = ScrapyAutohomeItem(category=category, image_urls=urls)
    #         yield item

        category = response.xpath(".//div[@class='uibox']/div/text()").get()
        srcs = response.xpath("//div[contains(@class, 'uibox-con')]/ul/li//img/@src").getall()
        # map(函数，参数二)，将参数二中的每个都就进行函数计算并返回一个列表
        srcs = list(map(lambda x:x.replace('t_','800x0_1_q87_'),srcs))
        # urls = {}
        # for src in srcs:
        #     url = response.url.join(src)
        #     urls.append(url)
        srcs = list(map(lambda x:response.urljoin(x),srcs))
        item = ScrapyAutohomeItem(category=category, image_urls=srcs)
        yield item
