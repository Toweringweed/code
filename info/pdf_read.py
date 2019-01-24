# -*- encoding: utf-8 -*-

# from personal.mysqldb import ToMysql
import sys
import numpy as np
from personal.getFile import GetFile
import os

from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.pdfdevice import PDFDevice
from urllib.request import urlopen
from io import StringIO
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')



def pdf_read(file):
    #创建一个一个与文档关联的解释器
    parser = PDFParser(file)
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

f = open('d:\工作\土地法规政策\【2018.7】深圳市人民政府《关于完善国有土地供应管理的若干意见》（深府规〔2018〕11 号）.pdf', 'rb')

if __name__ == "__main__":
    pdf_read(f)