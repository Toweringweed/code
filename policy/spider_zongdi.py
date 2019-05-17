#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataSciece.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'policy'))
	print(os.getcwd())
except:
	pass

#%%
import re
import time
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import pandas as pd


browser = webdriver.Chrome(r'chromedriver.exe')
# browser = webdriver.Ie(r'C:/Program Files/Internet Explorer/IEDriverServer.exe')
browser.maximize_window()
browser.get('http://www.szpl.gov/')    
frame = browser.find_element_by_xpath('/html/body/div[2]/div[4]/div[4]/div[1]/div[2]/table/tbody/tr[1]/td/iframe')
browser.switch_to.frame(frame)

# 登陆

browser.find_element_by_name('username').send_keys('weixw')
time.sleep(1)
browser.find_element_by_name('password').send_keys('Wei#1202')
time.sleep(1)
browser.find_element_by_id('btnlogin').click()

all_handles = browser.window_handles
print(all_handles)

browser.switch_to.window(all_handles[-1])

print(browser.current_window_handle)
browser.implicitly_wait(10)

print(browser.title)


#%%
menu = browser.find_element_by_id('menu_10345658')

action = ActionChains(browser)
action.move_to_element(menu).perform()
guodu = browser.find_element_by_link_text('法定图则制定')
action.move_to_element(guodu).perform
browser.find_element_by_link_text('地政管理').click()
print(browser.title)
a2 = browser.window_handles  # 获取窗口
browser.switch_to.window(a2[-1])  # 切换到最后一个窗口
print(browser.title)  # 打印窗口标题
browser.find_element_by_id('td5').click()  # 点击批约管理按钮
browser.implicitly_wait(15)


#%%
zongdi = pd.read_excel(r'E:\python\宗地_new.xlsx')
# # zongdi_2 = zongdi[zongdi['context'] != zongdi['context']]
zongdi_list = zongdi['PARCEL_NO'].tolist()


#%%
a2 = browser.window_handles  # 获取窗口
browser.switch_to.window(a2[-1])  # 切换到最后一个窗口
data = []
for i in zongdi_list:
    print(i)
    browser.switch_to.frame('Main')
    browser.switch_to.frame('xChildMain')
    browser.find_element_by_name('_PARCEL_NO1').clear()
    browser.find_element_by_name('_PARCEL_NO1').send_keys(i)
    browser.find_element_by_xpath('//*[@id="diva"]/input[1]').click()
    browser.implicitly_wait(15)
    browser.switch_to.frame('ChildMain')
    jj = browser.find_elements_by_xpath('//table[@class="tableCss"]//tr[td[2][contains(text(), "合")]]/td[9]/a')
#     jj2 = browser.find_elements_by_xpath('//table[@class="tableCss"]//tr[td[3][contains(text(), "划拨")]]/td[9]/a')
#     jj3 = browser.find_elements_by_xpath('//table[@class="tableCss"]//tr[td[3][contains(text(), "租赁")]]/td[9]/a')
#     jj = jj1 + jj2 + jj3
    context_list = []
    if jj:
        for j in jj:
            j.click()
            browser.implicitly_wait(15)
            browser.switch_to.window(browser.window_handles[-1])
            browser.find_element_by_id('3Num').click()
            browser.implicitly_wait(15)
            browser.switch_to_frame('test')
            context = browser.find_element_by_name('PR_REMARK').text    # 建筑面积说明
            context_list.append(context)
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            browser.switch_to.frame('Main')
            browser.switch_to.frame('xChildMain')
            browser.switch_to.frame('ChildMain')
        context_all = '///'.join(context_list)
        data_i = [i, context_all]
    else:
        data_i = [i, '无']
    data.append(data_i)
    browser.switch_to_default_content()
    df = pd.DataFrame(data=data, columns=['zongdi', 'context'])

    df.to_excel("e:/python/ss3.xlsx")
# # zongdi_list = zongdi_2['PARCEL_NO'].tolist()


