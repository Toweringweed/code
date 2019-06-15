
# 该文件包含特征选择与数据处理函数
import xgboost as xgb
import operator
from sklearn.linear_model import Lasso, LogisticRegression
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
# 随机森林的另一个模块
import xgboost as xgb
from sklearn.utils import shuffle
from path import Path
import sys
# 确认feature的顺序是否正确
filename = 'product_model'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from doc_files.files_path import load_file, docs_path
from data_process.get_fit_data import process_data, load_woe_data
# 返回lasso结果


def lasso_func(X, Y, cols, alp, positive=False, line=0, save=False):
    Y1 = Y.copy()
    Y1[Y1 == 0] = -1
    # 存储feature比重
    index = np.zeros([X.shape[1], ])
    for i in range(100):
        # 设定alpha的值
        alpha = random.uniform(alp[0], alp[1])
        clf = Lasso(alpha=alpha, positive=positive)
        clf.fit(X, Y1)
        data = clf.coef_
        data[data != 0] = 1
        index = index + data
    # 关联列名得到选出的列
    df_lasso = pd.DataFrame(index / 100)
    cols = cols
    df_lasso = pd.concat([df_lasso, pd.DataFrame(cols)],
                         ignore_index=True, axis=1)
    df_lasso.columns = ['percent', 'col']
    df_lasso = df_lasso[df_lasso['percent'] > line]
    df_lasso = df_lasso.sort_values(by=['percent'], ascending=False)
    if save:
        df_lasso.to_excel('lasso_select_temp.xlsx')
    return df_lasso

# 返回随机森林结果


def rf_func(X, Y, cols, n_estimators=200, line=0):
    clfs = {'random_forest': RandomForestClassifier(n_estimators=n_estimators)}
    clf = clfs['random_forest']
    X, Y = shuffle(X, Y)
    clf.fit(X, Y)
    # feature 需要添加name，df参数
    cols = cols
    df_rf = pd.DataFrame(clf.feature_importances_)
    df_rf = pd.concat([df_rf, pd.DataFrame(cols)], ignore_index=True, axis=1)
    df_rf.columns = ['percent', 'col']
    df_rf = df_rf[df_rf['percent'] > line]
    df_rf = df_rf.sort_values(by=['percent'], ascending=False)
    # df_rf.to_excel(r'E:\data\work\company_model\select_features\rf_select.xlsx')
    return df_rf

# xgboost效果


def xgb_func(X, Y, cols, num_boost_round=200, line=0):
    dtrain = xgb.DMatrix(X, label=Y)
    # 定义参数
    params = {'booster': 'gbtree',
              'objective': 'binary:logistic',
              'eval_metric': 'auc',
              'seed': 7,
              'nthread': 4,
              'silent': 1}
    watchlist = [(dtrain, 'train')]
    bst = xgb.train(
        params, dtrain, num_boost_round=num_boost_round, evals=watchlist)
    # 取出模型各列的影响值
    importance = sorted(bst.get_fscore().items(), key=operator.itemgetter(1))
    df_xgb = pd.DataFrame(importance, columns=['feature', 'fscore'])
    df_xgb['feature'] = df_xgb['feature'].apply(lambda x: int(x[1:]))
    df_xgb.index = df_xgb['feature']
    df_xgb = pd.concat([df_xgb, pd.DataFrame(cols)], ignore_index=True, axis=1)
    df_xgb.columns = ['feature', 'fscore', 'col']
    df_xgb.drop(['feature'], axis=1)
    df_xgb = df_xgb[df_xgb['fscore'] > line]
    df_xgb.sort_values(by=['fscore'], ascending=False, inplace=True)
    # df_xgb.to_excel(r'E:\data\work\company_model\select_features\xgb_select.xlsx')
    return df_xgb


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    test_num = random.choice([i for i in range(4)])
    product = '微加贷'
    df_cols = load_file('original_cols')
    cols = df_cols[df_cols['是否使用'] == 1]['英文'].tolist()
    product_info = (product, test_num)
    df_data_or = load_woe_data(*product_info)
    alp = (0, 0.1)
    df_data = df_data_or.sample(frac=1)
    X, Y, _, _ = process_data(df_data)
    df_lasso = lasso_func(X, Y, cols, alp)
    df_lasso.rename(columns={'col': '英文'}, inplace=True)
    df_final = pd.merge(df_cols, df_lasso, on='英文', how='left')
    lasso_path = str(docs_path['lasso_select']).format(product)
    df_final.to_excel(lasso_path)
