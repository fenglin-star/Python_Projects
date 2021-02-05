#-*-coding: utf-8-*-
import time,random,datetime,os
import platform

# 查看系统类型
platform_ = platform.system()
is_win = is_linux = is_mac = False

if platform_ == "Windows":
    is_win = True
elif platform_ == "Linux":
    is_linux = True
elif platform_ == "Mac":
    is_mac = True


#config 设置部分,0为不延时运行
config_sleep = 1
html_base_Language = "zh-cn"

# 代理设置
proxies = {'http': '154.91.145.140:6666','https': '154.91.145.140:6666'} # 远程代理
# proxies = "" # 不使用代理

# print(proxies)

#config WP 连接设置部分
web_host = "https://wordpress.202014.xyz"
wp_host = '{}/xmlrpc2020.php'.format(web_host)
wp_user = 'root'
wp_password = 'kZBHKNVlKObpe@v@BA'


# 远程MySQL设置部分
host = '144.172.126.40'
port = 3306  # 端口号
user = 'google_tranlate'  # 用户名
password = "YAXYNmEeNRhcGbjD"  # 密码
db = "google_tranlate"  # 库
table = "en"  # 表


# 随机UserAgent
fake_UserAgent = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
]

