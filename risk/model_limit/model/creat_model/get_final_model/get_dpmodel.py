# from sklearn.externals import joblib
from keras.utils import np_utils, plot_model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import metrics
from keras.wrappers.scikit_learn import KerasClassifier
import numpy as np
from keras.constraints import maxnorm
# from process_data import get_pro_data
import json
from keras.optimizers import SGD
from sklearn.metrics import classification_report
from collections import Counter
import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from model.creat_model.assist_funcs.roc_cuttable import get_table
# 由get_rflog_param确定input_dim,init,activation,dropout,neurons,optimizer,weight_constraint,lr等参数
# 根据实际情况调整层数
'''
params=dict(init='uniform',activation='relu',
	dropout=0.2,neurons=300,optimizer='SGD',weight_constraint=2,
	num_classes=2,lr=0.1,epochs=6,batch_size=32)
'''


def get_keras_fmodel(X, Y, x_test, y_test,params, num_classes=2, save_model=False):
    # dp1 = str(docs_path['param_json']).format(product, 'dp1')
    # f = open(dp1, 'r')
    # params1 = json.load(f)
    # dp2 = str(docs_path['param_json']).format(product, 'dp2')
    # f = open(dp2, 'r')
    # params2 = json.load(f)
    # params = {**params1, **params2}
    Y = np_utils.to_categorical(Y, num_classes=num_classes)
    y_test_or = y_test
    y_test = np_utils.to_categorical(y_test, num_classes=num_classes)
    input_dim = X.shape[1]
    model = Sequential()
    model.add(Dense(params['first_neuron'], init=params['init'], input_dim=input_dim))
    model.add(Activation(params['activation']))
    # model.add(Dropout(params['dropout']))

    model.add(Dense(10))
    model.add(Activation(params['activation']))
    model.add(Dropout(params['dropout']))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer=SGD(lr=params['lr']), 
                  loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X, Y, epochs=1000, batch_size=256, shuffle=False)
    y_pre = (np.asarray(model.predict(x_test, 256)))
    score = classification_report(y_test, y_pre.round())
    clf_score = (model.evaluate(X, Y), model.evaluate(x_test, y_test))
    # 修改
    table, result = get_table(y_pre[:, 1], y_test[:, 1], 'dp')
    print(Counter(model.predict(x_test, 256)[:, 1].round()))
    return table, result, clf_score
