# -*- coding:utf-8 -*-
import urllib2
import re

# https://bbs.sjtu.edu.cn/bbstdoc,board,LoveBridge.html  LoveBridge URL

class LoveBridge:
    def __init__(self):
        self.url = 'https://bbs.sjtu.edu.cn/bbstdoc,board,LoveBridge.html'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
    def getPage(self):
        try:
            request = urllib2.Request(self.url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('gbk')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'reason'):
                print e.reason
            print u'连接失败'
            return None
    def getPageItems(self):
        pageCode = self.getPage()
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
                print inform[0],'    ', inform[1],'    ', inform[2]
        for page in prepage:
            pre = re.search(u"上一页", page[1])
            if pre:
                print page[0], '    ', page[1]
    def start(self):
        print u'读取饮水思源BBS，LoveBridge板信息'
        self.getPageItems()


lb = LoveBridge()
lb.start()