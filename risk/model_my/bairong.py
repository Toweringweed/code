#%%
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from collections import Counter
from sklearn.linear_model import Lasso
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def model_report(model):
    print(model)
    print( "---------start----------")
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print("Train Score: ", train_score)
    print("Test Score: ", test_score)

    y_true = np.array(y_test)
    y_pred = model.predict(X_test)
    print(y_true, y_pred)

    f1_0 = metrics.f1_score(y_true=y_test, y_pred=y_pred, pos_label=0)
    print("Test Precision 0: ", metrics.precision_score(y_true, y_pred, pos_label=0))
    print("Test Recall 0: ", metrics.recall_score(y_true=y_test, y_pred=model.predict(X_test), pos_label=0))
    print("Test f1 0: ", f1_0)

    print("Test Precision 1: ", metrics.precision_score(y_true, y_pred, pos_label=1))
    print("Test Recall 1: ", metrics.recall_score(y_true=y_test, y_pred=model.predict(X_test), pos_label=1))
    print("Test f1 1: ", metrics.f1_score(y_true=y_test, y_pred=y_pred, pos_label=1))

    predict = model.predict(X_test)
    probe = model.predict_proba(X_test)
    print("预测结果：", Counter(model.predict(X_test)))
    print("实际结果: ", Counter(list(np.array(y_test))))
    print("---------------end---------------")


def importance_out(model, feature_list):
    importances = model.feature_importances_
    indices = np.argsort(-importances)
    cols = [feature_list[x] for x in indices]
    out = dict(zip(cols, sorted(importances, reverse=True)))
    print(out)

#%% 

df = pd.read_csv(r'd:/data/model/bairong_data2.csv', encoding='gbk')
df.info()
df.columns

#%%
df.loc[:, 'sl_id_bank_bad':'value.1'] = df.loc[:, 'sl_id_bank_bad':'value.1'].applymap(lambda x: -99 if x=="null" else x)
df['user_mark'] = df['data_hbyh2'].map(lambda x: 1 if x=='good' else -1)
df.head()
df.to_csv(r'd:/data/model/bairong_data2_c.csv')


#%% Lasso

# df = pd.read_csv(r'd:/data/model/bairong_data_en_min_c.csv')

lasso_value_matrix = []
X_train = df.loc[:, 'sl_id_bank_bad':'value.1']
y_train= df['user_mark']

for i in range(0, 1000):
    alpha = np.random.uniform(0, 0.2)
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train, y_train)
    lasso_value = list(lasso.coef_)
    lasso_value_matrix.append(lasso_value)
#     out = dict(zip(list_var, lasso_value))
lasso_df = pd.DataFrame(lasso_value_matrix, columns=list(X_train.columns))
lasso_dfx = lasso_df.applymap(lambda x: 1 if np.abs(x)>0 else 0)
lasso_sum = lasso_dfx.apply(lambda x: x.sum())
lasso_result = pd.DataFrame(lasso_sum, columns=['value'])
print(lasso_result)

lasso_result.to_csv( r"d:/data/model/bairong_lasso3.csv")


#%% logit_stat

import statsmodels.api as sm 

df_var = pd.read_csv( r"d:/data/model/bairong_lasso3.csv")
var_list = list(df_var[df_var.ratio>0.2]['feature'])
X= df.loc[:, var_list]
y = df['user_mark'].map(lambda x: 0 if x==-1 else x)

logit = sm.Logit(y, X)
result = logit.fit()
print(result.summary2())

#%% LR
df = pd.read_csv(r'd:/data/model/bairong_data2_c.csv', encoding='gbk')
df_var = pd.read_csv( r"d:/data/model/bairong_lasso3.csv")
var_list = list(df_var[df_var.value==1000]['feature'])
X = df.loc[:, 'sl_id_bank_bad':'value.1']
y = df['user_mark'].map(lambda x: 0 if x==-1 else x)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
model_lr = LogisticRegression()
model_report(model_lr)
model_rf = RandomForestClassifier()
model_report(model_rf)


#%% RF importance
importance_out(model_rf, var_list)





#%%
df.info()

#%%
