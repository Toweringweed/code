#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataSciece.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'policy'))
	print(os.getcwd())
except:
	pass

#%%
import numpy as np
import pandas as pd
import re
from datetime import datetime

np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 500
pd.options.display.max_columns = 100
pd.set_option('expand_frame_repr', False)


#%%
df = pd.read_excel(r'D:/workspace/建筑面积解析-2019-01-30 15-f.xlsx')
mis_list = [
	'A121-1802',
	'A926-0077',
	'B302-0041',
	'B405-0233',
	'B406-0047',
	'G03512-0079',
	'G03512-0080',
	'G07213-0385',
	'G07232-0073',
	'G16516-0139',
	'H403-0052',
	'K408-0015',
	'K601-0005',
	'T404-0038'
]



#%% 数据合并
df_x = pd.read_excel('D:\workspace\数据解析-住宅-all.xlsx')
df_x.drop(['YDMJ','JZMJ', 'HT_DLMC', 'GB_DLMC', '建筑面积说明'], axis=1, inplace=True)
df_c = pd.merge(df_f, df_x, on='PARCEL_NO', how='left')
df_cols = pd.read_excel('D:\workspace\字段列表.xlsx')
col_list = df_cols['name'].tolist()


pd.DataFrame.to_excel(df_c, 'D:\workspace\数据2005-2019-3.xlsx', columns=col_list)

#%%  纠错
df_c = pd.read_excel( 'D:\workspace\数据2005-2019-3.xlsx')
def bigest_num(b_col, cols):
    return 0 if b_col >= sum(cols) else 1
             
df_c['mistake_住宅'] = df_c.apply(lambda x: bigest_num(x["住宅-总"], [x["住宅-安居型商品房"], x["住宅-公共租赁住房"], x["住宅-人才住房"], x['住宅-人才公寓']]), axis=1)
             
df_c[df_c.mistake>0][["建筑面积说明", "住宅-总", "mistake"]]


