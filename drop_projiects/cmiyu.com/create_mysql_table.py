#-*-coding: utf-8-*-
# 创建时间: 2020/9/18 10:29
import pymysql
from config import *

table_list = [
"gxmy",
"zmmy",
"cymy",
"dwmy",
"aqmy",
"dmmy",
"rmmy",
"dm",
"cy",
"dgmy",
"ry",
"etmy",
"wpmy",
"zwmy",
"jmmy",
"sbmy",
"symy",
"ypmy",
"yymy",
"ysmy",
"cwmy",
"qita",
]

for i in table_list:
    try:
        # 打开数据库连接
        db = pymysql.connect(host='localhost', user='cmiyu',
                              passwd='P5nWLFjWJZ3BKNRF',db="cmiyu", charset='utf8' )

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("DROP TABLE IF EXISTS {}".format(i))

        # 使用预处理语句创建表
        sql = """CREATE TABLE `cmiyu`.`{}` ( `url` TEXT NOT NULL , `mimian` TEXT NOT NULL , `midi` TEXT NOT NULL , `xiaotieshi` TEXT NOT NULL ) ENGINE = InnoDB;""".format(i)
        cursor.execute(sql)
        print("CREATE TABLE OK")
        # 关闭数据库连接
        db.close()
    except pymysql.err.InternalError as e:
        print("错误",e)


