#-*-coding: utf-8-*-
# 创建时间: 2020/9/5 15:22

from flask import request, Flask,jsonify
from clark_demo.mail_send import send_usermail
from clark_demo.img_yunpan import img_up_self
from flask_translate import google_translate,caiyun_translate

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



# def list_to_str(source):
#     # 解析list 转为flask能接受的str
#     data = ''
#     for i in source:
#         data = data + '*|*|*|*' + i
#     return data
#
#
# def str_to_list(source):
#     # 解析str，转换为list
#     datas = source.replace("*|*|*|*", "", 1).split("*|*|*|*")
#     return datas



@app.route('/', methods=['GET'])
def index():
    return "hello world",201


#远程图片储存Api
@app.route('/img', methods=['POST'])
def post_img():
    token = request.form['token']
    if token == '202014xyz':
        img_type = request.form['img_type']
        if img_type == 'url':
            content = request.form['content']
            img = img_up_self(url=content)  # 上传图片
            weburl = img.set_img_up()
            return weburl, 201

        elif img_type == 'html':
            content = request.form['content']
            img = img_up_self(html=content)  # 调用类class
            weburl = img.html_img_up()
            return weburl, 201

        else:
            return "img_type error", 201

    else:
        return "token error", 201


#邮件发送Api
@app.route('/mail', methods=['POST'])
def post_mail():
    token = request.form['token']
    if token == '202014xyz':
        title = request.form['title']
        mail_content = request.form['mail_content']
        send_mail = request.form['send_mail']
        res= send_usermail(title, mail_content, send_mail)
        return 'Message has been sent：'+res, 201
    else:
        return "token error", 201


#翻译Api-caiyun
@app.route('/translate-caiyun', methods=['POST'])
def post_caiyun_translate():
    token = request.form['token']
    if token == '202014xyz':
        language = request.form['language']
        source = request.form['source']
        response = caiyun_translate(language,source)
        return response, 201
    else:
        return "token error", 201


#翻译Api-google
@app.route('/translate-google', methods=['POST'])
def post_google_translate():
    token = request.form['token']
    if token == '202014xyz':
        language = request.form['language']
        source = request.form['source']
        response = google_translate(language,source)
        return response, 201
    else:
        return "token error", 201


#翻译Api-google
@app.route('/telegrambot', methods=['POST'])
def post_telegrambot():
    token = request.form['token']
    if token == '202014xyz':
        import telebot
        TOKEN = '1693960412:AAEzPGakWSuqShcacJDxE849etNu-NAdrsA'
        tb = telebot.TeleBot(TOKEN)
        text = request.form['text']
        tb.send_message(808721783, text)
        return '已发送消息', 201
    else:
        return "token error", 201


#Request Api
# @app.route('/request', methods=['POST'])
# def post_request():
#     token = request.form['token']
#     if token == '202014xyz':
#         language = request.form['language']
#         url = request.form['url']
#         response = google_translate(language,source)
#         return response, 201
#     else:
#         return "token error", 201


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,threaded=True)