#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: ershouche

import pandas as pd
import numpy as np
import pymysql


# c2_youxin = pd.read_csv('E:\Python\data2\youxin.csv')
# p1 = c2_youxin[['pinpai', 'chexi']].head()

class DataClean:
    def __init__(self, sql_query):
        self.con = pymysql.connect(host='localhost', user='root', passwd='luoxue99', db='ershouche', charset='utf8')
        self.data = pd.read_sql(sql_query, con=self.con)
        self.con.close()

    def data_show(self):
        return self.data

    def data_save(self, df, table_name):
        pd.DataFrame.to_csv(df, table_name, index=False, sep='\t')
        return "kk"
        # pd.DataFrame.to_sql(df, name=table_name, con=self.con, index=False)

sql_query = 'select * from ershouche_youxin_a'
mydata = DataClean(sql_query).data_show()

df = mydata.iloc[0:20, 0:-12]
# DataClean.data_save(df, 'ershouche_youxin_x')
DataClean.data_save(df=df, table_name='E:\Python\11.csv')



# p2 = c2_youxin2[['pinpai', 'licheng']][9:15]
#
# des = p2.describe().round(2)
# print(des)
#
# raw_look = c2_youxin2.sort(columns='pinpai')
#
#
# pt1 = pd.pivot_table(c2_youxin2, index=['pinpai'] )





