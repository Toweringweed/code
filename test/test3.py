#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from six import itervalues
print("卧室")

# li = ["a", "b", "c", "d"]
# lis = []
# for i in li:
#     dicts = {}
#     dicts["id"] = i
#     lis.append(dicts)
# print(lis)

# values = {"a":[0,4,5], "b":["uu","rt","gh"], "c":[3,5,7]}
# _keys = ",".join(k for k in values)
# _values = ",".join(['%s',]*len(values))
# sql_query = "insert into (%s) values (%s)" % (_keys,_values)
# u = list(itervalues(values))
# u2 = [[row[i] for row in u] for i in range(len(u))]
# print(sql_query, u2)

# import re
# urls = ['/chushou/3_212098015.htm', '/chushou/3_212057443.htm']


# uids = []
# for i in urls:
#     uid = re.findall(re.compile(r'chushou/(.*?).htm'), i)
#     uid = uid[0] if uid else ''
#     uids.append(uid)
# print(uids)

for i in range(100):
    print(i)