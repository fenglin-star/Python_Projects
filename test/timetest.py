#-*-coding: utf-8-*-
# 创建时间: 2021/2/21

# import time
# print(type(time.strftime('%H:%M',time.localtime(time.time()))))


with open("num_list.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        print(line)