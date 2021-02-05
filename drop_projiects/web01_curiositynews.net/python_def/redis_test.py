#-*-coding: utf-8-*-
#Python分布式爬虫demo
import redis
import time,os
from config import *

rd = redis.Redis(host='23.225.151.156', port=16379,
                password='202014xyz', db=2)
redis_table = "curiositynews_tw_start"


#插入Redis队列
def insert_redis_urls():
    # 生产10个url任务
    for i in range(10):
        url = "http://{}.html".format(i)
        rd.lpush(redis_table, url)
        print("插入",url)


# 从Redis队列取出数据，运行爬虫程序
def crawl(value):
    task = value.decode('utf-8')
    print('爬取url： {}'.format(task))


if __name__ == '__main__':
    insert_redis_urls()
    while True:
        value = rd.rpop(redis_table)
        if not value:
            print("no")
            continue
        else:
            crawl(value)