# coding=utf-8
from python_def.config import *
from python_def.WordPress import wordpress_artice
from multiprocessing import Pool
import redis
from requests.adapters import HTTPAdapter
from zhconv import convert

# redis设置部分
rd = redis.Redis(host='23.225.151.156', port=16379,
                password='202014xyz', db=2)
redis_table = "curiositynews_tw"

# config WP 连接设置部分
wp_host = 'https://www.curiositynews.net/xmlrpc.php'
wp_user = 'Author'
wp_password = 'CNUSE6PMQBzRi4KGsu'



def get_redis_data():
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            value = rd.rpop(redis_table)
            return value
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue


# BS4解析页面HTML，提取关键元素
def analysis_html(task):
    data_list = task.replace("\n", "").split('|||')
    # 获取标题
    wp_title = data_list[0]
    wp_slug_title = data_list[1]
    wp_content = data_list[2]
    wp_category = data_list[3].replace("[", "").replace("]", "").replace("''", "").replace("'", "").split()
    wp_post_tag = data_list[4].replace("[", "").replace("]", "").replace("''", "").replace("'", "").split(", ")

    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            # publish：已发布   pending：等待复审  draft：草稿
            wppost_status = "publish"
            wordpress_artice(wppost_status, wp_title, wp_slug_title, wp_content, wp_category, wp_post_tag,
                             wp_host, wp_user, wp_password)
            break

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue



# 数据库去重、文本翻译、插入WordPress
def main(i):
    value = get_redis_data()
    if not value:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),"没有可执行的任务")
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "正在执行{}".format(i) + "任务")
        task = value.decode('utf-8')
        analysis_html(task)



if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 获取全部的URL链接
    pool = Pool(4)
    for i in range(1,10):
        pool.apply_async(func=main, args=(i,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)