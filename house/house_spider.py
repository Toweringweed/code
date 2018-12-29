#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-11 10:51:14
# Project: house_spider

from pyspider.libs.base_handler import *
from personal.mysqldb import ToMysql
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://sz.esf.fang.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#kesfqbfylb_A01_03_01 > ul > li > a').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(age=10 * 24 * 60 * 60)
    def list_page(self, response):
        url = response.url
        for i in range(1, 100):
            list_url = url + r'/i3' + str(i)
            self.crawl(list_url, callback=self.ll_page)
            i = i + 1
            
    @config(age=10 *24 * 60 * 60)
    def ll_page(self, response):
        for each in response.doc('h4 > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)            

    @config(priority=2)
    def detail_page(self, response):
        uid = re.findall(re.compile(r'chushou/(.*?).htm'))
        uid = uid[0] if uid else ''
        tabs = response.doc('.trl-item1 > tt').text().split(' ')
        return {
            "url": response.url,
            "uid": uid,
            "title": response.doc('h1').text(),
            "zongjia": response.doc('').text(),
            "tag": response.doc('').text(),
            "huxing": tabs[0],
            "mianji": tabs[1],
            "price_i": tabs[2],
            "chaoxiang": tabs[3],
            "cengji": ,
            "zongcenggao": ,
            "zhuangxiu": ,
            "xiaoqu": response.doc('#kesfsfbxq_A01_01_05').text(),
            "quyu": response.doc('#kesfsfbxq_C03_07').text(),
            "jiedao": response.doc('#kesfsfbxq_C03_08').text()
            

        }


