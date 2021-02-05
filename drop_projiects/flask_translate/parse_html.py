#-*-coding: utf-8-*-
from html.parser import HTMLParser
from caiyun import *
import re



class MyHTMLParser(HTMLParser):
    def __init__(self,):
        self.d = []
        super().__init__()

    def handle_data(self, data):
        if data =="\n":
            pass
        else:
            self.d.append(data)
            # print("Encountered some data  :", data)

    def return_data(self):
        return self.d


def parse_html_zh2en(html):
    parser = MyHTMLParser()
    parser.feed(html)
    html_list = parser.return_data()
    en_html_list = caiyun_translate_list(html_list)

    new_html = html
    for cn,en in zip(html_list,en_html_list):
        html = new_html
        new_html = html.replace(cn,en,1)

    return new_html



def sub_biaoqian_en2zh(html):
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
    en_html_list = caiyun_translate_list(html_list)
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
    html = '''
<p>To save typing, you can import the <code>datetime</code> object from the <code>datetime</code> module:</p>
    '''
    print(sub_biaoqian_en2zh(html))
    # print(re.sub("<(\S*?)[^>]*>.*?|<.*? />", "", new_html))