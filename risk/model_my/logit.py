import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df_list = pd.read_excel(r'E:\hoomsun_data\analysis\models\字段列表.xlsx', sheet_name='feature')
df_list = list(df_list['feature'][df_list.是否使用==1])
print(df_list)


df_train = pd.read_excel(r'E:\hoomsun_data\analysis\models\贡献值结果-2018-06-28.xlsx', sheet_name='woe')
# df_test = pd.read_excel(r'E:\hoomsun_data\analysis\models\data_woe_test6.30.xlsx')


df = pd.read_excel(r'E:\hoomsun_data\analysis\models\贡献值结果-2018-06-28.xlsx', sheet_name='woe')
X = df[df_list]
Y = df['user_mark']
X_train, X_test, y_train, y_test = train_test_split(X, Y, )


df_train_x = df_train[df_list]
df_train_x = df_train_x.dropna(axis=0)
print(df_train_x.columns)

# df_test_x = df_test[df_list]
#
# df_test_x = df_test_x.dropna(axis=0)
#
# X_train = df_train_x[1:13150]
# y_train = df_train['user_mark'][1:13150]
#
# X_test = df_test_x[1:5000]
# y_test = df_test['user_mark'][1:5000]

model = LogisticRegression()
model.fit(X_train, y_train)
gg = model.score(X_test, y_test)
print(gg)

predict = model.predict(X_test)
probe = model.predict_proba(X_test)
print(predict, probe)
