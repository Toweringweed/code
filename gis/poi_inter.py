# -*- encoding: utf-8 -*-

#%%
import numpy as np
import pandas as pd


df = pd.read_table('D:/GIS/study/2/poi/inter_poi_fish.txt', encoding='utf-8', sep=',')
df

#%%
df['Id'] = df['FID_fishne']

# 将兴趣点分类列表切分，获得第一个分类
df['class'] = df['categorys'].map(lambda x: str(x).split(' ')[0])
df['class']

#%% 数据透视表，计算每个网格中每类兴趣点的数量

df['cc'] = 1
dfx = pd.pivot_table(df, columns=['class'], values=['cc'], index=['Id'], aggfunc='sum', fill_value=0)

# 获得所有分类的列表，并去重
class_set = sorted(list(set(df['class'])))
class_set

col = ['Id'] + class_set 
dfs = pd.DataFrame(dfx.reset_index().as_matrix(), columns=col)

#%%
dfs['num_max'] = dfs[class_set].apply(lambda x: max(x), axis=1)
# 获取行最大值的列标签名 
dfs['class_max'] = dfs[class_set].idxmax(axis=1)
dfs['class_ratio'] = dfs[class_set].apply(lambda x: round(max(x)/sum(x),2), axis=1)

dfs = dfs[['Id', 'class_max', 'num_max', 'class_ratio']]
dfs.to_csv('D:/GIS/study/2/poi/class_compute.csv', index=False)



