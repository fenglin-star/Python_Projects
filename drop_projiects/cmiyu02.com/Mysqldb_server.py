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
def write_mysql(url,title,content,host,port,user,password,db,table):
    # 连接数据库
    mysqlCommand = MySQLCommand(host,port,user,password,db,table)
    mysqlCommand.connectMysql()
    #把爬取到的每条数据组合成一个字典用于数据库数据的插入
    news_dict = {
        # .replace("'", "''").replace('"', '""') 是为了MySQL数据入库时特殊字符进行处理
        "datatime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        "url": url.replace("'","''").replace('"','""'),
        "title": title.replace("'","''").replace('"','""'),
        "content" : content.replace("'","''").replace('"','""'),
    }
    try:
        # 插入数据，如果已经存在就不在重复插入
        res = mysqlCommand.insertData(news_dict)
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句
    mysqlCommand.closeMysql()  # 最后一定要要把数据关闭
    return res




if __name__ == '__main__':
    host = '222.186.56.136'
    port = 3306  # 端口号
    user = 'python_use'  # 用户名
    password = "Nx5mnaADaw3CsGip"  # 密码
    db = "python_use"  # 库
    table = "test"  # 表
    charset = 'utf8'

#     for i in range(0,10):
#         urls = "https://www.202014.xyz/{}.html"
#         url = urls.format(str(i))
#         title = "测试去重"
#         content = '''
#   <img alt=---为何香港购物更便宜？有哪些攻略？的头图--- id=---daily-img--- src=---https://gss0.bdstatic.com/70cFsj3f_gcX8t7mm9GUKT-xh_/jctuijian/0501/1292S6312L10-4Z54.jpg---/><div class=---cont--- id=---daily-cont--->
# <p>包括笔者在内的很多人，在购物的时候可能会有同样的感受：|||在香港或是国外购买一些价格较高的数码产品、化妆品等商品，价格往往要较内地便宜，有时差价甚至可以达到上千元。但也有一些商品（如香烟），不仅两地差价很小甚至于国外更贵，而且在通关的时候也有严格限制，有时甚至会被海关没收或补缴高额关税。其实，这样的价格差异，一般是由多种因素共同形成的，今天的这篇文章，将会对造成商品差价的因素进行讨论，还会提供一些较为省钱的购物策略。</p><p><strong>【造成售价差异的因素】</strong></p><p>一般而言，产品的价格除了取决于研发成本、生产成本等因素以外，还会受到部分人为和政策因素的影响，这部分影响往往构成了商品在不同地区的差价。常见的构成差价的因素有：</p><p><strong>增值税</strong></p><p>增值税主要出现在服务行业、商品销售等产生增值额（可以简化地认为增值额是售出商品或服务所产生的价值金额）的情况之下。增值税针对产生的增值额，按一个固定比例进行征税，且产生一次增值额时只征税一次。在我国，日常消费产生的增值税适用两种税率：</p><p>・17%：这一税率被称为“基本税率”，适用于日常生活中出现的绝大多数商品；</p><p>・13%：这一税率被称为“低税率”，适用于农产品、农资、图书、音像制品、居民用自然资源（如自来水、煤气、天然气）等商品；</p><p>尽管绝大多数地区都征收增值税，但仍有一些例外，例如购物者较为喜欢的香港特区（香港为了鼓励贸易，维护国际贸易中心地位，不征收增值税）和美国（美国是极少数不征收增值税的工业化国家）。</p><p>这样一来，在这些不征收增值税的地区进行购物，买到的商品就会相较一般地区便宜10%～20%。例如一台标配的11寸苹果MacBook Air笔记本电脑，内地官方售价为7088元，香港官方售价为7688港币（约合人民币6159元），差价大致相当于它在内地应缴纳的增值税（1030元）。</p><p><strong>关税</strong></p><p>关税是针对进出口商品所征收的一种税，几乎所有地区都会征收关税，因此一般情况下关税很难造成对商品的差价。但也有例外情况：香港为了鼓励贸易，采取自由港政策，除四类应课税品（汽油、甲醇、酒和酒精、烟草）以外进出口一律不收关税，但和其他地区一样，这四种应课税品的税率很高，这也是酒和香烟在不同地区难以产生差价的原因之一。</p><p>由于贸易和工业发展等原因，很多国外品牌的数码、食品、日用品等商品都在国内生产，这些商品一般在国内销售不会产生关税。值得注意的是，无论个人或团体，在香港或国外购买的全新商品（如电子、数码产品）如果原封进行过关，可能会被海关查扣，或补缴20%关税。由海外邮寄到国内的全新商品，在过关途中，海关会以抽查形式征收数额不等的关税。</p><p><strong>消费税</strong></p><p>消费税针对在地区境内进行销售的商品来征收，一般税率或征税额会按照商品价值或拟出售商品的数量来确定。在我国，烟、酒和酒精、化妆品、汽车、贵重首饰和珠宝等商品会被征收消费税。</p><p>绝大多数地区均对部分种类商品征收消费税，但香港依然例外，原因还是鼓励贸易的相关政策。这在一定程度上也形成了化妆品、珠宝首饰等商品的两地差价。</p><p><strong>其他因素</strong></p><p>除征税差异之外，有一些因素也会参与到差价的形成过程之中，比较常见的有汇率和手机等数码产品的定制问题。</p><p>大多数商品在制定价格时，会以某一首发地区的价格为基准，经过汇率转换并加上应征税额之后，确定最终的售价。由于货币的汇率经常出现变动，因此消费者在不同地区购买到的商品便会因为汇率原因产生差价。不过，汇率产生的差价一般有限，通常会在几十元到几百元之间。</p><p>而在手机销售之中，合约机、定制机等特殊机型也会带来巨大的差价。无论在国内还是国外，通过手机运营商购买，并和运营商签订一段时间合约的手机都会相较裸机有一定的差价。但为了保护运营商的利益，很多国家的合约机会有着一定的限制，在合约期间内合约卡和合约机不能分离，或是该款合约机只能使用合约运营商的网络（一般称为“有锁版”）。例如在美国，官方销售的苹果iPhone 5S有锁版（需和指定运营商签订两年合约）仅需要199美元（约合人民币1236元），而同一款机型的无锁版价格则上涨了两倍多，需要699美元（约合人民币4342元），和香港价格（5588港币，约合人民币4477元）相接近。</p><p><strong>【购物省钱攻略】</strong></p><p>・可以在购买较高价物品之前查询多个地区的售价，然后在售价较低的地区购买。可以使用国际转运业务（将从某一地区购买的商品转运到你的所在地），但转运业务会收取一定费用。当然，也可以请在当地的朋友或家人代为购买，不过要小心抽查关税（实际上抽查关税并不多）。</p><p>・如果计划去香港购物，事先应该熟悉所购物品在两地的差价，并了解该款商品是否支持内地联保（部分商品需要申请联保，极个别商品只能在香港本地保修）。如果是带封商品，回到内地过关之前最好拆封，建议直接在香港当地拆封使用一段时间，既可以测试商品有无质量问题，也可一定程度上避免缴纳关税。</p><p>・如果希望购买到价格最为超值的手机数码类商品，且对有锁（短时间内不能升级系统、需要使用卡贴、不支持3G等）或定制（带有定制标识、当地语言键盘等）并不在乎，可以考虑购买有锁或定制机型。在某些国家（如日本），手机很少提供有锁版，去当地购买手机数码产品，有锁版可能是唯一选择。</p>
# </div> ||| ['百科'] ['攻略', '购物', '便宜', '香港', '2014']
#         '''
#         return_mysql = mysql_url(url,title,content,host,port,user,password,db,table)
#         # 插入成功返回1，失败返回0。
#         # print(return_mysql)
#         if return_mysql == 0:
#             print("数据库中已存在，未插入数据")
#         else:
#             pass

    # 读数据库试例
    url_lists = read_mysql(host,port,user,password,db,table,count=100,table_list=2)
    for i in url_lists:
        print(i)