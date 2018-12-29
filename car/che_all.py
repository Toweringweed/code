#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 14:01:59
# Project: che_all

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.chechong.com/maiche/', callback= self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.z_c>a').items():
            self.crawl(each.attr.href, callback= self.list_page)

    def list_page(self, response):
        p_url = response.url
        pinpai_url = p_url[:-2]
        for each in pinpai_url:
            while self.page_num <= self.total_num:
                url_a = pinpai_url + str(self.page_num)
                self.crawl(url_a, callback=self.ll_page)
                self.page_num += 1

    def ll_page(self, response):
        for each in response.doc('h4 > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "标题": response.doc('body>div.box.clearfix.mb55>div>div.detail_head_r>a> h3').text(),
            "使用情况": response.doc('div.detail_head_r>p').text(),
            "价格": response.doc('div.detail_price>div.price>p>span.fon36').text(),
            "原价": response.doc('div.detail_price>div.price>p>span.labs>label').text(),
            "过户次数": response.doc('.important_info > table > tr:nth-child(2) > td:nth-child(4)').text(),
            "用途": response.doc('.important_info > table > tr:nth-child(3) > td:nth-child(4)').text(),
            "生产厂商": response.doc('.mb50 > table > tr:nth-child(2)> td:nth-child(2)').text(),
            "上市时间": response.doc('.mb50 > table > tr:nth-child(2)> td:nth-child(4)').text(),
            "车型级别": response.doc('.mb50 > table > tr:nth-child(3)> td:nth-child(2)').text(),
            "车身结构": response.doc('.mb50 > table > tr:nth-child(3)> td:nth-child(4)').text(),
            "排气量": response.doc('.mb50 > table > tr:nth-child(4)> td:nth-child(2)').text(),
            "进气方式": response.doc('.mb50 > table > tr:nth-child(4)> td:nth-child(4)').text(),
            "变速箱": response.doc('.mb50 > table > tr:nth-child(5)> td:nth-child(2)').text(),
            "驱动形式": response.doc('.mb50 > table > tr:nth-child(5)> td:nth-child(4)').text(),
            "长宽高（mm）": response.doc('.mb50 > table > tr:nth-child(6)> td:nth-child(2)').text(),
            "轴距": response.doc('.mb50 > table > tr:nth-child(6)> td:nth-child(4)').text(),
            "最大功率": response.doc('.sy > table > tr:nth-child(1)> td:nth-child(2)').text(),
            "最大扭矩": response.doc('.sy > table > tr:nth-child(1)> td:nth-child(4)').text(),
            "最高车速": response.doc('.sy > table > tr:nth-child(2)> td:nth-child(2)').text(),
            "官方综合油耗（L/100km）": response.doc('.sy > table > tr:nth-child(2)> td:nth-child(4)').text(),
            "前轮胎规格": response.doc('.sy > table > tr:nth-child(3)> td:nth-child(2)').text(),
            "后轮胎规格": response.doc('.sy > table > tr:nth-child(3)> td:nth-child(4)').text(),
            "燃料标号": response.doc('.sy > table > tr:nth-child(4)> td:nth-child(2)').text(),
            "排放标准": response.doc('.sy > table > tr:nth-child(4)> td:nth-child(4)').text()
        }