import pandas as pd
import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
import matplotlib.pylab as plt
from sklearn.externals import joblib

df = pd.read_excel(r'E:\hoomsun_data\analysis\models\贡献值结果-2018-07-13 14.xlsx', sheet_name='woe')
df = df.fillna(0)

var_list = pd.read_excel(r'E:\hoomsun_data\analysis\models\字段列表.xlsx')
feature_list = list(var_list['字段名称'][var_list.融易贷==1])

X_train = df[feature_list][df.train_test == 1]
X_test = df[feature_list][df.train_test == 0]

y_train = df['user_mark'][df.train_test == 1]
y_test = df['user_mark'][df.train_test == 0]

# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)


def Random_forest(n_estimators, max_features):
    print("----", n_estimators, max_features, "-----")
    model = RandomForestClassifier(oob_score=True, random_state=5, n_estimators=n_estimators, max_features=max_features)
    model.fit(X_train, y_train)
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print("Train Score: ", train_score)
    print("Test Score: ", test_score)

    y_true = np.array(y_test)
    y_pred = model.predict(X_test)
    print("Test Precision 0: ", metrics.precision_score(y_true, y_pred, pos_label=0))
    print("Test recall 0: ", metrics.recall_score(y_true, y_pred, pos_label=0))
    print("Test f1 0: ", metrics.recall_score(y_true, y_pred, pos_label=0))

    print("Test Precision 1: ", metrics.precision_score(y_true, y_pred, pos_label=1))
    print("Test recall 1: ", metrics.recall_score(y_true, y_pred, pos_label=1))
    print("Test f1 1: ", metrics.recall_score(y_true, y_pred, pos_label=1))

    pres = model.predict(X_test)   # 预测分值
    pres2 = model.predict_proba(X_test)  # 预测分类概率

    print('预测结果: ', Counter(pres))
    print('实际结果:', Counter(list(np.array(y_test))))

    # 输出importance
    importances = model.feature_importances_
    indices = np.argsort(-importances)
    cols = [feature_list[x] for x in indices]
    out = dict(zip(cols, sorted(importances, reverse=True)))
    print(out)

## 逻辑回归
logit = sm.Logit(y_train, X_train)
result = logit.fit()

print(result.summary2())

# print(X_test.shape)
# ss = logit.predict(X_test)
# print(ss)



# print(model.oob_score_)
# y_predict = model.predict_proba(X_train)[:, 1]
# print(y_predict)
# print(metrics.roc_auc_score(y_train, y_predict))

