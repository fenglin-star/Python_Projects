#-*-coding: utf-8-*-
from html.parser import HTMLParser
import re



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
            print("Encountered some data:",data)

    def return_data(self):
        return self.d




html = '''

'''


def sub_biaoqian(html):
    new_a_html = html
    a_list = re.findall(r'<a[\s\S]*?</a>', html)
    a_biaoqian = zip(a_list,range(0,len(a_list)))
    for i,o in a_biaoqian:
        o = "<a{}_biaoqian>".format(o)
        html = new_a_html
        new_a_html = html.replace(i,o, 1)


    code_list = re.findall(r'<code[\s\S]*?</code>', html)
    code_biaoqian = zip(code_list,range(0,len(code_list)))
    for i,o in code_biaoqian:
        o = "<code{}_biaoqian>".format(o)
        html = new_a_html
        new_a_html = html.replace(i,o, 1)

    parser = MyHTMLParser()
    parser.feed(html)
    html_list = parser.return_data()
    en_html_list = caiyun_translate_list(html_list)
    for cn,en in zip(html_list,en_html_list):
        html = new_html
        new_html = html.replace(cn,en,1)

    for i,o in a_biaoqian:
        o = "<a{}_biaoqian>".format(o)
        html = new_a_html
        new_a_html = html.replace(o,i, 1)

    for i, o in code_biaoqian:
        o = "<code{}_biaoqian>".format(o)
        html = new_a_html
        new_a_html = html.replace(o,i, 1)

    return new_html


sub_biaoqian(html)