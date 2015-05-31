# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os

class LoveBridge:
    def __init__(self):
        # 主站URL
        self.siteURL = "https://bbs.sjtu.edu.cn/"
        # LB 板URL
        self.lburl = self.siteURL + 'bbstdoc,board,LoveBridge.html'
        # 伪装浏览器
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        # 保存当前页面的各条主题URL
        self.subjects = []
        # 保存当前页面前一页的URL
        self.preurl = ""

    # 获得指定页面（URL）的HTML文件
    def getPage(self, url, subject):
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            # 为什么具体主题页不使用GBK编码，因为尝试了不行。。。
            if subject:
                pageCode = response.read()
            else:
                pageCode = response.read().decode('gbk')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'reason'):
                print e.reason
            print u'连接失败'
            return None

    # 获取页面中各条主题的URL
    def getPageItems(self, url):
        pageCode = self.getPage(url, False)
        if not pageCode:
            print u'页面加载失败'
            return None
        informPattern = re.compile('<tr><td>(.*?)<td><td><a href=.*?</a>.*?<td>.*?<a href=(.*?)>(.*?)</a>', re.S)
        prepagePattern = re.compile('<hr>.*?<a href=(.*?)>(.*?)</a>', re.S)
        informs = re.findall(informPattern, pageCode)
        prepage = re.findall(prepagePattern, pageCode)
        for inform in informs:
            haveOther = re.search("font", inform[0])
            if not haveOther:
                print inform[0], '    ', inform[1], '    ', inform[2]
                self.subjects.append(inform[1].strip())
        for page in prepage:
            pre = re.search(u"上一页", page[1])
            if pre:
                print page[0], '    ', page[1]
                self.preurl = page[0]

    # 获取具体主题页面的图片URL
    def getPics(self, url):
        pageCode = self.getPage(url, True)
        if not pageCode:
            print u'页面加载失败'
            return None
        pattern = re.compile('<IMG SRC="/file/LoveBridge/(.*?).jpg"', re.S)
        subjs = re.findall(pattern, pageCode)
        for s in subjs:
            s = s.split(".")[0]
            imgUrl = 'https://bbs.sjtu.edu.cn/file/LoveBridge/' + s +".jpg"
            self.saveImage(imgUrl, 'Images/' + s + '.jpg')

    # 创建文件夹
    def mkdir(self, path):
        path = path.strip()
        isExist = os.path.exists(path)
        if not isExist:
            print u"创建了文件夹:" , path , u"保存图片"
            os.mkdir(path)
            return True
        else:
            return False

    # 保存图片
    def saveImage(self, url, fname):
        u = urllib.urlopen(url)
        data = u.read()
        f = open(fname, 'wb')
        f.write(data)
        f.close()

    # 方法入口
    def start(self, pages):
        print u'读取饮水思源BBS，LoveBridge板信息'
        self.mkdir("Images")
        if pages < 1:
            print u"查询页面必须大于1"
            return None
        else:
            url = self.lburl
            for i in range(pages):
                print u"打开第 " , i+1 , u" 个页面， " , url
                self.getPageItems(url)
                for subj in self.subjects:
                    self.getPics(self.siteURL + subj)
                url = self.siteURL + self.preurl

# 创建对象
lb = LoveBridge()
# 设置需要抓取多少个页面的图片
lb.start(10)

