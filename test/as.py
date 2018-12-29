#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-02-18 16:29:21
# Project: test

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://movie.douban.com/tag/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://movie.douban.com/tag/\w+", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.list_page)

    def list_page(self, response):
        for each in response.doc('HTML>BODY>DIV#wrapper>DIV#content>DIV.grid-16-8.clearfix>DIV.article>DIV>TABLE TR.item>TD>DIV.pl2>A').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        # 翻页
        for each in response.doc('HTML>BODY>DIV#wrapper>DIV#content>DIV.grid-16-8.clearfix>DIV.article>DIV.paginator>A').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('HTML>BODY>DIV#wrapper>DIV#content>H1>SPAN').text(),
            "rating": response.doc('HTML>BODY>DIV#wrapper>DIV#content>DIV.grid-16-8.clearfix>DIV.article>DIV.indent.clearfix>DIV.subjectwrap.clearfix>DIV#interest_sectl>DIV.rating_wrap.clearbox>P.rating_self.clearfix>STRONG.ll.rating_num').text(),
            "导演": [x.text() for x in response.doc('a[rel="v:directedBy"]').items()],
        }
