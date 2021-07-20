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
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X  10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
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
        return response.status_code

    except Exception as e:
        print("出现错误:", e)
        return 404


def get_dnspod_dns(domain):
    post_data = {
        "login_token": "216027,1406d367543fef1e471b78d894b379c2",
        "format": "json",
        "domain":domain,
    }
    # requests 设置最多五次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    res = s.post(
        url="https://dnsapi.cn/Record.List",  # 翻译
        data=post_data,timeout=20,)
    data_txt = res.text
    return data_txt


def get_dnspod_ip(domain,name):
    post_data = {
        "login_token": "216027,1406d367543fef1e471b78d894b379c2",
        "format": "json",
        "domain":domain,
    }
    # requests 设置最多五次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    res = s.post(
        url="https://dnsapi.cn/Record.List",  # 翻译
        data=post_data,timeout=20,)
    data_txt = json.loads(res.text)['records']

    for i in data_txt:
        if i['name'] == name:
            print('域名{}：'.format(domain),i['name'],i['value'],'id为:',i['id'],'line为:',i['line'])
            return i['value']  #返回查询域名现在的解析ip


def modify_dnspod_ip(domain,record_id,sub_domain,value,record_type='CNAME'):
    post_data = {
        "login_token": "216027,1406d367543fef1e471b78d894b379c2",
        "format": "json",
        "domain": domain,
        "record_id" : record_id,
        'sub_domain' : sub_domain,
        'value' : value,
        'record_type' : record_type,
        'record_line_id' : 0
    }
    # requests 设置最多五次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    res = s.post(
        url="https://dnsapi.cn/Record.Modify",  # 翻译
        data=post_data,timeout=20,)
    res.encoding = res.apparent_encoding
    data_txt = json.loads(res.text)
    print(data_txt)
    return data_txt


def get_cf_ip():
    payload = {"key": "iDetkOys"}
    header = {
        "Host": "api.hostmonit.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json;charset=utf-8",
        "Content-Length": "18",
        "Origin": "https://stock.hostmonit.com",
        "Connection": "keep-alive",
        "Referer": "https://stock.hostmonit.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Cache-Control": "max-age=0",
    }
    # 字典转换为json串
    data = json.dumps(payload)
    url = 'https://api.hostmonit.com/get_optimization_ip'
    res = requests.post(url, data=data, headers=header)
    print(json.loads(res.text).get('info')[0])
    new_ip = json.loads(res.text).get('info')[0].get('ip')
    return new_ip



if __name__ == '__main__':
    modify_dnspod_ip(domain='2021214.xyz', record_id='846237677', sub_domain='cfyes',
                     value=get_cf_ip(),
                     record_type='A')