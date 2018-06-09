#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
from html.parser import HTMLParser
from html.entities import name2codepoint
from utils.stopWatch import StopWatch
import re

class klHtmlParser(HTMLParser):
    
    def __init__(self,url):        
        HTMLParser.__init__(self)
        
        self._tagName=''
        self._list=[]
        self._item={}
        self._carsCount=0
        self._url=url
        
    def getAttrValue(self,attrs,key):
        if len(attrs) == 0: 
            return ''         
        for (variable, value)  in attrs:
            if variable == key:
                 return value
        return ''

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            #如果已经读取到数据，就保存到list
            if len(self._item) > 0:
                self._list.append(self._item)
                self._carsCount+= len(self._item['cars']) if self._item.get('cars')  else 0
                self._item={}                
            self._item['src']=self.getAttrValue(attrs,'src')
            
        elif tag=='div' and self.getAttrValue(attrs,'class') =='h3-tit':
            self._tagName='brand'
        elif tag=='ul' and self.getAttrValue(attrs,'class') =='rank-list-ul':
            self._tagName='rank-list-ul'
        elif tag=='h4' and self._tagName=='rank-list-ul':
            self._tagName='rank-list-ul>h4'
        elif tag=='a' and self._tagName=='rank-list-ul>h4':
            self._tagName='rank-list-ul>h4>a'
        

    def handle_endtag(self, tag):
        pass # print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self._tagName=='brand':
            self._tagName=''
            self._item['brand']=data
        elif self._tagName=='rank-list-ul>h4>a':
            cars= self._item.get('cars')
            if cars !=None:
                cars.append(data)
            else:
                 self._item['cars']=[data]
            
            #清除self._tagName回到rank-list-ul
            self._tagName=self._tagName.split('>')[0]            

    def handle_comment(self, data):
        pass # print('<!--', data, '-->')

    def handle_entityref(self, name):
        pass # print('&%s;' % name)

    def handle_charref(self, name):
        pass # print('&#%s;' % name)
        
    def loadUrl(self):
        req = request.Request(self._url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36')
        self._html=''
        charset='utf-8'      
                  
        print('********************************************')
        sw = StopWatch()        
        with request.urlopen(req) as f:
            print('下载html成功')
            print('Status:', f.status, f.reason)
            for k, v in f.getheaders():
                print('%s: %s' % (k, v))
                if k=='Content-Type':
                    contentValueGroup = re.match(r'.*charset=(.+).*',v.lower())
                    if contentValueGroup!=None:
                        charset=contentValueGroup.group(1)
                        print('检测到编码字符集为：%s' % charset)
            sw.reset();
            print('开始读取html...')
            self._html=f.read().decode(charset)
            print('读取html完成，耗时: %d' % sw.stop())
        return self._html
        
    def run(self):
        self.loadUrl()
        print('开始解析html')
        sw = StopWatch()
        self.feed(self._html)
        self.close()     
        #把最后一个添加到list中  
        if len(self._item) > 0:
            self._list.append(self._item)
            self._carsCount+= len(self._item['cars']) if self._item.get('cars')  else 0
            self._item={}               
        print('解析html完成，耗时: %d' % sw.stop())
        print('获取到品牌：%d 个，车型：%d 个' % (len(self._list), self._carsCount))
        
    def getData(self):
        return self._list
    
    def clear(self):
        self._tagName=''
        self._list=[]
        self._item={}
        self._carsCount=0
        self._html=''
        
