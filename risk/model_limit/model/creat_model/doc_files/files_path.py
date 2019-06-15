import sys
from pathlib import Path
import pandas as pd
_data_dir = Path(__file__).parent

_data_dir_product = Path(__file__).parent / '{}'
filename = 'model_limit'
paths = str(Path(__file__))
final_path = paths[:paths.find(filename) + len(filename)]
sys.path.append(final_path)
from model.preprocess_data.db_access import loacl_db

docs_path = {'load_ordata': _data_dir / 'model_data.xlsx',
             'original_describe': _data_dir / 'original_info.xlsx',
             'original_cols': _data_dir / 'model_dict.xlsx',
             'split_data': _data_dir / 'data_trans.csv',
             'split_json': _data_dir / 'split_code_fix.json',
             'lasso_select': _data_dir_product / 'lasso_select.xlsx',
             # product_name,test_bath
             'woe_data': _data_dir_product / 'woe_data_{}.xlsx',
             'param_json': _data_dir_product / 'param_{}.json',
             'model_path': _data_dir_product / 'model_{}.h5'}


def load_file(data_name, *args):
    file_path = str(docs_path[data_name])
    if args:
        file_path = file_path.format(*args)
    if file_path.endswith('xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('csv'):
        return pd.read_csv(file_path)
    else:
        print('please check the {} name'.format(data_name))

def load_ordata():
    use_cols=['card_account', 'card_notsettled', 'card_overdue',
       'card_90overdue', 'card_guaranty', 'housing_loan_account',
       'housing_loan_notsettled', 'housing_loan_overdue',
       'housing_loan_90overdue', 'housing_loan_guaranty', 'other_loan_account',
       'other_loan_notsettled', 'other_loan_overdue', 'other_loan_90overdue',
       'other_loan_guaranty','uuid']
    query_cols = ','.join(use_cols)
    conn=loacl_db()
    summary=f'select {query_cols} from summary'
    df_summary=pd.read_sql(summary,conn)
    label_cardinfo='select uuid,idcard_area,sex,age,classification from cust_label'
    df_label_cardinfo=pd.read_sql(label_cardinfo,conn)
    # 征信数据
    # credit=''
    # df_credit=pd.read_sql(credit,conn)
    df_or=pd.merge(df_summary,df_label_cardinfo,how='left',on='uuid')
    # df_or=pd.merge(df_or,df_credit,how=left,on='uuid')
    df_or.drop('uuid',axis=1,inplace=True)
    return df_or


if __name__ == '__main__':
    print(str(docs_path['split_data'])+'2')
    # global product
    # product = '微加贷'
    # product_info = ('微加贷', '2')
    # load_file('woe_data', *product_info)
