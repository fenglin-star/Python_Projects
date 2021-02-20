#coding=utf-8
from urllib import parse
import random,time
import requests
from requests.adapters import HTTPAdapter
import json
from multiprocessing import Pool


list = []
# 随机UserAgent
fake_UserAgent = [
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
]




def requests_res(url,proxies):
    # 如果遇到错误就出试5次
    headers = {
        "user-agent": random.choice(fake_UserAgent)
    }
    # requests 设置最多5次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=2))
    s.mount('https://', HTTPAdapter(max_retries=2))
    response = s.get(url,headers=headers, proxies=proxies, timeout=15)
    response .encoding = response .apparent_encoding
    html = response.text
    return html



def post_telegrambot(text):
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {"token": '202014xyz',"text": text}
            # requests 设置最多2次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            res = s.post(
                url="https://hk-api.202014.xyz/telegrambot",
                data=post_data,timeout=25,)
            data_txt = res.text
            return data_txt


        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue



if __name__ == '__main__':
    success_num = 0
    while success_num < 6:
        try:
            proxies = {
                "http": "socks5://127.0.0.2:20808",
                'https': 'socks5://127.0.0.2:20808'
            }
            res = requests_res("http://ip-api.com/json/?lang=zh-CN", proxies)
            print("正常状态：",json.loads(res).get('query'), json.loads(res).get('country'), json.loads(res).get('regionName'))
            break

        except Exception as e:
            success_num = success_num + 1
            print("正在重试:",success_num, e)
            continue

    if success_num >= 3:
        title = 'V2ray存在问题'
        print(title,success_num, post_telegrambot(text=title))