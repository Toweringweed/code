#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che_renren

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        city = ''
        pinpai = ''
        chexi = ''

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.renrenche.com/cn/', callback= self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#js-cities-pos > div.area-city-letter > div.area-line > a').items():
            self.crawl(each.attr.href, callback= self.list_page, validate_cert=False)

    def list_page(self, response):
        p_url = response.url
        self.page_num = 1
        self.total_num = 50
        while self.page_num <= self.total_num:
            url_a = p_url + "/ershouche/p" + str(self.page_num)
            self.crawl(url_a, callback=self.ll_page, validate_cert=False)
            self.page_num += 1

    def ll_page(self, response):
        for each in response.doc('li.car-item > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "标题": response.doc('.title > h1').text(),
            "车主信息": response.doc('p.owner-info').text(),
            "价格": response.doc('p.box-price').text(),
            "新车价": response.doc('p.bar-subscript').text(),
            "初登日期": response.doc('div.row-fluid-wrapper > ul > li:nth-child(1) > p > strong').text(),
            "行驶里程": response.doc('div.row-fluid-wrapper > ul > li:nth-child(2) > p > strong').text(),
            "环保标准": response.doc('div.row-fluid-wrapper > ul > li:nth-child(3) > p > strong').text(),
            "检测时间": response.doc('#report > div > div > p > span:nth-child(1)').text(),
            "车身颜色": response.doc('div.card-table > table > tr:nth-child(1) > td:nth-child(2)').text(),
            "归属地": response.doc('#report > div > div > div.card-table > table > tr:nth-child(2) > td:nth-child(2)').text(),
            "过户次数": response.doc('#report > div > div > div.card-table > table > tr:nth-child(2) > td:nth-child(4)').text(),
            "有无购车发票": response.doc('div.card-table > table > tr:nth-child(2) > td:nth-child(6)').text(),
            "有无改装": response.doc('div.card-table > table > tr:nth-child(3) > td:nth-child(2)').text(),
            "车型": response.doc('#tab-option-2 > ul > li:nth-child(1) > p > span.node-right').text(),
            "发动机": response.doc('#tab-option-2 > ul > li:nth-child(2) > p > span.node-right').text(),
            "变速箱": response.doc('#tab-option-2 > ul > li:nth-child(3) > p > span.node-right').text(),
            "长宽高": response.doc('#tab-option-2 > ul > li:nth-child(4) > p > span.node-right').text(),
            "轴距": response.doc('#tab-option-2 > ul > li:nth-child(5) > p > span.node-right').text(),
            "车身结构": response.doc('#tab-option-2 > ul > li:nth-child(6) > p > span.node-right').text(),
            "整备质量": response.doc('#tab-option-2 > ul > li:nth-child(7) > p > span.node-right').text(),
            "发动机参数": response.doc('#tab-option-3 > ul > li > p > span').text(),
            "底盘参数": response.doc('#tab-option-4 > ul > li > p > span').text(),
            "安全配置": response.doc('#tab-option-5 > ul > li > p > span').text()
        }

