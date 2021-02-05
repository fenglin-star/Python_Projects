#-*-coding: utf-8-*-
from clark_demo.import_config import *
from clark_demo.customize_request import *
import requests
from bs4 import BeautifulSoup
from clark_demo.caiyun_translate import *
from clark_demo.Mysqldb_server import mysql_url,read_mysql
from clark_demo.post_wordpress import wordpress_artice
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
from zhconv import convert
import redis


def get_complete_url(base_url):
    html = requests_res(base_url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    #关键词抽取
    urls = []
    for i in body.select('header > h3 > a'):
        i = i.get('href')
        url = parse.urljoin(base_url, i)
        urls.append(url)
    return urls


# 程序员大本营 https://www.pianshen.com/
def analysis_pianshen_com(url):
    html = requests_res(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    # 去除a标签
    # [s.extract() for s in body("a")]
    [s.extract() for s in soup("script")]

    # replace with `soup.findAll` if you are using BeautifulSoup3  去掉不想要的class元素
    for div in soup.find_all("div", {'class': 'gl_wk'}):
        div.decompose()

    # 获取标题
    title_content = str(body.select('div.col-md-8 > h2 > span')[0].get_text()).replace("\n", "")

    # 获取文本内容
    Articles_contents = str(body.select('#article_content')[0])

    # 获取分类
    all_art = "技术博客"
    category_list = [all_art]

    #关键词抽取
    post_tag = []
    for i in body.select('div.col-md-8 > p > a'):
        post_tag.append(i.get_text())

    data_txt_html = [title_content, Articles_contents, category_list, post_tag]
    return data_txt_html


def write_wp(data_txt_html):
    # config WP 连接设置部分
    wp_host = 'https://knstack.com/xmlrpc2020.php'
    wp_user = 'Author'
    wp_password = 'kZBHKNVlKObpe@v@BA' #wp默认密码

    list_contexts = data_txt_html
    wp_title = list_contexts[0]
    wp_content = list_contexts[1]
    wp_category = list_contexts[2]
    wp_post_tag = list_contexts[3]

    success_num = 0
    while success_num < 5:
        try:
            wp_slug_title = caiyun_translate_txt(language="en", source=wp_title)
            wppost_status = "draft"  # publish：已发布   pending：等待复审  draft：草稿
            wordpress_artice(wppost_status, wp_title, wp_slug_title, wp_content, wp_category, wp_post_tag,
                             wp_host, wp_user, wp_password)
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


def main(base_url):
    for url in get_urls(base_url):
        data_txt_html = analysis_pianshen_com(url)
        write_wp(data_txt_html)


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取全部的URL链接
    pool = Pool()
    for i in range(1,12):
        url = "https://www.pianshen.com/list/{}/".format(i)
        pool.apply_async(func=main, args=(url,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)