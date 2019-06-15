import sys
from pathlib import Path
import pandas as pd
import numpy as np
import json
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from binning_woe import sklearn_woe
from binning_woe.binning import sklearn_bin
from model.creat_model.doc_files.files_path import load_ordata
from model.preprocess_data.data_files import sqlcol
from model.creat_model.data_process import data_normalize

def data_transform(train,test,label='classification',woe=True):
    num_cols=[]
    cat_cols=['idcard_area','sex']
    cols=train.columns
    for i in cols:
        if i not in cat_cols:
            num_cols.append(i)
        #先丢弃datetime
    if woe:
        Sp=sklearn_bin.NumtoCategorical(bins_num=5)
        #can input chi or tree,and save json file for predict transform
        clf=Sp.fit(train[num_cols],label,split_func='tree')
        woe_data=clf.transform()
        train=pd.concat([woe_data,train[cat_cols]],axis=1,ignore_index=True)
        train.columns=cols
        #woe
        Cw=sklearn_woe.CattoWoe(label)
        wclf=Cw.fit(train)
        train=wclf.transform()
        woe_data=clf.transform(test[num_cols])
        test=pd.concat([woe_data,test[cat_cols]],axis=1,ignore_index=True)
        test.columns=cols
        test=wclf.transform(test)
        return train,test
    else:
        #todo
        pass






# 分段之后保存的文件
# if __name__ == '__main__':