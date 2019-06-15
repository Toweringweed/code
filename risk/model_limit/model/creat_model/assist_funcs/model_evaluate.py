# 懒得写了用之前jupyter的吧
import pandas as pd
from sklearn.metrics import auc, roc_curve
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from doc_files.files_path import _data_dir
from assist_funcs.roc_cuttable import plot_roc


def get_pt(df, var, columns, label):
    out_put = pd.pivot_table(
        df, columns=columns, values=label, index=var, aggfunc='count', margins=True)
    f1 = pd.DataFrame()
    out_put['All'] = out_put[0] + out_put[1]
    print(out_put)
    for i in out_put.columns:
        i_sum = out_put[i].sum() / 2
        f1[str(i)] = out_put[i]
        f1[str(i) + '%'] = (out_put[i] / out_put['All'] * 100).round(2)
    f1.drop('All%', axis=1, inplace=True)
    return f1


def get_table(df, name,cols='avg'):
    df['num'] = df.index
    bins = [x * 10 for x in range(11)]
    df[name] = pd.cut(df[cols], bins, include_lowest=True)
    table = get_pt(df, name, 'dp1', 'num')
    df['pre'] = df[cols].apply(lambda x: 0 if x < 50 else 1)
    print(classification_report(df['dp1'], df['pre']))
    plot_roc(name, df['dp1'], df[cols], 2)
    return table

if __name__ == '__main__':
    df_rong = pd.read_excel(str(_data_dir / 'predict_wei.xlsx'))
    # df_wei = pd.read_excel(str(_data_dir / 'predict_wei.xlsx'))
    # print(get_table(df_wei, 'all_wei'))
    for i in ['rf0','log0','xgb0','dp0','avg']:
        print(get_table(df_rong, i+'_label',i))
