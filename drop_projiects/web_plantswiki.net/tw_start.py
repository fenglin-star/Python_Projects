# coding=utf-8
from python_def.config import *
import requests
from bs4 import BeautifulSoup
from python_def.caiyun import *
from python_def.Mysqldb_server import mysql_url,read_mysql
from python_def.WordPress import wordpress_artice
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
from zhconv import convert
import redis

# MySQL设置部分
host = '23.225.151.156'
port = 33060  # 端口号
user = 'python_use'  # 用户名
password = "Nx5mnaADaw3CsGip"  # 密码
db = "python_use"  # 库
table = "curiositynews_tw"  # 表

# redis设置部分
rd = redis.Redis(host='23.225.151.156', port=16379,
                password='202014xyz', db=2)
redis_table = "curiositynews_tw"


# 下载一个页面HTML
def requests_download(url):
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
            html_content = response.text
            break

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue

    # 检测是否为空文本
    soup = BeautifulSoup(html_content, 'lxml')
    # replace with `soup.findAll` if you are using BeautifulSoup3
    for div in soup.find_all("div", {'class': 'detail_statement article-source'}):
        div.decompose()
    body = soup.body
    #去除a标签
    [s.extract() for s in body("a")]
    [s.extract() for s in body("script")]

    # 获取文本内容
    txt_contents = str(body.select('#daily-cont')[0]).replace("百度", "好奇心百科")

    if "�" in str(html_content):
        print("无法识别的字体：", html_content)
        pass
    else:
        if len(txt_contents) > 400:
            # print("\n", "开始任务：", url)
            return html_content
        else:
            print("空白文章：", url)



# BS4解析页面HTML，提取关键元素
def analysis_html(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    # 去除a标签
    # [s.extract() for s in body("a")]
    [s.extract() for s in soup("script")]

    # replace with `soup.findAll` if you are using BeautifulSoup3  去掉不想要的class元素
    for div in soup.find_all("div", {'class': 'detail_statement article-source'}):
        div.decompose()

    # 获取标题
    title_contents = body.select('#daily-title')
    title_content = title_contents[0].get_text()
    title_content = str(title_content).replace("\n", "")

    # 获取文本内容
    txt_contents = str(body.select('#daily-cont')[0])
    first_img_contents = str(body.select('#daily-img')[0]).replace("百度知道","Curiosity News").replace("百度","搜索引擎")
    Articles_contents = first_img_contents + txt_contents

    # 获取分类
    all_art = "百科"
    category_list = [all_art]

    # 基于TextRank算法分析标题进行关键词抽取
    post_tag = analyse_post_tag(title_content, file_name="../web01_curiositynews.net/python_def/stop_text.txt")
    data_category = str(body.select('#j-daily-union-dom > div.info > span:nth-child(1)')[0].get_text())
    # 发表日期也加入标签
    post_tag.append(str(data_category[0:4]))
    data_txt_html = [title_content, Articles_contents, category_list, post_tag]

    return data_txt_html


# 转换为繁体中文
def html_to_tw(data_txt_html):
    html_data = data_txt_html
    title_content = html_data[0]
    Articles_contents = html_data[1]
    category_list = html_data[2]
    post_tag = html_data[3]

    # 标题内容转换
    title_content = convert(title_content, "zh-tw")

    # 文本内容转换
    Articles_contents = convert(Articles_contents, "zh-tw")  # 繁体中文转换

    # 分类
    category_lists = []
    for category in category_list:
        category = convert(category, "zh-tw")
        category_lists.append(category)

    # 标签
    post_tags = []
    for tag in post_tag:
        tag = convert(tag, "zh-tw")
        post_tags.append(tag)

    tw_data_txt_html = [title_content, Articles_contents, category_lists, post_tags]
    return tw_data_txt_html


# 数据库去重、文本翻译、插入Redis列表
def main(url):
    # 请求网页内容并获取文本
    html = requests_download(url)
    base_html_data = analysis_html(html)
    html_data = html_to_tw(base_html_data)

    # 以下是标题、文本内容、分类、标签
    wp_title = str(html_data[0])
    wp_slug_title = caiyun_translate_txt(wp_title)
    wp_content = '''<div class="wp_content_html">{}</div>'''.format(str(html_data[1]))
    wp_category = html_data[2]
    wp_post_tag = html_data[3]

    content = str(wp_title +"|||" + wp_slug_title +"|||" + wp_content + "|||"+ str(wp_category) + "|||"+ str(wp_post_tag))
    # 数据库去重，以url为标记值，0表示数据库已存在链接，1表示之前没有存在。
    # return_mysql = mysql_url(url=url,title=wp_title,content=content,host=host,port=port,user=user,password=password,db=db,table=table)
    return_mysql = 2
    if return_mysql == 0:
        print("数据库中已存在，未插入数据:", wp_title, url)
    else:
        # 插入redis列表，如果遇到错误就重试5次
        success_num = 0
        while success_num < 5:
            try:
                rd.lpush(redis_table,content)
                print("插入成功", wp_title, url)
                break

            except Exception as e:
                print("正在重试:",e)
                success_num = success_num + 1
                continue



if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取全部的URL链接
    pool = Pool()
    # for i in range(24610,24612):
    for i in range(71422, 71432):
        url = "https://zhidao.baidu.com/daily/view?id={}".format(i)
        pool.apply_async(func=main, args=(url,))  # 多进程运行
    pool.close()
    pool.join()



    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)