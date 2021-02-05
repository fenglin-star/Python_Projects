#-*-coding: utf-8-*-
# 创建时间: 2020/10/8 16:16
from PIL import Image
import os

dir = os.getcwd()
path = "1.jpg"
newPath = "new.jpg"


img = Image.open(path)
img_size = img.size
new_size = (0, 0, img_size[0], img_size[1]-50)  #裁剪图片底部50单位
print(new_size)

cropped = img.crop(new_size)  # (left, upper, right, lower)
cropped.save(newPath)