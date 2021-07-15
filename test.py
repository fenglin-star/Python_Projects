import requests
import json
payload = {"key":"iDetkOys"}
header = {
        "Host":"api.hostmonit.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Accept":"application/json, text/plain, */*",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding":"gzip, deflate, br",
        "Content-Type":"application/json;charset=utf-8",
        "Content-Length":"18",
        "Origin":"https://stock.hostmonit.com",
        "Connection":"keep-alive",
        "Referer":"https://stock.hostmonit.com/",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-site",
        "Cache-Control":"max-age=0",
}
# 字典转换为json串
data = json.dumps(payload)
url = 'https://api.hostmonit.com/get_optimization_ip'
res = requests.post(url,data=data,headers=header)
new_ip = json.loads(res.text).get('info')[0].get('ip')
print(new_ip)
