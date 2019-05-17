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
def read_e(df, date):
    # df = pd.read_excel('D:/workspace/1/20181101.xlsx')
    # df.info()
    col2 = [
        '区域',
        '1全部',
        '2更新',
        '3全部',
        '4更新',
        '5全部',
        '6更新',
        '7全部',
        '8更新',
        '9全部',
        '10更新',
        '11全部',
        '12更新',
        '13全部',
        '14更新',
        '15全部',
        '16更新',
        '17全部',
        '18更新',
        '19全部',
        '20更新',
        '21全部',
        '22更新',
        '23全部',
        '24更新',
        '25合计',
        '26排名'
]

    cols = {
        '2018年11月01日9点全市未巡查、疑似闲置及超期未处理土地情况': '区域',
        'Unnamed: 1': '全部1',
        'Unnamed: 2': '更新2',
        'Unnamed: 3': '全部3',
        'Unnamed: 4': '更新4',
        'Unnamed: 5': '全部5',
        'Unnamed: 6': '更新6',
        'Unnamed: 7': '全部7',
        'Unnamed: 8': '更新8',
        'Unnamed: 9': '全部9',
        'Unnamed: 10': '更新10',
        'Unnamed: 11': '全部11',
        'Unnamed: 12': '更新12',
        'Unnamed: 13': '全部13',
        'Unnamed: 14': '更新14',
        'Unnamed: 15': '全部15',
        'Unnamed: 16': '更新16',
        'Unnamed: 17': '全部17',
        'Unnamed: 18': '更新18',
        'Unnamed: 19': '全部19',
        'Unnamed: 20': '更新20',
        'Unnamed: 21': '全部21',
        'Unnamed: 22': '更新22',
        'Unnamed: 23': '全部23',
        'Unnamed: 24': '更新24',
        'Unnamed: 25': '合计25',
        'Unnamed: 26': '排名26'
    }
    df=pd.DataFrame(df.values, columns=col2)
    df2 = df.loc[df.区域=="总计"][0:1]
    df2['日期'] = date
    df2 = df2[['日期']+ col2]
    return df2

#%%
import os
import re
date_txt = [i.replace('年', '-').replace('月', '-').replace('日', '') for i in date_txt if date_txt else '']
dfx = pd.DataFrame()
files_dir = os.walk('D:/workspace/巡查数据')
r_list = []
for root, dirs, files in files_dir:
    for f in files:
        f1 = re.findall(re.compile('\d+.*?xlsx?'), f)
        f2 = f1[0] if f1 else None
        f3 = os.path.join(root, f2)
        r_list.append(f3)
print(r_list)

for r in r_list:
    df = pd.read_excel(r, sheet_name='Sheet1')
    date = re.findall(re.compile('20\d+'), r)
    date = date[0] if date else '未知'

    dfi = read_e(df, date=date)
    dfx = pd.concat([dfx, dfi])
 
dfx.to_excel('D:/workspace/output/合并数据-{}.xlsx'.format(str(datetime.today())[0:13]))
#%%


#%%
