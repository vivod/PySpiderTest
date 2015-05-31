# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os

class LoveBridge:
    def __init__(self):
        # ��վURL
        self.siteURL = "https://bbs.sjtu.edu.cn/"
        # LB ��URL
        self.lburl = self.siteURL + 'bbstdoc,board,LoveBridge.html'
        # αװ�����
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        # ���浱ǰҳ��ĸ�������URL
        self.subjects = []
        # ���浱ǰҳ��ǰһҳ��URL
        self.preurl = ""

    # ���ָ��ҳ�棨URL����HTML�ļ�
    def getPage(self, url, subject):
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            # Ϊʲô��������ҳ��ʹ��GBK���룬��Ϊ�����˲��С�����
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
            print u'����ʧ��'
            return None

    # ��ȡҳ���и��������URL
    def getPageItems(self, url):
        pageCode = self.getPage(url, False)
        if not pageCode:
            print u'ҳ�����ʧ��'
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
            pre = re.search(u"��һҳ", page[1])
            if pre:
                print page[0], '    ', page[1]
                self.preurl = page[0]

    # ��ȡ��������ҳ���ͼƬURL
    def getPics(self, url):
        pageCode = self.getPage(url, True)
        if not pageCode:
            print u'ҳ�����ʧ��'
            return None
        pattern = re.compile('<IMG SRC="/file/LoveBridge/(.*?).jpg"', re.S)
        subjs = re.findall(pattern, pageCode)
        for s in subjs:
            s = s.split(".")[0]
            imgUrl = 'https://bbs.sjtu.edu.cn/file/LoveBridge/' + s +".jpg"
            self.saveImage(imgUrl, 'Images/' + s + '.jpg')

    # �����ļ���
    def mkdir(self, path):
        path = path.strip()
        isExist = os.path.exists(path)
        if not isExist:
            print u"�������ļ���:" , path , u"����ͼƬ"
            os.mkdir(path)
            return True
        else:
            return False

    # ����ͼƬ
    def saveImage(self, url, fname):
        u = urllib.urlopen(url)
        data = u.read()
        f = open(fname, 'wb')
        f.write(data)
        f.close()

    # �������
    def start(self, pages):
        print u'��ȡ��ˮ˼ԴBBS��LoveBridge����Ϣ'
        self.mkdir("Images")
        if pages < 1:
            print u"��ѯҳ��������1"
            return None
        else:
            url = self.lburl
            for i in range(pages):
                print u"�򿪵� " , i+1 , u" ��ҳ�棬 " , url
                self.getPageItems(url)
                for subj in self.subjects:
                    self.getPics(self.siteURL + subj)
                url = self.siteURL + self.preurl

# ��������
lb = LoveBridge()
# ������Ҫץȡ���ٸ�ҳ���ͼƬ
lb.start(10)

