#%%
import requests
import re

# 批量获取地址经纬度
basic_url = 'http://api.map.baidu.com/geocoder/v2/'

address_list = [
    '北京市海淀区上地十街10号',
    '深圳市福田区景田东路36号景丽花园'
]

jw = []
for a in address_list:
    d= {
        "address": a,
        "output": 'json',
        "ak": '8iXegYGpk2XxxWP7gyNlcblB6vnO31qf',
        "callback": 'showLocation',
    }
    result = requests.get(basic_url, params=d).text
    result_json = re.findall(re.compile(r'showLocation\((.*?)\)'), result)
    jw.extend(result_json)
print(jw)

