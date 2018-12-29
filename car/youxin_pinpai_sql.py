#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che_youxin

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMysql

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.xin.com/quanguo/s/', callback= self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.brand-more > dl > dd > a').items():
            self.crawl(each.attr.href, callback= self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
        "url": response.url,
        "pinpai": response.doc('div.select-result > dl > dd > a').text(),
        "chexing": response.doc('#select2 > dd > a').text()
        }

    def on_result(self, result):
        if not result or not result['pinpai']:
            return

        kwargs = {  'host':'localhost',
                    'user':'root',
                    'passwd':'luoxue99',
                    'db':'youxin',
                    'charset':'utf8'}

        sql = ToMysql(kwargs)
        sql.into('che_pinpai', **result)