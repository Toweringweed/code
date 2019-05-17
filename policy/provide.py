
#%%
import numpy as np
import pandas as pd
import re
from datetime import datetime

np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 500
pd.options.display.max_columns = 100
pd.set_option('expand_frame_repr', False)

df = pd.read_excel(r'd:/workspace/土地供应-总.xlsx')

df.drop(inplace=True, columns=['土地性质', '土地用途.1'], axis=1)
df.info()

#%% 去重
df['dup'] = df.duplicated(['合同号', '合同字号', '宗地号', '签订日期', '土地用途', '用地面积', '建筑面积说明', '容积率'], keep=False)
df2 = df.loc[df.dup==True]
df2.to_excel(r'd:/workspace/output/土地供应-总-dup.xlsx')

df.drop_duplicates(inplace=True, keep='first',
    subset=['合同号', '合同字号', '宗地号', '签订日期', '土地用途', '用地面积', '建筑面积说明', '容积率'])
df.to_excel(r'd:/workspace/output/土地供应-总-nodup.xlsx')
df.sort_values(by=['合同号', '宗地号', '签订日期', '合同字号'])
#%% 容积率数据清理

def get_num(con):
    p_num = re.findall(re.compile('(\d+(\.\d+)?)'), con)
    num = p_num[0][0] if p_num else 0
    return num

def clean_str(con):
    p_list = [' ', '-', '―', '/', '≤', '=', '<', '≤', '〈', '＜', '《', '>', '≤']
    for i in p_list:
        con = con.replace(i, '')
    return con
df = pd.read_excel(r'd:/workspace/output/土地供应-总-nodup.xlsx')

df['plot_ratio'] = df['容积率'].map(lambda x: get_num(str(x)))   
dfx = pd.pivot_table(df, index=['宗地号'], values=['plot_ratio'], aggfunc=[np.max, np.min])
dfx = pd.DataFrame(dfx).reset_index()
dfx.head()
dfx.info()

dfx['提容'] = df['(amax, plot_ratio) '] - df['(amin, plot_ratio)']

dfx.to_excel(r'd:/workspace/output/土地供应-总-process.xlsx')

#%%
