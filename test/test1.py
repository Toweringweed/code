
# import re

# c = '净使用150平方米的通信机房'

# pub = '共?(\d+(\.\d+)?)(平方|平方米|平米|㎡)' 
# pt2 = re.findall(re.compile(pub + '的' + '通信机房'), c) #第二种匹配模式搜寻

# if pt2:
#     num2 = 0
#     for n in range(0, len(pt2)):
#         num2 = num2 + float(pt2[n][0])
#         print(num2)


#%%
import numpy as np
import pandas as pd
import re
import time

np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 500
pd.options.display.max_columns = 100
pd.set_option('expand_frame_repr', False)

from datetime import datetime

s = time.strftime('%Y/%m/%d', time.gmtime(time.mktime((1995,1,10, 0, 0, 0, 0, 0, 0))))
print(s)

# df = pd.read_csv(r'D:\GIS\年期数据\Export_Output31.csv')

#%%
s='咲錖|G戺齋垧戏隵T~桒*在鉫2芜跓'
print(s.encode('ISO-8859-1').decode('utf8'))


#%%


#%%
