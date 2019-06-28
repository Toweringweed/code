#%%
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
from sklearn import metrics
from sklearn import model_selection as ms
from sklearn.model_selection import train_test_split


def set_param(model):
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    y_pred = model.predict(X_test)
    f1_0 = metrics.f1_score(y_true=y_test, y_pred=y_pred, pos_label=0)
    f1_1 = metrics.f1_score(y_true=y_test, y_pred=y_pred, pos_label=1)
    recall_0 = metrics.recall_score(y_true=y_test, y_pred=model.predict(X_test), pos_label=0)
    recall_1 = metrics.recall_score(y_true=y_test, y_pred=model.predict(X_test), pos_label=1)
    return train_score, test_score, f1_1, recall_1, f1_0, recall_0


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

def logit_coef(model, feature_list):
    coef = model.coef_
    coef = coef[0]
    b = model.intercept_
    indices = np.argsort(-coef)
    indices = indices.tolist()
    print(indices)
    cols = [feature_list[x] for x in indices]
    out = dict(zip(cols, sorted(coef, reverse=True)))
    print(out)
    
#%%
df = pd.read_excel(r'd:/data/model/贡献值结果-2019-06-16 18.xlsx', sheetname="woe")
df = df.fillna(0)
df.head()
df_list = pd.read_excel(r'd:/data/model/贡献值结果-2019-06-16 18.xlsx', sheetname='IV汇总')
print(df_list)
list_var = list(df_list['英文'])
list_var2 = list(df_list[df_list.IV值>=0.03]['英文'])

X_train = df[df.train_test==1][list_var]
X_test = df[df.train_test==0][list_var]
y_train = df[df.train_test==1]['user_mark']
y_test = df[df.train_test==0]['user_mark']


#%% Lasso
from sklearn.linear_model import Lasso

lasso_value_matrix = []
y_train2= y_train.copy()
y_train2[y_train2==0] = -1 
for i in range(0, 300):
    alpha = np.random.uniform(0, 0.2)
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train, y_train2)
    lasso_value = list(lasso.coef_)
    lasso_value_matrix.append(lasso_value)
#     out = dict(zip(list_var, lasso_value))
lasso_df = pd.DataFrame(lasso_value_matrix, columns=list_var)
lasso_dfx = lasso_df.applymap(lambda x: 1 if np.abs(x)>0 else 0)
lasso_sum = lasso_dfx.apply(lambda x: x.sum())
print(lasso_sum)
lasso_result = pd.DataFrame(lasso_sum, columns=['value'])
print(lasso_result)

lasso_result.to_csv( r"d:/data/model/lasso_feature.csv")


#%%
# 随机森林

list_var = pd.read_csv( r"d:/data/model/lasso_feature.csv")

list_var = list(list_var[list_var.value>1]['feature'])
print(list_var)


#%%
df = pd.read_excel(r'd:/data/model/贡献值结果-2019-06-16 18.xlsx', sheetname="woe")
df = df.fillna(0)
X_train = df[df.train_test==1][list_var]
X_test = df[df.train_test==0][list_var]
y_train = df[df.train_test==1]['user_mark']
y_test = df[df.train_test==0]['user_mark']

rf_param = {'n_estimators': [50, 200, 500],
#            
            'max_features': ['log2', 'sqrt', 'auto'],
            'criterion': ['entropy', 'gini'],
            'max_depth': [3, 5, 10],
            'min_samples_split': [2, 3, 5, 10, 20],
            'min_samples_leaf': [1, 5, 8, 15]
            }
model_rf = RandomForestClassifier(oob_score=True, random_state=5, n_jobs=-1)
grid_obj = ms.GridSearchCV(model_rf, rf_param, scoring="roc_auc", cv=5)
grid_obj = grid_obj.fit(X_train, y_train)
print(grid_obj.cv_results_)
print(grid_obj.best_params_)
print(grid_obj.best_score_)

model_rf = grid_obj.best_estimator_
model_rf.fit(X_train, y_train)
model_report(model_rf)    




#%%
