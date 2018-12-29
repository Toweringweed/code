#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che_youxin

from pyspider.libs.base_handler import *
import MySQLdb


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
        "品牌": response.doc('div.select-result > dl > dd > a').text(),
        "车系": response.doc('#select2 > dd > a').text()
        }
    def on_result(self, result):
        try:
            conn = MySQLdb.connect('localhost', 'root', 'luoxue99')
            cur = conn.cursor()
            cur.execute('create database if not exists python2')
            conn.select_db('python2')
            cur.execute('create table test(id int, pinpai varchar(20), info varchar(20))')

            values = result
            for i in len(values):
                values.append((i, 'info'+str(i)))
                cur.executemany('insert into test values(%s,%s)', values)

            conn.commit()
            cur.close()
            conn.close()

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

