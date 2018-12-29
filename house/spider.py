
import random
import re
import time
from personal.mysqldb import ToMysql

import requests
from lxml import etree
from selenium import webdriver

kwargs = {  'host':'localhost',
            'user':'root',
            'passwd':'luoxue99',
            'db':'house',
            'charset':'utf8'}

sql = ToMysql(kwargs)

def crawl_page(pici):
    browser = webdriver.Chrome(r'chromedriver.exe')
    browser.get('http://sz.esf.fang.com/')
    
    # browser.find_element_by_name('').send_keys('')
#     data = browser.page_source
#     html = etree.HTML(data)
    area_urls = []
    
    for i in browser.find_elements_by_xpath('//li[@id="kesfqbfylb_A01_03_01"]/ul/li/a'):
        area_urls.append(i.get_attribute('href'))

    print('-- start %s --' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print('-- 抓取一级目录链接数量：%s --' % len(area_urls))
    k = 1
    for url in area_urls:
        print(url)
        browser.get(url)
        data = browser.page_source
        html = etree.HTML(data)
        total_page_text = html.xpath('//div[@id="list_D10_15"]/p[3]/text()')
        total_page = re.findall(re.compile(r'共(\d+)页'), total_page_text[0]) if total_page_text else [0]
        total_page = int(total_page[0]) if total_page else 0
        print(total_page)
        for i in range(1, total_page):
            current_url = url + '/i3' + str(i)
            browser.get(current_url)
            print(url + '/i3' + str(i))
            time.sleep(random.uniform(5,10))
            data = browser.page_source
            html = etree.HTML(data)
            jiexi(html, pici, k)
            k = k + 1
            print('共插入頁面' + str(k) + ' -- ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))    

    browser.quit()

def clean(obj):
    
    return [i.replace(' ', '').replace('\n', '') for i in obj]

def jiexi(html, pici, k):
    print('-- 开始解析 --')
    title = html.xpath('//span[@class="tit_shop"]/text()')
    urls = html.xpath('//h4/a/@href')
    uids = []
    for i in urls:
        uid = re.findall(re.compile(r'chushou/(.*?).htm'), i)
        uid = uid[0] if uid else ''
        uids.append(uid)
    print(len(uids))    
    mianji = html.xpath('//p[@class="tel_shop"]/text()[2]'), 
    mianji = mianji[0] if mianji else ''
    mj = clean(mianji)
    huxing = html.xpath('//p[@class="tel_shop"]/text()[1]')
    hx = clean(huxing)
    cengji = html.xpath('//p[@class="tel_shop"]/text()[3]')
    cj = clean(cengji)
    chaoxiang = html.xpath('//p[@class="tel_shop"]/text()[4]')
    cx = clean(chaoxiang)
    jianzhuniandai = html.xpath('//p[@class="tel_shop"]/text()[5]')
    jznd = clean(jianzhuniandai)
    xiaoqu = html.xpath('//p[@class="add_shop"]/a/text()')
    xq = clean(xiaoqu)
    jiedao = html.xpath('//p[@class="add_shop"]/span/text()')
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    date_time = [time_now]*len(uids) 
    result = {
        'pici': [pici] * len(uids),
        'k': [k] * len(uids),
        'title': title,
        'uid': uids,
        'zongjia': html.xpath('//dd[@class="price_right"]//span//b/text()'),
        'price_i': html.xpath('//dd[@class="price_right"]//span[2]/text()'),
        'mianji': mj,
        'huxing': hx,
        'cengji': cj,
        'chaoxiang':cx, 
        'jianzhuniandai': jznd, 
        'xiaoqu': xq,
        'jiedao': jiedao,
        'date_time': date_time,
    }

    print('-- 插入数据库 --' )

    sql.into_many('basis', **result)
   

if __name__ == "__main__":
        for pici in range(10, 9999):
            crawl_page(pici)
            time.sleep(random.uniform(60*60*24,60*60*30))
