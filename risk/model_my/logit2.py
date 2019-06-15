import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from collections import Counter
from sklearn import metrics
from sklearn import model_selection as ms


from sklearn import cross_validation as cv


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
    print(model, "---------start----------")
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






df = pd.read_excel(r'E:\hoomsun_data\analysis\models\贡献值结果-2018-07-18 13.xlsx', sheet_name='woe')
print(df.shape)
df = df.fillna(0)
print(df.shape)
df = df[df.card_account != 0.3079]
df_list = pd.read_excel(r'E:\hoomsun_data\analysis\models\贡献值结果-2018-07-18 13.xlsx', sheet_name='IV汇总')
list_var = list(df_list[df_list.IV值>=0.04]['英文'])
df['user_mark'] = df['user_mark'].map(lambda x: 0 if x==1 else 1)

# df_x = df[df_list]
# df_x = df_x.dropna()
# X = df_x
# Y = df['user_mark']

X_train = df[df.train_test==1][list_var]
X_test = df[df.train_test==0][list_var]
y_train = df[df.train_test==1]['user_mark']
y_test = df[df.train_test==0]['user_mark']


def run_kfold(model, X_train, X_test, y_train, y_test):
    kf = ms.KFold(n_splits=3)
    for train_index, test_index in kf.split(X_train):
        print('train_index: %s, test_index: %s' % (train_index, test_index))
        X_train = X_train[train_index]
        y_train = y_train[train_index]
        X_test = X_test[test_index]
        y_test = y_test[test_index]
        model_report(model)
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)


# model_lr = LogisticRegression(verbose=1)

# 随机森林


rf_param = {'n_estimators': [100, 200, 500],
            'max_features': ['log2', 'sqrt', 'auto'],
            'criterion': ['entropy', 'gini'],
            'max_depth': [2, 3, 5, 10],
            'min_samples_split': [2, 3, 5, 10, 20],
            'min_samples_leaf': [1, 5, 8, 15]
            }
model_rf = RandomForestClassifier(oob_score=True, random_state=5, n_jobs=-1)
# acc_score = metrics.make_scorer(metrics.accuracy_score(y_true=y_test, y_pred=model_rf.predict(X_test)))
# grid_obj = ms.GridSearchCV(model_rf, rf_param, acc_score)
# grid_obj = grid_obj.fit(X_train, y_train)
#
# model_rf = grid_obj.best_estimator_
# model_rf.fit(X_train, y_train)
# model_report(model_rf)

run_kfold(model_rf, X_train, X_test, y_train, y_test)



# for i in rf_param['n_estimators']:
#     for j in rf_param['max_features']:
#         model_rf = RandomForestClassifier(oob_score=True, random_state=5, n_jobs=-1, n_estimators=i, max_features=j)
#         f1_0 = set_param(model_rf)
#         print(i, j, f1_0)


# model_report(model_lr)
# logit_coef(model_lr, list_var)
# model_rf = RandomForestClassifier(oob_score=True, random_state=5, n_estimators=500, max_features=80)
# model_report(model_rf)
# importance_out(model_rf, list_var)
