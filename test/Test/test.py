import cv2
import numpy as np
from PIL import Image
import os

dir = os.getcwd()
path = "1.jpg"
newPath = "new.jpg"

from PIL import Image

img = Image.open(path)
img_size = img.size
new_size = (0, 0, img_size[0], img_size[1]-50)
print(new_size)
cropped = img.crop(new_size)  # (left, upper, right, lower)
cropped.save(newPath)