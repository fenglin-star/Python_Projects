#coding=utf-8
from urllib import parse
import random,time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
]


# 下载一个页面中的文章URL
def selenium_res(url):
    #如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            # 进入浏览器设置
            chrome_options = Options()

            # 无头模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

            # 设置中文
            chrome_options.add_argument('lang=zh_CN.UTF-8')
            browser = webdriver.Chrome(chrome_options=chrome_options)

            browser.set_page_load_timeout(30)  # 设置30秒超时等待
            browser.get(url)
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            html = browser.page_source
            browser.close()
            return html
            break

        except Exception as e:
            browser.close()
            print("正在重试:", e)
            success_num = success_num + 1
            continue



def requests_res(url,proxies):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            headers = {
                "user-agent": random.choice(fake_UserAgent)
            }
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(url,headers=headers, proxies=proxies, timeout=25)
            response .encoding = response .apparent_encoding
            html = response.text
            return html
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue

def requests_img(url,proxies):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            headers = {
                "user-agent": random.choice(fake_UserAgent)
            }
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(url,headers=headers, proxies=proxies, timeout=25)
            response .encoding = response .apparent_encoding
            return response
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


# 获取完整的url
# def get_complete_url(base_url):
#     html = requests_res(base_url)
#     soup = BeautifulSoup(html, 'lxml')
#     body = soup.body
#
#     #关键词抽取
#     urls = []
#     for i in body.select('header > h3 > a'):
#         i = i.get('href')
#         url = parse.urljoin(base_url, i)
#         urls.append(url)
#     return urls


def main(i):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            proxies = {'http': '159.75.5.165:10808','https': '159.75.5.165:10808',}
            res = requests_res("http://ip-api.com/json/?lang=zh-CN",proxies)
            # list.append(str(json.loads(res).get('query')))
            print(i,json.loads(res).get('query'),json.loads(res).get('country'),json.loads(res).get('regionName'))
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


if __name__ == '__main__':
    pool = Pool()
    for i in range(0,100):
        pool.apply_async(func=main, args=(i,))  # 多进程运行
    pool.close()
    pool.join()

    # print(len(set(list)))
    # print(set(list))