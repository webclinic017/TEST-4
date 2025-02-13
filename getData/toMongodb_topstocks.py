# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:55:29 2020
获取所有股票并添加龙头股属性并入库
@author: 李博
"""

import pandas as pd
import json


# MONGODB CONNECT
#入库
from pymongo import MongoClient
import tushare as ts
pro = ts.pro_api('003137d7baa1439f01f9d2917992de6b8511f70f84612c78574d6996')

#查询当前所有正常上市交易的股票列表
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,market,name,area,industry,list_date')
#建立龙头股属性 是否为龙头 年度（2020）加权分（0-1）概念 行业 备注
df['top_flag'] = None
df['top_year'] = None
df['top_weighting'] = None
df['top_concenpt'] = None
df['top_industry'] = None
df['top_memo'] = None
print (df)
df.to_csv('topstocks.csv')


#标准写入函数
def csvtomongodb(filename,collection):
   client = MongoClient('mongodb://112.12.60.2:27017')
   mydb=client["ptest"]
   mycollection=mydb[collection]
   mycollection.remove()
   path_df=open(filename+'.csv','r',encoding='UTF-8')
   df_csv = pd.read_csv(path_df)
   records = json.loads(df_csv.T.to_json()).values()
   #print (records)
   mycollection.insert(records) 

#入库

csvtomongodb(u'topstocks',u'topstocks')

