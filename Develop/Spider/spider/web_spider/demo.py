#-*-coding: utf-8-*-
from clark_demo.import_config import *
from clark_demo.customize_request import selenium_res,requests_res
import requests
from bs4 import BeautifulSoup
from clark_demo.caiyun_translate import *
from clark_demo.Mysqldb_server import mysql_url,read_mysql
from clark_demo.post_wordpress import wordpress_artice
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
from zhconv import convert
import redis


# MySQL数据库信息
host = '119.28.49.98'
port = 3306  # 端口号
user = 'web_demo'  # 用户名
password = "Nt3Lh5syNAKkbe6N"  # 密码
db = "web_demo"  # 库
table = "knstack"  # 表
charset = 'utf8'


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
    post_tag = analyse_post_tag(title_content, file_name=stop_text_path)
    data_category = str(body.select('#j-daily-union-dom > div.info > span:nth-child(1)')[0].get_text())
    # 发表日期也加入标签
    post_tag.append(str(data_category[0:4]))

    data_txt_html = [title_content, Articles_contents, category_list, post_tag]
    return data_txt_html



# 数据库去重、文本翻译、插入Redis列表
def main(url):
    # 请求网页内容并获取文本
    html = requests_res(url)
    html_data = analysis_html(html)

    # 以下是标题、文本内容、分类、标签
    wp_title = str(html_data[0])
    wp_slug_title = caiyun_translate_txt(wp_title)
    wp_content = '''<div class="wp_content_html">{}</div>'''.format(str(html_data[1]))
    wp_category = html_data[2]
    wp_post_tag = html_data[3]

    while success_num < 5:
        try:
            # publish：已发布   pending：等待复审  draft：草稿
            wppost_status = "publish"
            wordpress_artice(wppost_status, wp_title, wp_slug_title, wp_content, wp_category, wp_post_tag,
                             wp_host, wp_user, wp_password)
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取全部的URL链接
    pool = Pool()
    for i in range(71422, 71432):
        url = "https://zhidao.baidu.com/daily/view?id={}".format(i)
        pool.apply_async(func=main, args=(url,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)