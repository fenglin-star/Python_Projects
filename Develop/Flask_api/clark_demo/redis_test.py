#-*-coding: utf-8-*-
#Python分布式爬虫demo
import redis
import time,os
from import_config import *
from multiprocessing import Pool

rd = redis.Redis(host='94.199.101.74', port=16379,
                 password='202014xyz', db=5)
redis_table = "curiositynews_tw_start"


class open_redis_self():
    #定义变量
    def __init__(self,url):
        self.url = url

    #插入Redis队列
    def insert_redis_urls(self):
        # 生产10个url任务
        rd.lpush(redis_table,self.url)
        print("插入",url)

    # 从Redis队列取出数据，运行爬虫程序
    def crawl(self):
        value = rd.rpop(redis_table)
        return value


if __name__ == '__main__':
    pool = Pool()
    for i in range(1, 200):
        url = "http://{}.html".format(i)
        open_redis = open_redis_self(url)

        # pool.apply_async(func=open_redis.insert_redis_urls(), args=(url,))  # 多进程插入数据

        value = open_redis.crawl()
        if not value:
            print("no")
            continue
        else:
            print('爬取url： {}'.format(value.decode('utf-8')))

    pool.close()
    pool.join()



