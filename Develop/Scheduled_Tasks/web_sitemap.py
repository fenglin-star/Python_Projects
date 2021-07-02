        # coding=utf-8
import os
import time
import random


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.html'):
                fullname = os.path.join(root,f)
                yield fullname


def write_head(f):
    with open(f, "a", encoding="utf-8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
        file.write('''<?xml version="1.0" encoding="UTF-8"?>
    <urlset
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
           http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    >''' + "\n" + "\n")


def write_foot(f):
    with open(f, "a", encoding="utf-8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
        file.write('''</urlset>''' + "\n" + "\n")


def write_body(i,f):
  # sitemap 开头
    if "index.html" in str(i):
            print(i)
            priority = 1.0
    else:
        prioritys = [0.3, 0.4, 0.5, 0.6, 0.7]
        priority = random.choice(prioritys)
    i = str(i).replace(base,web_url)
    with open(f, "a", encoding="utf-8") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
        sitemap = '''<url>
 <loc>{}</loc>
 <priority>{}</priority>
 <lastmod>{}</lastmod>
 <changefreq>{}</changefreq>
</url>'''
        file.write(sitemap.format(i,priority,lastmod,weekly) + "\n"+ "\n")


if __name__ == '__main__':
    datatime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    base = str(os.getcwd()) + "/"
    # base = r"/www/wwwroot/panel_ssl_site/data/User/admin/home/desktop/panel_ssl_site/translate_Web/Pending/tw.plantswiki.net" + "/"
    web_url = "https://tw.plantswiki.net/"

    lastmod = datatime
    weekly = 'weekly'

    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    f = base  + "sitemap.xml"
    if os.path.exists(f):
        os.remove(f)

    files = findAllFile(base)
    num = 0
    for i in files:
        num = int(num) + int(1)
    print(num)

    write_head(f)
    for i in files:
        write_body(i, f)
    write_foot(f)

    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("开始时间：",start_time + "\n" + "结束时间：",end_time )
    print("生成地图：",web_url + "sitemap.xml" )
    print('sitemap:',f)

