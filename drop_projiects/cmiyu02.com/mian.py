#-*-coding: utf-8-*-
import requests
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from multiprocessing import Pool
from bs4 import BeautifulSoup
from config import *
import pymysql
from Mysqldb_server import write_mysql


# requests获取网页源码
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
            response = s.get(url,headers=headers, proxies=proxies, timeout=25)
            r_code = response.apparent_encoding

            #解决中文乱码问题
            if 'gbk' or 'GBK' in str(r_code):
                response.encoding = "gbk"
            else:
                response.encoding = response.apparent_encoding
            html = response.text
            return html
            break

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


# 获取各个分类第一列表页url
def frist_page_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    urls = body.select('body > div.miyuheader > ul > li > a')
    for i in urls:
        url = urljoin("http://www.cmiyu.com/",i['href'])
        yield url


# 获取下一列表页url
def next_page_url(url):
    html = requests_url(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    next_page = body.select('li.sy3 > a')
    for i in next_page:
        if i.get_text() == "下一页":
            return i['href']


# frist_page_urls + next_page_url 获取全部列表页url
def parse_all_page_urls(base_url):
    urls = []
    next_url = base_url
    while True:
        try:
            new_url = base_url + next_page_url(next_url)
            urls.append(new_url)
            next_url = new_url

        except Exception as e:
            print("分类URL已采集完毕")
            break
    print(urls)
    return urls


# 获取列表页中的文章页url
def parse_article_urls(url):
    html = requests_url(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    urls = body.select('div.list > ul > li > a')
    for i in urls:
        url = urljoin(url,i['href'])
        yield url


# 获取文章页中需要的文本
def parse_article_content(url,key):
    html = requests_url(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    md = body.select('div.md > h3')
    mimian = md[0].get_text()
    midi = md[1].get_text()
    try:
        xiaotieshi = body.select('div.zy > p')[0].get_text()
    except Exception as e:
        xiaotieshi = "暂无"
    md_data = [url,mimian,midi,xiaotieshi]
    if "�" in str(md_data):
        print("无法识别的字体：",md_data)
        pass
    else:
        #插入数据库
        url = md_data[0]
        mimian = md_data[1]
        midi = md_data[2]
        xiaotieshi = md_data[3]
        content = str(mimian + "|||" + midi + "|||" + xiaotieshi)
        return_mysql = write_mysql(url=url,title=key,content=content,
                host=host,port=port,user=user,password=password,db=db,table=table)
        if return_mysql == 0:
            print("数据库中已存在，未插入数据")
        else:
            pass


# 主运行程序，获取网站中所有需要的资料
def mian(key):
    base_url = "http://www.cmiyu.com/{}/".format(key)
    for url in parse_all_page_urls(base_url): # 全部列表页URL
        for article_url in parse_article_urls(url): # 全部列表页文章URL
            # print("开始任务：",article_url)
            try:
                parse_article_content(article_url,key)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    table_list = [
        "gxmy",
        "zmmy",
        "cymy",
        "dwmy",
        "aqmy",
        "dmmy",
        "rmmy",
        "dm",
        "cy",
        "dgmy",
        "ry",
        "etmy",
        "wpmy",
        "zwmy",
        "jmmy",
        "sbmy",
        "symy",
        "ypmy",
        "yymy",
        "ysmy",
        "cwmy",
        "qita",
    ]

    pool = Pool()
    for key in table_list:
        pool.apply_async(func=mian, args=(key,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)

