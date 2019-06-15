import pandas as pd
import numpy as np
import pymysql
from dateutil.parser import parse
from datetime import datetime
import math
import re

def calculating_age(loan_id, id_card):
    try:
        data_in = parse(re.findall(r'\d{8}', loan_id)[0])
    except IndexError:
        data_in = datetime.today()
    born = parse(id_card[6:14])
    try:
        birthday = born.replace(year=data_in.year)
    except ValueError:
        birthday = born.replace(year=data_in.year, day=28)
    if birthday > born:
        return data_in.year - born.year - 1
    else:
        return data_in.year - born.year

def get_area(x):
    y = ''
    if x == 0:
        y = '市区'
    elif (x == 1) | (x == 2):
        y = '偏远区县'
    elif (x == 3) | (x == 4) | (x == 5):
        y = '村、乡'
    elif x == 8:
        y = '县级市'
    return y


def get_good(x, y):
    g = ''
    if x >= 2:
        g = 'bad'
    elif (x == 0) & (y >= 6):
        g = 'good'
    else:
        g = 'unknow'
    return g


def get_city_area(x):
    y = ''
    if (re.search(r'县', x) != None):
        y = '县'
    elif (re.search(r'市|区',x) != None):
        y = '市'
    return y


def city_match(x1, x2):
    return True if (re.search(x1, x2) != None) else False


def final_flow(x, y, z):
    if (x == 0) & (y == 0):
        flow = z
    elif (x == 0) & (y != 0):
        flow = y
    else:
        flow = x
    return flow


def handle_inf(x):
    return 0 if math.isinf(x) else x

def get_max(x, y):
    return x if x >= y else y


df = pd.read_csv(r'E:\hoomsun_data\analysis\models\data_7.16.csv')
df = df.fillna('缺失')

df_list = pd.read_excel(r'E:\hoomsun_data\analysis\models\建模字典v4.xlsx')
list_var = list(df_list[df_list.是否使用==1]['英文'])
df = df[df.classification != 'unknow']
df['product'] = df['final_product_name']

# 随机将样本切分为n等份
def split_random(df, n):
    df = df.sample(frac=1)
    point = int(int(1/n * df.shape[0]))
    cut_index = range(point, df.shape[0], point)
    dfc1 = df[0: cut_index[0]]
    dfc = [df[cut_index[cut_index.index(i)-1]: i] for i in cut_index]
    dfc.append(dfc1)
    return dfc

dfc = split_random(df, 5)

# 设定训练集
def set_train_test(df, n, test_num):
    df_test = df[test_num]
    n_list = list(range(0, n))
    n_list.remove(test_num)
    print(n_list)
    df_train = pd.concat(df[i]for i in n_list)
    df_train['train_test'] = 1
    df_test['train_test'] = 0
    df = pd.concat([df_train, df_test])
    return df

def cal_woe(df, classification, col_count, feature_list, other_var):
    save_path = r'E:\hoomsun_data\analysis\models\贡献值结果-{}.xlsx'.format(str(datetime.today())[0:13])
    writer = pd.ExcelWriter(save_path)
    df_IV = pd.DataFrame(columns=['英文', 'IV值'])
    index = 0
    offset = 0
    df_train = df[df.train_test == 1]
    for i in feature_list:
        print(i)
        pt = pd.pivot_table(df_train, index=classification, columns=i, values=col_count, aggfunc='count').T
        print(pt)
        pt['WOEi'] = np.log((pt['good']/pt['good'].sum())/(pt['bad']/pt['bad'].sum())).round(4)
        pt['IVi'] = pt.WOEi.mul((pt.good/pt.good.sum())-(pt.bad/pt.bad.sum())).round(3)
        pt = pt.fillna(0)
        pt.to_excel(writer, 'woe明细', startrow=offset)
        key = pt.index.tolist()
        value = pt.WOEi.tolist()
        dict_v = dict(zip(key, value))
        print(dict_v)
        df[i] = df[i].map(dict_v)   # 将woe值注入测试集
        iv = pt.IVi.sum()
        df_IV.at[index, '英文'] = i
        df_IV.at[index, 'IV值'] = iv
        index += 1
        offset += (pt.shape[0] + 2)
    pd.merge(df_IV, df_list, on='英文', how='left').to_excel(writer, sheet_name='IV汇总')
    woe_value = df[other_var + feature_list].copy()
    woe_value.to_excel(writer, sheet_name='woe', index=False)
    writer.save()

df_split = set_train_test(dfc, 5, 1)
cal_woe(df_split, 'classification', 'loan_id', feature_list=list_var,
        other_var=['loan_id', 'classification', 'user_mark', 'train_test'])

