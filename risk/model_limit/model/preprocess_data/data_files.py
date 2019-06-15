import sys
from pathlib import Path
filename = 'model_limit'
paths = str(Path(__file__))
final_path = paths[:paths.find(filename) + len(filename)]
sys.path.append(final_path)
from model.preprocess_data.db_access import oracle_db,loacl_db,hd_db
import numpy as np
import pandas as pd
from datetime import timedelta
from sqlalchemy.types import NVARCHAR, Float,DateTime,Integer
from dateutil.parser import parse
#summary_table
def updatesummary():

    conn = oracle_db('hsdc','hsdc2018')
    sql = r'SELECT b.ID_CARD,b.SELECTTIME,s.* FROM CREDIT_BASIC b INNER JOIN CREDIT_SUMMARY s ON b.UUID = s.UUID where s.card_account is not null'
    df_summary = pd.read_sql(sql, conn)
    print(df_summary.shape)

    conn = oracle_db('credit','credit2018')
    sql = r'SELECT al.loan_id,al.con_no, al.card_no AS id_card,al.loan_date,ha.APPLY_DATE FROM AFTER_LOANBAL al left join HS_APPLY ha on ha.loan_id=al.loan_id'
    df_apply = pd.read_sql(sql, conn)
    df_apply.sort_values('apply_date')
    print(df_apply.shape)
    df_apply=df_apply[df_apply['loan_date']>df_apply['apply_date']]
    print(df_apply.shape)
    df_apply.drop_duplicates('apply_date',inplace=True,keep='last')

    df_summary['selecttime'] = df_summary['selecttime'].astype('datetime64[ns]')
    df = pd.merge(df_apply, df_summary, on='id_card', how='inner')
    print(df.shape)
    df['M'] = df.apply_date - df.selecttime
    df = df[(df.M > timedelta(days=0)) & (df.M < timedelta(days=10))]
    print(df.shape)
    df.drop_duplicates('loan_id',inplace=True,keep='last')
    df.columns=[item.lower() for item in df.columns]
    return df

def get_debt(x,ratio,house):
    #ratio 信用卡负债占比，house 房贷是否算
    debt=round((x.card_award_used_highest*ratio+x.loan_house_moneymonthly*house+x.loan_other_moneymonthly),1)
    return debt

#debet_table
def debet():
    conn=loacl_db()
    sql='select id_card,card_award_used_highest,loan_house_moneymonthly,loan_other_moneymonthly from credit_statistic limit 200'
    df=pd.read_sql(sql,conn)
    df['in_debt_house_1'] = df.apply(lambda x: get_debt(x,0.01,True),axis=1)
    df['in_debt_nohouse_1'] = df.apply(lambda x: get_debt(x,0.01,False),axis=1)
    df['in_debt_house_5'] = df.apply(lambda x: get_debt(x,0.05,True),axis=1)
    df['in_debt_nohouse_5'] = df.apply(lambda x: get_debt(x,0.05,False),axis=1)
    df['in_debt_house_10'] = df.apply(lambda x: get_debt(x,0.1,True),axis=1)
    df['in_debt_nohouse_10'] = df.apply(lambda x: get_debt(x,0.1,False),axis=1)
    df.to_sql('debet', con=conn, if_exists='replace',dtype=sqlcol(df))
    print('debet table finish')

def get_classif(x,y,z):
    classif=''
    if z==1:
        classif='good'
    else:
        if y == y:
            if (x >= 6) & (y <=15):
                classif = 'good'
            elif int(y) > 15:
                classif = 'bad'
            else:
                classif = 'unknow'
        else:
            classif = 'no'
    return classif

def calculating_age(apply_date, id_card):
    data_in = apply_date
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


def idcard_info(x):
    x['idcard_district']=x['id_card'][:6]
    x['idcard_area']=get_area(int(x[4:5]))
    x['sex']='female' if int(x['id_card'][-2])% 2 == 0 else 'male'
    x['age']=calculating_age(x['apply_date'], x['id_card'])
    return x

#cust_label table
def cust_label():
    conn = hd_db()
    sql = 'SELECT con_no,should_period,clear,hst_max_overdue_days FROM warehouse_summary'
    my_conn=loacl_db()
    summary_sql='select uuid,con_no,apply_date,id_card from summary'
    df_summary=pd.read_sql(summary_sql,my_conn)
    df_summary=df_summary.apply(lambda x:idcard_info(x),axis=1)
    df = pd.read_sql(sql, conn)
    df=df_summary.merge(df,how='left',on='con_no')
    df['classification'] = df.apply(lambda x: get_classif(x.should_period, x.hst_max_overdue_days,x.clear),axis=1)
    df.to_sql('cust_label', con=my_conn, if_exists='replace',dtype=sqlcol(df))
    print('cust_label table finish')

def sqlcol(dfparam):    

    dtypedict = {}
    for i,j in zip(dfparam.columns, dfparam.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=100)})
        if "datetime" in str(j):
            dtypedict.update({i: DateTime})
        if "float" in str(j):
            dtypedict.update({i: Float})
        if "int" in str(j):
            dtypedict.update({i: Integer})
    return dtypedict
import math
def handle_inf(x):
    return 0 if math.isinf(x) else x

if __name__ == "__main__":
    # cust_label()
    # df=updatesummary()
    # use_cols={'loan_id':NVARCHAR(length=100), 'con_no':NVARCHAR(length=100), 
    # 'id_card':NVARCHAR(length=100), 'loan_date':DateTime, 'apply_date':DateTime, 
    # 'query_date':DateTime, 'card_account':Float, 'card_notsettled':Float, 'card_overdue':Float,
    # 'card_90overdue':Float, 'card_guaranty':Float, 'housing_loan_account':Float,
    # 'housing_loan_notsettled':Float, 'housing_loan_overdue':Float,
    # 'housing_loan_90overdue':Float, 'housing_loan_guaranty':Float, 'other_loan_account':Float,
    # 'other_loan_notsettled':Float, 'other_loan_overdue':Float, 'other_loan_90overdue':Float,
    # 'other_loan_guaranty':Float,'uuid':NVARCHAR(length=200),'selecttime':DateTime}
    # df=df[list(use_cols.keys())]
    # print(df.shape)
    df=pd.read_excel(r'C:\Users\Administrator\Desktop\credit_data.xlsx')
    conn=loacl_db()
    # df=df.applymap(handle_inf)
    df.to_excel('f:/data_6.6.xlsx')
    # df.to_sql('credit_data', con=conn,index=False, if_exists='replace',dtype=sqlcol(df))


