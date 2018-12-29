#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-4-27 16:18:45
# Project: carrer

from pyspider.libs.base_handler import *
from personal.mysqldb import ToMysql
import re
import time
import requests
import random
import string
import threading
from datetime import datetime, timedelta

poster_path = r"E:/Mycarrer/movie/poster/"

kwargs = {'host': 'localhost',
                  'user': 'root',
                  'passwd': 'Myluoxue99..',
                  'db': 'movie',
                  'charset': 'utf8'}
sql = ToMysql(kwargs)

time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Cookie": 'll="108296"; bid=LLf2q1LDtP4; gr_user_id=c1cc9c4d-e2ae-4366-985c-398300f92a18; __utmt=1; _vwo_uuid_v2=FCFD5141788469C52A797782585D76A9|f9d1f481fdec8395fc8692b3713d43d5; _pk_id.100001.8cb4=9825bb1db0c607d4.1494382639.3.1494582453.1494406513.; _pk_ses.100001.8cb4=*; __utma=30149280.1591339123.1494382640.1494579221.1494581174.6; __utmb=30149280.2.10.1494581174; __utmc=30149280; __utmz=30149280.1494581174.6.6.utmcsr=localhost:5000|utmccn=(referral)|utmcmd=referral|utmcct=/task/movie_douban3:8cf9cb6075cc945514c2e140e03c2fe5'
        }
    }

    def __init__(self):
        self.adress = []
        self.proxy_file = r'E:/Mycarrer/proxy_list_c.txt'
        list_f = open(self.proxy_file, 'r')
        list_c = list_f.read().split('\n')
        list_f.close()
        for lc in list_c:
            lc_li = lc.split(',')
            adress = lc_li[0] + "://" + lc_li[1] + ":" + lc_li[2]
            self.adress.append(adress)

    def get_proxy(self):
        ip_proxy = []
        time_file = open(r'E:/Mycarrer/proxy_time.txt', 'r').read()
        time_file = datetime.strptime(time_file, '%Y-%m-%d %H:%M:%S')
        time_n = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        time_n = datetime.strptime(time_n, '%Y-%m-%d %H:%M:%S')
        time_during = (time_n - time_file).total_seconds()
        if time_during > 60*5:
            list_f = open(self.proxy_file, 'r')
            list_c = list_f.read().split('\n')
            list_f.close()
            for lc in list_c:
                lc_li = lc.split(',')
                ad = lc_li[0] + "://" + lc_li[1] + ":" + lc_li[2]
                ip_proxy.append(ad)
        else:
            ip_proxy = self.adress

        return ip_proxy

    @every(minutes=24 * 60)
    def on_start(self):
        ip_proxy = self.get_proxy()
        self.crawl('https://movie.douban.com/tag/', callback=self.index_page)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        ip_proxy = self.get_proxy()
        for each in response.doc('.article > table:nth-child(5) > tbody> tr > td > a').items():
            self.crawl(each.attr.href, callback=self.list_page)

    def list_page(self, response):
        ip_proxy = self.get_proxy()
        p_url = response.url
        page_num = 0
        page_total = response.doc('#content > div > div.article > div.paginator > a:nth-last-child(2)').text()

        if page_total:
            page_total_num = int(page_total)
        else:
            page_total_num = 0
        while page_num < page_total_num:
            num_start = page_num * 20
            url_a = p_url + "?start=" + str(num_start) + "&type=T"
            self.crawl(url_a, callback=self.ll_page)
            page_num += 1

    def ll_page(self, response):
        ip_proxy = self.get_proxy()
        for each in response.doc('tr.item > td:nth-child(1) > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        ip_proxy = self.get_proxy()
        for each in response.doc('#info > span:nth-child(1) > span:nth-child(2) > a').items():
            if re.match("https://movie.douban.com/celebrity/.*", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.dt_detail)

        for each in response.doc('#info > span:nth-child(3) > span:nth-child(2) > a').items():
            if re.match("https://movie.douban.com/celebrity/.*", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.sw_detail)

        for each in response.doc('.actor > span:nth-child(2) > a').items():
            if re.match("https://movie.douban.com/celebrity/.*", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.actor_detail)


        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        cc = [c.replace('</span>', '') for c in re.findall(re.compile(r'pl">(.*?)<br'), response.doc('#info').html())]
        cc = "--".join(c for c in cc)

        r1 = re.findall(re.compile(r'制片国家/地区:(.*?)--'), cc)
        r2 = re.findall(re.compile(r'又名:(.*?)--'), cc)
        r3 = re.findall(re.compile(r'llow">(.*)</a'), cc)
        r4 = re.findall(re.compile(r'集数:(.*?)--'), cc)
        r5 = re.findall(re.compile(r'链接:.*href="(.*?)"'), response.doc('#info').html())
        r6 = re.findall(re.compile('allstar(\d+).*rating'), response.doc("#hot-comments").html())
        r7 = re.findall(re.compile(r'单集片长:(.*)(.*?)--'), cc)

        title = response.doc('h1 > span').text()
        img_src = [i.attr.src for i in response.doc('#mainpic > a > img').items()][0]
        img_content = requests.get(img_src).content
        poster_name = title + str(time_now).replace('-', '').replace(' ', '').replace(':', '')
        ex = Tool().get_ex(img_src)
        path = poster_path + poster_name + ex
        Tool().sav_img(img_content, path)

        # 获取imdb评分

        IMDB_link = ''
        ri1 = ['']
        ri2 = ['']
        if r5:
            IMDB_link = r5[0].strip()
            imdb_page = requests.get(IMDB_link).text
            ri1 = re.findall(re.compile(r'<span itemprop="ratingValue">(.*?)</span>'), imdb_page)
            ri2 = re.findall(re.compile(r'itemprop="ratingCount">(.*?)</span>'), imdb_page)

        main_info = {
            "url": response.url,
            "title": title,
            "director": response.doc('a[rel="v:directedBy"]').text(),
            "screenwriter": response.doc('#info > span:nth-child(3) > span.attrs').text(),
            "actors": response.doc('.actor > span:nth-child(2)').text(),
            "leixing": '/'.join(lx.text() for lx in response.doc('span[property="v:genre"]').items()),
            "area": r1[0] if r1 else '',
            "firt_play": '/'.join(lf.text() for lf in response.doc('span[property="v:initialReleaseDate"]').items()),
            "run_time": response.doc('span[property="v:runtime"]').text(),
            "name_else": r2[0] if r2 else '',
            "IMDB_num": r3[0] if r3 else '',
            "IMDB_link": IMDB_link,
            "IMDB_rating": ri1[0] if ri1 else '',
            "IMDB_voters": ri2[0] if ri2 else '',
            "rating": response.doc('strong.rating_num').text(),
            "rating_people": response.doc('span[property="v:votes"]').text(),
            "summary": response.doc('#link-report > span:nth-child(1)').text(),
            "award": '\n'.join([aw.text() for aw in response.doc('.mod > .award').items()]),
            "comment_short": '\n\r'.join([cx.text() for cx in response.doc('#hot-comments > div > div > p').items()]),
            "comment_rating": '\n\r'.join(r6) if r6 else '',
            "season": response.doc('#season > option:nth-last-child(1)').text(),
            "jishu": r4[0] if r4 else '',
            "time_1ji": r7[0] if r7 else '',
            "poster_name": poster_name,
            "time_update": time_now
        }

        if not main_info:
            return
        sql.into('douban_main', **main_info)

    def dt_detail(self, response):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        dt_info={
            "dt_name": response.doc('h1').text(),
            "dt_info": '\n'.join([dtx.text().replace('\n', '').replace(' ', '') for dtx in response.doc('#headline > div.info > ul > li').items()]),
            "dt_intro": response.doc('#intro > div.bd').text(),
            "time_update": time_now
        }
        if not dt_info:
            return
        sql.into('douban_dt', **dt_info)

    def sw_detail(self, response):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sw_info = {
            "sw_name": response.doc('h1').text(),
            "sw_info": '\n'.join([dtx.text().replace('\n', '').replace(' ', '') for dtx in response.doc('#headline > div.info > ul > li').items()]),
            "sw_intro": response.doc('#intro > div.bd').text(),
            "time_update": time_now
        }

        if not sw_info:
            return
        sql.into('douban_sw', **sw_info)

    def actor_detail(self, response):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        actor_info = {
            "actor_name": response.doc('h1').text(),
            "actor_info": '\n'.join([dtx.text().replace('\n', '').replace(' ', '') for dtx in response.doc('#headline > div.info > ul > li').items()]),
            "actor_intro": response.doc('#intro > div.bd').text(),
            "time_update": time_now
        }
        if not actor_info:
            return
        sql.into('douban_actor', **actor_info)

class Tool:
    def sav_img(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def get_ex(self, img_src):
        extension = '.' + img_src.split('.')[-1].strip()
        return extension

