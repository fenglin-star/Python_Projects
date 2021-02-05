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


def get_urls(base_url):
    html = requests_res(base_url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    #关键词抽取
    urls = []
    for i in body.select('div.look.wb.mb.bh > div:nth-child(2) > ul > li > a'):
        i = i.get('href')
        url = parse.urljoin(base_url, i)
        urls.append(url)
    return urls


def get_page_url(urls):
    html = requests_res(urls)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    for i in body.select('div.list_msg_top > h2 > a'):
        i = i.get('href')
        url = parse.urljoin(urls, i)
        yield url



# 植物百科 https://www.zw3e.com/
def analysis_zw3e_com(url):
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
    title_content = str(body.select('.hd > h1')[0].get_text()).replace("\n", "")

    # 获取文本内容
    Articles_contents = str(body.select('.con_body')[0])

    # 获取分类
    all_art = "植物百科"
    category_list = [all_art]

    #关键词抽取
    # post_tag = analyse_post_tag(title_content, file_name=stop_text_path) # 基于TextRank算法分析标题进行关键词抽取
    post_tag = []
    for i in body.select('.key>a'):
        post_tag.append(str(i.get_text()).replace(" ",""))

    data_txt_html = [title_content, Articles_contents, category_list, post_tag]
    return data_txt_html



def write_wp(data_txt_html):
    # config WP 连接设置部分
    wp_host = 'https://plantswiki.net/xmlrpc2020.php'
    wp_user = 'Author'
    wp_password = 'kZBHKNVlKObpe@v@BA'  # wp默认密码

    list_contexts = data_txt_html
    wp_title = list_contexts[0]
    wp_content = list_contexts[1]
    wp_category = list_contexts[2]
    wp_post_tag = list_contexts[3]

    success_num = 0
    while success_num < 5:
        try:
            wp_slug_title = caiyun_translate_txt(language="en", source=wp_title)
            wppost_status = "draft" # publish：已发布   pending：等待复审  draft：草稿
            wordpress_artice(wppost_status, wp_title, wp_slug_title, wp_content, wp_category, wp_post_tag,
                             wp_host, wp_user, wp_password)
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


def main(url):
    data_txt_html = analysis_zw3e_com(url)
    write_wp(data_txt_html)


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取全部的URL链接
    pool = Pool()
    base_url = "https://www.zw3e.com/zwdq/"
    for urls in get_urls(base_url)[0:150]:
        for i in get_page_url(urls):
            pool.apply_async(func=main, args=(i,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)