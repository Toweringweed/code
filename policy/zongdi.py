
import re
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import pandas as pd



# kwargs = {  'host':'localhost',
#             'user':'root',
#             'passwd':'luoxue99',
#             'db':'house',
#             'charset':'utf8'}

# sql = ToMysql(kwargs)

def crawl_page(pici, zongdi_list):
    browser = webdriver.Chrome(r'chromedriver.exe')
    # browser = webdriver.Ie(r'C:/Program Files/Internet Explorer/IEDriverServer.exe')
    browser.maximize_window()
    browser.get('http://www.szpl.gov/')    
    frame = browser.find_element_by_xpath('/html/body/div[2]/div[4]/div[4]/div[1]/div[2]/table/tbody/tr[1]/td/iframe')
    browser.switch_to_frame(frame)
    # browser.get('http://zwpt.szpl.gov/login_iframe.jsp')
    
    # 登陆

    browser.find_element_by_name('username').send_keys('weixw')
    time.sleep(1)
    browser.find_element_by_name('password').send_keys('Wei#1202')
    time.sleep(1)
    browser.find_element_by_id('btnlogin').click()

    all_handles = browser.window_handles
    print(all_handles)

    browser.switch_to_window(all_handles[-1])

    print(browser.current_window_handle)
    browser.implicitly_wait(10)

    print(browser.title)
   
    menu = browser.find_element_by_id('menu_10345658')

    action = ActionChains(browser)
    action.move_to_element(menu).perform()
    guodu = browser.find_element_by_link_text('法定图则制定')
    action.move_to_element(guodu).perform
    browser.find_element_by_link_text('地政管理').click()
    print(browser.title)
    a2 = browser.window_handles
    browser.switch_to_window(a2[-1])
    print(browser.title)
    browser.find_element_by_id('td5').click()
    browser.implicitly_wait(15)
    data = []
    for i in zongdi_list:
        print(i)
        browser.switch_to_frame('Main')
        browser.switch_to_frame('xChildMain')
        browser.find_element_by_name('_PARCEL_NO1').clear()
        browser.find_element_by_name('_PARCEL_NO1').send_keys(i)
        browser.find_element_by_xpath('//*[@id="diva"]/input[1]').click()
        browser.implicitly_wait(15)
        browser.switch_to_frame('ChildMain')
        jj = browser.find_elements_by_xpath('//table[@class="tableCss"]//tr[td[2][contains(text(), "合")]]/td[9]/a')
        context_list = []
        if jj:
            for j in jj:
                j.click()
                browser.implicitly_wait(15)
                browser.switch_to_window(browser.window_handles[-1])
                browser.find_element_by_id('3Num').click()
                browser.implicitly_wait(15)
                browser.switch_to_frame('test')
                context = browser.find_element_by_name('PR_REMARK').text
                context_list.append(context)
                browser.close()
                browser.switch_to_window(browser.window_handles[-1])
                browser.switch_to_frame('Main')
                browser.switch_to_frame('xChildMain')
                browser.switch_to_frame('ChildMain')
                
            context_all = '///'.join(context_list)
            print(context_all)
            data_i = [i, context_all]
        else:
            data_i = [i, '无']
        data.append(data_i)
        browser.switch_to_default_content()
        print(data)
        df = pd.DataFrame(data=data, columns=['zongdi', 'context'])
        print(df)
        df.to_excel("e:/python/ss4.xlsx")
# zongdi_list = zongdi_2['PARCEL_NO'].tolist()

zongdi = pd.read_excel(r'E:/python/zongdi.xlsx')

# zongdi_2 = zongdi[zongdi['context'] != zongdi['context']]
zongdi_list = zongdi['PARCEL_NO'].tolist()

if __name__ == "__main__":
        # for pici in range(2, 9999):
        crawl_page(1, zongdi_list)
            # time.sleep(random.uniform(60*60*24,60*60*30))



