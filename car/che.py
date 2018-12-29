#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: che


from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import ToMysql
import time

kwargs = {  'host':'localhost',
                    'user':'root',
                    'passwd':'luoxue99',
                    'db':'youxin',
                    'charset':'utf8'}

sql = ToMysql(kwargs)
sql_query = 'selcet * from ershouche limit 0,100'
sql.select()

