#coding=utf-8
import random,time
import requests
from requests.adapters import HTTPAdapter


# 随机UserAgent
fake_UserAgent = [
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
]

def post_telegrambot(text):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(url='https://eheh.org/push?account=42961135:12266197c0661036061fdae9dde84689c37e&descr={}'.format(text),timeout=25)
            response.encoding = response.apparent_encoding
            html = response.text
            return html + " 内容：{}".format(text)
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue

def requests_res(url):
    try:
        for i in range(0,3):
            headers = {
                "user-agent": random.choice(fake_UserAgent)
            }
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=2))
            s.mount('https://', HTTPAdapter(max_retries=2))
            response = s.get(url,headers=headers,timeout=10)
            # print("检测第{}次  ".format(i),response.status_code,"  ",url)
        # print(response.status_code,url)
        return response.status_code

    except Exception as e:
        print("出现错误:", e)
        return 404



if __name__ == '__main__':
    web_check = [
        'https://www.fangzhou.party',
        'https://fangzhou.cloud',
        'https://www.fangzhoucloud.net',
        'http://link.202014.xyz',
        'https://fangzhou.2021214.xyz',
        'https://fangzhou.link',
        'https://fangzhou.world',
        'https://fangzhou.202014.xyz'
    ]

    for i in web_check:
        if requests_res(i) == 200:
            print("{} 检测合格".format(i))
        else:
            print('通道失效：{}'.format(i))
            # post_telegrambot(text='通道失效：{}'.format(nodehk_url))
            pass


