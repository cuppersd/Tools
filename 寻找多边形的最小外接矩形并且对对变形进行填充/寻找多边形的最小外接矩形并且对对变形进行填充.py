
import numpy as np
import cv2
import matplotlib.pyplot as plt

b = np.array([[[100,100], [200,230], [150,200], [100,220]]], dtype = np.int32)  # 定义多边形点
rect = cv2.minAreaRect(b)  # 获取矩形几何中心和长宽
ss=cv2.boxPoints(rect)  # 将其转化为4个顶点
print(rect,ss)

im = cv2.imread('1539846414.586805.jpg')  # 读取图片 绘制矩形线条
cv2.line(im,tuple(ss[0]),tuple(ss[1]),(255,0,0),8)
cv2.line(im,tuple(ss[1]),tuple(ss[2]),(255,0,0),8)
cv2.line(im,tuple(ss[2]),tuple(ss[3]),(255,0,0),8)
cv2.line(im,tuple(ss[3]),tuple(ss[0]),(255,0,0),8)

cv2.fillPoly(im, b, (127,127,127))  # 矩形填充
plt.imshow(im)
plt.show()

