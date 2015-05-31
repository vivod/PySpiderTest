#### Create 2015.5.31
---
一个简单的Python爬虫，目前只能抓取[bbs.sjtu.edu.cn](bbs.sjtu.edu.cn)LoveBridge首页信息
可以抓取到每条主题的ID, URL, Title。 以及前一页的URL
接下来可以根据这些信息抓取每个主题的内容，图片，以及前一页面的这些信息

###### reference: [Python爬虫学习系列教程](http://cuiqingcai.com/1052.html)
---
#### update 2015.5.31
---
用法
```python
# 创建对象
lb = LoveBridge()
# 设置需要抓取多少个页面的图片
lb.start(10)
```
基本可以抓取到各主题页面的图片，但还有些bug