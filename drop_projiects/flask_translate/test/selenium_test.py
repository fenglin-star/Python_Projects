#-*-coding: utf-8-*-
from config import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

for i in range(1,10):
    # 进入浏览器设置
    chrome_options = Options()

    # 设置代理
    chrome_options.add_argument("--proxy-server=http://96.9.209.182:6666")

    # 无头模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 设置代理
    chrome_options.add_argument("--proxy-server=http://96.9.209.182:6666")

    # 设置中文
    chrome_options.add_argument('lang=zh_CN.UTF-8')

    # 更换UserAgent
    ua = random.choice(fake_UserAgent)
    chrome_options.add_argument('user-agent='+ua)

    # 不加载图片以节约时间
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_page_load_timeout(30)  # 设置30秒超时等待

    url = "https://httpbin.org/get?show_env=1"
    browser.get(url)
    html = browser.page_source
    print(html)
    browser.close()

# browser.quit()
