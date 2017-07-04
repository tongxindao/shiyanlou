# _*_ coding=UTF-8 _*_
from PIL import Image #PIL是一个Python图像处理库
import sys

image_name = "ascii_dora.png"
img = Image.open(image_name)
print(img.mode)
print(img.size)

img = img.convert('L')
img.show()
img.save('L_ascii.png')

w,h = img.size
if w > 100:
    h = int((w/100)*h)
    w = 100

img = img.resize((w,h),Image.ANTIALIAS)
img.save('L_ascii1.png')
data = []
chars = [' ' ,',', 'l', '+', 'n', 'D', '@', 'M']

for i in range(0,h):
    line = " "
    for j in range(0,w):
        pi = img.getpixel((j, i))
        for k in range(0, 8):
            if pi < (k + 1) * 32:
                line += chars[7-k]
                break
    data.append(line)
print(data)
f = open(image_name + '.txt', 'w')
for d in data:
    f.write(d)
    print(d)
f.close()
print('convert OK!!!')
