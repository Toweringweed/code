#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-12


from pypinyin import  pinyin, lazy_pinyin
import pypinyin
import sys

list_a = [
    "标题",
"价格",
"价格2",
"原价",
"原价2",
"上架时间",
"上牌时间",
"表显里程",
"排量",
"销售城市",
"车身颜色",
"工信部油耗",
"驱动形式",
"生产厂商",
"过户次数",
"使用性质",
"车身结构",
"年款代",
"座椅数",
"整备质量",
"轴距",
"最大扭矩",
"最大功率",
"最大马力",
"行程",
"发动机型号",
"变速箱类型",
"参数配置",
"参数配置2",
"基本信息",
"基本信息2",
"外观参数",
"外观参数2",
"发动机参数",
"发动机参数2",
"底盘参数",
"底盘参数2",
"性能参数",
"性能参数2",
"电动机参数",
"电动机参数2",
"安全配置",
"安全配置2",
"操控配置",
"操控配置2",
"车窗玻璃雨刷",
"车窗玻璃雨刷2",
"车外灯光",
"车外灯光2",
"外观套件",
"外观套件2",
"方向盘座椅",
"方向盘座椅2",
"影音娱乐",
"影音娱乐2",
"高科技配置",
"高科技配置2",
"车身参数",
"车身参数2",
"车轮制动参数",
"车轮制动参数2",
"变速箱参数",
"变速箱参数2",
"定速巡航",
"定速巡航2",
"多媒体配置",
"多媒体配置2"

]

i=0
for list_i in list_a:
    list_ii = list_i.decode('utf-8')
    list_st = ''.join(lazy_pinyin(list_ii))
    list_ss = 'v' + str(list_a.index(list_i)) +'_' + list_st
    print(list_ss)
    i =+1
