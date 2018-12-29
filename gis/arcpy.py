import arcpy
import numpy as np
import pandas as pd
import win32com.client
import pypyodbc

db_name = r'e:/GIS/土地供应20181130.mdb'
tb_name = '土地供应2005_2018_地表_全口径_宗地'

str = 'Driver={Microsoft Access Driver(*.mdb); DBQ=%s}' %(db_name)
conn = pypyodbc.win_connect_mdb(str)

cur = conn.cursor()
# cur.execute('select * from %s' %tb_name)



# conn = win32com.client.gencache.EnsureDispatch('ADODB.Connection')

# conn = win32com.client.Dispatch(r'ADODB.Connection')
# DSN = 'PROVIDER=Microsoft.Jet.OLEDB.12.0;DATA SOURCE=%s;' %(db_name)
# # DSN = 'PROVIDER = Microsoft.ACE.OLEDB.12.0;DATA SOURCE =%s;' %(db_name)
# conn.open(DSN)
# rs = win32com.client.Dispatch(r'ADODB.Recordset') 
# rs.Open('[' + tb_name + ']', conn, 1, 3) 

print('go')
df = pd.read_excel(r'E:/GIS/ss.xlsx')
for index, rows in df.iterrows:
    sql = 'update %s set context=%s where PARCEL_NO=%s' %(tb_name, rows['context'], rows['zongdi'])
    print(sql)
    cur.execute(sql)






