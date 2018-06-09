import utils
from utils.klHtmlParser import klHtmlParser
import json
import codecs
import copy  

tags=('A','B','C','D','F','G','H','J','K','L','M','N','O','P','Q','R','S','T','W','X','Y','Z')
urlFormat= lambda x: 'http://www.autohome.com.cn/grade/carhtml/'+x+'.html'
data={}
for t in tags:
    url=urlFormat(t)
    print('开始爬取：%s' % url)    
    hp = klHtmlParser(url)
    hp.run()
    brandWithCars=hp.getData()
    if len(brandWithCars)>0:
        data[t]=copy.deepcopy(brandWithCars)

print('*********************************')
print('解析完成')
print('开始保存数据到文件')
encodedjson = json.dumps(data,ensure_ascii=False)
file='d:\cars.json'
with codecs.open(file,'w','utf-8') as w:
    w.write(encodedjson)
print('已保存数据到：', file)



    