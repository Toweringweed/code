from sklearn.metrics import auc, roc_curve
import matplotlib.pyplot as plt
import pandas as pd
import time
import sys
from pathlib import Path
filename = 'model'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)

def timefunc(func):
    """Decorator to calc function's time cost."""
    def wrapper(*args, **kw):
        st = time.time()
        res = func(*args, **kw)
        # print(f'{func} cost {time.time() - st}s\n')
        print('{}cost {}s sec'.format(func, time.time() - st))
        return res
    return wrapper

# 分段统计
def get_pt(df, var, columns, label):
    out_put = pd.pivot_table(
        df, columns=columns, values=label, index=var, aggfunc='count', margins=True)
    f1 = pd.DataFrame()
    for i in out_put.columns:
        i_sum = out_put[i].sum() / 2
        f1[str(i)] = out_put[i]
        f1[str(i) + '%'] = (out_put[i] / out_put['All'] * 100).round(2)
    f1.drop('All%', axis=1, inplace=True)
    return f1

# 透视预测结果


def get_table(y_pre, y_test, func_name):
    df_pro = pd.DataFrame(y_pre * 100)
    df_result = pd.concat([df_pro, pd.DataFrame(y_test)],
                          ignore_index=True, axis=1)
    bins = [x * 10 for x in range(11)]
    df_result['pre'] = pd.cut(df_result[0], bins, include_lowest=True)
    df_result['test'] = df_result[1]
    df_result['num'] = df_result.index
    print(df_result.head())
    table = get_pt(df_result, 'pre', 'test', 'num')
    df_result = df_result[[0, 1]]
    df_result.rename(columns={0: '{}0'.format(
        func_name), 1: '{}1'.format(func_name)}, inplace=True)
    return table, df_result

# 绘制roc


def plot_roc(name, y_test, y_pre, num_classes):
    plt.figure()
    if num_classes > 2:
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(num_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_pre[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        for i in range(num_classes):
            plt.plot(fpr[i], tpr[i],
                     label='ROC curve of class {0} (area = {1:0.2f})'
                     ''.format(i, roc_auc[i]))
    else:
        fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, y_pre)
        roc_auc = auc(fpr_rf, tpr_rf)
        plt.plot(fpr_rf, tpr_rf, label='{} (area = {:.3f})'.format(name, roc_auc))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve'.format(name))
    plt.legend(loc='best')
    # plt.show()
    plt.savefig(str(_data_dir / '{}_roc.png').format(name))


def plot_score(train_score, test_score, x_label, model_list):
    plt.figure()
    fig, ax_lst = plt.subplots(2, 2)
    items = ((0, 0), (0, 1), (1, 0), (1, 1))
    for i in range(4):
        ax_lst[items[i]].plot(x_label, train_score[i],
                              label='train {}'.format(model_list[i]))
        ax_lst[items[i]].plot(x_label, test_score[i],
                              label='test {}'.format(model_list[i]))
        ax_lst[items[i]].legend(loc='upper right', fancybox=True)
    plt.xlabel('feature select value')
    plt.ylabel('model score')
    plt.savefig('model_score.png')

if __name__ == '__main__':
    plot_score(train_score)
