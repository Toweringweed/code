from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import classification_report
import json
import pandas as pd
from collections import Counter
from sklearn.externals import joblib
from sklearn.svm import SVC
import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from model.creat_model.assist_funcs.roc_cuttable import get_table
# 也可以将score_test保存到本地，以及添加保存模型
# 根据get_rflog_param结果调整基本参数
# 随机森林方法


def rf_model(X, Y, x_test, y_test, params, save_model=False):
    # rf = str(docs_path['param_json']).format(product, 'rf')
    # f = open(rf, 'r')
    # params = json.load(f)
    clfs = {'random_forest': RandomForestClassifier(**params)}
    # 构建分类器，训练样本，预测得分
    clf = clfs['random_forest']
    clf.fit(X, Y)
    clf_score = (clf.score(X, Y), clf.score(x_test, y_test))
    # 输出概率
    y_pre = clf.predict_proba(x_test)[:, 1]
    score_test = classification_report(y_test, clf.predict(x_test))
    table, result = get_table(y_pre, y_test, 'rf')
    return table, result, clf_score

# 逻辑回归方法


def log_model(X, Y, x_test, y_test,params, save_model=False):
    # log = str(docs_path['param_json']).format(product, 'log')
    # f = open(log, 'r')
    # params = json.load(f)
    clf = LogisticRegression(**params)
    clf.fit(X, Y)
    clf_score = (clf.score(X, Y), clf.score(x_test, y_test))
    y_pre = clf.predict_proba(x_test)[:, 1]
    score_test = classification_report(y_test, clf.predict(x_test))
    table, result = get_table(y_pre, y_test, 'log')
    return table, result, clf_score

# xgboost 方法////


def xgb_model(X, Y, x_test, y_test, params, save_model=False):
    clf = xgb.XGBClassifier()
    # xgb_path = str(docs_path['param_json']).format(product, 'xgb')
    # f = open(xgb_path, 'r')
    # params = json.load(f)
    # 读取优化之后的参数
    clf.set_params(**params)
    clf.fit(X, Y, eval_metric='auc')
    score_test = classification_report(Y, clf.predict(X))
    y_pre = clf.predict_proba(x_test)[:, 1]
    score_test = classification_report(y_test, clf.predict(x_test))
    clf_score = (clf.score(X, Y), clf.score(x_test, y_test))
    table, result = get_table(y_pre, y_test, 'xgb')
    print(Counter(clf.predict(x_test)), Counter(y_test))
    return table, result, clf_score

def svm_model(X, Y, x_test, y_test, params, save_model=False):
    clf=SVC(**params,probability=True)
    clf.fit(X, Y)
    clf_score = (clf.score(X, Y), clf.score(x_test, y_test))
    y_pre = clf.predict_proba(x_test)[:, 1]
    score_test = classification_report(y_test, clf.predict(x_test))
    table, result = get_table(y_pre, y_test, 'svm')
    # if save_model:
    #     log_model_path = str(docs_path['model_path']).format(product, 'log')
    #     joblib.dump(clf, log_model_path)
    return table, result, clf_score
