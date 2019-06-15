import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from doc_files.files_path import load_file, _data_dir
from keras.utils import np_utils
from gs_param.get_trandition_params import creat_model_rf, creat_model_log, creat_model_xgb
# from gs_param.get_dp_params import *
from data_process.get_fit_data import load_woe_data, process_data
from gs_param.get_dp_pas import *


def load_fit_data(product_name, test_num, important=0):
    df_cols = load_file('lasso_select', (product_name))
    cols = df_cols[(df_cols['是否使用'] == 1) & (
        df_cols['percent'] >= important)]['英文'].tolist()
    # cols = df_cols[df_cols['是否使用'] == 1]['英文'].tolist()
    product_info = (product_name, test_num)
    df_data = load_woe_data(*product_info)
    X, Y, x_test, y_test = process_data(df_data, workflow_name=product_name,upsample_name='smote')
    return X, Y, x_test, y_test


if __name__ == '__main__':
    import random
    product = '微加贷'
    test_num = random.choice([0, 1, 2, 3, 4])
    X, Y, x_test, y_test = load_fit_data(product, test_num)
    print('load fit data finish')
    # creat_model_rf(X, Y,product)
    # creat_model_log(X, Y, product)
    # creat_model_xgb(X, Y, x_test, y_test, product)
    get_paras(X, Y, x_test, y_test)
    # config, optim_func = get_first_param(X, Y, creat_model_ks1, product)
    # get_final_param(X, Y, creat_model_ks2, config, optim_func, product)
