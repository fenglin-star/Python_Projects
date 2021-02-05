#-*-coding: utf-8-*-
import requests
from requests.adapters import HTTPAdapter
import re,os,sys,random
import datetime,time
from bs4 import BeautifulSoup

web_list = [
"www.curiositynews.net",
'www.plantswiki.net',
'www.asiancuisineweb.com',
'www.10prime.net',
'www.zhujijiaocheng.com',
'www.bytequestion.com',
'www.jiemiyu.com',
'shici.jiemiyu.com',
]


# proxies = {} # 不使用代理
proxies = {'http': '119.45.181.78:6666','https': '119.45.181.78:6666'} # 远程代理


# 随机UserAgent
fake_UserAgent = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
]




def requests_url(url):
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
            response = s.get(url,headers=headers, proxies=proxies, timeout=30)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                return response.text
            break

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


def analysis_html(web):
    web = "https://{}/sitemap.xml".format(web)
    html = requests_url(web)
    urls = re.findall("<loc>(.*?)</loc>", html)
    for i in urls:
        url = "http://www.google.com/ping?sitemap={}".format(i)
        html = requests_url(url)
        if "successfully" in str(html):
            print("成功提交链接：{}".format(url))
        else:
            print("提交链接失败")



def main(web):
    url = "http://www.google.com/ping?sitemap=https://{}/sitemap.xml".format(web)
    html = requests_url(url)
    if "successfully" in str(html):
        print("成功提交链接：{}".format(url))
    else:
        print("提交链接失败")



if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for web in web_list:
        try:
            analysis_html(web)
            main(web)
        except Exception as e:
            print("错误",web,e)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)



