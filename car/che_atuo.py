#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che_auto

from pyspider.libs.base_handler import *
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.autohome.com.cn/car/', callback= self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.rankcar > .caricon-list > dd > a:nth-child(1)').items():
            self.crawl(each.attr.href, callback=self.list_page)

    def list_page(self, response):
        for each in response.doc('.rank-list-ul > li > h4 > a').items():
            self.crawl(each.attr.href, callback= self.ll_page)

    def ll_page(self, response):
        for each in response.doc('#navTop > ul > li:nth-child(2) > a').items():
            self.crawl(each.attr.href, callback= self.detail_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        return {
            "标题": response.doc('.subnav-title-name > a').text(),
            "车型": response.doc('.carbox > div > a').text(),
            "厂商指导价": response.doc('#tr_2000 > td:nth-child(2) > div').text(),
            "经销商参考价": response.doc('#tr_2001 > td > div').text(),
            "基本参数1-厂商": response.doc('#tr_0 > td > div').text(),
            "基本参数2-级别": response.doc('#tr_1 > td > div').text(),
            "基本参数3-发动机": response.doc('#tr_2 > td > div').text(),
            "基本参数4-变速箱": response.doc('#tr_3 > td > div').text(),
            "基本参数5-长宽高（mm）": response.doc('#tr_4 > td > div').text(),
            "基本参数6-车身结构": response.doc('#tr_5 > td > div').text(),
            "基本参数7-最高车速（km/h)": response.doc('#tr_6 > td > div').text(),
            "基本参数8-官方0-100km加速（s）": response.doc('#tr_7 > td > div').text(),
            "基本参数9-实测0-100km加速（s）": response.doc('#tr_8 > td > div').text(),
            "基本参数10-实测100-0km制动（m）": response.doc('#tr_9 > td > div').text(),
            "基本参数11-实测油耗（L/100km）": response.doc('#tr_10 > td > div').text(),
            "基本参数12-工信部综合油耗（L/100km）": response.doc('#tr_11 > td > div').text(),
            "基本参数13-实测离地间隙（mm）": response.doc('#tr_12 > td > div').text(),
            "基本参数14-整车质保": response.doc('#tr_13 > td > div > a').text(),
            "车身1-长度（mm）": response.doc('#tr_14 > td > div').text(),
            "车身2-宽度（mm）": response.doc('#tr_15 > td > div').text(),
            "车身3-高度（mm）": response.doc('#tr_16 > td > div').text(),
            "车身4-轴距（mm）": response.doc('#tr_17 > td > div').text(),
            "车身5-前轮距（mm）": response.doc('#tr_18 > td > div').text(),
            "车身6-后轮距（mm）": response.doc('#tr_19 > td > div').text(),
            "车身7-最小离地间隙（mm）": response.doc('#tr_20 > td > div').text(),
            "车身8-整备质量（kg）": response.doc('#tr_21 > td > div').text(),
            "车身9-车身结构": response.doc('#tr_22 >td > div').text(),
            "车身10-车门数（个）": response.doc('#tr_23 > td > div').text(),
            "车身11-座位数（个）": response.doc('#tr_24 > td > div').text(),
            "车身12-油箱容积（L）": response.doc('#tr_25 > td > div').text(),
            "车身13-行李箱容积（L）": response.doc('#tr_26 > td > div').text(),
            "发动机1-发动机型号": response.doc('#tr_27 > td > div').text(),
            "发动机2-排量（ml）": response.doc('#tr_28 > td > div').text(),
            "发动机3-进气形式": response.doc('#tr_30 > td > div').text(),
            "发动机4-气缸排列形式": response.doc('#tr_31 > td > div').text(),
            "发动机5-气缸数": response.doc('#tr_32 > td > div').text(),
            "发动机6-每缸气门数": response.doc('#tr_33 > td > div').text(),
            "发动机7-压缩比": response.doc('#tr_34 > td > div').text(),
            "发动机8-配气结构": response.doc('#tr_35 > td > div').text(),
            "发动机9-缸径（mm）": response.doc('#tr_36 > td > div').text(),
            "发动机10-行程（mm）": response.doc('#tr_37 > td > div').text(),
            "发动机11-最大马力（Ps）": response.doc('#tr_38 > td > div').text(),
            "发动机12-最大功率（kW）": response.doc('#tr_39 > td > div').text(),
            "发动机13-最大功率转速（rpm）": response.doc('#tr_40 > td > div').text(),
            "发动机14-最大扭矩（N·m）": response.doc('#tr_41 > td > div').text(),
            "发动机15-最大扭矩转速（rpm）": response.doc('#tr_42 > td > div').text(),
            "发动机16-发动机特有技术": response.doc('#tr_43 > td > div').text(),
            "发动机17-燃料形式": response.doc('#tr_44 > td > div').text(),
            "发动机18-燃油标号": response.doc('#tr_45 > td > div').text(),
            "发动机19-供油方式": response.doc('#tr_46 > td > div').text(),
            "发动机20-缸盖材料": response.doc('#tr_47 > td > div').text(),
            "发动机21-缸体材料": response.doc('#tr_48 > td > div').text(),
            "发动机22-环保标准": response.doc('#tr_49 > td > div').text(),
            "变速箱1-简称": response.doc('#tr_50 > td > div').text(),
            "变速箱2-档位个数": response.doc('#tr_51 > td > div').text(),
            "变速箱3-变速箱类型": response.doc('#tr_52 > td > div').text(),
            "车轮制动1-前制动器类型": response.doc('#tr_58 > td > div').text(),
            "车轮制动2-后制动器类型": response.doc('#tr_59 > td > div').text(),
            "车轮制动3-驻车制动类型": response.doc('#tr_60 > td > div').text(),
            "车轮制动4-前轮胎规格": response.doc('#tr_61 > td > div').text(),
            "车轮制动5-后轮胎规格": response.doc('#tr_62 > td > div').text(),
            "车轮制动6-备胎规格": response.doc('#tr_63 > td > div').text(),
            "安全装备1-主副驾驶座安全气囊": response.doc('#tr_200 > td > div').text(),
            "安全装备1-前后排侧气囊": response.doc('#tr_201 > td > div').text(),
            "安全装备1-前后排头部气囊": response.doc('#tr_202 > td > div').text(),
            "安全装备1-膝部气囊": response.doc('#tr_203 > td > div').text(),
            "安全装备1-胎压监测装置": response.doc('#tr_204 > td > div').text(),
            "安全装备1-零胎压继续行驶": response.doc('#tr_205 > td > div').text(),
            "安全装备1-安全带未系提示": response.doc('#tr_206 > td > div').text(),
            "安全装备1-儿童座椅接口": response.doc('#tr_207 > td > div').text(),
            "安全装备1-发动机电子防盗": response.doc('#tr_208 > td > div').text(),
            "安全装备1-车内中控锁": response.doc('#tr_209 > td > div').text(),
            "安全装备1-遥控钥匙": response.doc('#tr_210 > td > div').text(),
            "安全装备1-无钥匙启动系统": response.doc('#tr_211 > td > div').text(),
            "安全装备1-无钥匙进入系统": response.doc('#tr_212 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),
            "操控配置1-ABS防抱死": response.doc('#tr_213 > td > div').text(),




    }
