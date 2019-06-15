import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.externals import joblib


# feature_list = pd.read_excel(r'E:\hoomsun_data\analysis\models\字段列表.xlsx', sheet_name='feature')
# feature_list = list(feature_list['feature'][feature_list.是否使用==1])
# df = pd.read_excel(r'E:\hoomsun_data\analysis\models\data_6282.xlsx')
feature_list = [
    '身份证关联风险分',
    '手机号关联风险分',
    '最大关联风险分',

    '反欺诈分2.0',
    '大额现金贷分',
    '银行分',
    '反欺诈评分-线下消费分期',
    '反欺诈评分-信用卡（类信用卡）',
    '信用风险识别-汽车金融',
    '汽车金融-融资租赁信用风险识别结果',
    '信用风险识别-线下现金分期',
    '信用风险识别-线上现金分期',
    '线下消费客群评分',
    '信用风险识别-线上消费分期',
    '信用卡代偿客群评分',
    '评分-类信用卡'
]
df = pd.read_excel(r'E:\工作\31.智能风控\第三方+同盾复杂网络.xlsx')

df['user_mark'] = df['逾期期次'].map(lambda x: 0 if x==0 else 1)
print(df['user_mark'])

df = df.dropna()
df_x = df[feature_list]
df_y = df['user_mark']

print(df.head())
# print(df_x.describe())

# print(pd.crosstab(df['product'], df['user_mark'], rownames=['product']))

# df['product'].hist()
# plt.show()

logit = sm.Logit(df_y, df_x)
result = logit.fit()
print(result.summary2())

joblib.dump(logit, "logit_model.m")

ut = joblib.load("logit_model.m")
r1 = ut.fit()
print(r1.summary2())

