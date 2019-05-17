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
data = []
browser.switch_to.frame('Main')
browser.switch_to.frame('xChildMain')
browser.switch_to.frame('ChildMain')


#%%
# 向后翻页
browser.implicitly_wait(15)
for m in range(39):
    ylink = browser.find_element_by_link_text('下 页')
    if ylink:
        ylink.click()
        browser.implicitly_wait(15)


#%%
# 向前翻页
a2 = browser.window_handles  # 获取窗口
browser.switch_to.window(a2[-1])  # 切换到最后一个窗口
browser.switch_to.frame('Main')
browser.switch_to.frame('xChildMain')
browser.switch_to.frame('ChildMain')
browser.implicitly_wait(15)
for m in range(40):
    plink = browser.find_element_by_link_text('上 页')
    if plink:
        plink.click()
        browser.implicitly_wait(15)


#%%
a2 = browser.window_handles  # 获取窗口
browser.switch_to.window(a2[-1])  # 切换到最后一个窗口
browser.switch_to.frame('Main')
browser.switch_to.frame('xChildMain')
browser.switch_to.frame('ChildMain')
content_list = []
browser.implicitly_wait(15)
for j in range(2461):
    for i in range(2,17):
        c1 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[1]').text
        c2 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[2]').text
        c3 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[3]').text
        c4 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[4]').text
        c5 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[5]').text
        c6 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[6]').text
        c7 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[7]').text
        c8 = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[8]').text

        jlink = browser.find_element_by_xpath('//table[@class="tableCss"]//tr[' + str(i) +']/td[9]/a')
        if jlink:
            jlink.click()
            browser.implicitly_wait(15)
            browser.switch_to.window(browser.window_handles[-1])
            browser.implicitly_wait(15)
            if c2 != "函":
                if c2 == "划拨":
                    browser.switch_to.frame('test')
                    a1 = browser.find_element_by_name('LU_AREA').get_attribute('value')
                    a2 = a3 = a4 = a8 = a9= ''
                    a6 = browser.find_element_by_name('OPEN_DATE').get_attribute('value')
                    a7 = browser.find_element_by_name('COMPLETE_DATE').get_attribute('value')

                    cc1 = browser.find_element_by_name('PR_AREA').text
                    cc2 = cc4 = cc7 = ''
                    cc3 = browser.find_element_by_name('PLOT_RATIO').get_attribute('value')
                    cc5 = browser.find_element_by_name('PR_REMARK').get_attribute('value')
                    cc6 = browser.find_element_by_name('OTHERS').text
                else:
                    browser.switch_to.frame('test')
                    a1 = browser.find_element_by_name('LU_AREA').get_attribute('value')
                    a2 = ''
                    a3 = browser.find_element_by_name('LU_FUNCTION').get_attribute('value')
                    a4 = browser.find_element_by_name('LU_TERM').get_attribute('value')
                    a6 = browser.find_element_by_name('OPEN_DATE').get_attribute('value')
                    a7 = browser.find_element_by_name('COMPLETE_DATE').get_attribute('value')
                    a8 = browser.find_element_by_name('LP_LU_PROJ_NAME').get_attribute('value')
                    a9 = browser.find_element_by_name('NO_REDLINE_REASON').get_attribute('value')
                    browser.switch_to.default_content()
                    browser.find_element_by_id('3Num').click()
                    browser.implicitly_wait(15)
                    browser.switch_to.frame('test')
                    cc1 = browser.find_element_by_name('PR_REMARK').text    # 建筑面积说明
                    cc2 = browser.find_element_by_name('COVERAGE').get_attribute('value')  # 建筑覆盖率
                    cc3 = browser.find_element_by_name('PLOT_RATIO').get_attribute('value')  # 容积率
                    cc4 = browser.find_element_by_name('BLDG_HEIGHT').get_attribute('value') # 建筑层数
                    cc5 = browser.find_element_by_name('PR_AREA').get_attribute('value') # 建筑面积
                    cc6 = browser.find_element_by_name('SETBACK').text # 退红线要求
                    cc7 = browser.find_element_by_name('MAIN_BLDG').text # 主体建筑物性质
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            browser.switch_to.frame('Main')
            browser.switch_to.frame('xChildMain')
            browser.switch_to.frame('ChildMain')

        content_list.append([c1, c2, c3, c4, c5, c6, c7, c8, a1, a2, a3, a4, a6, a7, a8,a9, cc1, cc2, cc3, cc4, cc5, cc6, cc7])
        df = pd.DataFrame(data=content_list, columns=['合同号', '合同字号', '供应方式', '宗地代码', '宗地号','出让方名称', '土地用途', '签订日期', 
                                                      '用地面积', '土地性质', '土地用途', '使用年限', '开工日期', '竣工日期', '用地项目名称', 
                                                      '无用地方案原因',
                                                      '建筑面积说明', '建筑覆盖率', '容积率', '建筑层数', '建筑面积', '退红线要求', '主体建筑物性质'])
        df.to_excel("e:/python/all49.xlsx")
    ylink = browser.find_element_by_link_text('下 页')
    if ylink:
        ylink.click()


