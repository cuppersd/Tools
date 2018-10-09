import matplotlib.pyplot as plt
import numpy as np
from PIL import Image 
import cv2

filename='166.jpg'  # 文件名
im = Image.open(filename)  # 读取图像
plt.imshow(im, cmap = plt.get_cmap("gray"))  # 显示图像
pos=plt.ginput(4)  # 在图片上点选四个点
print(pos)  # 打印点选的四个点 [(9.889610389610255, 223.30952380952363), (722.0108225108225, 119.41341991341972), (780.4523809523811, 550.1493506493505), (81.3181818181817, 677.8549783549782)]
plt.close()  # 关闭显示的plt

img=cv2.imread(filename)
rows,cols,ch=img.shape
# 获取四个点，顺时针获取
left_top=pos[0]  # 左上角
right_top=pos[1]  # 右上角
right_down=pos[2]  # 右下角
left_down=pos[3]  # 左下角
#--------------------
# 计算距离四边形的距离
d12=np.sqrt(np.square(left_top[0]-right_top[0])+np.square(left_top[1]-right_top[1]))
d23=np.sqrt(np.square(right_top[0]-right_down[0])+np.square(right_top[1]-right_down[1]))
d34=np.sqrt(np.square(right_down[0]-left_down[0])+np.square(right_down[1]-left_down[1]))
d41=np.sqrt(np.square(left_down[0]-left_top[0])+np.square(left_down[1]-left_top[1]))
dx=2*900
dy=2*540
#--------------------
# dx 和 dy为图片的大小 
pts1=np.float32([left_top,right_top,right_down,left_down])
pts2=np.float32([[0,0],[dx,0],[dx,dy],[0,dy]])

# 计算透视变换的矩阵
M=cv2.getPerspectiveTransform(pts1,pts2)
# 透视变换
dst=cv2.warpPerspective(img,M,(int(dx),int(dy)))
# 结果展示
cv2.imwrite('crop.jpg',dst)
# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),
im = Image.open('crop.jpg')
plt.imshow(im)
plt.title('Output')
plt.show()
