# -*- encoding: utf-8 -*-

import pandas as pd
import os
import requests
import re
import time
import threading
import os


proxy_list = []
checked_list = []

r1 = re.compile(r'data-title="IP">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,4}).*?匿名.*?匿.*?(HTTPS|HTTP)', re.DOTALL)
r3 = re.compile(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,4}).*?匿.*?(HTTPS|HTTP)', re.DOTALL)

class ProxyGet:
    def __init__(self):
        self.timeout = 5
        self.test_url = "https://www.douban.com"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.96 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
        }

    def get_proxy(self, sites, pattern):

        for site in sites:
            req = requests.get(site, headers=self.header)
            print('目标网站：' + site + "....." + str(req.status_code))
            page = req.text
            time.sleep(0.5)
            raw_ip = re.findall(pattern, page)
            if raw_ip:
                for row in raw_ip:
                    ip_i = row[2].lower() + "://" + row[0] + ":" + row[1]
                    proxy_list.append(ip_i)

        list_content = open(proxy_file, 'r').read().split('\n')
        list_ccc = list(set(list_content + proxy_list))
        print(list_ccc)
        proxy_ss = '\n'.join(list_ccc)
        list_file = open(proxy_file, 'w')
        list_file.write(proxy_ss)

    def check_proxy(self):
        list_content = open(proxy_file, 'r').read().split('\n')
        for adress in list_content:
            proxy_i = {"http": adress}

            try:
                res = requests.get(self.test_url, proxies=proxy_i,timeout=self.timeout, headers=self.header)
                print(adress + "检测代码" + "....." + str(res.status_code))
                time.sleep(0.1)

                if res.status_code == 200:
                    checked_list.append(adress)
                checked_ss = '\n'.join(checked_list)
                list_file = open(proxy_file, 'w')
                list_file.write(checked_ss)

            except Exception as e:
                print(e)

    # def set_squid(self):
    #     defaut_conf = open(r'C:\Squid\etc\squid\squid.confd','r').read()
    #     df = pd.read_csv(proxy_file, encoding='gbk', dtype='unicode')
    #     for index, row in df.iterrows():
    #         proxy_conf = "cache_peer " + str(row['ip_url']) + "parent " + str(row['ip_port']) + \
    #                      " 0 no-query weighted-round-robin weight=1connect-fail-limit=2 allow-miss max-conn=5 name=" + \
    #                      str(row['ip_url']) + "." + str(index) + "\n"
    #         defaut_conf = defaut_conf + proxy_conf
    #     defaut_conf = defaut_conf + "never_direct allow all"
    #     conf = open(r'C:\Squid\etc\squid\squid.conf', 'w')
    #     conf.write(defaut_conf)
    #     conf.close()
    #     print('写入成功！')

for j in range(999999):

    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    site1 = []
    proxy_file = r'E:/Mycarrer/proxy_list.txt'

    for i in range(1, 3):
        site = r'http://www.kuaidaili.com/proxylist/%d/' % i
        site1.append(site)

    site3 = []
    for i in range(1, 3):
        site = r'http://www.xicidaili.com/nn/%d/' % i
        site3.append(site)
    p1 = ProxyGet()
    p1.get_proxy(site1, r1)
    p1.get_proxy(site3, r3)
    p1.check_proxy()
    print(time_now, '  第' + str(j) + '次执行')
    print('.'*10 + "总共抓取了 %s 个代理" % len(proxy_list) + '.'*10)
    print('.' * 10 + "总共有 %s 个代理通过校验" % len(checked_list) +'.' * 10)
    print('-----------------')

    time.sleep(60*30)

