#coding=utf-8
from urllib import parse
import random,time
import requests
from requests.adapters import HTTPAdapter
import json
from multiprocessing import Pool


list = []
# 随机UserAgent



def requests_res(url,proxies):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            headers = {
                "Host":"api.nike.com",
                "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
                "Accept":"*/*",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding":"gzip, deflate, br",
                "Referer":"https://www.nike.com/cn/w/mens-running-shoes-37v7jznik1zy7ok",
                "Origin":"https://www.nike.com",
            }
            # requests 设置最多5次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            response = s.get(url,headers=headers, proxies=proxies, timeout=25)
            response .encoding = response .apparent_encoding
            html = response.text
            return html
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


if __name__ == '__main__':
    url='https://api.nike.com/cic/browse/v1?queryid=products&anonymousId=BDD4D91C55A06C6D1886717FF2754DE2&country=cn&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(CN)%26filter%3Dlanguage(zh-Hans)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C49db2f3e-c999-48c2-b5b4-9296635ae75e)%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=zh-Hans&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    nike_json = requests_res(url, proxies='')
    data = json.loads(nike_json).get('data')
    print(len(data['products']['products']))
    for i in data['products']['products']:
        subtitle = "商品分类："+i['subtitle'] #商品分类
        title = "商品标题："+ i['title']  # 商品标题
        priceRangeCurrent = "商品价格："+ i['priceRangeCurrent']  # 商品价格
        url = "商品购买链接："+ i['url']  # 商品价格
        print(subtitle,"    ",title,"    " + priceRangeCurrent,"    " + url)




# def main(i):
#     # 如果遇到错误就出试5次
#     success_num = 0
#     while success_num < 5:
#         try:
#             proxies = {'http': '159.75.5.165:10808','https': '159.75.5.165:10808',}
#             res = requests_res("http://ip-api.com/json/?lang=zh-CN",proxies)
#             # list.append(str(json.loads(res).get('query')))
#             print(i,json.loads(res).get('query'),json.loads(res).get('country'),json.loads(res).get('regionName'))
#             break
#
#         except Exception as e:
#             print("正在重试:", e)
#             success_num = success_num + 1
#             continue
#
#
# if __name__ == '__main__':
#     pool = Pool()
#     for i in range(0,100):
#         pool.apply_async(func=main, args=(i,))  # 多进程运行
#     pool.close()
#     pool.join()
#
#     # print(len(set(list)))
    # print(set(list))