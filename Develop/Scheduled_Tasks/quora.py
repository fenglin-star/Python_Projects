import requests

# 下载一个页面中的文章URL
def download_urls(url):

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    html = requests.get(url,headers=header)
    html.encoding = html.apparent_encoding
    if html.content:
        html = html.text
        print(html)

if __name__ == '__main__':
    url = "http://google.com/search?q={}&sourceid=chrome&ie=UTF-8"
    url = url.format("Is Rhinitis very difficult to treat?site:www.quora.com")
    print(url)
    download_urls(url)
    "# rso > div:nth-child(1) > div > div.r > a > h3"
    "match-mod-horizontal-padding hide-focus-ring cbphWd"