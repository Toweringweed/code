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

poster_path = r"E:/Mycarrer/movie/poster_douban/"

kwargs = {'host': 'localhost',
          'user': 'root',
          'passwd': 'Myluoxue99..',
          'db': 'movie',
          'charset': 'utf8'}
sql = ToMysql(kwargs)

movie_class_list = ('电影', '剧集')
for m_l in movie_class_list:
    v_class = {"m_class": m_l}
    sql.into('movie_mclass', **v_class)

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Cookie": 'll="0"; bid=JR14vPvPQwk; _pk_id.100001.8cb4=ae445e76cba835e0.1496645997.1.1496645997.1496645997.; _pk_ses.100001.8cb4=*; __utmt=1; __utma=30149280.1985935733.1496645998.1496645998.1496645998.1; __utmb=30149280.1.10.1496645998; __utmc=30149280; __utmz=30149280.1496645998.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
        }
    }

    @every(minutes=2 * 60)
    def on_start(self):

        self.crawl('https://movie.douban.com/tag/', callback=self.index_page)

    @config(age=30 * 60)
    def index_page(self, response):

        for each in response.doc('.article > table:nth-child(5) > tbody> tr > td > a').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(age=30 * 60)
    def list_page(self, response):

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

    @config(age=30 * 60)
    def ll_page(self, response):

        for each in response.doc('tr.item > td:nth-child(1) > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        m_id = re.findall(re.compile(r'subject/(\d+)/'), response.url)
        m_id = int(m_id[0]) if m_id else -1
        for each in response.doc('#info > span:nth-child(1) > span:nth-child(2) > a').items():
            art_url = re.findall(re.compile(r'celebrity/(\d+)/'), each.attr.href)
            art_id = art_url[0] if art_url else -1
            art_v = {
                "m_id": m_id,
                "art_type": 1,
                "art_id": art_id
            }
            sql.into('movie_malist', **art_v)
            if re.match("https://movie.douban.com/celebrity/.*", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.art_detail)

        for each in response.doc('#info > span:nth-child(3) > span:nth-child(2) > a').items():
            art_url = re.findall(re.compile(r'celebrity/(\d+)/'), each.attr.href)
            art_id = art_url[0] if art_url else -1
            art_v = {
                "m_id": m_id,
                "art_type": 2,
                "art_id": art_id
            }
            sql.into('movie_malist', **art_v)

            if re.match("https://movie.douban.com/celebrity/.*", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.art_detail)

        for each in response.doc('.actor > span:nth-child(2) > a').items():
            art_url = re.findall(re.compile(r'celebrity/(\d+)/'), each.attr.href)
            art_id = art_url[0] if art_url else -1
            art_v = {
                "m_id": m_id,
                "art_type": 3,
                "art_id": art_id
            }
            sql.into('movie_malist', **art_v)

            if re.match("https://movie.douban.com/celebrity/.*", each.attr.href, re.U):
                self.crawl(each.attr.href, callback=self.art_detail)

        time_now = time.localtime()
        cc = [c.replace('</span>', '') for c in re.findall(re.compile(r'pl">(.*?)<br'), response.doc('#info').html())]
        cc = "--".join(c for c in cc)

        # 地区
        r1 = re.findall(re.compile(r'制片国家/地区:(.*?)--'), cc)
        m_area = r1[0] if r1 else '无'
        m_area_list = m_area.split('/')


        # 插入年代表，并取出年代id
        title = response.doc('h1 > span').text()
        r1 = re.findall(re.compile(r'[(（](\d{4})[)）]'), title)
        m_year = r1[0] if len(r1) > 0 else '无'
        v_year = {'m_year': m_year}
        sql.into('movie_myear', **v_year)
        year_id = sql.select("select id from movie_myear where m_year='%s'" % m_year)

        m_tag_list = [lx.text() for lx in response.doc('span[property="v:genre"]').items()]

        r2 = re.findall(re.compile(r'又名:(.*?)--'), cc)
        r3 = re.findall(re.compile(r'llow">(.*)</a'), cc)
        r4 = re.findall(re.compile(r'集数:(.*?)--'), cc)

        # 判断视频类型
        m_class_id = 2 if r4 else 1

        r5 = re.findall(re.compile(r'链接:.*href="(.*?)"'), response.doc('#info').html())

        r6 = re.findall(re.compile(r'allstar(\d+) rating'), response.doc("div#hot-comments").html()) \
            if response.doc("div#hot-comments").html() else ''

        r7 = re.findall(re.compile(r'单集片长:(\d+)分钟'), cc)
        title2 = response.doc('#content > div.grid-16-8.clearfix > div.article > div.related-info > h2 > i').text().replace("的剧情简介", "")
        img_src = [i.attr.src for i in response.doc('#mainpic > a > img').items()][0]
        img_content = requests.get(img_src).content
        time_now_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        poster_name = 'p-' + title2.split('/')[0].replace('\\', '').replace(' ', '').replace('"', '').replace('?', '') + \
                      str(time_now_s).replace('-', '').replace(' ', '').replace(':', '')
        ex = Tool().get_ex(img_src)
        path = poster_path + poster_name + ex
        Tool().sav_img(img_content, path)

        # 获取imdb评分

        IMDB_link = ''
        ri1 = []
        ri2 = []
        if r5:
            IMDB_link = r5[0].strip()
            imdb_page = requests.get(IMDB_link).text
            ri1 = re.findall(re.compile(r'<span itemprop="ratingValue">(.*?)</span>'), imdb_page)
            ri2 = re.findall(re.compile(r'itemprop="ratingCount">(.*?)</span>'), imdb_page)

        douban_rating = response.doc('strong.rating_num').text()
        m_douban_rating = float(douban_rating) if douban_rating else -1
        douban_voters = response.doc('span[property="v:votes"]').text().replace(',', '')
        m_douban_voters = int(douban_voters) if douban_voters else -1

        season = response.doc('#season > option:nth-last-child(1)').text()
        m_season = int(season) if season else -1

        main_info = {
            "m_id": m_id,
            "m_name": title,
            "m_name2": title2,
            "m_director": response.doc('a[rel="v:directedBy"]').text(),
            "m_writer": response.doc('#info > span:nth-child(3) > span.attrs').text(),
            "m_actor": response.doc('.actor > span:nth-child(2)').text(),
            "m_year_id": year_id,
            "m_class_id": m_class_id,
            "m_first_play": '/'.join([lf.text() for lf in response.doc('span[property="v:initialReleaseDate"]').items()]),
            "m_runtime": response.doc('span[property="v:runtime"]').text(),
            "m_other_name": r2[0] if r2 else '',
            "m_imdb_serial": r3[0] if r3 else '',
            "m_imdb_url": IMDB_link,
            "m_imdb_rating": float(ri1[0]) if len(ri1)>=1 else -1,
            "m_imdb_voters": int(ri2[0].replace(',', '')) if len(ri2)>=1 else -1,
            "m_douban_rating": m_douban_rating,
            "m_douban_voters": m_douban_voters,
            "m_summary": response.doc('#link-report > span:nth-child(1)').text(),
            "m_award": '\n'.join([aw.text() for aw in response.doc('.mod > .award').items()]),
            "m_comment_short": '\n\r'.join([cx.text() for cx in response.doc('#hot-comments > div > div > p').items()]),
            "m_comment_rating": '\n\r'.join(r6) if r6 else '',
            "m_season": m_season,
            "m_jishu": int(r4[0]) if r4 else -1,
            "m_time_ji": int(r7[0]) if r7 else -1,
            "m_poster": poster_name,
            "m_douban_url": response.url,
            "m_update_douban": time_now,
            "m_lan": '无',
            "m_zimu": '无',
            "m_file_format": '无',
            "m_file_size": '无',
            "m_size": '无',
            "m_time": '无',
            "m_download": '无',
            "m_update_piaohua": time_now,
            "m_update": time_now

        }

        if not main_info:
            return
        sql.into('movie_mdetail', **main_info)
        mm_id = sql.select("select id from movie_mdetail where m_id=%d" % m_id)
        mm_id = mm_id[0][0]

        # 插入tag表，并取出tag_id,然后插入中间表
        for tl in m_tag_list:
            v_tag = {'m_tag': tl.strip()}
            sql.into('movie_mtag', **v_tag)
            in_id = sql.select("select id from movie_mtag where m_tag= '%s'" % tl.strip())
            in_id = in_id[0][0]
            v_mm_tag = {
                'mdetail_id': mm_id,
                'mtag_id': in_id
            }
            sql.into('movie_mdetail_m_tag', **v_mm_tag)

        # 插入地区表，并取出地区id
        for al in m_area_list:
            v_area = {'m_area': al.strip()}
            sql.into('movie_marea', **v_area)
            area_id = sql.select("select id from movie_marea where m_area='%s'" % al.strip())
            area_id = area_id[0][0]
            v_mm_tag = {
                'mdetail_id': mm_id,
                'marea_id': area_id
            }
            sql.into('movie_mdetail_m_area', **v_mm_tag)

    @config(age=30 * 60)
    def art_detail(self, response):
        time_now = time.localtime()
        art_url = re.findall(re.compile(r'celebrity/(\d+)/'), response.url)
        art_id = art_url[0] if art_url else -1
        dt_info = {
            "art_id": art_id,
            "art_name": response.doc('h1').text(),
            "art_info": '\n'.join([dtx.text().replace('\n', '').replace(' ', '') for dtx in
                                  response.doc('#headline > div.info > ul > li').items()]),
            "art_intro": response.doc('#intro > div.bd').text(),
            "art_award": '\n'.join([ar.text() for ar in response.doc('.award').items()]),
            "art_update": time_now
        }
        sql.into('movie_martist', **dt_info)

class Tool:
    def sav_img(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def get_ex(self, img_src):
        extension = '.' + img_src.split('.')[-1].strip()
        return extension

