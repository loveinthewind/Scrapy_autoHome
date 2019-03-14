# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from Scrapy_autoHome import settings

class ScrapyAutohomePipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        # os.path.dirname()获取当前文件的路径；os.path.join（）获取当前目录并拼接成新目录
        if not os.path.exists(self.path):  # 判断路径是否存在
            os.mkdir(self.path)

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']

        category_path = os.path.join(self.path,category)
        if not os.path.exists(category_path):
            # 如果没有该路径，即创建一个
            os.mkdir(category_path)
        for url in urls:
            image_name = url.split('_')[-1]  # 以下划线“_”进行切割并取最后一个单元
            request.urlretrieve(url,os.path.join(category_path,image_name))
        return item

# 重写 继承自ImagesPipeline
class autoHomeImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用
        # 其实这个方法本身就是去发送下载请求的
        requests_objs = super(autoHomeImagesPipeline, self).get_media_requests(item,info)  # super()直接调用父类对象
        for requests_obj in requests_objs:
            requests_obj.item = item
        return requests_objs

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        path = super(autoHomeImagesPipeline, self).file_path(request,response,info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE  # 拿到在setting.py定义的IMAGES_STORE图片下载的路径
        category_path = os.path.join(images_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/","")
        image_path = os.path.join(category_path,image_name)
        return image_path