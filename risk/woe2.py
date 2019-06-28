
import pandas as pd
import numpy as np
import pymysql
from dateutil.parser import parse
from datetime import datetime
import math
import re
import json

def calculating_age(id, id_card):
    try:
        data_in = parse(re.findall(r'\d{8}', id)[0])
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


def get_city_area(x):
    y = ''
    if (re.search(r'县', x) != None):
        y = '县'
    elif (re.search(r'市|区',x) != None):
        y = '市'
    return y


def city_match(x1, x2):
    return True if (re.search(x1, x2) != None) else False


def handle_inf(x):
    return 0 if math.isinf(x) else x


## 给每个值重新编码为分段标签——对应ChiMerge_MaxInterval方法
def get_point_dur(x, point):
    z = ''
    if point:
        num_point = len(point) + 1
        if (x != -99):
            if x <= point[0]:
                z = '0- ~' + str(point[0])
            elif x > point[-1]:
                z = '{}- '.format(num_point-1) + str(point[-1]) + '~'
            else:
                for i in range(0, num_point-1):
                    if point[i] < x <= point[i+1]:
                        z = '{}- '.format(i+1) + str(point[i]) + '~' + str(point[i + 1])
        else:
            z = '-99'
    return z


def get_max(x, y):
    return x if x >= y else y

# 随机将样本切分为n等份
def split_random(df, n):
    df = df.sample(frac=1)
    point = int(int(1/n * df.shape[0]))
    cut_index = range(point, df.shape[0], point)
    dfc1 = df[0: cut_index[0]]
    dfc = [df[cut_index[cut_index.index(i)-1]: i] for i in cut_index]
    dfc.append(dfc1)
    return dfc

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
    save_path = r'd:/data/model/贡献值结果-{}.xlsx'.format(str(datetime.today())[0:13])
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



# df1 = pd.read_excel('d:/data/model/cust_label.xlsx')
# df1.head()
# df2 = pd.read_excel('d:/data/model/summary.xlsx')
# df2.head()
# df3 = pd.read_excel('d:/data/model/credit_features.xlsx')
# df3.head()

# 
# df = pd.merge(df1, df2, on=['con_no', 'id_card'], how='inner')
# df.info()
# df = df.drop(['apply_date_y', 'index_y', 'uuid_y'], axis=1)
# df = pd.merge(df, df3, left_on='uuid_x', right_on='uuid', how='inner')
# df.info()
# df.to_excel('d:/data/model/model_data.xlsx')


# df = pd.read_excel('d:/data/model/model_data.xlsx')
# df.info()
# df.head()


def re_trans(df, ChiMerge_list, target, onkey, save_path):
    df_chis = df.loc[:, ['id', 'user_mark', 'classification']]
    for var_li in lisan_list:
        df_li = df.loc[:, ['id', var_li]]
        df_chis = pd.merge(df_chis, df_li, how='left', on='id')
    for col in ChiMerge_list:
        print(col)
        df[col] = df[col].replace('-', None).astype(float)
        df_chi = df.loc[:, [onkey, col, target]]
        df_chi = df_chi.fillna(-99)
        with open(r'd:/code/risk/model_my/split_code_fix.json') as j_file:
            j = json.load(j_file)
        for i in j:
            if i['col_name'] == col:
                split_box = i['split_box']
                if split_box:
                    df_chi[col] = df_chi[col].apply(lambda x: get_point_dur(x, split_box))
            df_chi = df_chi.loc[:, [onkey, col]]

        df_chis = pd.merge(df_chis, df_chi, how='left', on=onkey)
        pd.DataFrame.to_csv(df_chis, save_path, sep=',', encoding="utf_8_sig")
        print(datetime.now())

    return df_chis




df_list = pd.read_excel(r'd:/data/model/model_dict.xlsx')
df = pd.read_excel(r'd:/data/model/use_data.xlsx')
df = df.fillna(-99)

lisan_list = ['sex']
list_var = list(df_list[(df_list.使用==1)&(df_list.属性=="num")]['英文'])
df = df[(df.classification == 'good')|(df.classification == 'bad')]
df['user_mark'] = df['classification'].map(lambda x: 1 if x=="good" else 0)
re_trans(df, list_var, 'user_mark', 'id', save_path=r'd:/data/model/data_614.csv')


df = pd.read_csv('d:/data/model/data_614.csv')
# df['product'] = df['con_product_name']
dfc = split_random(df, 5)
df_split = set_train_test(dfc, 5, 1)
cal_woe(df_split, 'classification', 'id', feature_list=list_var,
        other_var=['id', 'classification', 'user_mark', 'train_test'])



