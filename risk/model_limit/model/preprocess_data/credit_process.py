import pandas as pd
import numpy as np
import pymysql
import math
from dateutil.parser import parse
import re
from pandas.tseries.offsets import Day
import datetime
from sqlalchemy import types,create_engine
from db_access import oracle_db,loacl_db
time1=datetime.datetime.now()
# def into_time(into_id):
#     y = ''
#     if re.findall('\d{8}', into_id):
#         y = re.findall('\d{8}', into_id)[0]
#         try:
#             parse(y)
#         except ValueError:
#             y = '20200601'
#     else:
#         y = '20200601'
#     return parse(y)
def into_time(into_id):
    return into_id

def interval_month(start_date, end_date):
    months = 0
    if start_date.day > end_date.day:
        months = (end_date.year - start_date.year)*12 + (end_date.month - start_date.month) - 1
    elif start_date.day <= end_date.day:
        months = (end_date.year - start_date.year)*12 + (end_date.month - start_date.month)
    return months

def interval_day(start_date, end_date):
    days=(end_date-start_date).days+1
    return days

def pt(data_source, field, fun, name,fill=True):
    table = pd.DataFrame(pd.pivot_table(data_source, index='uuid', values=field, aggfunc=fun))
    table.rename(columns={field: name}, inplace=True)
    if fun=='count':
        table.fillna(0,inplace=True)
    return table


def get_rate(_bank, _type, _month, raw):
    _bank=str(_bank)
    if (_type == '公积金') and (_month < 61):
        _rate = 0.0275
    elif (_type == '公积金') and (_month > 60):
        _rate = 0.0325
    elif (_type == '商贷') and (_month < 61):
        _rate = 0.047
    elif (_type == '商贷') and (_month > 60):
        _rate = 0.049
    elif (_type == '农户贷款') and (_month <= 6):
        _rate = 0.056
    elif (_type == '农户贷款') and (_month > 6) and (_month <= 60):
        _rate = 0.0615
    elif (_type == '农户贷款') and (_month > 60):
        _rate = 0.0655
    elif (_type == '助学贷款') and (_month <= 60):
        _rate = 0.0475
    elif (_type == '助学贷款') and (_month > 60):
        _rate = 0.049
    elif re.match(regex1, _bank) and (_type == '抵押贷款') and (_month > 60):
        _rate = 0.065
    elif re.match(regex1, _bank) and (_type == '抵押贷款') and (_month <= 12):
        _rate = 0.05
    elif re.match(regex1, _bank) and (_type == '抵押贷款') and (_month > 12) and (_month <= 60):
        _rate = 0.058
    elif re.search(regex1, _bank) == None and (_type == '抵押贷款') and (_month > 12):
        _rate = 0.15
    elif re.search(regex1, _bank) == None and (_type == '抵押贷款') and (_month <= 12):
        _rate = 0.13
    elif re.match(regex1, _bank) and (_type == '经营贷款') and (_month <= 12):
        _rate = 0.06
    elif re.match(regex1, _bank) and (_type == '经营贷款') and (_month > 12) and (_month <= 36):
        _rate = 0.0615
    elif re.match(regex1, _bank) and (_type == '经营贷款') and (_month > 36) and (_month <= 60):
        _rate = 0.064
    elif re.match(regex1, _bank) and (_type == '经营贷款') and (_month > 60):
        _rate = 0.0655
    elif re.match(regex1, _bank) and (raw == '0'):
        _rate = 0.12
    elif re.search(r'网商银行|微众银行', _bank):
        _rate = 0.1825
    else:
        _rate = 0.28
    return _rate

def get_loan_type(a, b):
    c = ''
    if a == '购房贷款' and re.search(r'公积金', b):
        c = '公积金贷款'
    elif a == '购房贷款'and str(re.search(r'公积金', b)) == 'None':
        c = '商贷'
    elif a == '购房贷款'and re.search(r'住房', b):
        c = '商贷'
    elif a == '其他贷款' and re.search(r'农户', b):
        c = '农户贷款'
    elif a == '其他贷款' and re.search(r'助学', b):
        c = '助学贷款'
    elif a == '其他贷款' and re.search(r'经营', b):
        c = '经营贷款'
    elif a == '其他贷款' and re.search(r'抵押', b):
        c = '抵押贷款'
    else:
        c = '其他贷款'
    return c


def get_settle(credit_month, settle_month, money, pmt, yuqi_money, n):
    settle_money = 0
    if (credit_month <= n) & (settle_month < 0):
        settle_money = money
    elif (credit_month <= n) & (settle_month >= 0):
        settle_money = credit_month * pmt
    elif (credit_month > n) & (settle_month >= 0):
        settle_money = n * pmt
    elif (credit_month > n) & (settle_month <= 0) & (abs(settle_month) >= n):
        settle_money = (n + settle_month) * pmt
    elif (credit_month > n) & (settle_month <= 0) & (abs(settle_month) < n):
        settle_money = 0
    return settle_money if settle_money > yuqi_money else 0


def get_settle_future(settle_month, repay_type, money, pmt, yuqi_money, n):
    settle_money_future = 0
    if settle_month < 0:
        settle_money_future = 0
    elif (settle_month < n) & (settle_month >= 0) & (repay_type == '等额本息'):
        settle_money_future = (settle_month + 1) * pmt
    elif (settle_month < n) & (settle_month >= 0) & (repay_type == '先息后本'):
        settle_money_future = money
    elif (settle_month >= n) & (repay_type == '等额本息'):
        settle_money_future = n * pmt
    elif (settle_month >= n) & (repay_type == '等额本息'):
        settle_money_future = money
    return settle_money_future + yuqi_money


regex1 = re.compile(r'(^((?!公司).)*银行((?!公司).)*$)|中国邮政储蓄银行股份有限公司')
regex2 = re.compile(r'工商银行|农业银行|中国银行|建设银行|交通银行|招商银行|浦发银行|中信银行|华夏银行|光大银行|民生银行|兴业银行|广发银行|平安银行|浙商银行|渤海银行|恒丰银行')
regex3 = re.compile(r'天津银行|河北银行|张家口银行|承德银行|秦皇岛银行|唐山银行|廊坊银行|保定银行|沧州银行|衡水银行|邢台银行|邯郸银行|'
                    r'晋商银行|大同银行|晋城银行|晋中银行|阳泉市商业银行|长治银行|包商银行|内蒙古银行|鄂尔多斯银行|乌海银行|盛京银行|'
                    r'鞍山银行|抚顺银行|本溪市商业银行|丹东银行|锦州银行|营口银行|营口沿海银行|阜新银行|辽阳银行|铁岭市商业银行|朝阳银行|'
                    r'盘锦市商业银行|葫芦岛银行|吉林银行|龙江银行|上海银行|浙江稠州商业银行|莱商银行|江西银行|徽商银行|杭州银行|江苏银行|'
                    r'南京银行|江苏长江商业银行|苏州银行|温州银行|嘉兴银行|湖州银行|绍兴银行|金华银行|台州商行|浙江泰隆商业银行|宁波银行|'
                    r'福建海峡银行|泉州银行|九江银行|赣州银行|上饶银行|齐鲁银行|齐商银行|烟台银行|潍坊银行|临商银行|威海市商业银行|日照银行|'
                    r'德州银行|东营银行|济宁银行|泰安市商业银行|枣庄银行|中原银行|郑州银行|洛阳银行|平顶山银行|焦作中旅银行|湖北银行|'
                    r'汉口银行|长沙银行|华融湘江银行|广州银行|珠海华润银行|东莞银行|广东华兴银行|广东南粤银行|广西北部湾银行|柳州银行|'
                    r'桂林银行|海南银行|重庆三峡银行|浙江民泰商业银行|哈尔滨银行|贵阳银行|成都银行|泸州市商业银行|攀枝花市商业银行|'
                    r'宜宾市商业银行|乐山市商业银行|南充市商业银行|自贡市商业银行|长城华西银行|遂宁市商业银行|绵阳市商业银行|凉山州商业银行|'
                    r'雅安市商业银行|达州市商业银行|重庆银行|贵州银行|富滇银行|曲靖市商业银行|云南红塔银行|西藏银行|长安银行|西安银行|兰州银行|'
                    r'甘肃银行|青海银行|石嘴山银行|乌鲁木齐银行|昆仑银行|新疆汇和银行|库尔勒银行|哈密市商业银行|大连银行|宁波东海银行|'
                    r'宁波通商银行|厦门银行|厦门国际银行|青岛银行')
regex4 = re.compile(r'村镇银行')
regex5 = re.compile(r'农村信用|农村商业|农村合作')
regex6 = re.compile(r'汇丰中国|东亚银行|渣打银行|荷兰银行|东方汇理银行|中信嘉华银行|外换银行|德意志银行|法国兴业银行|国民银行|韩亚银行|'
                    r'蒙特利尔银行|摩根大通银行|瑞士银行|新韩银行|企业银行|友利银行|花旗中国|瑞穗中国|恒生中国|星展中国|三菱中国|华侨永亨中国|'
                    r'南商中国|大华中国|法巴中国|三井中国|汇理中国|盘谷中国|澳新中国|富邦华|华美中国|正信银行|浦发硅谷银行|星明财务|'
                    r'永丰银行|首都银行|协和银行有限公司|摩根士丹利国际银行|新联商业银行|华商银行|大新银行|中信银行国际|玉山银行')
regex7 = re.compile(r'小额贷款')
regex8 = re.compile(r'消费金融')
regex9 = re.compile(r'信托')
regex10 = re.compile(r'汽车金融')
regex11 = re.compile(r'平安普惠|哈尔滨银行龙青支行')
regex12 = re.compile(r'融资担保')
regex13 = re.compile(r'保险')
uuid='ac7782983f2f4e6da1ae54b0bea70fb2'
sql_card = f"SELECT uuid,bank,grant_date,account_category,account_state,query_date,credit_line,used_line,overdue,five_years_overdue,ninety_days_overdue,overdue_money,account_type FROM credit_card"
sql_loan = f"SELECT uuid,institution,grant_date,money,account_category,expired_date,query_date,figure,overdue,years5_overdue,days90_overdue,type as loan_type,yuqi_money,loan_state,account_category_main FROM credit_loan"
sql_credit_c = f"SELECT uuid,chaxun_date,caozuoyuan,reason FROM credit_chaxun1"
sql_credit_p = f"SELECT uuid,chaxun_date,reason FROM credit_chaxun2"
sql_summary=f'select uuid,selecttime,con_no from summary'
conn_credit = oracle_db('hsdc','hsdc2018')
my_conn=loacl_db()
df_summary=pd.read_sql(sql_summary,my_conn)
df_card = pd.read_sql(sql_card, conn_credit)
df_loan = pd.read_sql(sql_loan, conn_credit)
df_credit_c = pd.read_sql(sql_credit_c, conn_credit)
df_credit_p = pd.read_sql(sql_credit_p, conn_credit)
df_credit = pd.concat([df_credit_c, df_credit_p])
#union summary
df_card=df_summary.merge(df_card,how='left',on='uuid')
df_loan=df_summary.merge(df_loan,how='left',on='uuid')
df_credit=df_summary.merge(df_credit,how='left',on='uuid')

df_card['grant_date'] = df_card.grant_date.astype('datetime64[ns]')
df_card['query_date'] = df_card.query_date.astype('datetime64[ns]')
# df_card['selecttime'] = df_card.selecttime.map(into_time)
df_card.loc[df_card.account_type.isnull(), 'account_type'] = '无'
df_card = df_card[df_card.account_type.isin(['人民币账户', '无'])]

df_card['credit_month'] = df_card.apply(lambda x: interval_month(x.grant_date, x.selecttime), axis=1)
df_card.loc[df_card.credit_month < 0, 'credit_month'] = 2
df_card['used_month'] = df_card.apply(lambda x: interval_month(x.grant_date, x.query_date), axis=1)
df_card.loc[df_card.used_month < 0, 'used_month'] = df_card.credit_month
df_card['record_month'] = df_card.used_month.mask(df_card.used_month > 60, 60)
df_card['overdue_per'] = (df_card.five_years_overdue / (df_card.record_month + 1)).mul(100).round(0)
df_card['exceeding'] = np.where(df_card.credit_line < df_card.used_line, 1, 0)
df_card['exceeding_money'] = (df_card.used_line - df_card.credit_line) * df_card.exceeding


# c1信用卡账户数（只计人民币账户）
c1 = pt(df_card, 'account_state', 'count', 'card_count_only_rmb')
# c2信用卡未结清/未销户账户数（只计人民币账户） !!不确定判断规则是否正确
c2 = pt(df_card[(df_card.account_state != '销户') & (df_card.account_state != '未激活')], 'account_state', 'count', 'card_count_card_notsettled')
# c3首张信用卡发卡日期
c3 = pt(df_card, 'grant_date', 'min', 'card_date_first')
# c4首张信用卡发卡状态
c4 = pt(df_card.sort_values(by=['selecttime', 'grant_date']), 'account_state', 'first', 'card_date_first_status')
# c5首张信用卡（正常使用）发卡日期,是否剔除使用额度为0的账户及非人民币账户？
c5 = pt(df_card[df_card.account_state == '正常'], 'grant_date', 'min', 'card_date_first_normal')
# c6最近一张信用卡发卡日期
c6 = pt(df_card, 'grant_date', 'max', 'card_date_new')
# c7信用历史时长（月，以所有信用卡计）
c7 = pt(df_card, 'credit_month', 'max', 'card_credit_history')
# c8信用历史时长（月，以正常信用卡计）
c8 = pt(df_card[df_card.account_state == '正常'], 'credit_month', 'max', 'card_credit_history_normal')
# c9首张信用卡授信额度
c9 = pt(df_card.sort_values(by=['selecttime', 'grant_date']), 'credit_line', 'first', 'card_award_first')
# c10首张信用卡（正常使用）授信额度
c10 = pt(df_card[df_card.account_state == '正常'].sort_values(by=['selecttime', 'grant_date']), 'credit_line', 'first', 'card_award_first_normal')
# c11最近一张信用卡授信额度
c11 = pt(df_card[df_card.account_state == '正常'].sort_values(by=['selecttime', 'grant_date']), 'credit_line', 'last', 'card_award_new')
# c12信用卡单卡最高授信额度
c12 = pt(df_card[df_card.account_state == '正常'], 'credit_line', 'max', 'card_award_highest')
# c13信用卡单卡最高授信额度(优质银行)
c13 = pt(df_card[(df_card.bank.str.findall(regex2).str.len() > 0) & (df_card.account_state == '正常')], 'credit_line', 'max', 'card_award_highest_goodbank')
# c14最高授信额度信用卡已使用额度/li增加了used_line排序
c14 = pt(df_card[df_card.account_state == '正常'].sort_values(by=['selecttime', 'credit_line','used_line']), 'used_line', 'last', 'card_award_used_highest')
# c15信用卡总授信额度/li找不出原因
c15 = pt(df_card[df_card.account_state == '正常'], 'credit_line', 'sum', 'card_award_sum')
# c16信用卡总授信额已使用额度
c16 = pt(df_card[df_card.account_state == '正常'], 'used_line', 'sum', 'card_award_used')
# c17信用卡超额张数
c17 = pt(df_card, 'exceeding', 'sum', 'card_exceeding_count_')
# c18信用卡超额额度总计
c18 = pt(df_card, 'exceeding_money', 'sum', 'card_exceeding_money_sum')
# c19信用卡超额最大额度
c19 = pt(df_card, 'exceeding_money', 'max', 'card_exceeding_money_max')
# c20信用卡当前逾期张数,/li没有的话应该是0？
c20 = pt(df_card[df_card.overdue_money > 0], 'overdue_money', 'count', 'card_overdue_count')
# c21信用卡当前逾期总金额
c21 = pt(df_card, 'overdue_money', 'sum', 'card_overdue_money_sum')
# c22信用卡当前逾期最大金额
c22 = pt(df_card, 'overdue_money', 'max', 'card_overdue_money_max')
# c23信用卡五年内逾期总月数
c23 = pt(df_card, 'five_years_overdue', 'sum', 'card_overdue_months_in_5y')
# c24信用卡两年内逾期总月数（仅统计两年内发放的信用卡）
c24 = pt(df_card[df_card.credit_month <= 24], 'five_years_overdue', 'sum', 'card_overdue_months_in_2y')
# c25信用卡两年内逾期总月数（仅统计一年内发放的信用卡）
c25 = pt(df_card[df_card.credit_month <= 12], 'five_years_overdue', 'sum', 'card_overdue_months_in_1y')
# c26信用卡五年内90天以上逾期次数
c26 = pt(df_card, 'ninety_days_overdue', 'sum', 'card_overdue_over90_in_5y')
# c27信用卡两年内90天以上逾期次数（仅统计两年内发放的信用卡）
c27 = pt(df_card[df_card.credit_month <= 24], 'ninety_days_overdue', 'sum', 'card_overdue_over90_in_2y')
# c28信用卡两年内90天以上逾期次数（仅统计一年内发放的信用卡）
c28 = pt(df_card[df_card.credit_month <= 12], 'ninety_days_overdue', 'sum', 'card_overdue_over90_in_1y')
# c29单张信用卡最高逾期比例/li应该减一个月，尚未修改
c29 = pt(df_card, 'overdue_per', 'max', 'card_overdue_highest')
# c30信用卡逾期比例，/li尚未修改
pt_overdue_months = pd.pivot_table(df_card, index='uuid', values=['record_month', 'five_years_overdue'], aggfunc='sum')
pt_overdue_months['card_overdue_ratio'] = pt_overdue_months.five_years_overdue / pt_overdue_months.record_month
c30 = pt_overdue_months.drop(['five_years_overdue', 'record_month'], axis=1)
# c31逾期比例>0且<10%的信用卡账户数
c31 = pt(df_card[(df_card.overdue_per > 0) & (df_card.overdue_per < 10)], 'overdue_per', 'count', 'card_overdue_0_10')
# c32逾期比例>=10%信用卡账户数
c32 = pt(df_card[df_card.overdue_per >= 10], 'overdue_per', 'count', 'card_overdue_10')
# c33逾期比例>=20%信用卡账户数
c33 = pt(df_card[df_card.overdue_per >= 20], 'overdue_per', 'count', 'card_overdue_20')
# c34逾期比例>=30%信用卡账户数/li overdue_per 计算错误
c34 = pt(df_card[df_card.overdue_per >= 30], 'overdue_per', 'count', 'card_overdue_30')
# c351年内发放的信用卡逾期比例>=10%信用卡账户数
c35 = pt(df_card[(df_card.credit_month <= 12) & (df_card.overdue_per >= 10)], 'overdue_per', 'count', 'card_overdue_10_extend_1y')
# c361年内发放的信用卡逾期比例>=20%信用卡账户数
c36 = pt(df_card[(df_card.credit_month <= 12) & (df_card.overdue_per >= 20)], 'overdue_per', 'count', 'card_overdue_20_extend_1y')
# c371年内发放的信用卡逾期比例>=30%信用卡账户数
c37 = pt(df_card[(df_card.credit_month <= 12) & (df_card.overdue_per >= 30)], 'overdue_per', 'count', 'card_overdue_30_extend_1y')
# c382年内发放的信用卡逾期比例>=10%信用卡账户数
c38 = pt(df_card[(df_card.credit_month <= 24) & (df_card.overdue_per >= 10)], 'overdue_per', 'count', 'card_overdue_10_extend_2y')
# c392年内发放的信用卡逾期比例>=20%信用卡账户数
c39 = pt(df_card[(df_card.used_month <= 24) & (df_card.overdue_per >= 20)], 'overdue_per', 'count', 'card_overdue_20_extend_2y')
# c402年内发放的信用卡逾期比例>=30%信用卡账户数
c40 = pt(df_card[(df_card.used_month <= 24) & (df_card.overdue_per >= 30)], 'overdue_per', 'count', 'card_overdue_30_extend_2y')
# c41信用卡降额张数
c41 = pt(df_card[df_card.account_state == '降额'], 'account_state', 'count', 'card_decrease')
# c42信用卡冻结张数
c42 = pt(df_card[df_card.account_state == '冻结'], 'account_state', 'count', 'card_freeze')
# c43信用卡呆账张数
c43 = pt(df_card[df_card.account_state == '呆账'], 'account_state', 'count', 'card_doubtful')
# c44信用卡止付张数
c44 = pt(df_card[df_card.account_state == '止付'], 'account_state', 'count', 'card_suspend')
# c45信用卡未激活张数
c45 = pt(df_card[df_card.account_state == '未激活'], 'account_state', 'count', 'card_unactivated')
# c46信用卡未销户且授信金额小于100的账户数
c46 = pt(df_card[(df_card.account_state != '销户') & (df_card.credit_line <= 100)], 'account_state', 'count', 'credit_less_100')

time2=datetime.datetime.now()
print(time2-time1)
df_loan['grant_date'] = df_loan.grant_date.astype('datetime64[ns]')
df_loan['query_date'] = df_loan.query_date.astype('datetime64[ns]')
df_loan['expired_date'] = df_loan.expired_date.astype('datetime64[ns]')
# df_loan['selecttime'] = df_loan.selecttime.map(into_time)
df_loan.loc[df_loan.expired_date != df_loan.expired_date, 'expired_date'] = df_loan.query_date
df_loan.loc[df_loan.expired_date == df_loan.query_date, 'query_date'] = df_loan.selecttime
df_loan.loc[df_loan.account_category_main != df_loan.account_category_main, 'account_category_main'] = df_loan.account_category
df_loan['credit_month'] = df_loan.apply(lambda x: interval_month(x.grant_date, x.selecttime) + 1, axis=1)
#li 不是应截止到合同日期的吗？
df_loan['used_month'] = df_loan.apply(lambda x: interval_month(x.grant_date, min(x.expired_date, x.query_date)), axis=1)
df_loan['record_month'] = df_loan.used_month.mask(df_loan.used_month > 60, 60)
df_loan['settle_month'] = df_loan.apply(lambda x: interval_month(x.selecttime, x.expired_date), axis=1)
df_loan['overdue_per'] = (df_loan.years5_overdue / df_loan.record_month).mul(100).round(0)

df_loan['bank_type'] = np.where(df_loan.institution.str.findall(regex1).str.len() > 0, 1, 0)
df_loan['loan_month'] = df_loan.apply(lambda x: interval_month(x.grant_date, x.expired_date) + 1, axis=1)
df_loan['loan_type'] = df_loan.apply(lambda x: get_loan_type(x.loan_type, x.account_category_main), axis=1)
df_loan['rate'] = 0
df_loan['rate'] = df_loan.apply(lambda x: get_rate(x.institution, x.loan_type, x.loan_month, x.rate), axis=1).round(3)
try:
    df_loan['pmt'] = -np.pmt(df_loan.rate / 12, df_loan.loan_month, df_loan.money).astype(float).round(2)
except:
    df_loan['pmt'] = 0
df_loan.pmt = df_loan.pmt.mask(df_loan.pmt < 0, 0)
df_loan['repay_money'] = df_loan.money.sub(df_loan.figure)
df_loan.repay_money = df_loan.repay_money.mask(df_loan.repay_money < 0, 0)
df_loan['repay_type'] = np.where(df_loan.repay_money > (df_loan.pmt * df_loan.used_month * 0.5), '等额本息', '先息后本')
df_loan.loan_state.replace('已结清', '结清', inplace=True)
df_loan['settle_6'] = df_loan.apply(lambda x: get_settle(x.credit_month, x.settle_month, x.money, x.pmt, x.yuqi_money, 6), axis=1)
df_loan['settle_3'] = df_loan.apply(lambda x: get_settle(x.credit_month, x.settle_month, x.money, x.pmt, x.yuqi_money, 3), axis=1)
df_loan['settle_1'] = df_loan.apply(lambda x: get_settle(x.credit_month, x.settle_month, x.money, x.pmt, x.yuqi_money, 1), axis=1)
df_loan['settle_future_1'] = df_loan.apply(lambda x: get_settle_future(x.settle_month, x.repay_type, x.money, x.pmt, x.yuqi_money, 1), axis=1)
df_loan['settle_future_3'] = df_loan.apply(lambda x: get_settle_future(x.settle_month, x.repay_type, x.money, x.pmt, x.yuqi_money, 3), axis=1)
df_loan['settle_future_6'] = df_loan.apply(lambda x: get_settle_future(x.settle_month, x.repay_type, x.money, x.pmt, x.yuqi_money, 6), axis=1)
df_loan['settle_future_12'] = df_loan.apply(lambda x: get_settle_future(x.settle_month, x.repay_type, x.money, x.pmt, x.yuqi_money, 12), axis=1)


# l1贷款总笔数
l1 = pt(df_loan, 'loan_type', 'count', 'loan_total_account')
# l2贷款未结清账户数
l2 = pt(df_loan[df_loan.loan_state != '结清'], 'loan_type', 'count', 'loan_notsettled_account')
# l3贷款已结清账户数
l3 = pt(df_loan[df_loan.loan_state == '结清'], 'loan_type', 'count', 'loan_settle_account')
# l4贷款在过去6个月内结清笔数/li settle_month计算错误
l4 = pt(df_loan[(df_loan.loan_state == '结清') & (df_loan.settle_month >= -6)], 'expired_date', 'count', 'loan_settle_past6m')
# l5贷款在过去3个月内结清笔数
l5 = pt(df_loan[(df_loan.loan_state == '结清') & (df_loan.settle_month >= -3)], 'expired_date', 'count', 'loan_settle_past3m')
# l6贷款在过去1个月内结清笔数
l6 = pt(df_loan[(df_loan.loan_state == '结清') & (df_loan.settle_month >= -1)], 'expired_date', 'count', 'loan_settle_past1m')
# l7贷款在未来1个月内待结清笔数
l7 = pt(df_loan[(df_loan.loan_state != '结清') & (df_loan.settle_month < 1)], 'expired_date', 'count', 'loan_settle_next1m')
# l8贷款在未来3个月内待结清笔数
l8 = pt(df_loan[(df_loan.loan_state != '结清') & (df_loan.settle_month < 3)], 'expired_date', 'count', 'loan_settle_next3m')
# l9贷款在未来6个月内待结清笔数
l9 = pt(df_loan[(df_loan.loan_state != '结清') & (df_loan.settle_month < 6)], 'expired_date', 'count', 'loan_settle_next6m')
# l10贷款在未来12个月内待结清笔数
l10 = pt(df_loan[(df_loan.loan_state != '结清') & (df_loan.settle_month < 12)], 'expired_date', 'count', 'loan_settle_next12m')
# l11贷款在过去6个月内结清金额/li不清楚怎么计算
l11 = pt(df_loan, 'settle_6', 'sum', 'loan_award_past6m')
# l12贷款在过去3个月内结清金额
l12 = pt(df_loan, 'settle_3', 'sum', 'loan_award_past3m')
# l13贷款在过去1个月内结清金额
l13 = pt(df_loan, 'settle_1', 'sum', 'loan_award_past1m')
# l14贷款在未来1个月内待结清金额
l14 = pt(df_loan, 'settle_future_1', 'sum', 'loan_award_next1m')
# l15贷款在未来3个月内待结清金额
l15 = pt(df_loan, 'settle_future_3', 'sum', 'loan_award_next3m')
# l16贷款在未来1个月内待结清金额
l16 = pt(df_loan, 'settle_future_6', 'sum', 'loan_award_next6m')
# l17贷款在未来1个月内待结清金额
l17 = pt(df_loan, 'settle_future_12', 'sum', 'loan_award_next12m')
# l18贷款最早发放日期
l18 = pt(df_loan, 'grant_date', 'min', 'loan_first')
# l19贷款最早发放日期（不含助学贷款）
l19 = pt(df_loan[df_loan.loan_type != '助学贷款'], 'grant_date', 'min', 'loan_first_notstudent')
# l20最近一笔贷款发放日期
l20 = pt(df_loan, 'grant_date', 'max', 'loan_date_nearest')
# l21最近一笔贷款发放日期（不含助学贷款）
l21 = pt(df_loan[df_loan.loan_type != '助学贷款'], 'grant_date', 'max', 'loan_date_nearest_notstudent')
# l22贷款发放机构为银行的笔数(1年内)
l22 = pt(df_loan[(df_loan.institution.str.findall(regex1).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_bank')
# l23贷款发放机构为国有大行或股份制银行的笔数(1年内)
l23 = pt(df_loan[(df_loan.institution.str.findall(regex2).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_bank_country_stock')
# l24贷款发放机构为城市商业银行的笔数(1年内)
l24 = pt(df_loan[(df_loan.institution.str.findall(regex3).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_bank_commerce')
# l25贷款发放机构为村镇银行的笔数(1年内)
l25 = pt(df_loan[(df_loan.institution.str.findall(regex4).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_bank_village')
# l26贷款发放机构为农村信用社或商业银行的笔数(1年内)
l26 = pt(df_loan[(df_loan.institution.str.findall(regex5).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_bank_rcu_commerce')
# l27贷款发放机构为外资银行的笔数(1年内)
l27 = pt(df_loan[(df_loan.institution.str.findall(regex6).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_bank_foreign')
# l28贷款发放机构为小额贷款公司的笔数(1年内)
l28 = pt(df_loan[(df_loan.institution.str.findall(regex7).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_mcc')
# l29贷款发放机构为消费金融公司的笔数(1年内)
l29 = pt(df_loan[(df_loan.institution.str.findall(regex8).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_cfc')
# l30贷款发放机构为信托公司的笔数(1年内)
l30 = pt(df_loan[(df_loan.institution.str.findall(regex9).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_trust')
# l31贷款发放机构为汽车金融公司的笔数(1年内)
l31 = pt(df_loan[(df_loan.institution.str.findall(regex10).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_afc')
# l32贷款发放机构为重点监测机构的笔数(1年内)
l32 = pt(df_loan[(df_loan.institution.str.findall(regex11).str.len() > 0) & (df_loan.credit_month < 12)], 'institution', 'count', 'loan_count_check')
# l33贷款为房贷的笔数(1年内)
l33 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month < 12)], 'loan_type', 'count', 'loan_count_house')
# l34贷款为房贷的总额(1年内)
l34 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month < 12)], 'money', 'sum', 'loan_award_house')
# l35贷款为房贷的平均额度(1年内)
l35 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month < 12)], 'money', 'mean', 'loan_award_house_avg')
# l36贷款为公积金房贷的笔数(1年内)
l36 = pt(df_loan[(df_loan.loan_type == '公积金贷款') & (df_loan.credit_month < 12)], 'money', 'count', 'loan_count_afl')
# l37贷款为公积金房贷的总额(1年内)
l37 = pt(df_loan[(df_loan.loan_type == '公积金贷款') & (df_loan.credit_month < 12)], 'money', 'sum', 'loan_award_afl')
# l38贷款为公积金房贷的平均额度(1年内)
l38 = pt(df_loan[(df_loan.loan_type == '公积金贷款') & (df_loan.credit_month < 12)], 'money', 'mean', 'loan_award_afl_avg')
# l39贷款为个人消费贷款的笔数(1年内)
l39 = pt(df_loan[(df_loan.account_category_main == '个人消费贷款') & (df_loan.credit_month < 12)], 'money', 'count', 'loan_count_consume')
# l40贷款为个人消费贷款的总额(1年内)
l40 = pt(df_loan[(df_loan.account_category_main == '个人消费贷款') & (df_loan.credit_month < 12)], 'money', 'sum', 'loan_award_consume')
# l41贷款为个人消费贷款的平均额度(1年内)
l41 = pt(df_loan[(df_loan.account_category_main == '个人消费贷款') & (df_loan.credit_month < 12)], 'money', 'mean', 'loan_award_consume_avg')
# l42贷款为经营性贷款的笔数(1年内)/li 备注是一年内的但是没有加时间限制及没加时间的话应该为2但是是0--AKHC20180108001
l42 = pt(df_loan[(df_loan.account_category_main == '个人经营贷款')& (df_loan.credit_month < 12)], 'money', 'count', 'loan_count_operate')
# l43贷款为经营性贷款的总额(1年内)
l43 = pt(df_loan[(df_loan.account_category_main.isin(['个人经营贷款', '个人经营性贷款', '个人消费'])) & (df_loan.credit_month < 12)], 'money', 'sum', 'loan_award_operate')
# l44贷款为经营性贷款的平均额度(1年内)
l44 = pt(df_loan[(df_loan.account_category_main.isin(['个人经营贷款', '个人经营性贷款', '个人消费'])) & (df_loan.credit_month < 12)], 'money', 'mean', 'loan_award_operate_avg')
# l45贷款为农户贷款的笔数(1年内)
l45 = pt(df_loan[(df_loan.account_category_main == '农户贷款') & (df_loan.credit_month < 12)], 'money', 'count', 'loan_count_peasant')
# l46贷款为农户贷款的总额(1年内)
l46 = pt(df_loan[(df_loan.account_category_main == '农户贷款') & (df_loan.credit_month < 12)], 'money', 'sum', 'loan_award_peasant')
# l47贷款为农户贷款的平均额度(1年内)
l47 = pt(df_loan[(df_loan.account_category_main == '农户贷款') & (df_loan.credit_month < 12)], 'money', 'mean', 'loan_award_peasant_avg')
# l48贷款为汽车贷款的笔数(1年内)
l48 = pt(df_loan[(df_loan.account_category_main == '个人汽车贷款') & (df_loan.credit_month < 12)], 'money', 'count', 'loan_count_car')
# l49贷款为汽车贷款的总额(1年内)
l49 = pt(df_loan[(df_loan.account_category_main == '个人汽车贷款') & (df_loan.credit_month < 12)], 'money', 'sum', 'loan_award_car')
# l50贷款为汽车贷款的平均额度(1年内)
l50 = pt(df_loan[(df_loan.account_category_main == '个人汽车贷款') & (df_loan.credit_month < 12)], 'money', 'mean', 'loan_award_car_avg')
# l51贷款五年内逾期总月数
l51 = pt(df_loan, 'years5_overdue', 'sum', 'loan_overdue_month_5y')
# l52贷款两年内逾期总月数（仅统计两年内发放的贷款）
l52 = pt(df_loan[df_loan.credit_month < 24], 'years5_overdue', 'sum', 'loan_overdue_month_2y')
# l53贷款一年内逾期总月数（仅统计一年内发放的贷款）
l53 = pt(df_loan[df_loan.credit_month < 12], 'years5_overdue', 'sum', 'loan_overdue_month_1y')
# l54贷款五年内90天以上逾期次数
l54 = pt(df_loan, 'days90_overdue', 'sum', 'loan_90overdue_5y')
# l55贷款两年内90天以上逾期次数（仅统计两年内发放的贷款）
l55 = pt(df_loan[df_loan.credit_month < 24], 'days90_overdue', 'sum', 'loan_90overdue_2y')
# l56贷款两年内90天以上逾期次数（仅统计一年内发放的贷款）
l56 = pt(df_loan[df_loan.credit_month < 12], 'days90_overdue', 'sum', 'loan_90overdue_1y')
# l57房贷五年内逾期总月数/li没有统计到对应的房贷,应该修改loan_type函数
l57 = pt(df_loan[df_loan.loan_type.isin(['商贷', '公积金贷款'])], 'years5_overdue', 'sum', 'loan_house_overdue_month_5y')
# l58房贷两年内逾期总月数（仅统计两年内发放的贷款）
l58 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month <= 24)], 'years5_overdue',  'sum', 'loan_house_overdue_month_2y')
# l59房贷两年内逾期总月数（仅统计两年内发放的贷款）
l59 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month <= 12)], 'years5_overdue',  'sum', 'loan_house_overdue_month_1y')
# l60房贷五年内90天以上逾期次数
l60 = pt(df_loan[df_loan.loan_type.isin(['商贷', '公积金贷款'])], 'days90_overdue', 'sum', 'loan_house_90overdue_5y')
# l61房贷两年内90天以上逾期次数（仅统计两年内发放的贷款）
l61 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month <= 24)], 'days90_overdue', 'sum', 'loan_house_90overdue_2y')
# l62房贷两年内90天以上逾期次数（仅统计两年内发放的贷款）
l62 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.credit_month <= 12)], 'days90_overdue', 'sum', 'loan_house_90overdue_1y')
# l63单张贷款最高逾期比例
l63 = pt(df_loan, 'overdue_per', 'max', 'loan_overdue_highest')
# l64房贷逾期账户数
l64 = pt(df_loan[(df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.years5_overdue > 0)], 'loan_type', 'count', 'loan_overdue_house')
# l65逾期比例>=10%贷款账户数
l65 = pt(df_loan[df_loan.overdue_per >= 10], 'loan_type', 'count', 'loan_overdue_ratio_10')
# l66逾期比例>=20%贷款账户数
l66 = pt(df_loan[df_loan.overdue_per >= 20], 'loan_type', 'count', 'loan_overdue_ratio_20')
# l67逾期比例>=30%贷款账户数
l67 = pt(df_loan[df_loan.overdue_per >= 30], 'loan_type', 'count', 'loan_overdue_ratio_30')
# l681年内发放的贷款逾期比例>=10%贷款账户数
l68 = pt(df_loan[(df_loan.credit_month < 12) & (df_loan.overdue_per >= 10)], 'loan_type', 'count', 'loan_overdue_10_extend_1y')
# l691年内发放的贷款逾期比例>=20%贷款账户数
l69 = pt(df_loan[(df_loan.credit_month < 12) & (df_loan.overdue_per >= 20)], 'loan_type', 'count', 'loan_overdue_20_extend_1y')
# l701年内发放的贷款逾期比例>=30%贷款账户数
l70 = pt(df_loan[(df_loan.credit_month < 12) & (df_loan.overdue_per >= 30)], 'loan_type', 'count', 'loan_overdue_30_extend_1y')
# l712年内发放的贷款逾期比例>=10%贷款账户数
l71 = pt(df_loan[(df_loan.credit_month < 24) & (df_loan.overdue_per >= 10)], 'loan_type', 'count', 'loan_overdue_10_extend_2y')
# l722年内发放的贷款逾期比例>=20%贷款账户数
l72 = pt(df_loan[(df_loan.credit_month < 24) & (df_loan.overdue_per >= 20)], 'loan_type', 'count', 'loan_overdue_20_extend_2y')
# l732年内发放的贷款逾期比例>=30%贷款账户数
l73 = pt(df_loan[(df_loan.credit_month < 24) & (df_loan.overdue_per >= 30)], 'loan_type', 'count', 'loan_overdue_30_extend_2y')
# l74贷款正常笔数(2年内)
l74 = pt(df_loan[(df_loan.loan_state == '正常') & (df_loan.credit_month < 24)], 'loan_type', 'count', 'loan_count_normal')
# l75贷款结清笔数(2年内)/li 字段后是否加2y
l75 = pt(df_loan[(df_loan.loan_state == '结清') & (df_loan.credit_month < 24)], 'loan_type', 'count', 'loan_count_settle')
# l76贷款逾期笔数(2年内)
l76 = pt(df_loan[(df_loan.loan_state == '逾期') & (df_loan.credit_month < 24)], 'loan_type', 'count', 'loan_count_overdue')
# l77贷款呆账笔数(2年内)
l77 = pt(df_loan[(df_loan.loan_state == '呆账') & (df_loan.credit_month < 24)], 'loan_type', 'count', 'loan_count_doubtful')
# l78贷款转出笔数(2年内)
l78 = pt(df_loan[(df_loan.loan_state == '转出') & (df_loan.credit_month < 24)], 'loan_type', 'count', 'loan_count_out')
# l79贷款正常笔数(1年内)
l79 = pt(df_loan[(df_loan.loan_state == '正常') & (df_loan.credit_month < 12)], 'loan_type', 'count', 'loan_count_normal_in_1y')
# l80贷款结清笔数(1年内)
l80 = pt(df_loan[(df_loan.loan_state == '结清') & (df_loan.credit_month < 12)], 'loan_type', 'count', 'loan_count_settle_in_1y')
# l81贷款逾期笔数(1年内)
l81 = pt(df_loan[(df_loan.loan_state == '逾期') & (df_loan.credit_month < 12)], 'loan_type', 'count', 'loan_count_overdue_in_1y')
# l82贷款呆账笔数(1年内)
l82 = pt(df_loan[(df_loan.loan_state == '呆账') & (df_loan.credit_month < 12)], 'loan_type', 'count', 'loan_count_doubtful_in_1y')
# l83贷款转出笔数(1年内)
l83 = pt(df_loan[(df_loan.loan_state == '转出') & (df_loan.credit_month < 12)], 'loan_type', 'count', 'loan_count_out_in_1y')
# l84房贷已还期数/li 月数计算不正确？
l84 = pt(df_loan[df_loan.loan_type.isin(['商贷', '公积金贷款'])], 'used_month', 'sum', 'loan_house_repaymonth')
# l85房贷当前每月应还款额
l85 = pt(df_loan[df_loan.loan_type.isin(['商贷', '公积金贷款'])], 'pmt', 'sum', 'loan_house_moneymonthly')
# l86其他贷款当前每月应还款额
l86 = pt(df_loan[(~df_loan.loan_type.isin(['商贷', '公积金贷款'])) & (df_loan.loan_state != '结清')], 'pmt', 'sum', 'loan_other_moneymonthly')
# l87贷款当前每月应还总额（估算）
l87 = pt(df_loan[df_loan.loan_state != '结清'], 'pmt', 'sum', 'loan_moneymonthly')
# l88贷款当前每月应还总额（不计抵押类贷款）
l88 = pt(df_loan[df_loan.loan_type.isin(['其他贷款', '农户贷款', '助学贷款'])], 'pmt', 'sum', 'loan_moneymonthly_notmortgage')
# l89贷款总额
l89 = pt(df_loan, 'money', 'sum', 'loan_award_total')
# l90贷款余额
l90 = pt(df_loan, 'figure', 'sum', 'loan_balance')
# l91贷款当前逾期账户数
l91 = pt(df_loan[df_loan.yuqi_money > 0], 'yuqi_money', 'count', 'loan_overdue_account')
# l92贷款当前逾期金额
l92 = pt(df_loan[df_loan.yuqi_money > 0], 'yuqi_money', 'sum', 'loan_award_overdue')
# l93房贷当前逾期金额
l93 = pt(df_loan[(df_loan.yuqi_money > 0) & (df_loan.loan_type.isin(['商贷', '公积金贷款']))], 'yuqi_money', 'sum', 'loan_overdue_money')
# l94贷款金额在1万以下的笔数
l94 = pt(df_loan[df_loan.money <= 10000], 'loan_type', 'count', 'loan_money_1')
# l95贷款金额在1万-2万之间的笔数
l95 = pt(df_loan[(df_loan.money > 10000) & (df_loan.money <= 20000)], 'loan_type', 'count', 'loan_money_1_2')
# l96贷款金额在2万-10万之间的笔数
l96 = pt(df_loan[(df_loan.money > 20000) & (df_loan.money <= 100000)], 'loan_type', 'count', 'loan_money_2_10')
# l97贷款金额在10万-20万之间的笔数
l97 = pt(df_loan[(df_loan.money > 100000) & (df_loan.money <= 200000)], 'loan_type', 'count', 'loan_money_10_20')
# l98贷款金额在20万-50万之间的笔数
l98 = pt(df_loan[(df_loan.money > 200000) & (df_loan.money <= 500000)], 'loan_type', 'count', 'loan_money_20_50')
# l99贷款金额在50万-100万之间的笔数
l99 = pt(df_loan[(df_loan.money > 500000) & (df_loan.money <= 1000000)], 'loan_type', 'count', 'loan_money_50_100')
# l100贷款金额在100万-200万之间的笔数
l100 = pt(df_loan[(df_loan.money > 1000000) & (df_loan.money <= 2000000)], 'loan_type', 'count', 'loan_money_100_200')
# l101贷款金额在200万以上的笔数
l101 = pt(df_loan[df_loan.money > 2000000], 'loan_type', 'count', 'loan_money_200')
# l102贷款金额在20万以上的笔数
l102 = pt(df_loan[df_loan.money > 200000], 'loan_type', 'count', 'loan_money_over_20')
# l103贷款金额在50万以上的笔数
l103 = pt(df_loan[df_loan.money > 500000], 'loan_type', 'count', 'loan_money_over_50')
# l104当前贷款金额在1万以下的笔数/li需要加贷款状态
l104 = pt(df_loan[(df_loan.money <= 10000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_1_now')
# l105当前贷款金额在1万-2万之间的笔数
l105 = pt(df_loan[(df_loan.money > 10000) & (df_loan.money <= 20000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_1_2_now')
# l106当前贷款金额在2万-10万之间的笔数
l106 = pt(df_loan[(df_loan.money > 20000) & (df_loan.money <= 100000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_2_10_now')
# l107当前贷款金额在10万-20万之间的笔数
l107 = pt(df_loan[(df_loan.money > 100000) & (df_loan.money <= 200000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_10_20_now')
# l108当前贷款金额在20万-50万之间的笔数
l108 = pt(df_loan[(df_loan.money > 200000) & (df_loan.money <= 500000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_20_50_now')
# l109当前贷款金额在50万-100万之间的笔数
l109 = pt(df_loan[(df_loan.money >= 500000) & (df_loan.money < 1000000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_50_100_now')
# l110当前贷款金额在100万-200万之间的笔数
l110 = pt(df_loan[(df_loan.money >= 1000000) & (df_loan.money < 2000000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_100_200_now')
# l111当前贷款金额在200万以上的笔数
l111 = pt(df_loan[(df_loan.money >= 2000000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_200_now')
# l112贷款金额在20万以上的笔数/li需要加贷款状态
l112 = pt(df_loan[(df_loan.money > 200000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_over_20')
# l113贷款金额在200万以上的笔数
l113 = pt(df_loan[(df_loan.money > 500000) & (df_loan.loan_state != '结清')], 'loan_type', 'count', 'loan_money_over_50')
# l114贷款发放机构为微众银行的笔数
l114 = pt(df_loan[df_loan.institution.str.findall(r'微众银行').str.len() > 0], 'institution', 'count', 'loan_count_weixin')
# l115贷款发放机构为浙江网商银行的笔数
l115 = pt(df_loan[df_loan.institution.str.findall(r'网商银行').str.len() > 0], 'institution', 'count', 'loan_count_mayi')
# l116微粒贷使用时长(按月计)/li少计算一个月,不满一月补全一月
l116 = pt(df_loan[df_loan.institution.str.findall(r'微众银行').str.len() > 0], 'used_month', 'max', 'loan_history_weixin')
# l117最近一笔微粒贷额度
l117 = pt(df_loan[(df_loan.institution.str.findall(r'微众银行').str.len() > 0)].sort_values(by=['selecttime', 'grant_date']), 'money', 'last', 'loan_award_weixin_last')
# l118借呗/网商贷使用时长(按月计)/li 少计算一个月，used_month计算错误
l118 = pt(df_loan[df_loan.institution.str.findall(r'网商银行|阿里巴巴').str.len() > 0], 'used_month', 'max', 'loan_history_mayi')
# l119最近一笔借呗/网商贷额度/li网商贷不能包括阿里巴巴，有一家重庆市阿里巴巴小额贷款有限公司
l119 = pt(df_loan[df_loan.institution.str.findall(r'网商银行|阿里巴巴').str.len() > 0].sort_values(by=['selecttime', 'grant_date']), 'money', 'last', 'loan_award_mayi_last')
# l120贷款信用时长（不包括助学贷款）
l120 = pt(df_loan[df_loan.loan_type != '助学贷款'], 'credit_month', 'max', 'loan_credit_history')

time1=datetime.datetime.now()
print(time1-time2)
df_credit['chaxun_date'] = df_credit.chaxun_date.astype('datetime64[ns]')
df_credit['selecttime'] = df_credit.selecttime.map(into_time)
df_credit.loc[df_credit.caozuoyuan != df_credit.caozuoyuan, 'caozuoyuan'] = '个人查询'
df_credit['credit_month'] = df_credit.apply(lambda x: interval_month(x.chaxun_date, x.selecttime), axis=1)
df_credit['credit_day']=df_credit.apply(lambda x: interval_day(x.chaxun_date, x.selecttime), axis=1)
# t1征信查询-1月内查询次数
t1 = pt(df_credit[df_credit.credit_month < 1], 'reason', 'count', 'credit_1m')
# t2征信查询-2月内查询次数
t2 = pt(df_credit[df_credit.credit_month < 2], 'reason', 'count', 'credit_2m')
# t3征信查询-3月内查询次数
t3 = pt(df_credit[df_credit.credit_month < 3], 'reason', 'count', 'credit_3m')
# t4征信查询-6月内查询次数
t4 = pt(df_credit[df_credit.credit_month < 6], 'reason', 'count', 'credit_6m')
# t5征信查询-12月内查询次数
t5 = pt(df_credit[df_credit.credit_month < 12], 'reason', 'count', 'credit_12m')
# t6征信查询-1月内机构查询次数
t6 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan != '个人查询')], 'reason', 'count', 'credit_org_1m')
# t7征信查询-2月内机构查询次数
t7 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan != '个人查询')], 'reason', 'count', 'credit_org_2m')
# t8征信查询-3月内机构查询次数
t8 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan != '个人查询')], 'reason', 'count', 'credit_org_3m')
# t9征信查询-6月内机构查询次数
t9 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan != '个人查询')], 'reason', 'count', 'credit_org_6m')
# t10征信查询-12月内机构查询次数
t10 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan != '个人查询')], 'reason', 'count', 'credit_org_12m')
# t11征信查询-1月内个人查询次数
t11 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan == '个人查询')], 'reason', 'count', 'credit_pers_1m')
# t12征信查询-2月内个人查询次数
t12 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan == '个人查询')], 'reason', 'count', 'credit_pers_2m')
# t13征信查询-3月内个人查询次数
t13 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan == '个人查询')], 'reason', 'count', 'credit_pers_3m')
# t14征信查询-6月内个人查询次数
t14 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan == '个人查询')], 'reason', 'count', 'credit_pers_6m')
# t15征信查询-12月内个人查询次数
t15 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan == '个人查询')], 'reason', 'count', 'credit_pers_12m')
# t16征信查询-1月内机构查询次数（不含贷后管理）
t16 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan != '个人查询') & (df_credit.reason != '贷后管理')], 'reason', 'count', 'credit_org_1m_notplm')
# t17征信查询-2月内机构查询次数（不含贷后管理）
t17 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan != '个人查询') & (df_credit.reason != '贷后管理')], 'reason', 'count', 'credit_org_2m_notplm')
# t18征信查询-3月内机构查询次数（不含贷后管理）
t18 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan != '个人查询') & (df_credit.reason != '贷后管理')], 'reason', 'count', 'credit_org_3m_notplm')
# t19征信查询-6月内机构查询次数（不含贷后管理）
t19 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan != '个人查询') & (df_credit.reason != '贷后管理')], 'reason', 'count', 'credit_org_6m_notplm')
# t20征信查询-12月内机构查询次数（不含贷后管理）
t20 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan != '个人查询') & (df_credit.reason != '贷后管理')], 'reason', 'count', 'credit_org_12m_notplm')
# t21征信查询-1月内信用卡审批次数
t21 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '信用卡审批')], 'reason', 'count', 'credit_card_1m')
# t22征信查询-1月内贷款审批次数
t22 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷款审批')], 'reason', 'count', 'credit_loan_1m')
# t23征信查询-1月内贷后管理次数
t23 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷后管理')], 'reason', 'count', 'credit_plm_1m')
# 征信查询-1月内资信审查次数
t24 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '资信审查')], 'reason', 'count', 'credit_qualified_1m')
# t25征信查询-1月内保前审查次数
t25 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '保前审查')], 'reason', 'count', 'credit_presafe_1m')
# t26征信查询-1月内保后管理次数
t26 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '保后管理')], 'reason', 'count', 'credit_pgmgmt_1m')
# t27征信查询-1月内准入资格审查次数
t27 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '准入资格审查')], 'reason', 'count', 'credit_admit_1m')
# t28征信查询-1月内担保资格审查次数
t28 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '担保资格审查')], 'reason', 'count', 'credit_guarantee_1m')
# t29征信查询-1月内贷款审批（银行）次数
t29 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex1).str.len() > 0)], 'reason', 'count', 'credit_loan_bank_1m')
# t30征信查询-1月内贷款审批（小贷公司）次数
t30 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_loan_mcc_1m')
# t31征信查询-1月内贷款审批（消费金融公司）次数
t31 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_loan_cfc_1m')
# t32征信查询-1月内贷款审批（融资担保）次数
t32 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex12).str.len() > 0)], 'reason', 'count', 'credit_loan_fing_1m')
# t33征信查询-1月内贷款审批（信托）次数
t33 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_loan_trust_1m')
# t34征信查询-3月内贷款审批（银行）次数
t34 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex1).str.len() > 0)], 'reason', 'count', 'credit_loan_bank_3m')
# t35征信查询-3月内贷款审批（小贷公司）次数
t35 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_loan_mcc_3m')
# t36征信查询-3月内贷款审批（消费金融公司）次数
#?为什么是card表
t36 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_loan_cfc_3m')
# t37征信查询-3月内贷款审批（融资担保）次数
t37 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex12).str.len() > 0)], 'reason', 'count', 'credit_loan_fing_3m')

# t38征信查询-3月内贷款审批（信托）次数
t38 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批') & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_loan_trust_3m')


#返回在指定指定时间内收到的贷款数目
def loan_reject(x):
    x['loan_reject_num']=df_loan[(df_loan['selecttime']==x.selecttime)&(df_loan['institution']==x.caozuoyuan)&((df_loan['grant_date'] >x.chaxun_date+2*Day()) & (df_loan['grant_date'] <= x.chaxun_date+30*Day()))].shape[0]
    return x
#时间区间计算十天到3月的数据
df_credit_reject=df_credit[(df_credit.credit_day>=10) &(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批')].apply(lambda x:loan_reject(x),axis=1)
df_credit_reject=df_credit_reject[df_credit_reject['loan_reject_num']==0]
# tmp-45-3月内贷款审批被拒次数
t44 = pt(df_credit_reject, 'reason', 'count', 'credit_reject_3m')
# t393月内贷款审批（银行）被拒次数
t39 = pt(df_credit_reject[df_credit_reject.caozuoyuan.str.findall(regex1).str.len() > 0], 'reason', 'count', 'credit_bank_reject_3m')
# t403月内贷款审批（小贷公司）被拒次数
t40 = pt(df_credit_reject[df_credit_reject.caozuoyuan.str.findall(regex7).str.len() > 0], 'reason', 'count', 'credit_mcc_reject_3m')
# t413月内贷款审批（消费金融公司）被拒次数
t41 = pt(df_credit_reject[df_credit_reject.caozuoyuan.str.findall(regex8).str.len() > 0], 'reason', 'count', 'credit_cfc_reject_3m')
# t423月内贷款审批（融资担保）被拒次数
t42 = pt(df_credit_reject[df_credit_reject.caozuoyuan.str.findall(regex12).str.len() > 0], 'reason', 'count', 'credit_fing_reject_3m')
# t433月内贷款审批（信托）被拒次数
t43 = pt(df_credit_reject[df_credit_reject.caozuoyuan.str.findall(regex9).str.len() > 0], 'reason', 'count', 'credit_trust_reject_3m')
# t443月内贷款审批（其他）被拒次数

# t45征信查询-2月内信用卡审批次数
t45 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '信用卡审批')], 'reason', 'count', 'credit_card_2m')
# t46征信查询-2月内贷款审批次数
t46 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '贷款审批')], 'reason', 'count', 'credit_loan_2m')
# t47征信查询-2月内贷后管理次数
t47 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '贷后管理')], 'reason', 'count', 'credit_plm_2m')
# t48征信查询-2月内资信审查次数
t48 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '资信审查')], 'reason', 'count', 'credit_approve_2m')
# t49征信查询-2月内保前审查次数
t49 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '保前审查')], 'reason', 'count', 'credit_presafe_2m')
# t50征信查询-2月内保后管理次数
t50 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '保后管理')], 'reason', 'count', 'credit_pgmgmt_2m')
# t51征信查询-2月内准入资格审查次数
t51 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '准入资格审查')], 'reason', 'count', 'credit_admit_2m')
# t52征信查询-2月内担保资格审查次数
t52 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '担保资格审查')], 'reason', 'count', 'credit_guarantee_2m')
# t53征信查询-3月内信用卡审批次数
t53 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '信用卡审批')], 'reason', 'count', 'credit_card_3m')
# t54征信查询-3月内贷款审批次数
t54 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷款审批')], 'reason', 'count', 'credit_loan_3m')
# t55征信查询-3月内贷后管理次数
t55 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '贷后管理')], 'reason', 'count', 'credit_plm_3m')
# t56征信查询-3月内资信审查次数
t56 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '资信审查')], 'reason', 'count', 'credit_approve_3m')
# t57征信查询-3月内保前审查次数
t57 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '保前审查')], 'reason', 'count', 'credit_presafe_3m')
# t58征信查询-3月内保后管理次数
t58 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '保后管理')], 'reason', 'count', 'credit_pgmgmt_3m')
# t59征信查询-3月内准入资格审查次数
t59 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '准入资格审查')], 'reason', 'count', 'credit_admit_3m')
# t60征信查询-3月内担保资格审查次数
t60 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '担保资格审查')], 'reason', 'count', 'credit_guarantee_3m')
# t61征信查询-6月内信用卡审批次数
t61 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '信用卡审批')], 'reason', 'count', 'credit_card_6m')
# t62征信查询-6月内贷款审批次数
t62 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '贷款审批')], 'reason', 'count', 'credit_loan_6m')
# t63征信查询-6月内贷后管理次数
t63 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '贷后管理')], 'reason', 'count', 'credit_plm_6m')
# t64征信查询-6月内资信审查次数
t64 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '资信审查')], 'reason', 'count', 'credit_approve_6m')
# t65征信查询-6月内保前审查次数
t65 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '保前审查')], 'reason', 'count', 'credit_presafe_6m')
# t66征信查询-6月内保后管理次数
t66 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '保后管理')], 'reason', 'count', 'credit_pgmgmt_6m')
# t67征信查询-6月内准入资格审查次数
t67 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '准入资格审查')], 'reason', 'count', 'credit_admit_6m')
# t68征信查询-6月内担保资格审查次数
t68 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '担保资格审查')], 'reason', 'count', 'credit_guarantee_6m')
# t69征信查询-12月内信用卡审批次数
t69 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '信用卡审批')], 'reason', 'count', 'credit_card_12m')
# t70征信查询-12月内贷款审批次数
t70 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '贷款审批')], 'reason', 'count', 'credit_loan_12m')
# t71征信查询-12月内贷后管理次数
t71 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '贷后管理')], 'reason', 'count', 'credit_plm_12m')
# t72征信查询-12月内资信审查次数
t72 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '资信审查')], 'reason', 'count', 'credit_approve_12m')
# t73征信查询-12月内保前审查次数
t73 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '保前审查')], 'reason', 'count', 'credit_presafe_12m')
# t74征信查询-12月内保后管理次数
t74 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '保后管理')], 'reason', 'count', 'credit_pgmgmt_12m')
# t75征信查询-12月内准入资格审查次数
t75 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '准入资格审查')], 'reason', 'count', 'credit_admit_12m')
# t76征信查询-12月内担保资格审查次数
t76 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '担保资格审查')], 'reason', 'count', 'credit_guarantee_12m')
# t77征信查询-1月内-查询机构为村镇银行的次数
t77 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex4).str.len() > 0)], 'reason', 'count', 'credit_bank_village_1m')
# t78征信查询-1月内-查询机构为农村信用社或农村商业银行的次数
t78 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex5).str.len() > 0)], 'reason', 'count', 'credit_bank_rcu_commerce_1m')
# t79征信查询-1月内-查询机构为小额贷款公司的次数
t79 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_bank_mcc_1m')
# t80征信查询-1月内-查询机构为消费金融公司的次数
t80 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_bank_cfc_1m')
# t81征信查询-1月内-查询机构为信托公司的次数
t81 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_bank_trust_1m')
# t82征信查询-1月内-查询机构为保险公司的次数
t82 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex13).str.len() > 0)], 'reason', 'count', 'credit_bank_insurer_1m')
# t83征信查询-1月内-查询机构为汽车金融公司的次数
t83 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex10).str.len() > 0)], 'reason', 'count', 'credit_bank_afc_1m')
# t84征信查询-1月内-查询机构为重点监测机构的次数
t84 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.caozuoyuan.str.findall(regex11).str.len() > 0)], 'reason', 'count', 'credit_bank_check_1m')
# t85征信查询-2月内-查询机构为农村信用社或商业银行的次数
t85 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex5).str.len() > 0)], 'reason', 'count', 'credit_bank_rcu_commerce_2m')
# t86征信查询-2月内-查询机构为小额贷款公司的次数
t86 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_bank_mcc_2m')
# t87征信查询-2月内-查询机构为消费金融公司的次数
t87 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_bank_cfc_2m')
# t88征信查询-2月内-查询机构为信托公司的次数
t88 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_bank_trust_2m')
# t89征信查询-2月内-查询机构为保险公司的次数
t89 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex13).str.len() > 0)], 'reason', 'count', 'credit_bank_insurer_2m')
# t90征信查询-2月内-查询机构为汽车金融公司的次数
t90 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex10).str.len() > 0)], 'reason', 'count', 'credit_bank_afc_2m')
# t91征信查询-2月内-查询机构为重点监测机构的次数
t91 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.caozuoyuan.str.findall(regex11).str.len() > 0)], 'reason', 'count', 'credit_bank_check_2m')
# t92征信查询-3月内-查询机构为村镇银行的次数
t92 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex4).str.len() > 0)], 'reason', 'count', 'credit_bank_village_3m')
# t93征信查询-3月内-查询机构为农村信用社或商业银行的次数
t93 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex5).str.len() > 0)], 'reason', 'count', 'credit_bank_rcu_commerce_3m')
# t94征信查询-3月内-查询机构为小额贷款公司的次数
t94 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_bank_mcc_3m')
# t95征信查询-3月内-查询机构为消费金融公司的次数
t95 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_bank_cfc_3m')
# t96征信查询-3月内-查询机构为信托公司的次数
t96 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_bank_trust_3m')
# t97征信查询-3月内-查询机构为保险公司的次数
t97 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex13).str.len() > 0)], 'reason', 'count', 'credit_bank_insurer_3m')
# t98征信查询-3月内-查询机构为汽车金融公司的次数
t98 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex10).str.len() > 0)], 'reason', 'count', 'credit_bank_afc_3m')
# t99征信查询-3月内-查询机构为重点监测机构的次数
t99 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.caozuoyuan.str.findall(regex11).str.len() > 0)], 'reason', 'count', 'credit_bank_check_3m')
# t100征信查询-6月内-查询机构为村镇银行的次数
t100 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex4).str.len() > 0)], 'reason', 'count', 'credit_bank_village_6m')
# t101征信查询-6月内-查询机构为农村信用社或商业银行的次数
t101 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex5).str.len() > 0)], 'reason', 'count', 'credit_bank_rcu_commerce_6m')
# t102征信查询-6月内-查询机构为小额贷款公司的次数
t102 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_bank_mcc_6m')
# t103征信查询-6月内-查询机构为消费金融公司的次数
t103 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_bank_cfc_6m')
# t104征信查询-6月内-查询机构为信托公司的次数
t104 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_bank_trust_6m')
# t105征信查询-6月内-查询机构为保险公司的次数
t105 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex13).str.len() > 0)], 'reason', 'count', 'credit_bank_insurer_6m')
# t106征信查询-6月内-查询机构为汽车金融公司的次数
t106 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex10).str.len() > 0)], 'reason', 'count', 'credit_bank_afc_6m')
# t107征信查询-6月内-查询机构为重点监测机构的次数
t107 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.caozuoyuan.str.findall(regex11).str.len() > 0)], 'reason', 'count', 'credit_bank_check_6m')
# t108征信查询-12月内-查询机构为村镇银行的次数
t108 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex4).str.len() > 0)], 'reason', 'count', 'credit_bank_village_12m')
# t109征信查询-12月内-查询机构为农村信用社或商业银行的次数
t109 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex5).str.len() > 0)], 'reason', 'count', 'credit_bank_rcu_commerce_12m')
# t110征信查询-12月内-查询机构为小额贷款公司的次数
t110 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex7).str.len() > 0)], 'reason', 'count', 'credit_bank_mcc_12m')
# t111征信查询-12月内-查询机构为消费金融公司的次数
t111 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex8).str.len() > 0)], 'reason', 'count', 'credit_bank_cfc_12m')
# t112征信查询-12月内-查询机构为信托公司的次数
t112 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex9).str.len() > 0)], 'reason', 'count', 'credit_bank_trust_12m')
# t113征信查询-12月内-查询机构为保险公司的次数
t113 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex13).str.len() > 0)], 'reason', 'count', 'credit_bank_insurer_12m')
# t114征信查询-12月内-查询机构为汽车金融公司的次数
t114 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex10).str.len() > 0)], 'reason', 'count', 'credit_bank_afc_12m')
# t115征信查询-12月内-查询机构为重点监测机构的次数
t115 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.caozuoyuan.str.findall(regex11).str.len() > 0)], 'reason', 'count', 'credit_bank_check_12m')
# t116征信查询-1月内-个人临柜查询次数 /li 原因未明，服务器表的原因？
t116 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason == '个人临柜查询')], 'reason', 'count', 'credit_self_1m')
# t117征信查询-1月内-个人互联网查询次数
t117 = pt(df_credit[(df_credit.credit_month < 1) & (df_credit.reason.str.findall(re.compile(r'互联网')).str.len() > 0)], 'reason', 'count', 'credit_internet_1m')
# t118征信查询-2月内-个人临柜查询次数
t118 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason == '个人临柜查询')], 'reason', 'count', 'credit_self_2m')
# t119征信查询-2月内-个人互联网查询次数
t119 = pt(df_credit[(df_credit.credit_month < 2) & (df_credit.reason.str.findall(re.compile(r'互联网')).str.len() > 0)], 'reason', 'count', 'credit_internet_2m')
# t120征信查询-3月内-个人临柜查询次数
t120 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason == '个人临柜查询')], 'reason', 'count', 'credit_self_3m')
# 征信查询-3月内-个人互联网查询次数
t121 = pt(df_credit[(df_credit.credit_month < 3) & (df_credit.reason.str.findall(re.compile(r'互联网')).str.len() > 0)], 'reason', 'count', 'credit_internet_3m')
# t122征信查询-6月内-个人临柜查询次数
t122 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason == '个人临柜查询')], 'reason', 'count', 'credit_self_6m')
# t123征信查询-6月内-个人互联网查询次数
t123 = pt(df_credit[(df_credit.credit_month < 6) & (df_credit.reason.str.findall(re.compile(r'互联网')).str.len() > 0)], 'reason', 'count', 'credit_internet_6m')
# t124征信查询-12月内-个人临柜查询次数
t124 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason == '个人临柜查询')], 'reason', 'count', 'credit_self_12m')
# t125征信查询-12月内-个人互联网查询次数
t125 = pt(df_credit[(df_credit.credit_month < 12) & (df_credit.reason.str.findall(re.compile(r'互联网')).str.len() > 0)], 'reason', 'count', 'credit_internet_12m')

time2=datetime.datetime.now()
print(time2-time1)
var_list1=[eval("c{}".format(i)) for i in range(1,47)]
var_list2=[eval("l{}".format(i)) for i in range(1,121)]
var_list3=[eval("t{}".format(i)) for i in range(1,126)]


result_var =var_list1+var_list2+var_list3

final_result=pd.concat(result_var,axis=1)
final_result['uuid']=final_result.index
final_result.replace([np.inf, -np.inf], 0,inplace=True)
print(final_result.shape)
#t126
# final_result['credit_other_reject_3m']=final_result['credit_reject_3m']-final_result['credit_bank_reject_3m'].fillna(0)-final_result['credit_mcc_reject_3m'].fillna(0)-final_result['credit_cfc_reject_3m'].fillna(0)-final_result['credit_fing_reject_3m'].fillna(0)-final_result['credit_trust_reject_3m'].fillna(0)
from data_files import sqlcol
try:
    final_result.to_sql('credit_features', con=my_conn,index=False,if_exists='replace',dtype=sqlcol(final_result))
    print('insert db success')
except:
    final_result.to_excel(r'C:\Users\Administrator\Desktop\credit_data.xlsx')
