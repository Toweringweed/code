#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-4-27 16:18:45
# Project: carrer

from pyspider.libs.base_handler import *
from personal.mysqldb import ToMysql
import requests
import re
import time
from datetime import datetime, timedelta
import math

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Cookie": 'verynginx_sign_javascript=fd8afa2e5436fcb2cca40da1d5e74419; 91turn_114=1; tanwanpf_2289=1; Hm_lvt_e4ae1fda69701b5c57a33af8004da16a=1493861108,1494298755,1494485430,1494555204; Hm_lpvt_e4ae1fda69701b5c57a33af8004da16a=1494557265'

        }
    }

    @every(minutes=2 * 60)
    def on_start(self):
        self.crawl('http://www.piaohua.com/', callback= self.index_page)

    @config(age=30 * 60)
    def index_page(self, response):
        for each in response.doc('#menu > ul > li > a').items():
            self.crawl(each.attr.href, callback=self.list_page)

        for each in response.doc('#iml1 > ul > li > a.img').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(age=30 * 60)
    def list_page(self, response):
        p_url = response.url
        p_url = p_url.split('/')
        p_url = p_url[0:-1]
        p_url = '/'.join(i for i in p_url) + '/'
        page_num = 1
        page_total = response.doc('#nml > div:nth-child(2) > strong:nth-child(13)').text()

        if page_total:
            page_total_num = int(page_total)
        else:
            page_total_num = 1
        while page_num <= page_total_num:
            url_a = p_url + "list_" + str(page_num) + ".html"
            self.crawl(url_a, callback=self.ll_page)
            page_num += 1

    @config(age=30 * 60)
    def ll_page(self, response):
        for each in response.doc('#list > dl > dt > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(age=30 * 60)
    def item_handle(self, intro):
        intro_new = intro.replace('下载地址和剧情：', '').replace('◎', '')\
            .replace('片名', '-oo-片名').replace('年代', '-oo-年代').replace('类型', '-oo-类型').\
            replace('类别', '-oo-类别').replace('语言', '-oo-语言').replace('字幕', '-oo-字幕').\
            replace('上映日期', '-oo-上映日期').replace('IMD', '-oo-IMD', ).replace('豆瓣评分', '-oo-豆瓣评分').\
            replace('文件格式', '-oo-文件格式').replace('文件大小', '-oo-文件大小').replace('片长', '-oo-片长').\
            replace('导演', '-oo-导演').replace('主演', '-oo-主演').replace('简介', '-oo-简介').\
            replace('剧情', '-oo-剧情').replace('下载地址', '-oo-下载地址').replace('视频尺寸', '-oo-视频尺寸')
        return intro_new

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('h3').text()
        movie_update = response.doc('#showdesc').text()
        intro = response.doc('#showinfo').text()
        intro = intro.replace(' ', '').replace("\u3000", '').replace("\xa0", '')
        # intro_html = response.doc('#showinfo').html().replace(' ', '').replace('&nbsp;', '')
        movie_update = re.findall(re.compile('发布时间：(.+)'), movie_update)
        intro_new = self.item_handle(intro)
        r1 = re.findall(re.compile(r'译名(.*?)-oo-'), intro_new)
        r2 = re.findall(re.compile(r'片名(.*?)-oo-'), intro_new)
        r3 = re.findall(re.compile(r'年代(.*?)-oo-'), intro_new)
        if r3:
            if len(r3[0]) > 150:
                r3 = ''
        r4 = re.findall(re.compile(r'类[别型](.*?)-oo-'), intro_new)
        r5 = re.findall(re.compile(r'语言(.*?)-oo-'), intro_new)
        if r5:
            if len(r5[0]) > 50:
                r3 = ''
        r6 = re.findall(re.compile(r'字幕(.*?)-oo-'), intro_new)
        r7 = re.findall(re.compile(r'上映日期(.*?)-oo-'), intro_new)
        r20 = re.findall(re.compile(r'IMDB评分(.*?)-oo-',  re.IGNORECASE), intro_new)

        r20 = r20[0].replace(',', '') if r20 else ''
        if "from" in r20:
            r20_1 = re.findall(re.compile(r'(\d+.\d+)\D+from(\d+)\D+'), r20)
        else:
            r20_1 = re.findall(re.compile(r'(\d+.\d+)\D+(\d+)\D+'), r20)
        r20_2 = re.findall(re.compile(r'IMDB链接(.*?)-oo-',  re.IGNORECASE), intro_new)
        r8 = re.findall(re.compile(r'豆瓣评分(.*?)-oo-'), intro_new)
        r8 = r8[0].replace(',', '') if r8 else ''
        if "from" in r8:
            r8_1 = re.findall(re.compile(r'(\d+.\d+)\D+from(\d+)\D+'), r8)
        else:
            r8_1 = re.findall(re.compile(r'(\d+.\d+)\D+(\d+)\D+'), r8)

        r9 = re.findall(re.compile(r'文件格式(.*?)-oo-'), intro_new)

        r10 = re.findall(re.compile(r'视频尺寸(.*?)-oo-'), intro_new)
        r11 = re.findall(re.compile(r'文件大小(.*?)-oo-'), intro_new)
        r12 = re.findall(re.compile(r'片长(.*?)-oo-'), intro_new)
        r13 = re.findall(re.compile(r'导演(.*?)-oo-'), intro_new)
        r14 = re.findall(re.compile(r'主演(.*?)<div>-oo-'), intro_new)
        r15 = re.findall(re.compile(r'^和(简介|剧情：)(.+?)-oo-'), intro_new)
        poster_urls = re.findall(re.compile(r'<img.*?src="(.*?)"'), intro_new)
        img_src = poster_urls[0] if poster_urls else ''
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        poster_name = ''
        if img_src:
            poster_path = r'E:/Mycarrer/movie/poster_piaohua/'
            try:
                img_content = requests.get(img_src)
                img_content = img_content.content
                poster_name = 'p' + title.split('/')[0].replace('\\', '').replace(' ', '').replace('"', '').replace('?', '') + \
                          str(time_now).replace('-', '').replace(' ', '').replace(':', '')
                ex = '.' + img_src.split('.')[-1].strip()
                path = poster_path + poster_name + ex
                Tool().sav_img(img_content, path)
            except Exception as e:
                print(e)

        return{
            "intro": intro,
            "title": title,
            "movie_update": movie_update[0] if movie_update else '',
            "pm_title1": r1[0] if r1 else '',
            "pm_title2": r2[0] if r2 else '',
            "pm_year": r3[0] if r3 else '',
            "pm_class": r4[0] if r4 else '',
            "pm_lan": r5[0] if r5 else '',
            "pm_zimu": r6[0] if r6 else '',
            "pm_firstplay": r7[0] if r7 else '',
            "pm_imdb_rating": r20_1[0][0] if r20_1 else '',
            "pm_imdb_voters": r20_1[0][1] if r20_1 else '',
            "pm_imdb_url": r20_2[0] if r20_2 else '',
            "pm_douban_rating": r8_1[0][0] if r8_1 else '',
            "pm_douban_voters": r8_1[0][1] if r8_1 else '',
            "file_format": r9[0] if r9 else '',
            "movie_size": r10[0] if r10 else '',
            "file_size": r11[0] if r11 else '',
            "movie_time": r12[0] if r12 else '',
            "poster_name": poster_name,
            "pm_director": r13[0] if r13 else '',
            "pm_actor": r14[0].replace('<div>', '').replace('</div>', '\n').replace('&nbsp;', '').replace('<br', '').replace('/', '') if r14 else '',
            "pm_intro": r15[0][1] if r15 else '',
            "download": '\n'.join([dl.text() for dl in response.doc('#showinfo > table > tbody > tr > td > a').items()]),
            "time_update": time_now
        }

    def on_result(self, result):
        kwargs = {  'host': 'localhost',
                    'user': 'root',
                    'passwd': 'Myluoxue99..',
                    'db': 'movie',
                    'charset': 'utf8'}

        if not result:
            return
        sql = ToMysql(kwargs)
        sql.into('piaohua_main', **result)

class Tool:
    def sav_img(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def get_ex(self, img_src):
        extension = '.' + img_src.split('.')[-1].strip()
        return extension

