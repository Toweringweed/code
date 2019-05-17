#%%
import numpy as np
import pandas as pd
import re
from datetime import datetime
# df = pd.read_excel(r'D:/workspace/建筑面积解析-2019-01-28 09.xlsx')
# df.ix[0:4914, ['住宅-总']] = df.ix[0:4914,['住宅-总1']]
# df.to_excel(r'D:/workspace/建筑面积解析-{}-tttt.xlsx'.format(str(datetime.today())[0:13]))

# a = [1,3,4]
# b = [7,9]
# c = zip(a, b)
# print(list(c))

# pid = str(datetime.today())[0:16]
# print(pid)


str = '3.2dff4.5'
def get_num(con):
    p = '(\d+)'
    p_num = 0
    if '.' in con:
        con = con.split('.', 1)
        p_num1 = re.findall(re.compile(p), con[0])
        p_num2 = re.findall(re.compile(p), con[1])
        if p_num2:
            if p_num1:
                p_num = (p_num1[0]) + '.' + (p_num2[0])
            else:
                p_num = '0' + '.' + (p_num2[0])
    else:
        p_num = re.findall(re.compile(p), con)
        p_num = p_num[0] if p_num else 0
    return p_num
    
print(get_num(str))