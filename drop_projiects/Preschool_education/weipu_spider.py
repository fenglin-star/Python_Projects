#coding=utf-8
from urllib import parse
import random,time
import requests
import re,sys,os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
from python_def.Mysqldb_server import mysql_url,read_mysql
from requests.adapters import HTTPAdapter


#config 设置部分,0为不延时运行
config_sleep = 2

#本地MySQL
host = '127.0.0.1'
port = 3306  # 端口号
user = 'python_use'  # 用户名
password = "kPXHsC2pSECsXxNF"  # 密码
db = "python_use"  # 库
table = "shishengguanxi"  # 表


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
path_txt =  table + ".txt"


# 下载一个页面中的文章URL
def selenium_urls(url):
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
            html = browser.page_source
            browser.close()
            return html
            break

        except Exception as e:
            browser.close()
            print("正在重试:", e)
            success_num = success_num + 1
            continue


def download_urls(url):
    html = selenium_urls(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    urls = body.select('table > tbody > tr:nth-child(1) > th > a')
    for i in urls:
        i = str(i.get('href'))
        url = parse.urljoin(url, i)
        yield url


def re_urlhtml(url):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
            }
            html = requests.get(url,headers=header, timeout=30)
            html.encoding = html.apparent_encoding
            html = html.text
            return html
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


# BS4解析页面HTML，提取关键元素
def analysis(url):
    html = re_urlhtml(url)
    soup = BeautifulSoup(html,'lxml')
    body = soup.body
    #去除a标签
    # [s.extract() for s in body("a")]
    [s.extract() for s in soup("script")]

    title = body.select('div.contains > span.detailtitle > h1')[0].get_text()  #标题

    # if key_paper in str(title_contents):
    txt_contents = body.select('span.detailtitle > strong > i > a:nth-child(1)')[0].get_text()
    # print(txt_contents)
    fabiaoqikan = re.search("《.*?》",txt_contents).group(0)    #发表期刊
    fabiaonianfen = re.search("\d{4}年", txt_contents).group(0)   #发表年份

    txt_keys = re.search('''<b class="black">【关键词】.*?</a> </td>''',str(soup)).group(0)
    qikan_keys = BeautifulSoup(txt_keys, 'lxml').select("a")# 关键词
    qikan_key = ""
    for i in qikan_keys:
        i = i.get_text()
        qikan_key = qikan_key +"|" + i

    qikan_zaiyao = body.select('.sum')[1] .get_text() # 摘要

    return_mysql = mysql_url(url=url,biaoti=title,fabiaoqikan=fabiaoqikan,
                             fabiaonianfen=fabiaonianfen,qikan_keys=qikan_key,
                             qikan_zaiyao=qikan_zaiyao,host=host,port=port,user=user,password=password,db=db,table=table)
    if return_mysql == 0:
        print("数据库中已存在，未插入数据")
    else:
        pass


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # #获取全部的URL链接
    k = "师生关系"
    urls = "http://www.cqvip.com/main/search.aspx?p={}&k={}"
    pool = Pool()
    for i in range(290,590):
        url = urls.format(i,k)
        print("第",i,"页：",url)
        for url in download_urls(url):
            try:
                pool.apply_async(analysis,args=(url,))  # 多进程运行
            except Exception as e:
                print(e)
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n","开始时间：", start_time + "\n" + "结束时间：", end_time)