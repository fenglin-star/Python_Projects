#-*-coding: utf-8-*-
from python_def.Mysqldb_server import mysql_url,read_mysql
import jieba
from jieba import analyse
import re,sys,os
from excel_lw import *

# 引入TF-IDF关键词抽取接口
textrank = analyse.textrank

# 本地MySQL
host = '127.0.0.1'
port = 3306  # 端口号
user = 'python_use'  # 用户名
password = "kPXHsC2pSECsXxNF"  # 密码
db = "python_use"  # 库
table = "shishengguanxi"  # 表

# 读数据库
title_lists = read_mysql(host,port,user,password,db,table,count=2500,table_list=2)
fabiaoqikan_lists = read_mysql(host,port,user,password,db,table,count=2500,table_list=3)
fabiaonianfen_lists = read_mysql(host,port,user,password,db,table,count=2500,table_list=4)
qikan_keys_lists = read_mysql(host,port,user,password,db,table,count=2500,table_list=5)

# 时间去重，按大小排序
set_time = set(fabiaonianfen_lists)
sort_time = []
for i in set_time:
    sort_time.append(i)
sort_time.sort()

# 期刊去重
set_qik = set(fabiaoqikan_lists)

# 关键词去重

def year_tj():
    year_list = []
    for i in sort_time:
        write_txt = [str(i),str(fabiaonianfen_lists.count(i))]
        year_list.append(write_txt)
    return year_list

# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]

def qik_tj():
    qik_tj_list = []
    for i in set_qik:
        write_txt = i,fabiaoqikan_lists.count(i)
        qik_tj_list.append(write_txt)
    qik_tj_list.sort(key=takeSecond)
    return qik_tj_list

def key_tj():
    keys_list = []
    for i in qikan_keys_lists:
        for o in i.split("|"):
            o = o.strip()  # 去空格
            if len(o) == 0:
                pass
            else:
                keys_list.append(o)

    key_tj_list = []
    # 期刊去重
    set_keys_list = set(keys_list)
    for t in set_keys_list:
        write_txt = t,int(keys_list.count(t))
        key_tj_list.append(write_txt)
    key_tj_list.sort(key=takeSecond)
    return key_tj_list

def write_excel_data(sheet_name_xlsx,value_list):
    book_name_xlsx = "excel/"+ sheet_name_xlsx + ".xlsx"
    sheet_name_xlsx = sheet_name_xlsx
    value3 = value_list
    write_excel_xlsx(book_name_xlsx, sheet_name_xlsx, value3)
    read_excel_xlsx(book_name_xlsx, sheet_name_xlsx)


if __name__ == '__main__':
    # 关键词统计
    # write_excel_data(sheet_name_xlsx="师生关系论文_年份统计", value_list=year_tj()[:10:-1])
    write_excel_data(sheet_name_xlsx="师生关系论文_期刊统计", value_list=qik_tj()[:50:-1])
    # write_excel_data(sheet_name_xlsx="师生关系论文_关键词统计", value_list=key_tj()[:50:-1])