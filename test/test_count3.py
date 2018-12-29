#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: **

from pyspider.database.mysql.mysqldb import ToMysql
from pypinyin import lazy_pinyin
import sys

kwargs = {'host': 'localhost',
          'user': 'root',
          'passwd': 'luoxue99',
          'db': 'youxin',
          'charset': 'utf8'}
sql = ToMysql(kwargs)
try:

    sql_query = 'select che_ershou.pinpai, che_ershou.chexi, pinpai.id from pinpai left join che_ershou on pinpai.pinpai = che_ershou.pinpai '
    rows = sql.select(sql_query)
    c_lists = list(set(rows))
    for c_list in c_lists:
        cases = ','.join('%s' % r for r in c_list)
        case = cases.split(',')

        p_id = case[2]
        pinpai = case[0]
        chexi = case[1]

        values = {
            'p_id': p_id,
            'pinpai': pinpai,
            'chexi': chexi

        }
        sql.into('chexi', **values)

finally:
    sql.cursor.close()
    sql.conn.close()
