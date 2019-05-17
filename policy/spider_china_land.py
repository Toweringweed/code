#%%
import random
import re
import time
from personal.mysqldb import ToMysql
from datetime import datetime
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

kwargs = {  'host':'localhost',
            'user':'root',
            'passwd':'luoxue99',
            'db':'china_land',
            'charset':'utf8'}

sql = ToMysql(kwargs)
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
browser = webdriver.Chrome(r'd:/code/policy/chromedriver.exe')
# browser = webdriver.Ie(r'C:/Program Files/Internet Explorer/IEDriverServer.exe')
# browser.maximize_window()
browser.get('http://www.landchina.com/default.aspx?tabid=262') 
  

#%%
def page_parser(html, content, url):
    # html_s1 = html.xpath('//table[@id="Table2"]//table')[0]
    # html_s2 = etree.tostring(html_s1, encoding='utf-8').decode('utf-8')
    pid = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    title = html.xpath('//span[@id="lblTitle"]/text()')
    date_out = html.xpath('//span[@id="lblCreateDate"]/text()')
    loc_full = html.xpath('//span[@id="lblXzq"]/text()')
    loc_full = loc_full[0] if loc_full else ''
    loc_list = loc_full.replace(' ', '').split('>') if '>' in loc_full else None
    province = city = xian = ''
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    open_during = html.xpath('//*[contains(text(), "公示期")]/u//text()')
    if loc_list:
        province = loc_list[0].replace('行政区：', '') if loc_list else ''
        city = loc_list[1] if len(loc_list)>1 else ''
        xian = loc_list[2] if len(loc_list)>2 else ''
    
    result_pub = {
        'title': title[0] if title else '',
        'pid': pid,
        'region': loc_full,
        'date_out': date_out[0].replace('发布时间：', '') if date_out else '',
        'province': province,
        'city': city,
        'xian': xian,
        'content': content,
        'open_during': open_during[0] if open_during else '',
        'url': url,
        'update_time': time_now

    }
    sql.into('public', **result_pub)
    table_str = '//*[@id="tdContent"]/table//table'
    table_num = html.xpath(table_str)
    insert_num = 0
    for i in range(1, len(table_num)+1):
        table_pre = table_str + str([i]) + '/tbody/tr'
        zongdi = html.xpath(table_pre + '/td[contains(text(), "编号")]/following-sibling::*[1]/text()')
        if zongdi != zongdi:
            spider_log = open(r'd:/code/spider_log.txt', 'w')
            print(date_out, ',', title, file=spider_log)
        address = html.xpath(table_pre + '/td[contains(text(), "位置")]/following-sibling::*[1]/text()')
        useness = html.xpath(table_pre + '/td[contains(text(), "用途")]/following-sibling::*[1]/text()')
        area = html.xpath(table_pre + '/td[contains(text(), "面积")]/following-sibling::*[1]/text()')
        project = html.xpath(table_pre + '/td[contains(text(), "项目名称")]/following-sibling::*[1]/text()')
        receiver = html.xpath(table_pre + '/td[contains(text(), "受让单位")]/following-sibling::*[1]/text()')
        years = html.xpath(table_pre + '/td[contains(text(), "出让年限")]/following-sibling::*[1]/text()')
        price = html.xpath(table_pre + '/td[contains(text(), "成交价")]/following-sibling::*[1]/text()')
        tiaojian = html.xpath(table_pre + '/td[contains(text(), "出让条件")]/following-sibling::*[1]/text()')
        result_zongdi = {
            'pid': pid,
            'date_out': date_out[0].replace('发布时间：', '') if date_out else '',
            'zongdi': zongdi[0] if zongdi else '',
            'region': loc_full,
            'province': province,
            'city': city,
            'xian': xian,
            'project': project[0] if project else '',
            'address': address[0] if address else '',
            'useness': useness[0] if useness else '',
            'area': area[0] if area else '',
            'years': years[0] if years else '',
            'price': price[0] if price else '',
            'receiver': receiver[0] if receiver else '',
            'tiaojian': tiaojian[0] if tiaojian else '',
            'update_time': time_now
        }
        
        sql.into('zongdi', **result_zongdi)
        insert_num = insert_num + 1

# 开始执行

browser.switch_to.window(browser.window_handles[0]) 
browser.implicitly_wait(30)
# for i in range(8):
#     page_next = browser.find_element_by_link_text('下页')
#     if page_next:
#         page_next.click()
#     time.sleep(random.uniform(1))
    
page_num_str = browser.find_element_by_xpath('//*[@id="mainModuleContainer_478_1112_1537_tdExtendProContainer"]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]').text
page_num_pa = re.findall(re.compile('共(\d+)页'), page_num_str)
if page_num_pa:
    page_num = page_num_pa[0]
    for i in range(int(page_num)+1):
        print('已插入页面：' + str(i+1))
        links = browser.find_elements_by_xpath('//table[@id="TAB_contentTable"]//tr/td[3]/a')
        for link in links:
            link.click()
            browser.switch_to.window(browser.window_handles[-1])
            browser.implicitly_wait(30)
            url = browser.current_url
            content = browser.find_element_by_xpath('//table[@id="Table2"]//table').text
            data = browser.page_source
            html = etree.HTML(data)
            page_parser(html, content, url)
            browser.close()
            browser.switch_to.window(browser.window_handles[0]) 
            time.sleep(random.uniform(10,30))    
        page_next = browser.find_element_by_link_text('下页')
        if page_next:
            page_next.click()
        else:
            browser.refresh()
        browser.implicitly_wait(30)
