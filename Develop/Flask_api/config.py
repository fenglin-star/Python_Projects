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
# proxies = {'http': '154.91.145.140:6666','https': '154.91.145.140:6666'} # 远程代理
proxies = "" # 不使用代理



