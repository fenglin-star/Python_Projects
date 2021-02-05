#coding=utf-8
import requests
import json
import random
import sys
from html.parser import HTMLParser
import re
from mail_send import send_usermail


#彩云小译API tokens，每个每月100字符，超过就无法使用
tokens = [
    "nayce5w4niupbzt7suwv", "oqbk1rmv5klxnunzll9h", "r9f3au6ewp3n21bq2ow9",
    "jqwp6km1cmuh0mc499je", "heh7enay4t0l68w8siyl", "zj0sqg5tpirb873voao2",
    "a8qjh8gins07q72qz2ww", "kbymilu02yje537nxrls", "d3xnbflunxut3hl2i0jv",
    "6se8xvgeeeceyq5cf889", "oo0qkkory6t37b4n55bd", "9sk3sdtwz9afpmkuxe1g",
    "p2j92sxjsrwetvveblwu","8j4802tg30z6xlxks3du","f0fd7fm8e3b823nd4v57",
    "pgbsrsurz2zx36y7xg45","r3f6b9h1j8mej5jeolev"
          ]

def tranlate_tokes(language,token,source):
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    # WARNING, this token is a test token for new developers, and it should be replaced by your token
    payload = {
        "source": source,
        # 中to英 zh2en     中to日 zh2ja   auto自动识别源语言
        "trans_type": "auto2{}".format(language),
        "request_id": "demo",
        "detect": True,
    }
    headers = {
        'content-type': "application/json",
        'x-authorization': "token " + token,
    }

    response = requests.request("POST",url,data=json.dumps(payload), headers=headers,timeout=30)
    return json.loads(response.text)['target']



def caiyun_translate_list(language,source):
    try:
        i = 1
        while i < 20:
            token = random.choice(tokens)
            try:
                target = tranlate_tokes(language,token,source)
                return target
                break

            except (KeyError, TypeError) as e:
                print(e,"删除无效toke：", token)
                tokens.remove(token)
                # print(tokens,"  错误代码：",e)
                continue
    except IndexError as e:
        print("所有的彩云小译api都已用完，程序结束")
        send_usermail("所有的彩云小译api都已用完，程序结束","所有的彩云小译api都已用完，程序结束","1094470534@qq.com")
        sys.exit()


def caiyun_translate_txt(language,source):
    list_txt = [source]
    entxts = caiyun_translate_list(language,list_txt)
    entxt = entxts[0]
    return entxt


def tj_tokes(language,source):
    try:
        i = 1
        while i < 20:
            i = i +1
            token = random.choice(tokens)
            try:
                target = tranlate_tokes(language,token,source)
                print("有效toke：", token ,target)
                pass

            except (KeyError, TypeError) as e:
                tokens.remove(token)
                # print(tokens,"  错误代码：",e)
                continue

    except IndexError as e:
        print("所有的彩云小译api都已用完，程序结束")
        send_usermail("所有的彩云小译api都已用完，程序结束","所有的彩云小译api都已用完，程序结束","1094470534@qq.com")
        sys.exit()


class MyHTMLParser(HTMLParser):
    def __init__(self,):
        self.d = []
        super().__init__()

    def handle_data(self, data):
        data = data.strip() # 去空格
        if len(data)== 0:
            pass
        else:
            self.d.append(data)
            print(data)

    def return_data(self):
        return self.d


def parse_html_zh2en(language,source):
    html = source
    parser = MyHTMLParser()
    parser.feed(html)
    html_list = parser.return_data()
    en_html_list = caiyun_translate_list(language,html_list)

    new_html = html
    for cn,en in zip(html_list,en_html_list):
        html = new_html
        new_html = html.replace(cn,en,1)

    return new_html


def sub_biaoqian_en2zh(language,source):
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

    #调用彩云小译代码Api翻译HTML
    parser = MyHTMLParser()
    parser.feed(html)
    html_list = parser.return_data()
    en_html_list = caiyun_translate_list(language,html_list)
    for cn, en in zip(html_list, en_html_list):
        html = new_html
        new_html = html.replace(cn, en, 1)


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
    #文本翻译
    print(caiyun_translate_txt(language="ja",source="测试"))

    #列表翻译
    print(caiyun_translate_list(language="ja",source=["Toke“”测试，"]))

    # html 翻译
    html = '''
<p>To save typing, you can import the <code>datetime</code> object from the <code>datetime</code> module:</p>
        '''
    new_html = sub_biaoqian_en2zh(language="zh",source=html)
    print(new_html)

    tj_tokes(language="ja",source=["测试"])