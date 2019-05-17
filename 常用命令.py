#%%
import pandas as pd
import numpy as np
import re

'''
Python 常用命令
'''

# pandas常用设置
np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 100000
pd.options.display.max_columns = 800
pd.set_option('expand_frame_repr', False)

#%%

old_value = 0
new_value = 1
# Dataframe 数据操作

# 新变量的生成
df = pd.DataFrame()
df['new_var'] = df['old_var']
df['new_var'] = 34
df.insert(loc=3, column='new_var', value=45)

# 变量值替换，方法1：
df['var'].str.replace(old_value, new_value)

# 变量值替换，方法2，更为强大，相当于if：
df.loc[df.old_var==old_value, 'new_var'] = new_value

# 二维数组转化为一维
list1 = list() 
list1 = sum(list1, [])

# 变量重命名， rename 必须使用inplace 才能生效

df.rename(inplace=True, columns={
    "v45_fangdai（zongbishu）": "loan_house_num",
    "v46_fangdai（jieqingbishu）": "loan_house_jieqing",

})

# 判断变量值为NaN值
var = ''
if var != var:
    var = -99

# 删除/保留某些行
df = df[df['合同编号'].str.len() > 2 ]

# pivot_table 中的问题： 重复行、重复列，应提前统一变量类型

# pivot实例
dft_age2 = pd.pivot_table(df, values='temp',  index=['APPLY_AMOUNT'], columns=['user_mark'],aggfunc=np.size)
dft_age2 = pd.DataFrame(dft_age2).reset_index()

# df zip
combined = list(zip(dft_age2['expect'], df['APPLY_AMOUNT']))

# df中replace的用法
df = df.ix[:, :].replace('nan%', '')
df['合同编号'] = df['合同编号'].str.replace('_01', '')

# 字符串格式化
df.apply('{:.2%}'.format)
df.apply(lambda x: '{}%'.format(round(x,2)))

# findall 在df中应用，str参数是关键,注意要通过下面两步完成，否则会出错
df.loc[df['v9_shenfenzhenghao'].str.findall(re.compile('\d{6}(\d{4})')).str.len() > 0, '出生年'] = \
    df['v9_shenfenzhenghao'].str.findall(re.compile('\d{6}(\d{4})'))
df.loc['出生年'] = df.loc['出生年'].str[0]

# 字符转化
ss = '{"name_data1": [{"value2": 0, "value1": 734, "name": "\u91cd\u5e86\u5927\u90fd\u4f1a"}, {"value2": 3, "value1": 418, "name": "\u4e2d\u5929\u5e7f\u573a\u8425\u9500\u4e00\u90e8"}, {"value2": 4, "value1": 413, "name": "\u6210\u90fd\u65f6\u4ee3\u516b\u53f7"}, {"value2": 1, "value1": 378, "name": "\u4e2d\u5929\u5e7f\u573a\u8425\u9500\u4e8c\u90e8"}, {"value2": 2, "value1": 361, "name": "\u5408\u80a5\u7eff\u5730\u8d62\u6d77"}, {"value2": 3, "value1": 358, "name": "\u5357\u5b81\u9752\u79c0\u4e07\u8fbe"}, {"value2": 7, "value1": 358, "name": "\u77f3\u5bb6\u5e84\u4e07\u8fbe\u5e7f\u573a"}, {"value2": 0, "value1": 357, "name": "\u6606\u660e\u5efa\u5de5\u5927\u53a6"}, {"value2": 6, "value1": 336, "name": "\u90d1\u5dde\u76db\u6da6\u767d\u5bab"}, {"value2": 1, "value1": 328, "name": "\u6d4e\u5357\u4e2d\u94f6\u5927\u53a6"}, {"value2": 2, "value1": 304, "name": "\u676d\u5dde\u897f\u5b50\u56fd\u9645"}, {"value2": 3, "value1": 258, "name": "\u6f4d\u574a\u4e07\u8fbe\u5e7f\u573a"}, {"value2": 0, "value1": 253, "name": "\u8d35\u9633\u82b1\u679c\u56ed"}, {"value2": 2, "value1": 249, "name": "\u4e34\u6c82\u5965\u65af\u5361CBD"}, {"value2": 2, "value1": 228, "name": "\u65e0\u9521\u6e05\u626c\u8def"}, {"value2": 0, "value1": 210, "name": "\u4e0a\u6d77\u5357\u8bc1\u5927\u53a6"}, {"value2": 2, "value1": 203, "name": "\u4fdd\u5b9a\u5eb7\u6cf0\u56fd\u9645"}, {"value2": 4, "value1": 198, "name": "\u6210\u90fd\u96c4\u98de\u4e2d\u5fc3"}, {"value2": 0, "value1": 196, "name": "\u5170\u5dde\u6c11\u5b89\u5927\u53a6\u7b2c\u4e00"}, {"value2": 0, "value1": 189, "name": "\u5929\u6d25\u5b9d\u5229\u56fd\u9645\u8425\u9500\u4e00\u90e8"}, {"value2": 1, "value1": 189, "name": "\u5b81\u6ce2\u6c47\u91d1\u5927\u53a6"}, {"value2": 1, "value1": 187, "name": "\u8944\u9633\u76db\u7279\u533a"}, {"value2": 2, "value1": 179, "name": "\u6d4e\u5b81\u4e07\u4e3d\u5bcc\u5fb7"}, {"value2": 2, "value1": 176, "name": "\u6dc4\u535a\u6f58\u57ce\u56fd\u9645"}, {"value2": 0, "value1": 155, "name": "\u897f\u5b89\u4e2d\u8d38\u5e7f\u573a"}, {"value2": 0, "value1": 146, "name": "\u5929\u6d25\u5b9d\u5229\u56fd\u9645\u8425\u9500\u4e8c\u90e8"}, {"value2": 2, "value1": 144, "name": "\u9547\u6c5f\u4e2d\u6d69\u56fd\u9645\u5e7f\u573a"}, {"value2": 2, "value1": 129, "name": "\u7389\u6797\u7f8e\u6865\u5546\u52a1\u4e2d\u5fc3"}, {"value2": 0, "value1": 127, "name": "\u5170\u5dde\u6c11\u5b89\u5927\u53a6\u7b2c\u4e8c"}, {"value2": 2, "value1": 126, "name": "\u70df\u53f0\u9633\u5149100"}, {"value2": 1, "value1": 123, "name": "\u5408\u80a5\u65b0\u57ce\u56fd\u9645"}, {"value2": 1, "value1": 122, "name": "\u5357\u901a\u91d1\u878d\u6c47"}, {"value2": 0, "value1": 108, "name": "\u897f\u5b89\u9526\u7ee3\u534e\u5ead"}, {"value2": 1, "value1": 103, "name": "\u897f\u5b81\u4e94\u56db\u5e7f\u573a"}, {"value2": 2, "value1": 99, "name": "\u67f3\u5dde\u6842\u4e2d\u5927\u9053"}, {"value2": 0, "value1": 94, "name": "\u4e1c\u8425\u534e\u6cf0\u5927\u53a6"}, {"value2": 1, "value1": 88, "name": "\u9075\u4e49\u822a\u5929\u5927\u53a6"}, {"value2": 1, "value1": 88, "name": "\u9752\u5c9b\u56fd\u534e\u5927\u53a6"}, {"value2": 0, "value1": 83, "name": "\u77f3\u5bb6\u5e84\u534e\u5f3a\u5e7f\u573a"}, {"value2": 0, "value1": 81, "name": "\u54b8\u9633\u5cf0\u6c47\u56fd\u9645"}, {"value2": 0, "value1": 81, "name": "\u6cf0\u5b89\u4e07\u8fbe\u5e7f\u573a"}, {"value2": 1, "value1": 67, "name": "\u53f0\u5dde\u5929\u548c\u5927\u53a6"}, {"value2": 0, "value1": 63, "name": "\u5357\u4eac\u57ce\u5f00\u5927\u53a6"}, {"value2": 1, "value1": 63, "name": "\u94a6\u5dde\u9633\u5149\u66fc\u54c8\u987f"}, {"value2": 0, "value1": 51, "name": "\u6ee8\u5dde\u56fd\u9645\u5927\u53a6"}, {"value2": 0, "value1": 44, "name": "\u5b9d\u9e21\u5929\u540c\u56fd\u9645"}, {"value2": 0, "value1": 38, "name": "\u82cf\u5dde\u5b8f\u6d77\u5927\u53a6"}, {"value2": 0, "value1": 36, "name": "\u6c49\u4e2d\u8d22\u5bcc\u9996\u5ea7"}, {"value2": 0, "value1": 29, "name": "\u62c9\u8428\u54c8\u8fbe\u6ee8\u6cb3\u82b1\u56ed"}, {"value2": 1, "value1": 20, "name": "\u94f6\u5ddd\u7d2b\u8346\u82b1\u5546\u52a1\u4e2d\u5fc3"}, {"value2": 0, "value1": 7, "name": "\u5b89\u5eb7\u6c49\u57ce\u56fd\u9645"}]}'
print(ss.encode('utf8').decode('utf-8'))

# json
import json
with open(r'E:\hoomsun_data\analysis\models\split_code.json') as j_file:
    j = json.load(j_file)
with open(r'E:\hoomsun_data\analysis\models\split_code.json', 'w') as j_file:
    j_file.write(j)
j_file.close()

# 加快执行速度
# @numba.jit
def Chi2(combined):
    chi2 = []
    for i in combined:
        chi = (i[1]-i[0])**2/i[0]
        chi2.append(chi)

    chi2 = np.sum(chi2)
    return chi2

def get_mark(x,y):
    z=-99
    if x>=1:
        z=0
    elif (x<1) & (y>=6):
        z=1
    else:
        z=-99
    return z
    
df['user_mark'] = df.apply(lambda x: get_mark(x.history_max_qici, x.current_period), axis=1)

# 删除列
dfx.drop(['开工日期_x','开工日期_y', '竣工日期_x','竣工日期_y','序号' ], inplace=True, axis=1)

# 排序
df = df.sort_values(by=['宗地号', '合同签订日', '合同字号_1'])

# 删除重复

# 获取行最大值的列标签名 
dfs['class_max'] = dfs[class_set].idxmax(axis=1)

# 规整pivot_table表
df['cc'] = 1
dfx = pd.pivot_table(df, columns=['category'], values=['cc'], index=['Id'], aggfunc='sum', fill_value=0)
class_list = sorted(list(set(df['category'])))
col = ['Id'] + class_list
dfs = pd.DataFrame(dfx.reset_index().as_matrix(), columns=col)
