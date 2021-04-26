#coding=utf-8
from urllib import parse
import random,time
import requests
from requests.adapters import HTTPAdapter
import json
from multiprocessing import Pool


# 随机UserAgent
fake_UserAgent = [
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
]


def requests_res(url):
    headers = {
        "user-agent": random.choice(fake_UserAgent)
    }
    # requests 设置最多5次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=2))
    s.mount('https://', HTTPAdapter(max_retries=2))
    response = s.get(url,headers=headers,timeout=5)
    print(response.status_code,"  ",url)



if __name__ == '__main__':
    url = ['http://node-hk.2021214.xyz:30345/',
           'http://nat-cu.2021214.xyz:30345',
           'http://nat-cm.2021214.xyz:30345/'
           ]

    for i in url:
        try:
            requests_res(i)
        except Exception as e:
            print("出现错误:", e)

