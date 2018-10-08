import requests
import numpy as np
import cv2
#  读取图片url，并将其转化为矩阵
def imgurl2mat(url):
    #  图片连接转化为图片矩阵
    #  传入参数为图片
    f = requests.get(url)
    nparr = np.fromstring(f.content, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np





# 测试部分
def main():
	url='https://avatars3.githubusercontent.com/u/30834154?s=460&v=4'
	img_np=imgurl2mat(url)
	print(img_np)
	cv2.imshow('123', img_np)
	cv2.waitKey()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()