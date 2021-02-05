#-*-coding: utf-8-*-
import requests
import json,time,os
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
proxies = ""


def post_img(web_url):
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {"web_url": web_url,}
            # requests 设置最多五次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            res = s.post(
                url = "http://23.225.151.156:5200/img",
                # url="http://127.0.0.1:5200/img",
                data=post_data,timeout=60,)
            response =json.loads(res.text).get('return_web_url')
            print(response)
            return response

        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue



def test_401(url):
    r = requests.get(url)
    if r.status_code == 200:
        print("图片正常：",url)
    else:
        print("错误：",url)


def mian(IMAGE_URL):
    url = post_img(IMAGE_URL)
    time.sleep(5)
    test_401(url)


if __name__ == '__main__':
    pool = Pool(8)
    IMAGE_URL = "https://cdn.jsdelivr.net/gh/fenglin-cdn/jingjiniao.info/template/acgi_c1/images/c1bg_1.jpg"
    for i in range(200):
        pool.apply_async(func=mian, args=(IMAGE_URL,))  # 多进程运行

    pool.close()
    pool.join()

