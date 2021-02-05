#-*-coding: utf-8-*-
from python_def.Mysqldb_server import mysql_url,read_mysql
import jieba
from jieba import analyse
import re,sys,os
from excel_lw import *

# 本地MySQL
host = '127.0.0.1'
port = 3306  # 端口号
user = 'python_use'  # 用户名
password = "kPXHsC2pSECsXxNF"  # 密码
db = "python_use"  # 库
table = "shishengguanxi"  # 表

qikan_keys_lists = read_mysql(host,port,user,password,db,table,count=10,table_list=5)


keys_list = []

for i in qikan_keys_lists:
    # print(type(i))
    for o in i.split("|"):
        o = o.strip()  # 去空格
        if len(o) == 0:
            pass
        else:
            keys_list.append(o)

print(keys_list)