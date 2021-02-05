#-*-coding: utf-8-*-
from config import *
import random,time
from googletrans import Translator

def translate_data(html_to_Language,data):
    #如果遇到错误就最多重试8次
    success_num = 0
    while success_num < 8:
        try:
            ua = random.choice(fake_UserAgent)
            translator = Translator(service_urls=[
                'translate.google.cn',
                'translate.google.com',
                'translate.google.com.hk',
            ],
                user_agent=ua,
                timeout=30,
                proxies=proxies,
            )
            en = translator.translate(data, dest=html_to_Language, src=html_base_Language).text
            return str(en).replace(", ",",")
            break

        except Exception as e:
            print(e,"正在重试:",data)
            success_num = success_num + 1
            continue


def translate_list_data(html_to_Language,data):

    #解析str，转换为list
    data = data.replace("*|||*", "", 1).split('*|||*')
    en_list = []

    #如果遇到错误就最多重试8次
    success_num = 0
    while success_num < 8:
        try:
            ua = random.choice(fake_UserAgent)
            translator = Translator(service_urls=[
                'translate.google.cn',
                'translate.google.com',
                'translate.google.com.hk',
            ],
                user_agent=ua,timeout=30,proxies=proxies,
            )
            for en in translator.translate(data, dest=html_to_Language, src=html_base_Language):
                en_list.append(str(en.text).replace(", ",","))
            return en_list
            break

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


# 解析list 转为flask能接受的str
def parse_list(data_list):
    data = ''
    for i in data_list:
        data = data+'*|||*'+i
    return data


if __name__ == '__main__':
    # 列表翻译
    data_list = ["测试文件","湖南第一师范学院"]
    print(translate_list_data(html_to_Language="en",data=parse_list(data_list)))

    # 短语翻译
    data_str = "湖南第一师范学院"
    print(translate_data(html_to_Language="en",data=data_str))
