#!/usr/bin/env python
# -*- coding: utf-8 -*
import pymysql
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def data_operation():
	conn = pymysql.connect(host='localhost', user='root', passwd='123456', database='lphcreat', charset='utf8')
	return conn	

def credit(name,passwd):
	conn = cx_Oracle.connect(f'{name}/{passwd}@113.200.105.35:1525/ORCL')
	return conn

if __name__ == '__main__':
	import pandas as pd
	# conn = credit('credit','credit2018')
	conn = credit('hsdc','hsdc2018')
	sql = r'SELECT b.ID_CARD,b.SELECTTIME,s.* FROM CREDIT_BASIC b INNER JOIN CREDIT_SUMMARY s ON b.UUID = s.UUID where ROWNUM<100'
	df_summary = pd.read_sql(sql, conn)
	conn.close()
	print(df_summary.shape)
	data_operation()