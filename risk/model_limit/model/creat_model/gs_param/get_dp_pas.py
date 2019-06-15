from keras.utils import np_utils, plot_model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import metrics
from keras import optimizers
import talos as ta
import sys
from pathlib import Path
from datetime import datetime,timedelta
now = datetime.now()
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from doc_files.files_path import docs_path
from collections import defaultdict

# 分布优化并将最终模型保存本地
'''
优化的参数包括：init-初始化函数；activation-激活函数；dropout-丢弃率；neurons-第一层的隐藏神经元数量；
optimizer-优化函数;lr-学斜率;momentum-动量因子;epochs;batch_size
'''
# 定义keras 中的create_model,优化init-初始化函数；activation-激活函数；dropout-丢弃率；neurons-第一层的隐藏神经元数量；
# optimizer-优化函数
# 构建模型结构
params = {'lr': (0.0001,0.01,0.1),
     'first_neuron':[16, 32],
     'init': ['uniform', 'normal', 'zero'],
     'dropout':  [0.2, 0.3, 0.4, 0.5],
     'optimizer': ['SGD','Adam', 'Nadam','RMSprop'],
     'loss': ['categorical_crossentropy','binary_crossentropy'],
     'activation': ['relu', 'sigmoid', 'tanh']}

def get_keras_fmodel(X, Y,x_val,y_val,params):
    Y = np_utils.to_categorical(Y, num_classes=2)
    y_val = np_utils.to_categorical(y_val, num_classes=2)
    model = Sequential()
    model.add(Dense(params['first_neuron'], init=params['init'], input_dim=X.shape[1]))
    model.add(Activation(params['activation']))

    model.add(Dense(10))
    model.add(Activation(params['activation']))
    model.add(Dropout(params['dropout']))
    model.add(Dense(2, activation='softmax'))
    optim_func=eval("optimizers.{}".format(params['optimizer']))
    optimizer = optim_func(lr=params['lr'])
    model.compile(optimizer=optimizer,
                  loss=params['loss'], metrics=['accuracy'])
    out=model.fit(X, Y, epochs=256, batch_size=256, shuffle=False,validation_data=[x_val, y_val])
    
    return out,model

def get_paras(X, Y,x_val,y_val):
    #time_limit=(now+timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
    h = ta.Scan(X, Y,x_val=x_val,y_val=y_val,params=params,model=get_keras_fmodel,round_limit=32)
    r=ta.Reporting(h)
    para_dict={}
    for k,v in params.items():
        para_dict[k]=v[0]
        for item in r.best_params()[0]:
            if item in v:
                para_dict[k]=item
    return para_dict