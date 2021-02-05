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



# 百度知道日报 https://zhidao.baidu.com/daily/square
def analysis_baidu(url):
    html = requests_res(url)
    # html.encoding = "gbk"
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

    if len(txt_contents) < 400 or "�" in str(html):
        print("无法识别的文章：", url)

    else:
        # 获取标题
        title_content = str(body.select('#daily-title')[0].get_text()).replace("\n", "")


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
            wppost_status = "draft" # publish：已发布   pending：等待复审  draft：草稿
            wordpress_artice(wppost_status, wp_title, wp_slug_title, wp_content, wp_category, wp_post_tag,
                             wp_host, wp_user, wp_password)
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


def main(url):
    data_txt_html = analysis_baidu(url)
    write_wp(data_txt_html)


if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取全部的URL链接
    pool = Pool()
    for i in range(220000, 220200):
        url = "https://zhidao.baidu.com/daily/view?id={}".format(i)
        pool.apply_async(func=main, args=(url,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)

    # main("https://zhidao.baidu.com/daily/view?id=220000")