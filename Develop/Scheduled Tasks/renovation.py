# coding=utf-8
import random
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import time

fake_UserAgent = [
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
]

# 下载一个页面HTML
def requests_download(url):
    #如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            # 随机UA
            ua = random.choice(fake_UserAgent)
            headers = {'User-Agent': ua}
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(url,headers=headers, timeout=25)
            r_code = response.apparent_encoding

            #解决中文乱码问题
            # if 'gbk' or 'GBK' in str(r_code):
            #     response.encoding = "gbk"
            # else:
            response.encoding = response.apparent_encoding
            html_content = response.text
            return html_content
            break

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


# BS4解析页面HTML，提取关键元素
def analysis_html(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    # print(body)

    # 获取标题
    title_list = body.select('div.list.clearfix > div.list_right.fr > ul')
    txts = title_list[0].select(".clearfix")
    list_post = []
    for i in txts[0:3]:
        txt = i.get_text()
        list_post.append(txt)
    return list_post


def send_usermail(receiver,mail_title,mail_txt):
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = '1094470534@qq.com'
    #pwd为qq邮箱的授权码
    pwd = 'dxfsmaqtkzdnghgc' ##
    #发件人的邮箱
    sender_qq_mail = '1094470534@qq.com'

    #邮件的正文内容
    mail_content = mail_txt
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
    now_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    receiver = "1094470534@qq.com"
    html = requests_download("http://jwc.hnfnu.edu.cn/tzgg1/xs.htm")
    number = html.count("重修")
    notice = "最近教务处通知: <br><br>"
    for i in analysis_html(html):
        notice = notice +i +"<br><br>"

    if number == 2:
        print("需要重修")
        mail_title = "需要重修，" + now_date
        mail_txt = notice
        send_usermail(receiver,mail_title, mail_txt)
    elif "重修" in str(notice):
        print("需要重修")
        mail_title = "需要重修，"  + now_date
        mail_txt = notice
        send_usermail(receiver,mail_title, mail_txt)
    else:
        print("不需要重修")
        mail_title = "未到重修时间，" + now_date
        mail_txt = notice
        send_usermail(receiver,mail_title, mail_txt)