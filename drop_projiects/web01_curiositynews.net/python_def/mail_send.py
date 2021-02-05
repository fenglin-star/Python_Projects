#! /usr/bin/env python
#coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL



def send_usermail(mail_title,mail_content,receiver):
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = '1094470534@qq.com'
    #pwd为qq邮箱的授权码
    pwd = 'dxfsmaqtkzdnghgc' ##
    #发件人的邮箱
    sender_qq_mail = '1094470534@qq.com'


    #邮件的正文内容
    mail_content = mail_content
    #邮件标题
    mail_title = mail_title

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
    send_usermail('教务处爬虫',"课程需要重修","1094470534@qq.com")