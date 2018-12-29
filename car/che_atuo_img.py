#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: Img_auto

from pyspider.libs.base_handler import *

DIR_PATH = 'py/car'

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.deal = Deal()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.autohome.com.cn/car/', callback= self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.rankcar > .caricon-list > dd > a:nth-child(1)').items():
            self.crawl(each.attr.href, callback=self.list_page)

    def list_page(self, response):
        for each in response.doc('.rank-list-ul > li > h4 > a').items():
            self.crawl(each.attr.href, callback= self.ll_page)

    def ll_page(self, response):
        for each in response.doc('.interval01-list-related > div > a:nth-child(2)').items():
            self.crawl(each.attr.href, callback= self.detail_page)


    @config(priority=2)
    def detail_page(self, response):
        name = response.doc('.cartab-title > h2 > a').text()
        dir_path = self.deal.mkDir(name)
        if dir_path:
            imgs = response.doc('.uibox-con > ul > li >a > img').items()
            count = 1
            for img in imgs:
                url = img.attr.src
                if url:
                    extension = self.deal.getEx(url)
                    file_name = name +str(count) + '.'+ extension
                    count +=1
                    print(file_name)
                    self.crawl(img.attr.src, callback = self.saveImg,
                               save = {'dir_path': dir_path, 'file_name': file_name})

    def saveImg(self, response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
        self.deal.saveImg(content, file_path)



import os
class Deal:
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path=self.path+'/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self, path):
        path = path.strip()
        dir_path=self.path+path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path

    def saveImg(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def saveBrife(self, content, dir_path, name):
        file_name = dir_path + "/" +name +".txt"
        f = open(file_name, "w+")
        f.write(content.encode('utf-8'))

    def getEx(self, url):
        extension = url.split('.')[-1]
        return extension

