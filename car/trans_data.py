#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: ershouche

import pandas as pd
import numpy as np
import pymysql


# c2_youxin = pd.read_csv('E:\Python\data2\youxin.csv')
# p1 = c2_youxin[['pinpai', 'chexi']].head()

con = pymysql.connect(host='localhost', user='root', passwd='luoxue99', db='ershouche', charset='utf8')

c2_youxin2 = pd.read_sql('select * from ershouche_youxin', con=con)
con.close()

p2 = c2_youxin2[['pinpai', 'licheng']][9:15]

des = p2.describe().round(2)
print(des)

raw_look = c2_youxin2.sort(columns='pinpai')


pt1 = pd.pivot_table(c2_youxin2, index=['pinpai'] )





