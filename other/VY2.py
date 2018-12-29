#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: VY

from pyspider.libs.base_handler import *

DIR_PATH = 'py/VY'

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.deal = Deal()
        self.pp = ''
        self.name2 = ''

    @every(minutes=24 * 60)
    def on_start(self):
        # self.crawl('http://thzthz.cc/forum.php?mod=forumdisplay&fid=181&filter=typeid&typeid=33', callback= self.index_page)
        # self.crawl('http://thzthz.cc/forum.php?mod=forumdisplay&fid=181&filter=typeid&typeid=35', callback= self.index_page)
        self.crawl('http://thzthz.cc/forum.php?mod=forumdisplay&fid=181&filter=typeid&typeid=36', callback= self.index_page)
        self.crawl('http://thzthz.cc/forum.php?mod=forumdisplay&fid=181&filter=typeid&typeid=38', callback= self.index_page)
        self.crawl('http://thzthz.cc/forum.php?mod=forumdisplay&fid=181&filter=typeid&typeid=39', callback= self.index_page)
        self.crawl('http://thzthz.cc/forum.php?mod=forumdisplay&fid=181&filter=typeid&typeid=49', callback= self.index_page)


        self.page_num = 1
        self.total_num = 280
        while self.page_num < self.total_num:
            url = 'http://thzbt.biz/forum-181-' + str(self.page_num) + '.html'
            self.crawl(url, callback= self.index_page)
            self.page_num += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a.s').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        s1 = response.doc('h1').text()
        name1 = s1[1:6]
        s2 = response.doc('#thread_subject').text()
        name2 = name1 + "/" + s2
        down1 = response.doc('p.attnm > a').attr('href')
        print(name1)
        dir_path = self.deal.mkDir(name2)
        self.deal.saveBrife(down1, dir_path, s2)
        if dir_path:
            imgs = response.doc('.t_f > img').items()
            count = 1
            for img in imgs:
                url = img.attr.src
                if url:
                    extension = self.deal.getEx(url)
                    file_name = s2 +str(count) + '.' + extension
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
        file_name = dir_path + "/" + name +".txt"
        f = open(file_name, "w+")
        f.write(content.encode('utf-8'))

    def getEx(self, url):
        extension = url.split('.')[-1]
        return extension

