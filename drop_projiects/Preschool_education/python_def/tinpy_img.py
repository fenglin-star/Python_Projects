import tinify
import os
import random
import time


tokens = ["KnFGgbjpkdDMfLNScmJghYzkvnbR6QQm", "W1ZmfP59f0ylTD2wtss843vvP340T4MR", "P59kwZW70CMqzvQgFRVwhXnQTpRgcbP5", "XdZyn5Mtwvdk1gRz0mVxGR3XD2l2QJpr"]

tinify.key = random.choice(tokens)
date = time.strftime('%Y%m%d',time.localtime(time.time()))
# print(r"C:/wwwroot/jingjiniao.info/data/attachment/forum/" + date[0:6] + "/" +date[6:8])
path = r"C:\Users\10944\Desktop\translate"

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.jpg') or f.endswith('.png'):
                fullname = os.path.join(root, f)
                yield fullname


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


if __name__ == '__main__':
    files = findAllFile(path)
    for file in files:
        imgpath = file
        size = get_FileSize(file)
        if float(size) >= 0.8:
            print("compressing ..." + imgpath,"    老文件大小：%.2f MB" % (size))
            tinify.from_file(imgpath).to_file(imgpath)
            size = get_FileSize(file)
            print("新文件大小：%.2f MB" % (size))
            print(" ")
        else:
            print("文件太小：%.2f MB" % (size),"不压缩")








