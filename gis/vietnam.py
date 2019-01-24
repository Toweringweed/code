#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#%%
from lxml import etree
import pandas as pd
import re

tree = etree.parse(r'D:\GIS\Vietnam\Quê-quán-lịch-triều-tiến-sĩ-1 (1).kml')
# tree = etree.parse(r'D:\GIS\Vietnam\test.xml')
root = tree.getroot()
print(root)
name = root.findall(".//Placemark/name")
name_text = [i.text for i in name]
coor = root.findall(".//Placemark//coordinates")
coor = [i.text.replace('\n', '').replace(' ', '') for i in coor]
df = pd.DataFrame()
df['name'] = name_text
df['coordinates'] = coor
print(df)

df.to_excel('d:/vieenam.xlsx')
#%%
