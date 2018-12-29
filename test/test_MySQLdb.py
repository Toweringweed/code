#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import MySQLdb

try:
    conn = MySQLdb.connect('localhost', 'root', 'luoxue99')
    cur = conn.cursor()
    cur.execute('create database if not exists python2')
    conn.select_db('python2')
    cur.execute('create table test(id int, info varchar(20))')

    values = []
    for i in range(1, 20):
        values.append((i, 'info'+str(i)))
    cur.executemany('insert into test values(%s,%s)', values)

    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

