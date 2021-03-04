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

default_inquire_id = ""

# 用来操作数据库的类
class MySQLCommand(object):
    # 类的初始化
    def __init__(self,host,port,user,password,db,table,inquire_id=default_inquire_id):
        self.host = host
        self.port = port  # 端口号
        self.user = user  # 用户名
        self.password = password  # 密码
        self.db = db  # 库
        self.table = table  # 表
        self.inquire_id = inquire_id

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')


    def ifinsertData(self,my_dict,key):
        table = self.table  # 要操作的表格
        # 注意，这里查询的sql语句url=' %s '中%s的前后要有空格
        char_sqls = "SELECT {} FROM {}".format(key,table)
        sqlExit = char_sqls + " WHERE {} = '{}'".format(key,my_dict[key])
        res = self.cursor.execute(sqlExit)
        if int(res) > 0 :  # res为查询到的数据条数如果大于0就代表数据已经存在
            return 0
        else:
            return 1


    # 插入数据，插入之前先查询是否存在，如果存在就不再插入ds
    def insertData(self, my_dict,key):
        table = self.table  # 要操作的表格
        try:
            cols = ', '.join(my_dict.keys())  # 用，分割
            values = '","'.join(my_dict.values())
            char_sqls = "INSERT INTO {}".format(table)
            sql = char_sqls + "(%s) VALUES (%s)" % (cols,'"'+values+'"')
            # print(sql)
            # 拼装后的sql如下
            # INSERT INTO home_list (img_path, url, id, title) VALUES ("https://img.huxiucdn.com.jpg"," https://www.huxiu.com90.html"," 12"," ")
            try:
                result = self.cursor.execute(sql)
                self.conn.commit()
                # 判断是否执行成功
                if result:
                    print("数据库插入成功",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), my_dict[key],"\n")

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


    # 查询某个条件下的数据
    def inquire_idMysql(self):
        sql = "SELECT * FROM {}".format(self.table) + " WHERE {}='{}';".format(self.inquire_id[0],self.inquire_id[1])
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchall()
            # 只取全部数据
            row_list = list(row)
            return row_list

        except:
            print(sql + ' execute failed.')


    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例




# 读取MySQL当中的数据
def read_mysql(host, port, user, password,db,table,count,table_list):
    url_list = []
    # 创建数据库操作类的实例
    mySQLCommand = MySQLCommand(host,port,user,password,db,table)
    mySQLCommand.connectMysql()
    row_list = mySQLCommand.queryMysql() #查询数据
    for i in row_list:
        i =list(i)
        url = i[table_list]
        url_list.append(url)
    mySQLCommand.closeMysql()  # 最后一定要要把数据关闭
    return url_list[0:count]


# 查询某个条件下的数据
def read_inquire_mysql(host, port, user, password,db,table,count,table_list,inquire_id):
    url_list = []
    # 创建数据库操作类的实例
    mySQLCommand = MySQLCommand(host,port,user,password,db,table,inquire_id)
    mySQLCommand.connectMysql()
    row_list = mySQLCommand.inquire_idMysql()   #查询某个条件下的数据
    for i in row_list:
        i =list(i)
        url = i[table_list]
        url_list.append(url)
    mySQLCommand.closeMysql()  # 最后一定要要把数据关闭
    return url_list[0:count]



# 插入MySQL当中的数据
def mysql_url(url,title,content,host,port,user,password,db,table):
    # 连接数据库
    mysqlCommand = MySQLCommand(host,port,user,password,db,table)
    mysqlCommand.connectMysql()

    def sql_str(data):
        # .replace("'", "''").replace('"', '""') 是为了MySQL数据入库时特殊字符进行处理
        data = str(data).replace("'", "''").replace('"', '""')
        return data

    # 把爬取到的每条数据组合成一个字典用于数据库数据的插入
    try:
        # 插入数据，如果已经存在就不在重复插入
        if_dict = {
            "url": sql_str(url),
        }
        ifnum = mysqlCommand.ifinsertData(if_dict)

        if ifnum == 0:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),"重复URL", if_dict['url'])

        else:
            news_dict = {
                "datatime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                "url": sql_str(url),
                "title": sql_str(title),
                "content": sql_str(content),
            }
            res = mysqlCommand.insertData(news_dict)
            return res

    except Exception as e:
        print("插入数据失败", e)  # 输出插入失败的报错语句
    mysqlCommand.closeMysql()  # 最后一定要要把数据关闭


if __name__ == '__main__':
    host = '111.230.47.98'
    port = 3306  # 端口号
    user = 'mydemo'  # 用户名
    password = "nwF4nEnRh4RFDwWJ"  # 密码
    db = "mydemo"  # 库
    table = "test"  # 表
    charset = 'utf8'

    for i in range(3,16):
        urls = "https://www.202014.xyz/{}.html"
        url = urls.format(str(i))
        title = "测试去重{}".format(str(i))
        content = '''aaaaa
        '''
        return_mysql = mysql_url(url,title,content,host,port,user,password,db,table)
        # 插入成功返回1，失败返回0。
        # print(return_mysql)
        if return_mysql == 0:
            print("数据库中已存在，未插入数据")
        else:
            pass

    # # 读数据库试例
    # url_lists = read_mysql(host,port,user,password,db,table,count=10,table_list=3)
    # for i in url_lists:
    #     print(i)


    # 查询某个条件下的数据
    url_lists = read_inquire_mysql(host,port,user,password,db,table,count=100,table_list=2,inquire_id=["title","测试去重3"])
    for i in url_lists:
        print(i)
