from sklearn.externals import joblib
from keras.utils import np_utils, plot_model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import metrics
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
import numpy as np
from keras.constraints import maxnorm
import json
from process_data import get_pro_data
import pandas as pd
from sklearn import preprocessing
import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from doc_files.files_path import docs_path
# 分布优化并将最终模型保存本地
'''
优化的参数包括：init-初始化函数；activation-激活函数；dropout-丢弃率；neurons-第一层的隐藏神经元数量；
optimizer-优化函数;lr-学斜率;momentum-动量因子;epochs;batch_size
'''
# 定义keras 中的create_model,优化init-初始化函数；activation-激活函数；dropout-丢弃率；neurons-第一层的隐藏神经元数量；
# optimizer-优化函数
# 构建模型结构


def creat_model_ks1(input_dim=10, init='uniform', activation='relu', dropout=0.2, neurons=300, optimizer='SGD', weight_constraint=2, num_classes=2):
    # 输入的features数量
    model = Sequential()
    model.add(Dense(neurons, init=init, input_dim=input_dim,
                    kernel_constraint=maxnorm(weight_constraint)))
    model.add(Activation(activation))
    # 层数最好的怎么找
    # model.add(Dropout(dropout))
    model.add(Dense(20, init=init))
    model.add(Dropout(dropout))
    model.add(Activation(activation))
    model.add(Dense(num_classes, init=init, activation='softmax'))
    # 确认是否可以更改metrics
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy', metrics=["accuracy"])
    return model


def get_first_param(X, Y, model,num_classes=2):
    # scores = ['precision', 'recall']
    Y = np_utils.to_categorical(Y, num_classes=num_classes)
    model = KerasClassifier(build_fn=creat_model_ks1,
                            epochs=10, batch_size=64, verbose=0)
    input_dim = X.shape[1]
    # 设置被优化参数范围，并返回最优解
    # init = ['uniform', 'lecun_uniform', 'normal', 'zero', 'glorot_normal', 'glorot_uniform',
    #  'he_normal', 'he_uniform']
    init = ['uniform', 'normal', 'zero']
    # activation = ['softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid']
    activation = ['relu', 'sigmoid', 'tanh']
    # optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
    optimizer = ['SGD', 'RMSprop', 'Adam']
    # dropout=[0.2]
    dropout = [0.2, 0.3, 0.4, 0.5]
    # weight_constraint = [1, 2, 3, 4, 5]
    neurons = [20]
    input_dim = [input_dim]
    batch_size = [128]
    # batch_size = [128]
    # epochs = [10, 50, 100]
    epochs = [10]
    # 构建参数字典
    param_grid = dict(input_dim=input_dim, init=init, activation=activation, optimizer=optimizer,
                      dropout=dropout, neurons=neurons, batch_size=batch_size, epochs=epochs)
    # 如果提示：INFO (theano.gof.compilelock)，设置n_jobs=1,为-1是并行
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        scoring='roc_auc', n_jobs=1)
    grid_result = grid.fit(X, Y)
    # 得到最佳参数
    params = grid_result.best_params_
    optim_func = params['optimizer']
    # 输出最优解
    print("Best: %f using %s" % (grid_result.best_score_, params))
    best_model = grid_result.best_estimator_.model
    config = best_model.get_config()
    # 参数写入json
    return config, optim_func
'''
输出每个具体的值
for params, mean_score, scores in grid_result.grid_scores_:
    print("%f (%f) with: %r" % (scores.mean(), scores.std(), params))
'''
# 根据
import keras.optimizers as optimizers
# 找到各项最优值之后优化：lr-学斜率;momentum-动量因子，假定找到的最优optimizer为SGD；根据第一次优化的效果选择这次优化的参数
# 新增加的参数在learn_rate后面添加并指定初始值，具体的参数参考’https://keras.io/optimizers/‘。


def creat_model_ks2(config=[], optim_func='SGD', learn_rate=0.01):
    # 需要确认加载参数之后可否重构
    # config,optim_func=get_keras_param(X,Y,creat_model)
    model = Sequential.from_config(config)
    # 定义optimizer函数
    optim_func = eval("optimizers.{}".format(optim_func))
    optimizer = optim_func(lr=learn_rate)
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy', metrics=["accuracy"])
    return model


def get_final_param(X, Y, creat_model_ks2, config, optim_func, num_classes=2):
    Y = np_utils.to_categorical(Y, num_classes=num_classes)
    model = KerasClassifier(build_fn=creat_model_ks2, verbose=0)
    learn_rate = [0.001, 0.01, 0.1, 0.2, 0.3]
    param_grid = dict(config=[config], optim_func=[
                      optim_func], learn_rate=learn_rate)
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        scoring='roc_auc', n_jobs=1)
    grid_result = grid.fit(X, Y)
    print("Best: %f using %s" %
          (grid_result.best_score_, grid_result.best_params_))
    best_model = grid_result.best_estimator_.model
    params = {'learn_rate': grid_result.best_params_['learn_rate']}
    input_path = str(docs_path['param_json']).format('dp2')
    with open(input_path, "w") as f:
        json.dump(params, f)
    pass
