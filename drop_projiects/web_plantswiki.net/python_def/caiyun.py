#coding=utf-8
import requests
import json
import random
import sys


#彩云小译API tokens，每个每月100字符，超过就无法使用
tokens = [
    "nayce5w4niupbzt7suwv", "oqbk1rmv5klxnunzll9h", "r9f3au6ewp3n21bq2ow9",
    "jqwp6km1cmuh0mc499je", "heh7enay4t0l68w8siyl", "zj0sqg5tpirb873voao2",
    "a8qjh8gins07q72qz2ww", "kbymilu02yje537nxrls", "d3xnbflunxut3hl2i0jv",
    "6se8xvgeeeceyq5cf889", "oo0qkkory6t37b4n55bd", "9sk3sdtwz9afpmkuxe1g",
    "p2j92sxjsrwetvveblwu","8j4802tg30z6xlxks3du","f0fd7fm8e3b823nd4v57",
    "pgbsrsurz2zx36y7xg45","r3f6b9h1j8mej5jeolev"
          ]

def tranlate_tokes(token,source):
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    # WARNING, this token is a test token for new developers, and it should be replaced by your token
    payload = {
        "source": source,
        # 中to英 zh2en     中to日 zh2ja   auto自动识别源语言
        "trans_type": "auto2en",
        "request_id": "demo",
        "detect": True,
    }
    headers = {
        'content-type': "application/json",
        'x-authorization': "token " + token,
    }

    response = requests.request("POST",url,data=json.dumps(payload), headers=headers,timeout=30)
    return json.loads(response.text)['target']



def caiyun_translate_list(source):
    try:
        i = 1
        while i < 20:
            token = random.choice(tokens)
            try:
                target = tranlate_tokes(token, source)
                return target
                break

            except (KeyError, TypeError) as e:
                print(e,"删除无效toke：", token)
                tokens.remove(token)
                # print(tokens,"  错误代码：",e)
                continue
    except IndexError as e:
        print("所有的彩云小译api都已用完，程序结束")
        sys.exit()


def caiyun_translate_txt(txt):
    list_txt = [txt]
    entxts = caiyun_translate_list(list_txt)
    entxt = entxts[0]
    return entxt


def tj_tokes(source):
    try:
        i = 1
        while i < 20:
            i = i +1
            token = random.choice(tokens)
            try:
                target = tranlate_tokes(token,source)
                print("有效toke：", token ,target)
                pass

            except (KeyError, TypeError) as e:
                tokens.remove(token)
                # print(tokens,"  错误代码：",e)
                continue

    except IndexError as e:
        print("所有的彩云小译api都已用完，程序结束")
        sys.exit()



if __name__ == '__main__':
    #文本翻译
    print(caiyun_translate_txt("Toke测试，"))

    #列表翻译
    print(caiyun_translate_list(["Toke测试，"]))

