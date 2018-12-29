#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che_youxin

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMysql
import time
from datetime import datetime, timedelta
import math


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.xin.com/quanguo/s/', callback= self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.brand-more > dl > dd > a').items():
            self.crawl(each.attr.href, callback= self.list_page)

    def list_page(self, response):
        p_url = response.url
        page_num = 1
        page_total = response.doc('.search_page_link > a:nth-last-child(2)').text()

        if page_total:
            page_total_num = int(page_total)
        else:
            page_total_num = 1
        while page_num <= page_total_num:
            url_a = p_url + "i" + str(page_num)
            self.crawl(url_a, callback=self.ll_page)
            page_num += 1

    def ll_page(self, response):
        for each in response.doc('li.con > a.aimg').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        bianhao = response.doc(' a.cd_m_info_cover_carid').text()
        v_bianhao = bianhao.replace('车辆编号：', '')
        pinpai =  response.doc('div.cd_m > div.cd_m_nav > a:nth-child(3)').text()
        pinpai2 = pinpai.replace('二手车', '')
        city = response.doc('table.cd_m_info_desc > tr:nth-child(2) > td:nth-child(3)> span.cd_m_info_desc_val').text()
        v_pinpai = pinpai2.replace(city, '')
        chexi = response.doc('div.cd_m > div.cd_m_nav > a:nth-child(4)').text()
        v_chexi = chexi.replace(city+'二手'+v_pinpai, '')
        jiage = response.doc('span.cd_m_info_jg > b').text()
        if '￥' in jiage:
            jiage2 = jiage.replace('￥', '')
            v_jiage = int(float(jiage2.replace('万', ''))*10000)
        else:
            v_jiage = -99
        v_yuanjia = response.doc('span.cd_m_info_fyb').text()

        licheng = response.doc(
            'table.cd_m_info_desc > tr:nth-child(1) > td:nth-child(1)> span.cd_m_info_desc_val').text()
        if "万公里" in licheng:
            v_licheng = int(float(licheng.replace('万公里',''))*10000)
        elif "公里" in licheng:
            v_licheng = int(licheng.replace('公里', ''))
        v_zhengbeizhiliang = response.doc(
            '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(2) > dd:nth-child(6) > span.cd_m_i_pz_val').text()
        v_zhouju = response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(2) > dd:nth-child(7) > span.cd_m_i_pz_val').text()
        v_pailiang = response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(3) > dd:nth-child(4) > span.cd_m_i_pz_val').text()

        v_paiqiliang = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(21) > span.cd_m_pop_pzcs_val').text()

        shangpaishijian = response.doc(
            'table.cd_m_info_desc > tr:nth-child(1) > td:nth-child(2)> span.cd_m_info_desc_val').text()
        shangpaishijian2 = datetime.strptime(shangpaishijian, "%Y-%m")
        shangjiashijian = response.doc(
            'table.cd_m_info_desc > tr:nth-child(1) > td:nth-child(3)> span.cd_m_info_desc_val').text()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        time_now2 = datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S")
        car_age_days = int((time_now2 - shangpaishijian2).total_seconds()/(60*60*24))
        car_age_months = int(math.ceil(car_age_days/30))
        car_age_years = int(math.ceil(car_age_months/12))
        v_zongheyouhao = response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(3) > dd:nth-child(7) > span.cd_m_i_pz_val').text()

        v_zuidagonglv = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(9) > span.cd_m_pop_pzcs_val').text()

        v_zuidagonglvzhuansu = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(8) > span.cd_m_pop_pzcs_val').text()

        v_zuidamali = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(10) > span.cd_m_pop_pzcs_val').text()

        v_zuidaniuju = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(7) > span.cd_m_pop_pzcs_val').text()

        v_zuidaniujuzhuansu = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(6) > span.cd_m_pop_pzcs_val').text()

        v_zuigaochesu = response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(5) > dl > dd:nth-child(5) > span.cd_m_pop_pzcs_val').text()

        guohucishu = response.doc('#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(1) > dd:nth-child(2) > span.cd_m_i_pz_val').text(),
        if '次' in guohucishu:
            v_guohucishu = int(guohucishu[0])
        else:
            v_guohucishu = 0

        return {
            "bianhao": v_bianhao,
            "pinpai": v_pinpai,
            "biaoti": response.doc('.cd_m > .cd_m_h > .cd_m_h_tit').text(),
            "chexi": v_chexi,
            "jiage": v_jiage,
            "yuanjia": v_yuanjia,
            "licheng": v_licheng,
            "shangpaishijian": shangpaishijian,
            "shangjiashijian": shangjiashijian,
            "car_age_days": car_age_days,
            "car_age_months": car_age_months,
            "car_age_years": car_age_years,
            "paifangbiaozhun": response.doc('table.cd_m_info_desc > tr:nth-child(2) > td:nth-child(1)> span.cd_m_info_desc_val').text(),
            "city": city,
            "guohucishu": v_guohucishu,
            "shiyongxingzhi": response.doc('#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(1) > dd:nth-child(4) > span.cd_m_i_pz_val').text(),
            "baoyangqingkuang": response.doc('#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(1) > dd:nth-child(7) > span.cd_m_i_pz_val').text(),
            "changshang": response.doc('#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(2) > dd:nth-child(2) > span.cd_m_i_pz_val').text(),
            "cheliangjibie": response.doc('#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(2) > dd:nth-child(3) > span.cd_m_i_pz_val').text(),
            "ranyoubiaohao": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(1) > span.cd_m_pop_pzcs_val').text(),
            "huanbaobaiozhun": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(2) > span.cd_m_pop_pzcs_val').text(),
            "zuidaniujuzhuansu": v_zuidaniujuzhuansu,
            "zuidaniuju": v_zuidaniuju,
            "zuidagonglvzhuansu": v_zuidagonglvzhuansu,
            "zuidagonglv": v_zuidagonglv,
            "zuidamali": v_zuidamali,
            "xingcheng": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(11) > span.cd_m_pop_pzcs_val').text(),
            "gangjing": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(12) > span.cd_m_pop_pzcs_val').text(),
            "yasuobi": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(14) > span.cd_m_pop_pzcs_val').text(),
            "qimenjishu": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(15) > span.cd_m_pop_pzcs_val').text(),
            "ranyoupengsheleixing": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(16) > span.cd_m_pop_pzcs_val').text(),
            "fadongjileixing": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd:nth-child(20) > span.cd_m_pop_pzcs_val').text(),
            "paiqiliang": v_paiqiliang,
            "houxuangualeixing": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(4) > dl > dd:nth-child(4) > span.cd_m_pop_pzcs_val').text(),
            "qianxuangualeixing": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(4) > dl > dd:nth-child(5) > span.cd_m_pop_pzcs_val').text(),
            "baigonglijiasu": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(5) > dl > dd:nth-child(4) > span.cd_m_pop_pzcs_val').text(),
            "zuigaochesu": v_zuigaochesu,
            "cheshenyanse": response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(2) > dd:nth-child(4) > span.cd_m_i_pz_val').text(),
            "cheshenjiegou": response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(2) > dd:nth-child(5) > span.cd_m_i_pz_val').text(),
            "zhengbeizhiliang": v_zhengbeizhiliang,
            "zhouju": v_zhouju,
            "fadongjixinghao": response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(3) > dd:nth-child(2) > span.cd_m_i_pz_val').text(),
            "biansuxiang": response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(3) > dd:nth-child(3) > span.cd_m_i_pz_val').text(),
            "pailiang": v_pailiang,
            "ranliaoleixing": response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(3) > dd:nth-child(5) > span.cd_m_i_pz_val').text(),
            "qudongxingshi": response.doc(
                '#cd_m_clxx > div.cd_m_i_pz > dl:nth-child(3) > dd:nth-child(6) > span.cd_m_i_pz_val').text(),
            "zongheyouhao": v_zongheyouhao,
            "jibenxinxi1": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(1) > dl > dd> span.cd_m_pop_pzcs_key').text(),
            "jibenxinxi2": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(1) > dl > dd> span.cd_m_pop_pzcs_val').text(),
            "fadongjicanshu": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd> span.cd_m_pop_pzcs_key').text(),
            "fadongjicanshu2": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(3) > dl > dd> span.cd_m_pop_pzcs_val').text(),
            "dipancanshu": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(4) > dl > dd> span.cd_m_pop_pzcs_key').text(),
            "dipancanshu2": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(4) > dl > dd> span.cd_m_pop_pzcs_val').text(),
            "xingnengcanshu": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(5) > dl > dd> span.cd_m_pop_pzcs_key').text(),
            "xingnengcanshu2": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(5) > dl > dd> span.cd_m_pop_pzcs_val').text(),
            "gengduocanshu": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(7) > dl > dd> span.cd_m_pop_pzcs_key').text(),
            "gengduocanshu2": response.doc(
                'div.cd_m_pop_pzcs_content > div > ul > li:nth-child(7) > dl > dd> span.cd_m_pop_pzcs_val').text(),
            "url": response.url,
            "time_now": time_now
        }

    def on_result(self, result):
        kwargs = {  'host': 'localhost',
                    'user': 'root',
                    'passwd': 'luoxue99',
                    'db': 'ershouche',
                    'charset': 'utf8'}

        if not result or not result['url']:
            return
        sql = ToMysql(kwargs)
        sql.into('ershouche_youxin', **result)

