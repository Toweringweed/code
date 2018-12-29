# -*- encoding: utf-8 -*-

from personal.mysqldb import ToMysql
import sys
import numpy as np
from personal.getFile import GetFile
import os


# try:
#     conn = MySQLdb.connect('localhost', 'root', 'luoxue99')
#     cur = conn.cursor()
#     cur.execute('create database if not exists python2')
#     conn.select_db('python2')
#     cur.execute('create table test(id int, info varchar(20))')

#     values = []
#     for i in range(1, 20):
#         values.append((i, 'info'+str(i)))
#         cur.executemany('insert into test values(%s,%s)', values)

#     conn.commit()
#     cur.close()
#     conn.close()

# except MySQLdb.Error, e:
#     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# s = GetFile(r'e:/gis').get_dir_list()

# print(s)

# ss = os.listdir('E:/gis')
# print(ss)

# import docx
# path = 'E:/工作/嘉瑜/【开标文件】0722-186FE2460SZB.docx'
# tt = docx.Document(path)
# for para in tt.paragraphs:
#     print(para.text)

# def load_file():
#     walk = os.walk('E:/工作')

# walk = os.walk('E:\工作')
# print(walk)
# for root, dirs, files in walk:
#     for name in files:
#         s = os.path.join(root, name)
#         print(s)

from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice

from urllib.request import urlopen
from io import StringIO

f = open('E:\工作\嘉瑜\【投标文件电子版】0722-186FE2460SZB-深圳市已批未建地数据清理、数据库建设及专项调查分析.pdf', 'rb')

# def readpdf(pdf_file):
#     resource = PDFResourceManager()
#     retstr = StringIO()
#     laparams = LAParams()
#     device = TextConverter(resource, retstr, laparams=laparams)
#     process_pdf(resource, device, pdf_file)
#     device.close()
#     content = retstr.getvalue()
#     retstr.close()
#     strs = content

#     return strs

# title = readpdf(f)
# print(title)

# f.close
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
  
#创建一个一个与文档关联的解释器
parser = PDFParser(f)

#PDF文档的对象
doc = PDFDocument()

#连接解释器和文档对象
parser.set_document(doc)
doc.set_parser(parser)

#初始化文档,当前文档没有密码，设为空字符串
doc.initialize("")

#创建PDF资源管理器
resource = PDFResourceManager()

#参数分析器
laparam = LAParams()

#创建一个聚合器
device = PDFPageAggregator(resource, laparams=laparam)

#创建PDF页面解释器
interpreter = PDFPageInterpreter(resource, device)

#使用文档对象得到页面的集合
for page in doc.get_pages():
    # 使用页面解释器读取
    interpreter.process_page(page)

    # 使用聚合器来获得内容
    layout = device.get_result()

    for out in layout:
        if hasattr(out, "get_text"):
            print(out.get_text())








