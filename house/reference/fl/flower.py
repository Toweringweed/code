# _*_ coding:utf-8 _*_
from lxml import etree
# from bs4 import BeautifulSoup
import time
from selenium import webdriver
import MySQLdb
import urllib.request
def hua():
    browser = webdriver.Chrome(r'chromedriver.exe')
    browser.get('http://www.brightenflower.cn')
    time.sleep(2)
    browser.find_element_by_name("yyid").send_keys("9996")
    time.sleep(3)
    browser.find_element_by_name("yyxx").send_keys("123456")
    time.sleep(3.5)
    key = input("输入验证码：")
    browser.find_element_by_name("yzms").send_keys(key)
    time.sleep(3.4)
    browser.find_element_by_xpath('//input[@class="button"]').click()
    time.sleep(11)
    browser.find_element_by_xpath('//div[@id="divSite"]//tr//td[1]//input').click()
    time.sleep(4.3)
    browser.find_element_by_xpath('//div//table//table//table//td[4]//a').click()
    # 解析需求数据
    for x in range(310):
        print(x)
        if x == 0:
            time.sleep(3.5)
            browser.find_element_by_xpath('//div[@align="center"]//a[1]').click()
            data = browser.page_source
            html = etree.HTML(data)
            jiexi(html)
            time.sleep(1.2)
        else:
            time.sleep(3.5)
            browser.find_element_by_xpath('//div[@align="center"]//a[3]').click()
            data = browser.page_source
            html = etree.HTML(data)
            jiexi(html)
            time.sleep(1.2)
    # time.sleep(100)
# 解析函数
def jiexi(html):
    uid = html.xpath('//div[@id="divInfo"]//td[2]/text()')
    uid.remove("编码")
    uids = []
    for ui in uid:
        dicts = {}
        dicts["id"] = int(ui)
        uids.append(dicts)
    name = html.xpath('//div[@id="divInfo"]//td[3]/text()')
    name.remove("品名")
    nam = []
    for na in name:
        dicts = {}
        dicts["name"] = na.replace('\xa0', '')
        nam.append(dicts)
    # print(len(nam),nam)
    colour = html.xpath('//div[@id="divInfo"]//td[4]/text()')
    colour.remove("颜色")
    col = []
    for co in colour:
        dicts = {}
        dicts["colour"] = co
        col.append(dicts)
    length = html.xpath('//div[@id="divInfo"]//td[5]')
    lengt = []
    for l in range(len(length)):
        lenth = html.xpath('//div[@id="divInfo"]//td[5]')[l].text
        lengt.append(lenth)
    lengt.remove("长度")
    leng = []
    for le in lengt:
        dicts = {}
        dicts["lenght"] = le
        leng.append(dicts)
    baozhuang = html.xpath('//div[@id="divInfo"]//td[6]/text()')
    baozhuang.remove("包装")
    bao = []
    for ba in baozhuang:
        dicts = {}
        dicts["baozhuang"] = ba
        bao.append(dicts)
    danjia = html.xpath('//div[@id="divInfo"]//td[7]/text()')
    danjia.remove("单价")
    dan = []
    for da in danjia:
        dicts = {}
        dicts["danjia"] = da
        dan.append(dicts)
    dijia = html.xpath('//div[@id="divInfo"]//td[11]')
    lis = []
    for y in range(len(dijia)):
        diji = html.xpath('//div[@id="divInfo"]//td[11]')[y].text
        lis.append(diji)
    di = []
    lis.remove("底价")
    for dij in lis:
        dicts = {}
        dicts["dijia"] = dij
        di.append(dicts)

    img_url = html.xpath('//div[@id="divInfo"]//td[1]//img/@onmousedown')
    img_name = []
    for img in img_url:
        try:
            time.sleep(2.3)
            imgs = img.replace("showPic", "")
            name = imgs[2:-4].replace("'", "")
            # 图片保存在本地
            names = "http://www.brightenflower.cn/PicPath/" + name
            # print(names)
            f = open(r"F:/flower/img/" + name, "wb")
            f.write(urllib.request.urlopen(names).read())
            f.close()
            dicts = {}
            dicts["url"] = names
            img_name.append(dicts)
        except Exception as e:
            print(e)
    i = 0
    while i < len(uids):
        try:
            dic = uids[i].update(nam[i])
            dic = uids[i].update(col[i])
            dic = uids[i].update(leng[i])
            dic = uids[i].update(bao[i])
            dic = uids[i].update(dan[i])
            dic = uids[i].update(di[i])
            dic = uids[i].update(img_name[i])
            items = uids[i]
        except Exception as e:
            print(e)
        try:
            print('连接sql')
            mysqlcli = MySQLdb.connect(host="192.168.1.4", user="root", db="public_opinion", port=3306,
                                       passwd="123456", charset="utf8")
            # mysqlcli = MySQLdb.connect(host="127.0.0.1", user="root", db="hoomsun", port=3306, passwd="123456",charset="utf8")
        except Exception as e:
            print('连接错误!')
            print(str(e))
        try:
        # 使用cursor 创建游标
            cur = mysqlcli.cursor()
            # sql 语句
            sql = "insert into flower(flower_number,flower_name,flower_colour,flower_lenght,packing,univalent,floor,img_url) values('%d','%s','%s','%s','%s','%s','%s','%s') on duplicate key update " \
                  "flower_number=values(flower_number),flower_name=values(flower_name),flower_colour=values(flower_colour),flower_lenght=values(flower_lenght),packing=values(packing),univalent=values(univalent),floor=values(floor),img_url=values(img_url)" % (
                  items['id'], items['name'], items['colour'], items['lenght'], items['baozhuang'], items['danjia'], items['dijia'], items['url'])
            # # 执行sql语句
            cur.execute(sql)
            print(cur.execute(sql))
            # 提交sql事五
            mysqlcli.commit()
            # 关闭本次操作
            cur.close()
            print('flower 插入完成!')
        except Exception as e:
            print('插入失败！')
            print(str(e))
        i += 1
    ye = html.xpath('//div[@align="center"]//a/text()')
    return ye
if __name__ == "__main__":
    hua()