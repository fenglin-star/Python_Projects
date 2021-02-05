#-*-coding: utf-8-*-
from google_trans_new import google_translator
from multiprocessing import Pool


def translate_data(language,source):
    #如果遇到错误就最多重试6次
    success_num = 0
    while success_num < 6:
        try:
            translator = google_translator(url_suffix="com",timeout=25,proxies={'http':'159.75.5.165:10808','https':'159.75.5.165:10808',})
            translate_text = translator.translate(source,lang_tgt=language)
            return translate_text
            break

        except Exception as e:
            print(e,"正在重试:",data)
            success_num = success_num + 1
            continue


def translate_list_data(language,source):

    def list_to_str(source):
        # 解析list 转为flask能接受的str
        data = ''
        for i in source:
            data = data + '$$$$$' + i
        return data

    def str_to_list(source):
        # 解析str，转换为list
        datas = source.replace("$$$$$", "", 1).split("$$$$$")
        return datas

    translator = google_translator(url_suffix="com", timeout=25,proxies={'http': '159.75.5.165:10808','https': '159.75.5.165:10808',})
    en_list = str_to_list(translator.translate(list_to_str(source), lang_tgt=language))

    return en_list



def main(i):
    # 列表翻译
    # data_list = ["测试文件","湖南第一师范学院","长沙衡远网络科技有限公司是一家百年企业"]
    data_list =  ['Changsha Hengyuan Network Technology Co., Ltd. is a century-old enterprise','Test files', 'Hunan First Normal University', ]
    print(i,translate_list_data(language="zh",source=data_list))



if __name__ == '__main__':
    pool = Pool()
    for i in range(0,5):
        pool.apply_async(func=main, args=(i,))  # 多进程运行
    pool.close()
    pool.join()

    # main(1)