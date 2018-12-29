#%%
import numpy as np
import pandas as pd
import re

np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 500
pd.options.display.max_columns = 100
pd.set_option('expand_frame_repr', False)

df_all = pd.read_excel(r'e:/GIS/土地供应2005_2018_地表_全口径_宗地.xlsx')
df = df_all[(df_all.GB_DLMC=='住宅用地')| (df_all.GB_DLMC=='工矿仓储用地') |(df_all.GB_DLMC=='商服用地') | (df_all.GB_DLMC=='工业用地')]
df = df[['PARCEL_NO', 'YDMJ','JZMJ', 'HT_DLMC', 'GB_DLMC', '建筑面积说明']]

col_dict = [
    {'name_en': 'HT_DLMC', 'name_zh': '合同_地类名称'},
    {'name_en': 'GB_DLMC', 'name_zh': '国标_地类名称'},
    {'name_en': 'ZDH', 'name_zh': '宗地号'},
    {'name_en': 'YDMJ', 'name_zh': '用地面积'},
    {'name_en': 'JZMJ', 'name_zh': '建筑面积'},
    
]
df.info()

#%%
def get_list_num(df, p_str_list, c, column_name):
    pub = '共?(\d+(\.\d+)?)(平方|平方米|平米|㎡)'
    list_sum = 0
    re_list = []
    for i in p_str_list:
        pt = re.findall(re.compile(i + pub), c)
        if pt:
            num = 0
            for j in range(0, len(pt)):
                num = num + float(pt[j][0])
                re_list.append(''.join(pt[j]))
            list_sum = list_sum + num
            for j in pt:
                jj = ''.join(j)
                c = re.sub(jj, '', c)
        pt2 = re.findall(re.compile(pub + '的' + i), c)
        if pt2:
            num2 = 0
            for k in range(0, len(pt2)):
                num2 = num2 + float(pt2[k][0])
                re_list.append(''.join(pt2[k]))
            list_sum = list_sum + num2
        for rr in re_list:
            c = c.replace(rr, '')
    df.at[index, column_name] = list_sum

for index, rows in df.iterrows():
    replace_list = [
        
        
    ]
    c = str(rows['建筑面积说明']).replace(' ', '').replace('\n', '').replace('\r', '').replace('面积', '').replace('用房', '')
    c = c.replace(':', '').replace('：', '').replace('中心', '').replace('不少于', '').replace('不超过', '').replace('场地', '').replace('用地', '')
    c = c.replace('建筑' , '').replace('总', '').replace('≤', '').replace('≥', '').replace('业务', '').replace(r'[独立占地]', '')
    c = c.replace('【', '').replace('】', '').replace('楼', '').replace('大楼', '').replace('总计', '')
    c = re.sub(r'（\D+）', '', c)
    
    p_dict = [
        {'col': '住宅-总', 'p': ['居住', '住宅', '[^保障性]住房']},
        {'col': '住宅-公共租赁住房', 'p': ['公共租赁住房', '保障性住房', '保障性用房']},
        {'col': '住宅-安居型商品房', 'p': ['安居型商品房']},
        {'col': '住宅-人才住房', 'p': ['人才住房']},
        
        {'col': '产业-总', 'p': ['产业', '厂房及配套', '产业研发', '产业生产']},
        {'col': '产业-工业用房', 'p': ['厂房', '设备', '车间', '仓库', '物流建筑']},
        {'col': '产业-创新型产业用房', 'p': ['创新型产业', '科研']},
        {'col': '产业配套用房-总', 'p': ['配套商业及行政办公', '配套综合服务']},
        {'col': '产业配套用房-宿舍食堂', 'p': ['宿舍', '食堂', '值班休息', '宿舍及配套']},
        {'col': '产业配套用房-配套办公', 'p': ['配套办公', '办公配套', '配套行政办公']},
        {'col': '产业配套用房-配套商业', 'p': ['配套商业', '商业配套','配套商业设施', '配套商业服务设施']},
        
        {'col': '商业', 'p': ['[^配套]商业', '[^配套]商业设施', '[^配套]商业服务设施', '^商业', '^商业设施', '^商业服务设施']},
        {'col': '办公', 'p': ['[^配套]办公', '^办公']},
        
        {'col': '商务公寓', 'p': ['商务公寓']},
        {'col': '人才公寓', 'p': ['人才公寓']},
        {'col': '服务业', 'p': ['服务业', '文化设施', '会所', '剧院', '美术馆', '剧院及其配套', '地上游乐设施及相关配套', '书城']},
        
        {'col': '酒店', 'p': ['酒店']},
        
        {'col': '公共设施配套-总', 'p': ['公共配套设施', '公共配套', '公建配套设施', '公建配套']},
        {'col': '公共设施配套-社区管理', 'p': ['居委会', '社区服务站', '警务室', '便民服务站']},
        {'col': '公共设施配套-社区文化体育', 'p': [ '文化活动室', '社区体育活动', '活动站', '文体活动', '文化室', '文化娱乐',
                                       '社区运动', '文化活动']},
        {'col': '公共设施配套-社区健康', 'p': ['社区健康服务',  '社康','康体', '康复']},
        {'col': '公共设施配套-养老', 'p': [ '照料', '老年活动', '照料服务']},
        {'col': '公共设施配套-生活', 'p': ['菜市场', '充电站']},
        {'col': '公共设施配套-幼儿园', 'p': ['幼儿园']},
        {'col': '公共设施配套-学校', 'p': ['学校']},
        {'col': '公共配套设施-卫生', 'p': ['回收点','回收站', '垃圾站', '垃圾收集站', '垃圾处理站', '污水处理站','垃圾转运站', '公厕', '厕所']},
        {'col': '公共配套设施-交通邮政', 'p': ['公交场站', '公交站场', '公交站','换乘站', '公交首末站',  '公交运营', '公交充电站' 
                                    '邮政局','邮政所', '邮电设施', '综合车站']},
        
        {'col': '配套设施-停车场', 'p': ['停车场', '停车库']},
        {'col': '配套设施-物业', 'p':['物管', '物业服务', '物业', '物业管理']}
    ]
    
    for i in p_dict:
        get_list_num(df, i['p'], c, i['col'])

df

#%%
pd.DataFrame.to_excel(df, 'E:/GIS/tt5.xlsx')
df.drop(['YDMJ','JZMJ', 'HT_DLMC', 'GB_DLMC', '建筑面积说明'], axis=1, inplace=True)
df_c = pd.merge(df_all, df, on='PARCEL_NO', how='left')
pd.DataFrame.to_excel(df_c, 'E:/GIS/tz.xlsx', index=None)

