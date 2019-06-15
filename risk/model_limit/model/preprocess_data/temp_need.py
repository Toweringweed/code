from db_access import oracle_db,loacl_db
import pandas as pd

conn = oracle_db('credit','credit2018')
my_conn=loacl_db()

summary_sql='select id_card,apply_date,loan_id from summary'
df_summary=pd.read_sql(summary_sql,my_conn)
# df_summary['idcard_birthday']=df_summary['id_card'].str[6:14]


hs_apply='select loan_id,cust_name,cust_mobile from hs_apply'
df_apply=pd.read_sql(hs_apply,conn)

df_need=pd.merge(df_summary,df_apply,how='left',on='loan_id')
df_need.to_excel(r'C:\Users\Administrator\Desktop\temp_data.xlsx')