from personal.mysqldb import ToMysql
import pymysql
import pandas as pd
from dateutil.parser import parse
import numpy as np
import json
import decimal
import re
import string
from datetime import datetime
import time
import numba

np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 100000
pd.options.display.max_columns = 800
pd.set_option('expand_frame_repr', False)


def get_good(x, y):
    z = ''
    if x >= 2:
        z = 'bad'
    elif (x < 2) & (y >= 6):
        z = 'good'
    else:
        z = 'unknow'
    return z

def get_mark(x,y):
    z=-99
    if x>=1:
        z=0
    elif (x<1) & (y>=6):
        z=1
    else:
        z=-99
    return z

def get_mark2(x):
    if x == "good":
        s = 1
    elif x=="bad":
        s = 0
    else:
        s = -99
    return s


@numba.jit()
def Chi2(df_arr, allBadRate):
    arr_except = df_arr[:, 1] * allBadRate
    arr = np.column_stack((df_arr[:, 2], arr_except))
    chi = (arr[:, 0] - arr[:, 1])**2/arr[:, 1]
    chi2 = sum(chi)
    return chi2

# ## 卡方计算
# def Chi2(df, total_col, bad_col, allBadRate):
#     '''
#         :param df: the dataset containing the total count and bad count
#         :param total_col: total count of each value in the variable
#         :param bad_col: bad count of each value in the variable
#         :param overallRate: the overall bad rate of the training set
#         :return: the chi-square value
#         '''
#     df2 = df.copy()
#     df2['expect'] = df[total_col].apply(lambda x: x * allBadRate)
#     combined = zip(df2['expect'], df[bad_col])
#     chi = [(i[1] - i[0]) ** 2 / i[0] for i in combined]
#     chi2 = sum(chi)
#     return chi2

def ChiMerge_MaxInterval(df, col, target, max_interval=5):
    '''
        :param df: the dataframe containing splitted column, and target column with 1-0
        :param col: splitted column
        :param target: target column with 1-0
        :param max_interval: the maximum number of intervals. If the raw column has attributes less than this parameter, the function will not work
        :return: the combined bins
    '''

    col_levels = set(df[col])  # 将col列处理为集合，并排除掉缺失值
    col_levels.remove(-99) if -99 in col_levels else None
    col_levels = sorted(list(col_levels))
    col_original_count = len(col_levels)
    if col_original_count <= max_interval:
        print('The original levels for {} is less than or equal to max intervals'.format(col))
    else:
        # Step 1: group the dataset by col and work out the total count & bad count in each level of the raw column
        total = df.groupby([col])[target].count()
        df_total = pd.DataFrame({'total': total})
        bad = df.groupby([col])[target].sum()
        df_bad = pd.DataFrame({'bad': bad})
        regroup = df_total.merge(df_bad, left_index=True, right_index=True, how='left')

        regroup.reset_index(level=0, inplace=True)


        N = sum(regroup['total'])
        B = sum(regroup['bad'])

        allBadRate = B * 1.0/N   # 统计全部的坏样本率

        # initially, each single attribute forms a single interval

        group_intervals = [[i] for i in col_levels]

        group_num = len(group_intervals)
        while group_num > max_interval:
            # in each step of iteration, we calcualte the chi-square value of each atttribute
            chisq_list = []
            for i in group_intervals:
                df2 = regroup.loc[regroup[col].isin(i)]
                df_arr = df2.values
                chisq = Chi2(df_arr, allBadRate)

                chisq_list.append(chisq)

            # find the interval corresponding to minimum chi-square, and combine with the neighbore with smaller chi-square
            min_position = chisq_list.index(min(chisq_list))

            if min_position == 0:
                combined_position = 1
            elif min_position == group_num - 1:
                combined_position = min_position - 1
            else:  ## 如果在中间，则选择左右两边卡方值较小的与其结合
                if chisq_list[min_position - 1] < chisq_list[min_position + 1]:
                    combined_position = min_position - 1
                else:
                    combined_position = min_position + 1
            group_intervals[min_position] = group_intervals[min_position] + group_intervals[combined_position]

            # after combining two intervals, we need to remove one of them
            group_intervals.remove(group_intervals[combined_position])
            group_num = len(group_intervals)

        group_intervals = [sorted(i) for i in group_intervals]
        cut_off_points = [i[-1] for i in group_intervals[:-1]]

        return cut_off_points


def ChiMerge_MinChisq(df, col, target, confidenceVal=3.841):
    '''
    :param df: the dataframe containing splitted column, and target column with 1-0
    :param col: splitted column
    :param target: target column with 1-0
    :param confidenceVal: the specified chi-square thresold, by default the degree of freedom is 1 and using confidence level as 0.95
    :return: the splitted bins
    '''
    col_levels = set(df[col])
    total = df.groupby([col])[target].count()
    total = pd.DataFrame({'total': total})
    bad = df.groupby([col])[target].sum()
    bad = pd.DataFrame({'bad': bad})
    regroup = total.merge(bad, left_index=True, right_index=True, how='left')
    regroup.reset_index(level=0, inplace=True)
    N = sum(regroup['total'])
    B = sum(regroup['bad'])
    overallRate = B * 1.0 / N
    col_levels = sorted(list(col_levels))
    groupIntervals = [[i] for i in col_levels]
    groupNum = len(groupIntervals)
    while (1):  # the termination condition: all the attributes form a single interval; or all the chi-square is above the threshould
        if len(groupIntervals) == 1:
            break
        chisqList = []
        for interval in groupIntervals:
            df2 = regroup.loc[regroup[col].isin(interval)]
            chisq = Chi2(df2, 'total', 'bad', overallRate)
            chisqList.append(chisq)
        min_position = chisqList.index(min(chisqList))
        if min(chisqList) >= confidenceVal:
            break
        if min_position == 0:
            combinedPosition = 1
        elif min_position == groupNum - 1:
            combinedPosition = min_position - 1
        else:
            if chisqList[min_position - 1] <= chisqList[min_position + 1]:
                combinedPosition = min_position - 1
            else:
                combinedPosition = min_position + 1
        groupIntervals[min_position] = groupIntervals[min_position] + groupIntervals[combinedPosition]
        groupIntervals.remove(groupIntervals[combinedPosition])
        groupNum = len(groupIntervals)
    return groupIntervals


def BadRateEncoding(df, col, target):
    '''
    :param df: dataframe containing feature and target
    :param col: the feature that needs to be encoded with bad rate, usually categorical type
    :param target: good/bad indicator
    :return: the assigned bad rate to encode the categorical fature
    '''
    total = df.groupby([col])[target].count()
    total = pd.DataFrame({'total': total})
    bad = df.groupby([col])[target].sum()
    bad = pd.DataFrame({'bad': bad})
    regroup = total.merge(bad, left_index=True, right_index=True, how='left')
    regroup.reset_index(level=0, inplace=True)
    regroup['bad_rate'] = regroup.apply(lambda x: x.bad * 1.0 / x.total, axis=1)
    br_dict = regroup[[col, 'bad_rate']].set_index([col]).to_dict(orient='index')

    df['badRateEnconding'] = df.loc[:, ['data_id', col, target]].apply(lambda x: br_dict[x[col]]['bad_rate'], axis=1)
    return {'encoding': df, 'br_rate': br_dict}


## 给每个值重新编码为分段标签——对应ChiMerge_MinChisq方法
def get_cat(x, tt):
    z = ''
    for i in tt:
        print(i)
        if min(i) <= x <= max(i):
            z = str(round(min(i), 2)) + '~' + str(round(max(i), 2))
    return z


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


def chi_trans(df, ChiMerge_list, target, onkey, save_path):
    df_chis = df.loc[:, ['data_id', 'user_mark']]  # 切片，先填充缺失值为-99
    code_list = []
    for col in ChiMerge_list:
        print(col)
        df[col] = df[col].replace('-', None).astype(float)

        df[col] = df[col].map(lambda x: round(x / 1000, 1)) if abs(df[col].mean()) >= 1000 else df[col]
        df_chi = df.loc[:, [onkey, col, target]]
        df_chi = df_chi.fillna(-99)
        split_box = ChiMerge_MaxInterval(df_chi, col, target, max_interval=6)
        print(split_box)
        code_dict = {'col_name': col, 'split_box': split_box}
        if split_box:
            df_chi[col] = df_chi[col].apply(lambda x: get_point_dur(x, split_box))
        df_chi = df_chi.loc[:, [onkey, col]]
        df_chis = pd.merge(df_chis, df_chi, how='left', on=onkey)

        pd.DataFrame.to_csv(df_chis, save_path, sep=',')
        code_list.append(code_dict)
        j = json.dumps(code_list)
        with open(r'E:\hoomsun_data\analysis\models\split_code' + save_path[len(save_path)-10: len(save_path)-4:] + '.json', 'w') as j_file:
            j_file.write(j)
        j_file.close()
        print(datetime.now())

    return df_chis


# # 计算WOE与IV
def CalcWOE(df, col, target, excel_path):
    '''
    :param df: dataframe containing feature and target
    :param col: 注意col这列已经经过分箱了，现在计算每箱的WOE和总的IV。
    :param target: good/bad indicator
    :return: 返回每箱的WOE(字典类型）和总的IV之和。
    '''
    total = df.groupby([col])[target].count()
    total = pd.DataFrame({'total': total})
    bad = df.groupby([col])[target].sum()
    bad = pd.DataFrame({'bad': bad})
    regroup = total.merge(bad, left_index=True, right_index=True, how='left')
    regroup.reset_index(level=0, inplace=True)
    N = sum(regroup['total'])
    B = sum(regroup['bad'])
    regroup['good'] = regroup['total'] - regroup['bad']
    G = N - B
    regroup['bad_pcnt'] = regroup['bad'].map(lambda x: x*1.0/B)
    regroup['good_pcnt'] = regroup['good'].map(lambda x: x * 1.0 / G)
    regroup['WOE'] = regroup.apply(lambda x: np.log(x.good_pcnt*1.0/x.bad_pcnt), axis = 1)
    WOE_dict = regroup[[col, 'WOE']].set_index(col).to_dict(orient='index')
    regroup['IV'] = regroup.apply(lambda x: (x.good_pcnt-x.bad_pcnt)*np.log(x.good_pcnt*1.0/x.bad_pcnt), axis =1)
    IV = sum(regroup['IV'])
    pd.DataFrame.to_excel(regroup, excel_writer=excel_path, sheet_name=col)
    return {"WOE": WOE_dict, 'IV': IV}

# # badRate单调检查  检查分箱以后每箱的bad_rate的单调性，如果不满足，那么继续进行相邻的两箱合并，知道bad_rate单调为止。(可以放宽到U型)
def BadRateMonotone(df, sortByVar, target):
    # df[sortByVar]这列数据已经经过分箱
    df = df[df[sortByVar] != -99]
    df2 = df.sort([sortByVar])
    total = df2.groupby([sortByVar])[target].count()
    total = pd.DataFrame({'total': total})
    bad = df2.groupby([sortByVar])[target].sum()
    bad = pd.DataFrame({'bad': bad})
    regroup = total.merge(bad, left_index=True, right_index=True, how='left')
    regroup.reset_index(level=0, inplace=True)
    combined = zip(regroup['total'], regroup['bad'])
    badRate = [x[1]*1.0/x[0] for x in combined]
    badRateMonotone = [badRate[i]<badRate[i+1] for i in range(len(badRate)-1)]
    Monotone = len(set(badRateMonotone))
    if Monotone == 1:
        return True
    else:
        return False


# read_path = r'E:\hoomsun_data\analysis\models\data_trans_all.csv'
# df = pd.read_csv(read_path, encoding='gbk')
# result = []
# for col in ChiMerge_list1:
#     re = col + ' ' + str(BadRateMonotone(df, col, 'user_mark'))
#     print(re)
#     result.append(re)



read_path = r"d:\hoomsun_data\analysis\models\model_datav2.xlsx"
df = pd.read_excel(read_path)
print(df.shape)
df = df[df.card_account == df.card_account]

# df['user_mark'] = df.apply(lambda x: get_mark(x.history_max_qici, x.current_period), axis=1)
df['user_mark'] = df['classification'].map(get_mark2)
df = df[df.user_mark != -99]
#
# save_path = r"E:\hoomsun_data\analysis\models\数据源自有加三方6.29t.xlsx"
# df.to_excel(save_path)

# 手工调整后重新分箱

df_list = pd.read_excel(r'd:\hoomsun_data\analysis\models\数据字典v2(1).xlsx')
lisan_list = list(df_list[df_list.属性 == 'cat']['英文'])
ChiMerge_list_recode = list(df_list[(df_list['属性']== 'num') & (df_list['是否使用']==1)]['英文'])

# read_path = r'E:\hoomsun_data\analysis\models\数据源自有加三方6.29t.xlsx'
# df = pd.read_excel(read_path)


print(df.head(5))
print(df.shape)

def re_trans(df, ChiMerge_list, target, onkey, save_path):
    df_chis = df.loc[:, ['loan_id', 'user_mark', 'classification']]
    for var_li in lisan_list:
        df_li = df.loc[:, ['loan_id', var_li]]
        df_chis = pd.merge(df_chis, df_li, how='left', on='loan_id')
    for col in ChiMerge_list:
        print(col)
        df[col] = df[col].replace('-', None).astype(float)
        df_chi = df.loc[:, [onkey, col, target]]
        df_chi = df_chi.fillna(-99)
        with open(r'd:\hoomsun_data\analysis\models\split_code_fix.json') as j_file:
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

re_trans(df, ChiMerge_list_recode, 'user_mark', 'loan_id', save_path=r'd:\hoomsun_data\analysis\models\data_8.17.csv')


