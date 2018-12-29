#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-20 16:18:45
# Project: air

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMysql
import time;


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.tianqihoubao.com/aqi/', callback= self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.citychk > dl > dd > a').items():
            self.crawl(each.attr.href, callback= self.list_page)

    def list_page(self, response):
        for each in response.doc('div.box.p > ul > li > a').items():
            self.crawl(each.attr.href, callback= self.detail_page)    
  
    @config(priority=2)
    def detail_page(self, response):
        return {
            "v_url": response.url,
            "v_city": response.doc('h1').text(),
            "v_day": response.doc('div.api_month_list > table > tr > td:nth-child(1)').text(),
            "v_AQI": response.doc('div.api_month_list > table > tr > td:nth-child(2)').text(),
            "v_rank": response.doc('div.api_month_list > table > tr > td:nth-child(3)').text(),
            "v_position": response.doc('div.api_month_list > table > tr > td:nth-child(4)').text(),
            "v_pm25": response.doc('div.api_month_list > table > tr > td:nth-child(5)').text(),
            "v_pm10": response.doc('div.api_month_list > table > tr > td:nth-child(6)').text(),
            "v_So2": response.doc('div.api_month_list > table > tr > td:nth-child(7)').text(),
            "v_No2": response.doc('div.api_month_list > table > tr > td:nth-child(8)').text(),
            "v_Co": response.doc('div.api_month_list > table > tr > td:nth-child(9)').text(),
            "v_O3": response.doc('div.api_month_list > table > tr > td:nth-child(10)').text(),
            "v_INS_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            
        }
    def on_result(self, result):
        kwargs = {  'host':'localhost',
                    'user':'root',
                    'passwd':'luoxue99',
                    'db':'air_quality',
                    'charset':'utf8'}

        if not result or not result['v_city']:
            return
        sql = ToMysql(kwargs)
        sql.into('air', **result)

