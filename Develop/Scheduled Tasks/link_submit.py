#coding=utf-8
import requests
import re,os,sys
import datetime,time


# 下载一个页面中的文章URL
def download_urls(urls):

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    html = requests.get(urls,headers=header)
    html.encoding = html.apparent_encoding
    if html.content:
        html = html.text
        result = re.findall("<loc>(.*?)</loc>",html)
        for i in result:
            yield i


def txt_mian(urls):
    html = download_urls(urls)

    # 每个网站每天提交500个URL
    html_urls = list(html)[0:500]
    html_url = '|'.join(html_urls)

    proj_name = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    url = 'https://api.linkprocessor.net/api.php'
    s = {
        'apikey': '1455351661e404863bccaecd6106a232765fb947d774',
        'proj_name': proj_name,
        'dripfeed': '7',
        'urls': html_url,
    }
    r = requests.post(url, data=s)
    print(urls,r.text)




if __name__ == '__main__':
    web = "www.knowledgetrivia.net"
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if len(str(month)) == 1:
        month = "0" + str(month)
    base_urls = "https://{}/sitemap-pt-post-{}-{}.xml".format(web, year, month)

    urls = []
    for i in download_urls(base_urls):
        print(i)
        urls.append(i)

    print(len(urls))


    web_lists = open(r"web_list.txt", encoding="utf-8")
    web_list = []
    for line in web_lists:
        line = str(line).replace("\n", "")
        web_list.append(line)
    web_lists.close()

    webs = web_list
    nums = len(webs)
    print("本次执行的任务数：", nums)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    month2 = month - 1
    if len(str(month)) == 1:
        month = "0" + str(month)

    #获取上月的文章链接
    if len(str(month2)) == 1:
        month2 = "0" + str(month2)

    urls_list = []
    urls = "https://{}/sitemap-pt-post-{}-{}.xml"
    for i in webs:
        url1 = urls.format(i, year, month)
        url2 = urls.format(i, year, month2)
        urls_list.append(url1)
        # urls_list.append(url2)

    for i in urls_list:
        txt_mian(i)

