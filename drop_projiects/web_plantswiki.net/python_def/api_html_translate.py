#-*-coding: utf-8-*-
import requests
import json,time
from multiprocessing import Pool
from requests.adapters import HTTPAdapter


# 解析list 转为flask能接受的str
def parse_list(data_list):
    data = ''
    for i in data_list:
        data = data+'*|||*'+i
    return data


def html_translate(wp_content):
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {"wp_content": wp_content,}
            # requests 设置最多五次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            res = s.post(
                url="http://translation.202014.xyz/html/en",  # HTML文本翻译
                data=post_data,timeout=60,)
            data_txt =json.loads(res.text).get('wp_content')
            return data_txt


        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


def txt_translate(wp_content):
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {"wp_content": wp_content,}
            # requests 设置最多五次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            res = s.post(
                url="http://translation.202014.xyz/translate/en",  # HTML文本翻译
                data=post_data,timeout=60,)
            data_txt =json.loads(res.text).get('wp_content')
            return data_txt


        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


def list_txt_translate(wp_content):
    wp_content = parse_list(wp_content)
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {"wp_content": wp_content,}
            # requests 设置最多五次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            res = s.post(
                url="http://translation.202014.xyz/translate_list/en",  # list文本翻译
                data=post_data,timeout=60,)
            data_txt =json.loads(res.text).get('wp_content')
            return data_txt

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


def main(wp_content):
    data_txt = html_translate(wp_content)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),data_txt)

if __name__ == '__main__':
    pool = Pool(1)
    for i in range(10):
        wp_content = "软件程序,程序员,创业公司,中国共产党,长沙衡远网络科技有限公司"
        # 因为无法post列表字符，所以先转为str，后端再解析
        # wp_content = ["软件程序","程序员","创业公司","中国共产党","长沙衡远网络科技有限公司"]
        pool.apply_async(func=main, args=(wp_content,))  # 多进程运行
    pool.close()
    pool.join()