import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from model.creat_model.get_final_model.get_dpmodel import get_keras_fmodel
from model.creat_model.get_final_model.get_tradmodel import rf_model, log_model, xgb_model,svm_model
from multiprocessing import cpu_count, Queue, Pool
import pandas as pd
from functools import partial
from model.creat_model.assist_funcs.roc_cuttable import plot_roc, get_table
from model.creat_model.gs_param import get_trandition_params
from sklearn.model_selection import train_test_split
from model.creat_model.data_process.get_fit_data import load_fit_data
def fit_model(args):
    [x_train, y_train, x_test, y_test] = args
    X,x_val,Y,y_val=train_test_split(x_train,y_train,test_size=0.2)
    svm_paras=get_trandition_params.creat_model_svm(X, Y)
    # save_params(svm_paras,'svm')
    _, result_svm, score_svm = svm_model(
        x_train, y_train, x_test, y_test,svm_paras)
    rf_paras=get_trandition_params.creat_model_rf(X, Y)
    # rf_paras=get_params('rf')
    _, result_rf, score_rf = rf_model(
        x_train, y_train, x_test, y_test,rf_paras)
    log_paras=get_trandition_params.creat_model_log(x_train, y_train)
    _, result_log, score_log = log_model(
        x_train, y_train, x_test, y_test, log_paras)
    xgb_paras=get_trandition_params.creat_model_xgb(X,Y,x_val,y_val)
    _, result_xgb, score_xgb = xgb_model(
        x_train, y_train, x_test, y_test,xgb_paras)
    # dp_paras=get_dp_pas.get_paras(X,Y,x_val,y_val)
    # _, result_dp, score_dp = get_keras_fmodel(
    #     x_train, y_train, x_test, y_test,dp_paras)
    print(score_rf, score_log, score_xgb,score_svm)
    return pd.concat([result_rf, result_log, result_xgb,result_svm], axis=1)

def get_params(model_name):
    rf = str(docs_path['param_json']).format('微加贷', model_name)
    f = open(rf, 'r')
    return json.load(f)

def save_params(paras,model_name):
    input_path = str(docs_path['param_json']).format('微加贷', model_name)
    with open(input_path, "w") as f:
        json.dump(paras, f)

if __name__ == '__main__':
    X,Y,x_test,y_test=load_fit_data()
    fit_model([X,Y,x_test,y_test])

    #  = '微加贷'
    # pool = Pool(processes=cpu_count())
    # models = partial(fit_model, =)
    # fit_data = [load_fit_data(, x, important=0.2) for x in range(5)]
    # predict_data = pool.map(models, fit_data)
    # df = pd.concat(predict_data, ignore_index=True)
    # df['avg'] = df[['rf0', 'log0', 'xgb0', 'dp0','svm0']].sum(axis=1) / 5
    # df.to_excel(str(_data_dir / 'predict_wei.xlsx'))

