# encoding: utf-8

from scrapy import cmdline

# 下载缩略图
# cmdline.execute("scrapy crawl autoHome".split())

# 下载高清图片
cmdline.execute("scrapy crawl autoHome_HD".split())
