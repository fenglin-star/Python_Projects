# @Author: 夕日 <xirikm@gmail.com>
# @Time:   2020/04/14 19:02:41
# @Update  2020/09/06 21:55:10
# @URL:    https://xirikm.net/2020/414-1.html

import os
import smtplib
import email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender(object):
    """
    邮件发送器，封装smtp发送邮件的常用操作
    """

    def __init__(self, user: str, password: str, host: str, port: int):
        """
        初始化smtp服务器连接

        :param user: 邮箱用户，支持 name<prefix@example.com> 的形式，会自动从中提取邮箱地址用于登录
        :param password: smtp登录密码
        :param host: smtp服务器地址
        :param port: smtp服务器端口，仅能使用25、465和587
        """
        self.__user = user
        # 提取出邮箱地址用于登录
        self.__login_mail = email.utils.getaddresses([user])[0][1]

        # 连接到smtp服务器，限制只允许使用25、465、587这三个端口
        if port == 25:
            self.__smtp_server = smtplib.SMTP(host=host, port=port)
        elif port == 465:
            self.__smtp_server = smtplib.SMTP_SSL(host=host, port=port)
        elif port == 587:
            self.__smtp_server = smtplib.SMTP(host=host, port=port)
            self.__smtp_server.starttls()
        else:
            raise ValueError("Can only use port 25, 465 and 587")

        # 登录smtp服务器
        self.__smtp_server.login(user=self.__login_mail, password=password)

    def send(
        self, to_user: str, subject: str = "", content: str = "", subtype: str = "plain"
    ):
        """
        发送纯文本邮件

        :param to_user: 收件人，支持 name<prefix@example.com> 的形式，如需同时发给多人，将多个收件人用半角逗号隔开即可
        :param subject: 邮件主题，默认为空字符串
        :param content: 邮件正文，默认为空字符串
        :param subtype: 邮件文本类型，只能为 plain 或 html，默认为 plain
        """
        self.__check_subtype(subtype)

        # 构造邮件
        msg = MIMEText(content, _subtype=subtype, _charset="utf-8")
        msg["From"] = self.__user
        msg["To"] = to_user
        msg["subject"] = subject

        # 发送邮件
        self.__smtp_server.send_message(msg)

    def send_with_attachment(
        self,
        to_user: str,
        attachment_path: str,
        attachment_name: str = "",
        subject: str = "",
        content: str = "",
        subtype: str = "plain",
    ):
        """
        发送带附件的邮件

        :param to_user: 收件人，支持 name<prefix@example.com> 的形式，如需同时发给多人，将多个收件人用半角逗号隔开即可
        :param attachment_path: 附件文件的路径
        :param attachment_name: 附件在邮件中显示的名字，设为空字符串时（默认）直接使用文件名
        :param subject: 邮件主题，默认为空字符串
        :param content: 邮件正文，默认为空字符串
        :param subtype: 邮件文本类型，只能为 plain 或 html，默认为 plain
        """
        self.__check_subtype(subtype)

        # 读取附件内容
        with open(attachment_path, "rb") as f:
            file_content = f.read()
        # 默认以文件名作为附件名
        if attachment_name == "":
            attachment_name = os.path.basename(attachment_path)

        # 构造一封多组件邮件
        msg = MIMEMultipart()
        # 添加文本内容
        text_msg = MIMEText(content, _subtype=subtype, _charset="utf-8")
        msg.attach(text_msg)
        # 添加附件
        file_msg = MIMEApplication(file_content)
        file_msg.add_header(
            "content-disposition", "attachment", filename=attachment_name
        )
        msg.attach(file_msg)

        msg["From"] = self.__user
        msg["To"] = to_user
        msg["subject"] = subject

        # 发送邮件
        self.__smtp_server.send_message(msg)

    def __check_subtype(self, subtype: str):
        if subtype not in ("plain", "html"):
            raise ValueError('Error subtype, only "plain" and "html" can be used')
        else:
            pass


def send_usermail(title,mail_content,send_mail):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            sender = MailSender("mail@fangzhoucloud.net", "202014xyZ", "api.fangzhoucloud.net", 465)
            sender.send(send_mail, title, mail_content, "html")
            return title + send_mail
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue



if __name__ == "__main__":
    title = '邮件发送测试'
    send_mail = "1094470534@qq.com"

    mail_content = """
    <p>邮件发送测试</p>
    <p><a href="https://xirikm.net/">这是一个链接</a></p>
    """
    # attachment_path = "xxx/xxx.txt"  # 附件的文件路径

    send_usermail(title, mail_content,send_mail)



    # sender = MailSender("mail@jingjiniao.info", "202014xyZ", "mail.jingjiniao.info", 25)

    # sender.send("1094470534@qq.com", "纯文本邮件", mail_content, "plain")

    # sender.send("1094470534@qq.com", "html邮件", mail_content, "html")

    # sender.send_with_attachment(
    #     "test2@xxx.xxx", attachment_path, "xxx.txt", "带附件的html邮件", mail_content, "html"
    # )

    # 默认参数测试
    # sender.send_with_attachment("test2@xxx.xxx", attachment_path)