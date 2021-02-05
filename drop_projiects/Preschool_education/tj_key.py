#coding=utf-8
import re,sys,os
from excel_lw import *

key_paper = "儿童情绪"
f1 = r"{}\tj_key.txt".format(key_paper)
if os.path.exists(f1):
    os.remove(f1)


title = open(r"{}\title_contents.txt".format(key_paper), encoding="utf-8")
title_list = []
for line in title:
    line = str(line).replace("\n","")
    title_list.append(line)
# print(title_list)
title.close()


qik = open(r"{}\qik.txt".format(key_paper), encoding="utf-8")
qik_list = []
for line in qik:
    line = str(line).replace("\n","")
    qik_list.append(line)
# print(qik_list)
qik.close()


qik_time = open(r"{}\qik_time.txt".format(key_paper), encoding="utf-8")
qik_time_list = []
for line in qik_time:
    line = str(line).replace("\n","").replace("年","")
    qik_time_list.append(line)
# print(qik_time_list)
qik_time.close()


keys_list = open(r"{}\keys_list.txt".format(key_paper), encoding="utf-8")
keys_list_list = []
for line in keys_list:
    line = str(line).replace("\n","")
    keys_list_list.append(line)
# print(keys_list_list)
keys_list.close()


#标题0、期刊1、期刊时间2、期刊关键词3
zip_list = zip(title_list,qik_list,qik_time_list,keys_list_list)
data_list = []
for i in zip_list:
    data_list.append(i)


def key_time(time):
    key1 = 0
    key2 = 0
    key3 = 0
    key4 = 0
    key5 = 0
    key6 = 0
    key7 = 0
    key8 = 0
    # key9 = key
    # key10 = key

    for i in data_list:
        # print(i[2])
        if str(i[2]) == time:
            key = str(i[3])
            # print(key)
            if "情绪调节" in key or "情绪管理" in key:
                key1 = key1 + 1
            if "婴幼儿" in key or "岁" in key or "孩子" in key or "幼儿" in key:
                key2 = key2 + 1
            if "园" in key or "环境" in key or "绘本" in key or "游戏" in key or "幼儿园环境" in key or "家园共育" in key:
                key3 = key3 + 1
            if "家庭" in key or "父母" in key or "关爱" in key or "家庭教育" in key or "家园共育" in key:
                key4 = key4 + 1
            if "幼儿教师" in key or "教师" in key:
                key5 = key5 + 1
            if "教育活动" in key or "教育环境" in key or "教育策略" in key or "培养" in key or "幼儿教育" in key or "情绪教育" in key or "策略" in key or "绘本" in key or "游戏" in key:
                key6 = key6 + 1
            if "小班幼儿" in key or "同伴接纳" in key:
                key7 = key7 + 1
            if "不良情绪" in key or "情绪理解" in key or "负面情绪" in key or "情绪反应" in key or "幼儿情绪" in key or "消极情绪" in key or "积极情绪" in key or "情绪情感" in key:
                key8 = key8 + 1
            # if "公共" or "服务" in key:
            #     key9 = key9 + 1
            # if "服务" in key:
            #     key10 = key10 + 1
        else:
            pass

    txt = [time,key1,key2,key3,key4,key5,key6,key7,key8]
    list_time_data.append(txt)
    # print(txt)


if __name__ == '__main__':
    # time = "2019"
    set_time = set(qik_time_list)
    print(set_time)
    list_time_data = []
    frist_list = ["","幼儿心理研究","幼儿生理研究","学校环境对幼儿情绪的影响","家庭环境对幼儿情绪的影响","教师对幼儿情绪的影响","教学内容、教学方式对幼儿情绪的影响","同学、伙伴对幼儿情绪的影响","幼儿情绪研究"]
    list_time_data.append(frist_list)
    for time in set_time:
        key_time(time)

    list_time_data.sort()
    # print(type(list_time_data))
    for i in list_time_data:
        print(i)

    book_name_xlsx = '学前教育论文.xlsx'
    sheet_name_xlsx = '关键词统计'
    value3 = list_time_data
    write_excel_xlsx(book_name_xlsx, sheet_name_xlsx, value3)
    read_excel_xlsx(book_name_xlsx, sheet_name_xlsx)