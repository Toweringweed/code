#!/usr/bin/env python
# -*- coding: utf-8 -*
import pymysql
import cx_Oracle
import os
from sqlalchemy import create_engine
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def loacl_db():
	conn=create_engine('mysql+pymysql://root:123456@localhost:3306/lphcreat?charset=utf8')
	return conn	

def oracle_db(name,passwd):
	conn = create_engine('oracle+cx_oracle://{}:{}@113.200.105.35:1525/ORCL'.format(name,passwd))
	return conn

def hd_db():
	conn=create_engine('mysql+pymysql://lipenghui:lipenghui123@113.200.105.35:3307/data_operation?charset=utf8')
	return conn

if __name__ == '__main__':
	import pandas as pd
	# conn = oracle_db('credit','credit2018')
	conn = oracle_db('hsdc','hsdc2018')
	sql = r'SELECT b.ID_CARD,b.SELECTTIME,s.* FROM CREDIT_BASIC b INNER JOIN CREDIT_SUMMARY s ON b.UUID = s.UUID where ROWNUM<100'
	df_summary = pd.read_sql(sql, conn)
	conn.close()
	print(df_summary.shape)