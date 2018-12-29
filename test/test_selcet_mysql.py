#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-12-11 16:52:45
# Project: test_select_mysql

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMysql


kwargs = {  'host':'localhost',
                    'user':'root',
                    'passwd':'luoxue99',
                    'db':'youxin',
                    'charset':'utf8'}

sql = ToMysql(kwargs)
sql_query = "select * from che_pinpai"
sql.select(sql_query)





