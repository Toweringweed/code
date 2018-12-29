#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che_ranliao

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMysql


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)


    def on_start(self):
        i =1
        while i <=4062:
            url = 'http://chaxun.miit.gov.cn/asopCmsSearch/searchIndex.jsp?params=%257B%2522goPage%2522%253A' + str(i) + '%252C%2522orderBy%2522%253A%255B%257B%2522orderBy%2522%253A%2522pl%2522%252C%2522reverse%2522%253Afalse%257D%255D%252C%2522pageSize%2522%253A10%252C%2522queryParam%2522%253A%255B%257B%2522shortName%2522%253A%2522allRecord%2522%252C%2522value%2522%253A%25221%2522%257D%255D%257D&callback=jsonp1481768527900&_=1481769015490'
            self.crawl(url, callback= self.detail_page)
            i +=1

    @config(priority=2)
    def detail_page(self, response):
        return {
            "v_url": response.url,
            "v_shengchanqiye": response.text()
        }
