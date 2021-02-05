#-*-coding: utf-8-*-
# 创建时间: 2021/1/2

import cv2
src = cv2.imread("1.jpg",1)
cv2.imwrite("saveImg.jpg",src,[cv2.IMWRITE_JPEG_QUALITY,0])