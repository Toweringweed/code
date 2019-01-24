
# coding: utf-8

#%%
import numpy as np
import pandas as pd
import re
from datetime import datetime

np.set_printoptions(threshold=100000)
pd.options.display.max_rows = 500
pd.options.display.max_columns = 100
pd.set_option('expand_frame_repr', False)

df_cols = pd.read_excel(r'D:/workspace/字段列表.xlsx')
col_list = df_cols['name'].tolist()
print(col_list)


#%%

df = pd.read_excel(r'D:/workspace/数据2005-2019-3.xlsx')
df.info()
df.head()


#%%
### 定义字典
dict_peitao = [
    {'col': '配套用房_总', 'p': ['配套商业及行政办公', '配套综合服务']},
    {'col': '配套用房_宿舍食堂', 'p': ['宿舍', '食堂', '值班休息', '宿舍及配套', '配餐']},
    {'col': '配套用房_配套办公', 'p': ['配套办公', '办公配套', '配套行政办公']},
    {'col': '配套用房_配套商业', 'p': ['配套商业', '商业配套','配套商业设施', '配套商业服务设施']}
]

dict_res = [
    {'col': '住宅_人才住房', 'p': ['人才住房', '人才安居住房', '人才安居房', '人才房']},
    {'col': '住宅_安居型商品房', 'p': ['安居型商品房']},
    {'col': '住宅_公共租赁住房', 'p': ['公共租赁住房', '保障性住房', '保障性', '公共租赁','公共租赁房', '公共租赁型住房', '保障房']},
    {'col': '住宅_总', 'p': ['居住', '住宅', '住房']},
    {'col': '住宅_人才公寓', 'p': ['人才公寓']},
    {'col': '住宅_别墅', 'p':['别墅']}
]

dict_ind = [
    {'col': '产业_工业用房', 'p': ['厂房', '设备', '车间']},
    {'col': '产业_仓库', 'p': ['仓库']},
    {'col': '产业_物流', 'p': ['物流']},
    {'col': '产业_创新型产业用房', 'p': ['创新型产业']},
    {'col': '产业_科研用房', 'p': ['科研']},
    {'col': '产业_总', 'p': ['厂房及配套', '研发', '产业生产', '产业']},
    {'col': '产业配套_总', 'p': ['产业配套', '工业配套']},
    
]

dict_com = [
    {'col': '商业_地下商业', 'p': ['地下商业']},
    {'col': '商业', 'p': ['商业', '商业设施', '商业服务设施', '商业', '商业设施', '商业服务设施']},
    {'col': '办公', 'p': ['办公']},
    {'col': '商务公寓', 'p': ['商务公寓']},
    {'col': '公寓', 'p': ['公寓']},
    {'col': '服务业', 'p': ['服务业']},
    {'col': '文化设施', 'p': ['文化设施',]},
    {'col': '会所', 'p': ['会所']},
    {'col': '剧院', 'p': ['剧院', '剧院及配套', '剧院及其配套']},
    {'col': '美术馆', 'p': [ '美术馆']},
    {'col': '书城', 'p': ['书城']},
    {'col': '游乐设施', 'p': ['地上游乐设施', '地上游乐设施及相关配套']},
    {'col': '酒店', 'p': ['酒店', '旅馆业']}
]

dict_gov = [
    {'col': '学校', 'p': ['教育', '教学']},   # 需细化
        
]
dict_pub = [
    {'col': '计容总面积', 'p': ['容积率', '容积率为', '容积率的']},
    {'col': '公共设施配套_总', 'p': ['公共配套设施', '公共配套', '公建配套设施', '公建配套']},
    {'col': '公共设施配套_居委会', 'p': ['居委会']},
    {'col': '公共设施配套_社区管理', 'p': ['社区管理']},
    {'col': '公共设施配套_便民服务站', 'p': ['便民服务站']},
    {'col': '公共设施配套_社区服务中心', 'p': ['社区服务站', '社区服务']},
    {'col': '公共设施配套_社区警务室', 'p': ['警务室']},
    {'col': '公共配套设施_党群服务中心', 'p':['党群服务中心']},

    {'col': '公共设施配套_文体活动', 'p': ['文体活动', '文体活动站', '文体活动室', '文体设施']},
    {'col': '公共设施配套_文化活动', 'p': ['文化活动站', '文化活动室', '文化室', '文化娱乐', '文化站', '文化', '文化活动', '文化设施']},
    {'col': '公共设施配套_体育活动', 'p': ['社区体育活动', '社区运动', '体育活动室', '体育室', '体育', '体育设施', '体育活动结合屋顶设置']},
    {'col': '公共设施配套_社区健康', 'p': ['社区健康服务', '社康', '康体', '康复']},
    {'col': '公共设施配套_日间照料中心', 'p': ['照料', '照料服务', '照料中心']},
    {'col': '公共设施配套_老年活动', 'p': ['老年活动', '老年活动室']},
    {'col': '公共设施配套_菜市场', 'p': ['菜市场']},

    {'col': '公共配套设施_垃圾站', 'p': ['垃圾站', '垃圾收集站', '垃圾收集点', '垃圾处理站', '垃圾转运站']},
    {'col': '公共配套设施_再生资源回收点', 'p': ['再生资源回收点', '再生资源回收站']},
    {'col': '公共配套设施_公厕', 'p': ['公厕', '厕所']},
    {'col': '公共配套设施_污水处理站', 'p': ['污水处理站']},
    {'col': '公共配套设施_公交场站', 'p': ['公交场站', '公交站场', '公交站', '换乘站', '公交首末站']},
    {'col': '公共配套设施_公交配套', 'p': ['公交运营', '公交配套']},
    {'col': '公共配套设施_综合车站', 'p': ['综合车站']},
    {'col': '公共配套设施_自行车停靠点', 'p': ['自行车停靠点']},
    {'col': '公共配套设施_充电站', 'p': ['充电站','充电桩']},
    {'col': '公共配套设施_邮政', 'p': ['邮政局','邮政所', '邮电设施', '邮政']},
    {'col': '公共配套设施_消防', 'p':['消防', '消防站', '消防设施']},
    {'col': '公共配套设施_变电站', 'p':['变电站']},
    {'col': '公共配套设施_环卫工人休息站', 'p':['休息站', '休息房', '作息站', '作息房']},
    {'col': '公共配套设施_机房', 'p':['机房', '通信机房']},
    {'col': '公共配套设施_公共配套用房', 'p':['公共配套用房']},
    
]

dict_edu = [
    {'col': '', 'p': []}
]

dict_other = [
    {'col': '其他_停车场', 'p': ['停车场', '停车库']},
    {'col': '其他_地下停车场', 'p':['地下停车场', '地下车库']},
    {'col': '其他_公共停车位', 'p':['公共停车位']},
    {'col': '其他_配电装置', 'p':['配电装置']},
    {'col': '其他_机房', 'p':['机房']},
    {'col': '其他_物业', 'p':['物管', '物业服务', '物业', '物业管理', '物业服务办公']}  # 放在办公之前
    
]

# 特殊处理，不进入循环，仅列出
dict_num = [
    {'col': '公共设施配套_幼儿园_地面', 'p': ['独立']},  
    {'col': '公共停车位（个）', 'p':['公共停车位']},
    {'col': '公共设施配套_幼儿园_班数', 'p': ['班']},  
    
]

# ### 定义匹配模式

# In[61]:
class Buliding:
    def __init__(self, df, con):
        self.re_list = []
        self.con = con
        self.df = df
        
    def get_num(self, j, pattern, con, ty):
        list_sum = 0
        pt = re.findall(re.compile(pattern), con)
        if pt:
            num = 0
            for k in range(0, len(pt)):
                num = num + float(pt[k][0])
                self.re_list.append(j + "".join(pt[k]))
                if ty==1:
                    self.con = self.con.replace(j + "".join(pt[k]), '', 1) 
                if ty==2:
                    self.con = self.con.replace("".join(pt[k])+ '的'+j,'', 1)
                if ty==3: 
                    self.con = self.con.replace("".join(pt[k]),'', 1)
            list_sum = list_sum + num
        return list_sum
            
    def get_df_num(self, dict_all, pub):
        
        # 先处理特殊情况
        child_tu = 0
        child_ban = 0
        child_jian = 0
        car_num = 0
        sp = re.split('[,，。、；]', self.con)
        if sp:
            for s in sp:
                if "幼儿园" in s:
                    child_tu = child_tu + self.get_num('独立', '独立'+ pub_area, s, 1)
                    child_ban = child_ban + self.get_num('', pub_ban, s, 1)
                    child_jian = child_jian + self.get_num('幼儿园', pub_area, s, 1)
                if "公共停车位" in s:
                    car_num = car_num + self.get_num('', pub_ge, s, 1)
        self.df.at[index, '公共设施配套_幼儿园-建面'] = child_jian
        self.df.at[index, '公共设施配套_幼儿园-地面'] = child_tu
        self.df.at[index, '公共设施配套_幼儿园-班数'] = child_ban
        self.df.at[index, '公共设施配套_公共停车位'] = car_num                
        
        # 循环处理各类型用地
        
        for i in dict_all:
            list_sum = 0
            for j in i['p']:
                pattern1 = j + pub
                pattern2 = pub + '的' + j
                list_sum = list_sum + self.get_num(j, pattern1, self.con, 1) + self.get_num(j, pattern2, self.con, 2)
            self.df.at[index, i['col']] = list_sum
            
        # 第二轮提取，拆句
        st = re.split('[,，。、；]', self.con)
        for s in st:
            pub_str = re.findall(re.compile(pub_area), s)   # 判断是否含有数字
            if pub_str:
                if len(pub_str) == 1:
                    for i in dict_all:
                        list_sum = 0
                        for j in i['p']:
                            if j in s: 
                                list_sum = list_sum + self.get_num(j, pub, s, 3)

                        self.df.at[index, i['col']] = self.df.at[index, i['col']] + list_sum
            
        st_remain = re.split('[,，。、；]', self.con)
        st_re = []
        for s in st_remain:
            pub_str = re.findall(re.compile(pub_area), s)   # 判断是否含有数字
            if pub_str:
                st_re.append(s)

        self.df.at[index, 'remain'] = '，'.join(st_re)
        
            
pub_area = '共?(\d+(\.\d+)?)(平方|平方米|平米|㎡)' 
pub_ge = '(\d+(\.\d+)?)(个)'
pub_ban = '(\d+(\.\d+)?)(班)'

dict_all = dict_peitao + dict_ind + dict_other + dict_com + dict_pub

replace_list = [
        ' ', '\n', '\r', '≤', '≥', ':', '：', '【', '】', 
        '面积', '用房', '中心', '不少于', '不小于','不超过', '总计',  '总', '场地', '用地', 
        '建筑', '业务', '楼', '大楼', '占地，', '占地', '1处',
    ]

for index, rows in df.iterrows():
    c = str(rows['建筑面积说明'])
    c = re.sub(r'（\D+）', '', c)  
    for m in replace_list:
        c = c.replace(m, '')
    buliding = Buliding(df, c)
    buliding.get_df_num(dict_all, pub_area)

# ### 执行

# In[18]:
from datetime import datetime
df.to_excel('D:\workspace\建筑面积解析-{}.xlsx'.format(str(datetime.today())[0:13]))




# In[41]:


# df2 = df[df.PARCEL_NO=='G04310-0032']
# df2


# In[6]:


pd.DataFrame.to_excel(df, 'D:\GIS\深圳专题\workspace\数据11-12月-解析.xlsx')


# In[9]:


df.drop(['YDMJ','JZMJ', 'HT_DLMC', 'GB_DLMC', '建筑面积说明'], axis=1, inplace=True)


# In[10]:


df_c = pd.merge(df_all, df, on='PARCEL_NO', how='left')
pd.DataFrame.to_excel(df_c, 'D:\GIS\深圳专题\workspace\数据11-12月-含解析.xlsx', index=None)

