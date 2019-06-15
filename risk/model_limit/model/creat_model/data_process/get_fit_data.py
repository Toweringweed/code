from pathlib import Path
import sys
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from model.creat_model.data_process.data_normalize import *
import pandas as pd
from sklearn.model_selection import train_test_split
from model.creat_model.doc_files.files_path import load_ordata
from model.creat_model.data_process.data_encode import data_transform
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler


def load_fit_data(smote=True):
    or_data=load_ordata()
    or_data=or_data[or_data['classification'].isin(['good','bad'])]
    or_data['classification']=or_data['classification'].replace({'good':1,'bad':0})
    train,test=train_test_split(or_data,test_size=0.25)
    train,test = data_transform(train,test=test)
    X,Y=split_data(train,label='classification')
    x_test,y_test=split_data(test,label='classification')
    X,x_test=pro_data(X,x_test=x_test)
    if smote:
        X,Y=smote_sample(X,Y)
    return X,Y,x_test,y_test

if __name__ == '__main__':
    load_fit_data()