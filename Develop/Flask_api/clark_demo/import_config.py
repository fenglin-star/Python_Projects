#-*-coding: utf-8-*-
import time,random,datetime,os,re,sys
import jieba
from jieba import analyse


# 查看系统类型
import platform
platform_ = platform.system()
is_win = is_linux = is_mac = False

if platform_ == "Windows":
    is_win = True
elif platform_ == "Linux":
    is_linux = True
elif platform_ == "Mac":
    is_mac = True


# 引入TF-IDF关键词抽取接口
def analyse_post_tag(txt,file_name):
    textrank = jieba.analyse.tfidf
    jieba.analyse.set_stop_words(file_name)
    keywords = textrank(txt)
    post_tag = keywords[0:5]
    return post_tag


if is_win == True:
    stop_text_path = r"python_def/stop_text.txt"
elif is_linux == True:
    stop_text_path = r"/www/wwwroot/panel_ssl_site/web_shell/shell/stop_text.txt"

textrank = analyse.textrank




