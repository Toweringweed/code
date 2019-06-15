# from sklearn.grid_search import GridSearchCV
# 0.20版本
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import xgboost as xgb
import json
import random
import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)

def creat_model_rf(X, Y):
    # scoring recall
    model = RandomForestClassifier()
    # 设定参数选取范围
    n_estimators = [random.randint(100, 500) for i in range(5)]
    max_depth = [random.randint(10, 30) for i in range(5)]
    # max_depth=[None]
    max_features = ['sqrt', 'log2', 'auto']
    param_grid = dict(n_estimators=n_estimators, max_depth=max_depth,
                      max_features=max_features)
    # 构建gridsearch，选取roc作为评价依据
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        scoring='roc_auc',n_jobs=1)
    grid_result = grid.fit(X, Y)
    print("Best: %f using %s" %
          (grid_result.best_score_, grid_result.best_params_))
    best_model = grid_result.best_estimator_
    # 输出最优参数
    return grid_result.best_params_

# 查询逻辑回归最优参数


def creat_model_log(X, Y):
    model = LogisticRegression()
    # penalty = ['l1','l2']
    penalty = ['l2']
    solver = ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
    C = [0.3,1,10]
    param_grid = dict(penalty=penalty,C=C)
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        scoring='roc_auc', n_jobs=1)
    grid_result = grid.fit(X, Y)
    print("Best: %f using %s" %
          (grid_result.best_score_, grid_result.best_params_))
    best_model = grid_result.best_estimator_
    return grid_result.best_params_

# 查询xgboost决策树最优参数;暂时不考虑


def creat_model_xgb(X, Y, x_test, y_test):
    model = xgb.XGBClassifier()
    # max_depth = [random.randint(3, 10) for i in range(5)]
    params = {'learning_rate': [0.001, 0.01, 0.1,0.5],
              'max_depth': [random.randint(10, 30) for i in range(5)],
              'n_estimators': [random.randint(100, 500) for i in range(5)],
              'booster':['gbtree','gblinear','dart'],
              'objective': ['binary:logistic']}
    fit_params = {"early_stopping_rounds": 3, "eval_set": [[x_test, y_test]]}
    grid = GridSearchCV(model, param_grid=params, scoring='roc_auc', verbose=2,
                        fit_params=fit_params)
    grid_result = grid.fit(X, Y)
    print("Best: %f using %s" %
          (grid_result.best_score_, grid_result.best_params_))
    best_model = grid_result.best_estimator_
    return grid_result.best_params_

def creat_model_svm(X, Y):
    model = SVC()
    kernel = ['rbf','linear','poly','sigmoid']
    # penalty = ['l2']
    # solver = ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
    C = [0.3,1,10]
    param_grid = dict(kernel=kernel,C=C)
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        scoring='roc_auc', n_jobs=1)
    grid_result = grid.fit(X, Y)
    print("Best: %f using %s" %
          (grid_result.best_score_, grid_result.best_params_))
    return grid_result.best_params_