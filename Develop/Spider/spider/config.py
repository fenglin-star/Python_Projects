#-*-coding: utf-8-*-
import redis,pymysql
import time

# 爬虫代理设置
proxies = ""  # 不使用代理

# 数据库连接
host = '119.28.49.98'
port = 3306  # 端口号
user = 'python_use'  # 用户名
password = "Nx5mnaADaw3CsGip"  # 密码
db = "python_use"  # 库
table = "test"  # 表
charset = 'utf8'

# Redis连接
rd = redis.Redis(host='94.199.101.74', port=16379,
                 password='202014xyz', db=5)
redis_table = "curiositynews_tw_start"

# HTML生成目录
website_html_path = ""