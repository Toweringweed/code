# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
    def __init__(self,baseUrl,seeLZ):
        self.baseURL=baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.File = None

    def getPage(self,pageNum):
        try:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None
    def getTitle(self,page):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>.*?',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents

    def getAllImg(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        content = re.findall(pattern,page)
        #从代码中提取图片
        patternImg = re.compile('<img class="BDE_Image".*?src="(.*?)"',re.S)
        images = re.findall(patternImg,content.group(1))
        return images

    def saveImgs(self,images,name):
        number = 1
        print u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1

    def saveImg(self,imageURL,fileName):
         u = urllib.urlopen(imageURL)
         data = u.read()
         f = open(fileName, 'wb')
         f.write(data)
         print u"保存图片为",fileName
         f.close()

    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False


    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle +".txt","w+")
    def writeData(self,contents):
        for item in contents:
            self.file.write(item)

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "Url已经失效"
            return
        try:
            print "该帖子共有"+str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
                images = self.getAllImg(page)
                self.mkdir(images)
        except IOError,e:
            print "写入异常，原因"+e.message
        finally:
            print "写入完成"




baseUrl = 'http://tieba.baidu.com/p/4352140663'
bdtb = BDTB(baseUrl,1)
bdtb.start()




