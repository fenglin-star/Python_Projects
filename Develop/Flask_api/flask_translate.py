#-*-coding: utf-8-*-
# 创建时间: 2021/1/5
import re
from clark_demo.caiyun_translate import MyHTMLParser,Caiyun_tranlate
from clark_demo.google_translation import translate_list_data
from clark_demo.Mysqldb_server import MySQLCommand,read_inquire_mysql
import time
# def list_to_str(source):
#     data = ''
#     for i in source:
#         data = data + '*|||*' + i
#     return data
#
#
# def str_to_list(source):
#     # 解析str，转换为list
#     datas = source.replace("*|||*", "", 1).split("*|||*")
#     return datas


# 通过标签替换来翻译HTML
def base_html_translate(api_tpye,language, source):

    html = source
    new_html = html

    # 不翻译<a>标签中的内容
    a_list = re.findall(r'<a[\s\S]*?</a>', html)
    for i, o in zip(a_list, range(0, len(a_list))):
        o = "<a{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(i, o, 1)

    # 不翻译<code>标签中的内容
    code_list = re.findall(r'<code[\s\S]*?</code>', html)
    for i, o in zip(code_list, range(0, len(code_list))):
        o = "<code{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(i, o, 1)

    parser = MyHTMLParser()
    parser.feed(new_html)
    html_list = parser.return_data()

    if api_tpye == "caiyun":
        tranlate = Caiyun_tranlate(language=language, source=html_list).caiyun_list()
    else:
        tranlate = translate_list_data(language=language, source=html_list)

    en_html_list = tranlate

    for cn, en in zip(html_list, en_html_list):
        html = new_html
        new_html = html.replace(cn, en, 1)
        # print(cn,"翻译内容：",en)

    # 把占位符替换回去
    for i, o in zip(a_list, range(0, len(a_list))):
        o = "<a{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(o, i, 1)

    for i, o in zip(code_list, range(0, len(code_list))):
        o = "<code{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(o, i, 1)

    return new_html


# 通过标签替换来翻译HTML
def html_translate(api_tpye,language, source):
    new_html = base_html_translate(api_tpye, language, source)
    return new_html


# 通过标签替换来翻译HTML
# def html_translate(api_tpye,language, source):
#     key = 'base_txt'
#     if len(source) > 20:
#         new_html = base_html_translate(api_tpye, language, source)
#         return new_html
#
#     else:
#         host = '209.126.11.73'
#         port = 3306  # 端口号
#         user = 'py_translate'  # 用户名
#         password = "dn73iTWTbyhAPeBP"  # 密码
#         db = "py_translate"  # 库
#         table = language  # 表
#         charset = 'utf8'
#
#         # 连接数据库
#         mysqlCommand = MySQLCommand(host, port, user, password, db, table)
#         mysqlCommand.connectMysql()
#
#         def sql_str(data):
#             data = str(data).replace("'", "''").replace('"', '""')
#             return data
#
#         try:
#             # 插入数据，如果已经存在就不在重复插入
#             if_dict = {
#                 "base_txt": sql_str(source),
#             }
#             if mysqlCommand.ifinsertData(if_dict,key) == 0:
#                 url_lists = read_inquire_mysql(host, port, user, password, db, table, count=100, table_list=3,
#                                                inquire_id=["base_txt", str(source)])
#                 repeat_txt = url_lists[0]
#                 print("重复语句:",source)
#                 return repeat_txt
#
#             else:
#                 new_html = base_html_translate(api_tpye,language, source)
#                 news_dict = {
#                     "datatime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
#                     "base_txt": sql_str(source),
#                     "translate_txt": sql_str(new_html),
#                 }
#                 mysqlCommand.insertData(news_dict,key)
#                 return new_html
#
#         except Exception as e:
#             print("数据错误", e)  # 输出插入失败的报错语句
#         mysqlCommand.closeMysql()  # 最后一定要要把数据关闭




def caiyun_translate(language, source):
    return html_translate("caiyun",language, source)


# 通过标签替换来翻译HTML
def google_translate(language, source):
    return html_translate("google", language, source)



if __name__ == '__main__':

    # html 翻译
    data_str = '''Bus is too congested or there is no space, one way up to half an hour'''

    print(len(data_str))
    print(caiyun_translate(language="zh",source=data_str))

    print(google_translate(language="zh", source=data_str))
    # print(caiyun_translate(language="en", source=data_str))



