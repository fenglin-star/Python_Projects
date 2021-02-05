# coding=utf-8
import requests
import json
import random
import sys
from html.parser import HTMLParser
import re
from clark_demo.mail_send import send_usermail


class MyHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def __init__(self, ):
        self.d = []
        super().__init__()

    def handle_data(self, data):
        data = data.strip()  # 去空格
        if len(data) == 0:
            pass
        else:
            self.d.append(data)
            # print(data)

    def return_data(self):
        return self.d


class Caiyun_tranlate(object):
    # 类的初始化
    def __init__(self, language, source):
        # 彩云小译API tokens，每个每月100字符，超过就无法使用
        self.tokens = [
            "nayce5w4niupbzt7suwv", "oqbk1rmv5klxnunzll9h", "r9f3au6ewp3n21bq2ow9",
            "jqwp6km1cmuh0mc499je", "heh7enay4t0l68w8siyl", "zj0sqg5tpirb873voao2",
            "a8qjh8gins07q72qz2ww", "kbymilu02yje537nxrls", "d3xnbflunxut3hl2i0jv",
            "6se8xvgeeeceyq5cf889", "oo0qkkory6t37b4n55bd", "9sk3sdtwz9afpmkuxe1g",
            "p2j92sxjsrwetvveblwu", "8j4802tg30z6xlxks3du", "f0fd7fm8e3b823nd4v57",
            "pgbsrsurz2zx36y7xg45", "r3f6b9h1j8mej5jeolev"
        ]

        self.language = language
        self.source = source


    def caiyun_base(self):
        url = "http://api.interpreter.caiyunai.com/v1/translator"
        # WARNING, this token is a test token for new developers, and it should be replaced by your token
        payload = {
            "source": self.source,
            # 中to英 zh2en     中to日 zh2ja   auto自动识别源语言
            "trans_type": "auto2{}".format(self.language),
            "request_id": "demo",
            "detect": True,
        }
        headers = {
            'content-type': "application/json",
            'x-authorization': "token " + random.choice(self.tokens),
        }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, timeout=30)
        return json.loads(response.text)['target']


    def caiyun_list(self):
        try:
            i = 1
            while i < 20:
                try:
                    tranlate = Caiyun_tranlate(self.language, self.source)
                    target = tranlate.caiyun_base()
                    return target
                    break

                except (KeyError, TypeError) as e:
                    print(e, "删除无效toke：", token)
                    self.tokens.remove(token)
                    # print(tokens,"  错误代码：",e)
                    continue

        except IndexError:
            print("所有的彩云小译api都已用完，程序结束")
            send_usermail(title="所有的彩云小译api都已用完，程序结束", mail_content="所有的彩云小译api都已用完，程序结束",
                          send_mail="1094470534@qq.com")
            sys.exit()


    def tj_tokes(self):
        try:
            i = 1
            while i < 20:
                i = i + 1
                token = random.choice(self.tokens)
                try:
                    tranlate = Caiyun_tranlate(self.language, self.source)
                    target = tranlate.caiyun_list()
                    print("有效toke：", token, target)
                    pass

                except (KeyError, TypeError) as e:
                    self.tokens.remove(token)
                    # print(tokens,"  错误代码：",e)
                    continue

        except IndexError as e:
            print("所有的彩云小译api都已用完，程序结束")
            send_usermail(title="所有的彩云小译api都已用完，程序结束", mail_content="所有的彩云小译api都已用完，程序结束")
            sys.exit()


# 通过标签替换来翻译HTML
def caiyun_translate(language, source):
    html = source
    new_html = html

    # 不翻译<a>标签中的内容
    a_list = re.findall(r'<a[\s\S]*?</a>', html)
    for i, o in zip(a_list, range(0, len(a_list))):
        o = "<a{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(i, o, 1)

    # 不翻译<code>标签中的内容
    code_list = re.findall(r'<code[\s\S]*?</code>', html)
    for i, o in zip(code_list, range(0, len(code_list))):
        o = "<code{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(i, o, 1)

    # 调用彩云小译代码Api翻译HTML
    parser = MyHTMLParser()
    parser.feed(new_html)
    html_list = parser.return_data()
    tranlate = Caiyun_tranlate(language=language, source=html_list)
    en_html_list = tranlate.caiyun_list()
    for cn, en in zip(html_list, en_html_list):
        html = new_html
        new_html = html.replace(cn, en, 1)
        # print(cn,"翻译内容：",en)

    # 把占位符替换回去
    for i, o in zip(a_list, range(0, len(a_list))):
        o = "<a{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(o, i, 1)

    for i, o in zip(code_list, range(0, len(code_list))):
        o = "<code{}_biaoqian>".format(o)
        html = new_html
        new_html = html.replace(o, i, 1)

    return new_html



if __name__ == '__main__':
    # data_str = ['1','有直达公交(不堵车，有空位)或直达地铁','单程 1 小时-1.5 小时。可以在座位上看书或看视频，不算浪费时间。只要不至于早上太早起床就行。']
    # # data_str = '有直达公交(不堵车，有空位)或直达地铁'
    # print(len(data_str))
    #
    # # 文本或列表翻译
    # tranlate = Caiyun_tranlate(language="en",source=data_str)
    # print(tranlate.caiyun_list())



    #
    # html 翻译
    html = '''
    1，有直达公交(不堵车，有空位)或直达地铁，单程 1 小时-1.5 小时。可以在座位上看书或看视频，不算浪费时间。只要不至于早上太早起床就行。<br>
    2，骑自行车，10km，单程 40 <a>分钟</a>。太远就太累了。<br>
    3，开车，单程 20 分钟。我宁愿坐 1 小时地铁也不开车——开车太浪费时间，啥也干不了。<br>
    4，公交太堵或者没空位，单程最多半小时。再长换交通工具。<br>
        '''
    new_html = sub_biaoqian_en2zh(language="en", source=html)
    print(new_html)

    tranlate = Caiyun_tranlate(language="en", source=["测试"])

    # tranlate.tj_tokes()
