#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import codecs
from utils.mssql import MSSQL

print('开始保存数据到数据库')

file='d:\cars.txt'

with codecs.open(file,'r','utf-8') as r:
   # encodedjson=r.read()
    cars=json.load(r)

ms = MSSQL(host="others.chinacloudapp.cn",user="newhope",pwd="newhope1234",db="newhope2")
reslist = ms.ExecQuery("select Id from AspNetUsers")
for i in reslist:
    print(i)