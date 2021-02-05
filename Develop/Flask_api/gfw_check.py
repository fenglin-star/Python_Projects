#-*-coding: utf-8-*-
# 创建时间: 2021/1/9
import time
import requests
import random
from requests.adapters import HTTPAdapter
import json
from clark_demo.mail_send import send_usermail
import codecs


def requests_res(url,proxies=""):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            headers =  {
                "Host":"check.fanghong.net",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding":"gzip, deflate, br",
                "Referer":"https://check.fanghong.net/",
                "X-Requested-With":"XMLHttpRequest",
                "Connection":"keep-alive",
                "Cookie":"Hm_lvt_21835ff7f48811b07e89eee6b586bf80=1610016352,1610156000; Hm_lpvt_21835ff7f48811b07e89eee6b586bf80=1610156000",
                "TE":"Trailers",
                "Pragma":"no-cache",
                "Cache-Control":"no-cache",
                }
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(url,headers=headers, proxies=proxies, timeout=25)
            response.encoding = 'utf-8'
            html = codecs.decode(response.text,'unicode_escape')
            return html
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


def gfw_requests(host):
    url = 'https://check.fanghong.net/api/wr.php?url='+ host
    # 随机UA
    res_json = json.dumps(requests_res(url), ensure_ascii=False)
    return res_json


if __name__ == '__main__':
    domain = [
        'fangzhou.link',
        'fangzhou.202014.xyz',
        'fangzhou.world',
        # 'fangzhou.cloud', #已污染
        'www.jingjiniao.info',
    ]

    for host in domain:
        gfw = gfw_requests(host)
        if "已污染" in gfw:
            print("已污染",gfw)
            send_usermail('网站检测', str(gfw), "1094470534@qq.com")
        else:
            print("无事",gfw)

