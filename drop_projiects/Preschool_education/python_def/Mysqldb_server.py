# -*- coding: utf-8 -*-
import time
import random
import pymysql


# 查看系统类型
import platform

platform_ = platform.system()
is_win = is_linux = is_mac = False

if platform_ == "Windows":
    is_win = True
elif platform_ == "Linux":
    is_linux = True
elif platform_ == "Mac":
    is_mac = True

# 用来操作数据库的类
class MySQLCommand(object):
    # 类的初始化
    def __init__(self,host,port,user,password,db,table):
        self.host = host
        self.port = port  # 端口号
        self.user = user  # 用户名
        self.password = password  # 密码
        self.db = db  # 库
        self.table = table  # 表

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')


    # 插入数据，插入之前先查询是否存在，如果存在就不再插入
    def insertData(self, my_dict):
        table = self.table  # 要操作的表格
        # 注意，这里查询的sql语句url=' %s '中%s的前后要有空格
        char_sqls = "SELECT url FROM {}".format(table)
        sqlExit = char_sqls + " WHERE url = ' %s '" % (my_dict['url'])
        res = self.cursor.execute(sqlExit)
        if int(res) > 0 :  # res为查询到的数据条数如果大于0就代表数据已经存在
            # print("数据已存在", res)
            # db_true = 0
            return 0
        else:
            # 数据不存在才执行下面的插入操作
            try:
                cols = ', '.join(my_dict.keys())  # 用，分割
                values = '"," '.join(my_dict.values())
                char_sqls = "INSERT INTO {}".format(table)
                sql = char_sqls + "(%s) VALUES (%s)" % (cols,'"' + values + '"')
                # 拼装后的sql如下
                # INSERT INTO home_list (img_path, url, id, title) VALUES ("https://img.huxiucdn.com.jpg"," https://www.huxiu.com90.html"," 12"," ")
                try:
                    result = self.cursor.execute(sql)
                    insert_id = self.conn.insert_id()  # 插入成功后返回的id
                    self.conn.commit()
                    # 判断是否执行成功
                    if result:
                        # 查询当前数据表中有多少条数据
                        query = " select count(*) from {}".format(table)
                        try:
                            self.cursor.execute(query)
                            count_wm = self.cursor.fetchall()
                            count_table = count_wm[0][0]
                        except:
                            print(query + ' execute failed.')

                        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '数据表共有:', count_table, '数据'," 数据库插入成功",  my_dict['url'], my_dict['title'],"\n")
                        return insert_id + 1

                except pymysql.Error as e:
                    # 发生错误时回滚
                    self.conn.rollback()
                    # 主键唯一，无法插入
                    if "key 'PRIMARY'" in e.args[1]:
                        print("数据已存在，未插入数据",values)
                    else:
                        print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
            except pymysql.Error as e:
                print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 查询最后一条数据的id值
    def getLastId(self):
        sql = "SELECT max(id) FROM " + self.table
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例


# 用来操作数据库的类
class Read_MySQLCommand(object):
    # 类的初始化
    def __init__(self,host,port,user,password,db,table):
        self.host = host
        self.port = port  # 端口号
        self.user = user  # 用户名
        self.password = password  # 密码
        self.db = db  # 库
        self.table = table  # 表

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    # 查询数据
    def queryMysql(self):
        sql = "SELECT * FROM " + self.table

        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchall()
            #只取一条数据
            # row = self.cursor.fetchone()
            # 只取全部数据
            row_list = list(row)
            # print(list(row))
            return row_list
            # print(type(row))

        except:
            print(sql + ' execute failed.')


    def closeMysql(self):
        self.cursor.close()
        self.conn.close()



# 读取MySQL当中的数据
def read_mysql(host, port, user, password,db,table,count,table_list):
    url_list = []
    # 创建数据库操作类的实例
    mySQLCommand = Read_MySQLCommand(host,port,user,password,db,table)
    mySQLCommand.connectMysql()
    row_list = mySQLCommand.queryMysql()   #查询数据
    for i in row_list:
        i =list(i)
        url = i[table_list]
        url_list.append(url)
    mySQLCommand.closeMysql()  # 最后一定要要把数据关闭
    return url_list[0:count]


# 插入MySQL当中的数据
def mysql_url(url,biaoti,fabiaoqikan,fabiaonianfen,qikan_keys,qikan_zaiyao,host,port,user,password,db,table):
    # 连接数据库
    mysqlCommand = MySQLCommand(host,port,user,password,db,table)
    mysqlCommand.connectMysql()
    #把爬取到的每条数据组合成一个字典用于数据库数据的插入
    news_dict = {
        # .replace("'", "''").replace('"', '""') 是为了MySQL数据入库时特殊字符进行处理
        "datatime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        "url": url.replace("'","''").replace('"','""'),
        "title": biaoti.replace("'","''").replace('"','""'),
        "fabiaoqikan" : fabiaoqikan.replace("'","''").replace('"','""'),
        "fabiaonianfen": fabiaonianfen.replace("'", "''").replace('"', '""'),
        "qikan_keys": qikan_keys.replace("'", "''").replace('"', '""'),
        "qikan_zaiyao": qikan_zaiyao.replace("'", "''").replace('"', '""'),
    }
    try:
        # 插入数据，如果已经存在就不在重复插入
        res = mysqlCommand.insertData(news_dict)
        return res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句
    mysqlCommand.closeMysql()  # 最后一定要要把数据关闭




if __name__ == '__main__':
    # 本地MySQL
    host = '127.0.0.1'
    port = 3306  # 端口号
    user = 'python_use'  # 用户名
    password = "kPXHsC2pSECsXxNF"  # 密码
    db = "python_use"  # 库
    table = "shishengguanxi"  # 表

    url = biaoti = fabiaoqikan = fabiaonianfen = qikan_keys = qikan_zaiyao ="test"
    return_mysql = mysql_url(url=url, biaoti=biaoti, fabiaoqikan=fabiaoqikan,
                             fabiaonianfen=fabiaonianfen, qikan_keys=qikan_keys,
                             qikan_zaiyao=qikan_zaiyao, host=host, port=port, user=user, password=password, db=db,
                             table=table)
    # 插入成功返回1，失败返回0。
    # print(return_mysql)
    if return_mysql == 0:
        print("数据库中已存在，未插入数据")
    else:
        pass

    # # 读数据库试例
    # url_lists = read_mysql(host,port,user,password,db,table,count=100,table_list=2)
    # for i in url_lists:
    #     print(i)