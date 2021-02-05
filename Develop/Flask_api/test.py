# #-*-coding: utf-8-*-
# # 创建时间: 2021/1/4
#
# # from google_trans_new import google_translator
# #
# # translator = google_translator()
# # translate_text = translator.translate('สวัสดีจีน', lang_tgt='en')
# # print(translate_text)
# #
# #
# #
# # from google_trans_new import google_translator
# #
# # # You can set the url_suffix according to your country. You can set url_suffix="hk" if you are in hong kong,url_suffix use in https://translate.google.{url_suffix}/
# # # If you want use proxy, you can set proxies like proxies={'http':'xxx.xxx.xxx.xxx:xxxx','https':'xxx.xxx.xxx.xxx:xxxx'}
# # translator = google_translator(url_suffix="hk",timeout=20,proxies={'http': '159.75.5.165:10808','https':'159.75.5.165:10808',})
# # # <Translator url_suffix=cn timeout=5 proxies={'http':'xxx.xxx.xxx.xxx:xxxx','https':'xxx.xxx.xxx.xxx:xxxx'}>
# # #  default parameter : url_suffix="cn" timeout=5 proxies={}
# # translate_text = translator.translate('สวัสดีจีน',lang_tgt='zh')
# # # <Translate text=สวัสดีจีน lang_tgt=th lang_src=zh>
# # #  default parameter : lang_src=auto lang_tgt=auto
# # #  API can automatically identify the src translation language, so you don’t need to set lang_src
# # print(translate_text)
# #
# #
# #
# # from google_trans_new import google_translator
# #
# # detector = google_translator()
# # detect_result = detector.detect('测试')
# # # <Detect text=สวัสดีจีน >
# # print(detect_result)
#
#
# #coding=utf-8
# # import requests
# # import json
# # import random
# # import sys
# # from html.parser import HTMLParser
# # import re
# # from clark_demo.mail_send import send_usermail
# #
# #
# # class MyHTMLParser(HTMLParser):
# #     def __init__(self,):
# #         self.d = []
# #         super().__init__()
# #
# #     def handle_data(self, data):
# #         data = data.strip() # 去空格
# #         if len(data)== 0:
# #             pass
# #         else:
# #             self.d.append(data)
# #             # print(data)
# #
# #     def return_data(self):
# #         return self.d
# #
# #
# # html = '''
# #     1，有直达公交(不堵车，有空位)或直达地铁，单程 1 小时-1.5 小时。可以在座位上看书或看视频，不算浪费时间。只要不至于早上太早起床就行。<br>
# #     2，骑自行车，10km，单程 40 <a0_biaoqian>。太远就太累了。<br>
# #     3，开车，单程 20 分钟。我宁愿坐 1 小时地铁也不开车——开车太浪费时间，啥也干不了。<br>
# #     4，公交太堵或者没空位，单程最多半小时。再长换交通工具。<br>
# #      '''
# #
# # parser = MyHTMLParser()
# # parser.feed(html)
# # html_list = parser.return_data()
# # for cn in html_list:
# #     print(cn)
# #     print("------")
# #
# #
# # def post_translate(language,source):
# #
# #     post_data = {
# #         "token": "202014xyz",
# #         "translate_type": "html",  # 替换HTML
# #         # "translate_type": "list",  #替换List
# #         "source":source,
# #     }
#
#
# # def list_to_str(source):
# #     # 解析list 转为flask能接受的str
# #     data = ''
# #     for i in source:
# #         data = data + '*|*|*|*' + i
# #     return data
# #
# #
# # def str_to_list(source):
# #     # 解析str，转换为list
# #     datas = source.replace("*|*|*|*", "", 1).split("*|*|*|*")
# #     return datas
# #
# #
# # source = ['单程 1 小时-1.5 小时。','可以在座位上看书或看视频，']
# # source = list_to_str(source)
# # print(source)
# #
# # source = str_to_list(source)
# # print(source)
# #
#
# from multiprocessing import Pool
# import requests
# from requests.adapters import HTTPAdapter
#
#
# def post_caiyun_translate(language,source):
#     post_data = {
#         "token": '202014xyz',
#         "language": language,
#         "source": source,
#     }
#
#     # requests 设置最多五次超时
#     s = requests.Session()
#     s.mount('http://', HTTPAdapter(max_retries=5))
#     s.mount('https://', HTTPAdapter(max_retries=5))
#     res = s.post(
#         url="https://hk-api.202014.xyz/translate-caiyun",  # 翻译
#         data=post_data,timeout=120,)
#
#     data_txt = res.text
#     return data_txt
#
#
#
# def main(source):
#     # num = str(source[0] + post_caiyun_translate(language = "en",source=source[1]))
#     # # range_list.append(num)
#     # print(num)
#     print(source[0],post_caiyun_translate(language = "en",source=source[1]))
#
#
# if __name__ == '__main__':
#     pool = Pool()
#     for i in range(20):
#         # 因为无法post列表字符，所以先转为str，后端再解析
#         source = [i,"长沙衡远网络科技有限公司"]
#         pool.apply(func=main, args=(source,))  # 多进程运行,apply()阻塞版本,apply_async()并行版本
#     pool.close()
#     pool.join()
#
#     # print(range_list)
#

# print(len("4，公交太堵或者没空位，单程最多半小时。再长换交通工具。<br>"))

import asyncio
import async_google_trans_new


# async def coro():
#     g = async_google_trans_new.google_translator()
#     print(await g.translate("こんにちは、世界！","en"))
# loop=asyncio.get_event_loop()
# loop.run_until_complete(coro())



import asyncio
from async_google_trans_new import google_translator

async def coro(texts):
    # g = google_translator(url_suffix="com",timeout=25,proxies={'http':'159.75.5.165:10808','https': '159.75.5.165:10808',})
    
    g = google_translator(url_suffix="cn")
    gathers = []
    for text in texts:
        gathers.append(g.translate(text, "en"))

    return await asyncio.gather(*gathers)

def main(texts):
    loop=asyncio.get_event_loop()
    print(loop.run_until_complete(coro(texts)))



if __name__ == '__main__':
    texts = ["一师范1", "第一师范2", "一师范3", "第一师范4", "一师范5", "第一师范6", "一师范7", "第一师范8", "一师范9", "第一师范10", "一师范11", "第一师范12",
             "一师范13", "第一师范99", "一师范1", "第一师范2", "一师范3", "第一师范4", "一师范5", "第一师范6", "一师范7", "第一师范8", "一师范9", "第一师范10", "一师范11", "第一师范12",
             "一师范13", "第一师范99","一师范1", "第一师范2", "一师范3", "第一师范4", "一师范5", "第一师范6", "一师范7", "第一师范8", "一师范9", "第一师范10", "一师范11", "第一师范12",
             "一师范13", "第一师范99","一师范1", "第一师范2", "一师范3", "第一师范4", "一师范5", "第一师范6", "一师范7", "第一师范8", "一师范9", "第一师范10", "一师范11", "第一师范12",
             "一师范13", "第一师范99","一师范1", "第一师范2", "一师范3", "第一师范4", "一师范5", "第一师范6", "一师范7", "第一师范8", "一师范9", "第一师范10", "一师范11", "第一师范12",
             "一师范13", "第一师范99",]

    for i in range(0,100):
        main(texts)