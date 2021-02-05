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
    # 基于TextRank算法分析标题进行关键词抽取
    post_tag = analyse_post_tag(title_content, file_name=stop_text_path)

    data_txt_html = [title_content, Articles_contents, category_list, post_tag]
    return data_txt_html


# VPS信号旗播报 https://www.vpsxhq.com/
def analysis_vpsxhq_com(url):
    html = requests_res(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    # 去除a标签
    # [s.extract() for s in body("a")]
    [s.extract() for s in soup("script")]

    # 获取标题
    title_content = str(body.select('.entry-title')[0].get_text()).replace("\n", "")

    # 获取文本内容
    Articles_contents = str(body.select('.entry-content')[0])

    # 获取分类
    all_art = "技术资讯"
    category_list = [all_art]

    #关键词抽取
    post_tag = []
    for i in body.select('.tags-links > a'):
        post_tag.append(i.get_text())

    data_txt_html = [title_content, Articles_contents, category_list, post_tag]
    return data_txt_html


# 百度知道日报 https://zhidao.baidu.com/daily/square
def analysis_baidu(url):
    html = requests_res(url)
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body

    # 去除a标签
    # [s.extract() for s in body("a")]
    [s.extract() for s in soup("script")]

    # replace with `soup.findAll` if you are using BeautifulSoup3  去掉不想要的class元素
    for div in soup.find_all("div", {'class': 'detail_statement article-source'}):
        div.decompose()

    # 获取文本内容
    txt_contents = str(body.select('#daily-cont')[0]).replace("百度", "好奇心百科")

    if "�" in str(html):
        print("无法识别的字体：", html)
        pass
    else:
        if len(txt_contents) < 400:
            print("空白文章：", url)
            pass
        else:
            # 获取标题
            title_content = str(body.select('.entry-title')[0].get_text()).replace("\n", "")


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



if __name__ == '__main__':
    url = "https://www.pianshen.com/article/32982043605/"
    print(analysis_pianshen_com(url))