#coding=utf-8
import re
import requests
from urllib.parse import quote,unquote
from config import *

def download_urls(url):
    header = {
        "GET": url,
        "Host": "www.google.com",
        "referer": "https://www.google.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }

    html = requests.get(url,headers=header)
    # print(html.encoding)
    html.encoding = html.encoding
    html = html.text
    # print(html)
    return html


def google_association(key):
    key = quote(key)
    URLS = "https://www.google.com/complete/search?q={}&cp=3&client=psy-ab&xssi=t&gs_ri=gws-wiz&hl=en-hk&authuser=0&psi=sdLEXtLBF5WchwOu5I-4CA.1589957299119&ei=sdLEXtLBF5WchwOu5I-4CA"
    URL = URLS.format(key)
    txt = download_urls(URL).replace("[","").replace("0]","").replace(")]}'","").replace("]","").replace(",,",",")
    re_compile = ''',{".*?"}'''
    txt = re.sub(re_compile,"", txt)
    txt = txt.split(",")
    keytxt = txt[0:5]
    enkeys = []

    for i in keytxt:
        i = i.encode('utf-8').decode('unicode_escape')
        i = re.sub(r"<(\S*?)[^>]*>.*?|<.*? />", "", i)
        i = i.replace('''"''',"").replace('''\n''',"")
        if len(i) <=3:
            pass
        else:
            enkeys.append(i)

    if "Error" in str(enkeys):
        return []
    else:
        return enkeys


if __name__ == '__main__':
    key = "WordPress"
    print(google_association(key))
    # for i in google_association(key):
    #     print(i)

