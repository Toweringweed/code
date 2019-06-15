import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
# 分割标签数据与特征数据


def split_data(all_data,label):
    # 分label与features
    cols=list(filter(lambda item:item !=label,all_data.columns))
    #need fix
    all_data.fillna(0, inplace=True)
    feature_data = np.array(all_data[cols])
    label_data = np.array(all_data[[label]])
    X, Y = shuffle(feature_data, label_data)
    return X, Y

# 数据预处理，保存transform参数为部署模型使用


def pro_data(X, x_test=None, fit_func=preprocessing.StandardScaler(),save=False):
    # 处理数据，可以选择归一化或者正则化
    normalizer = StandardScaler()
    normalizer.fit(X)
    StandardScaler(copy=True, with_mean=True, with_std=True)
    X = normalizer.transform(X)
    x_mean = normalizer.mean_
    x_std = normalizer.var_
    if save:
        np.save(r'F:\sh_data\keras\x_mean2.npy', x_mean)
        np.save(r'F:\sh_data\keras\x_std2.npy', x_std)
    if x_test is not None:
        x_test = normalizer.transform(x_test)
    return X, x_test

def smote_sample(X, y):
    smote_nc = SMOTE()
    X_resampled, y_resampled = smote_nc.fit_resample(X, y)
    return X_resampled,y_resampled