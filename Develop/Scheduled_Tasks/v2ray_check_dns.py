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
    response.encoding = response.apparent_encoding
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



if __name__ == '__main__':
    domain='2021214.xyz'
    # record_id='761863200'
    sub_domain='node-cm'
    value='node-hk.2021214.xyz'

    # get_dnspod_dns(domain) #全部子域名的记录

    get_dnspod_ip(domain, name='cfyes')  #查询子域名对应的ID

    # modify_dnspod_ip(domain='2021214.xyz',record_id='761863200', sub_domain='node-cm', value='node-hk.2021214.xyz', record_type='CNAME')


    # modify_dnspod_ip(domain='2021214.xyz', record_id='758263007', sub_domain='smart-node',
    #                  value='node-cm.2021214.xyz', record_type='CNAME')
    #
    # modify_dnspod_ip(domain='202014.xyz', record_id='737826514', sub_domain='node',
    #                  value='node-cm.2021214.xyz', record_type='CNAME')
    #
    # print(get_dnspod_ip('202014.xyz','node'))
    #
    # print(get_dnspod_ip('2021214.xyz','smart-node'))