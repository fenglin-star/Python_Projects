#! /usr/bin/env python
#coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
# from google_tranlate.import_def.read_mysql import read_host_mysqlurls
import time,os,random


def send_usermail(receiver):
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = '1094470534@qq.com'
    #pwd为qq邮箱的授权码
    pwd = 'dxfsmaqtkzdnghgc' ##
    #发件人的邮箱
    sender_qq_mail = '1094470534@qq.com'


    # #qq邮箱smtp服务器
    # host_server = 'mail.cloudflarecdn.net'
    # #sender_qq为发件人的qq号码
    # sender_qq = 'mail@cloudflarecdn.net'
    # #pwd为qq邮箱的授权码
    # pwd = '202014xyZ' ##
    # #发件人的邮箱
    # sender_qq_mail = 'mail@cloudflarecdn.net'


    #邮件的正文内容
    mail_content = "课程需要重修"
    #邮件标题
    mail_title = '教务处爬虫'

    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    try:
        msg = MIMEText(mail_content, "html", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = Header(receiver) ## 接收者的别名
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功 " + " 邮件标题:" + mail_title + "  发送邮箱:" + receiver)

    except Exception as e:
        print("失败",e)


if __name__ == '__main__':

    # 远程MySQL设置部分
    # host = '144.172.126.40'
    # port = 3306  # 端口号
    # user = 'jingjiniao_info'  # 用户名
    # password = "p7AWAihz7HTTstew"  # 密码
    # db = "jingjiniao_info"  # 库
    # table = "pre_common_member"  # 表
    # url_lists = read_host_mysqlurls(host,port,user,password,db,table,count=10000,table_list=1)
    #
    # success_num = 0
    # for i in url_lists:
    #     while success_num < 20:
    #         try:
    #             start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #             print(start_time)
    #             receiver = i
    #             send_usermail(receiver)
    #             time.sleep(random.choice(range(6,15)))
    #             break
    #
    #         except Exception as e:
    #             time.sleep(30)
    #             print(e,"正在重试:",receiver)
    #             success_num = success_num + 1
    #             continue

    send_usermail("1094470534@qq.com")