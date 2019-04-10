import cv2
import numpy as np
import os
point_size = 4
line_width = 2

def vis(img_path,  txt_path):
	line_color = (0, 255, 0) #4
	img=cv2.imread(img_path)
	f = open(txt_path,'r',encoding ='utf-8').readlines()
	for eachline in f:
		if eachline.strip().split(',')[-1] == "###":
			line_color = (0, 0, 255)
		point_list = np.array(eachline.split(',')[:8]).astype(int).reshape(4,2)
		cv2.line(img, tuple(point_list[0]), tuple(point_list[1]), line_color, line_width) #5
		cv2.line(img, tuple(point_list[1]), tuple(point_list[2]), line_color, line_width) #5
		cv2.line(img, tuple(point_list[2]), tuple(point_list[3]), line_color, line_width) #5
		cv2.line(img, tuple(point_list[3]), tuple(point_list[0]), line_color, line_width) #5
		cv2.circle(img, tuple(point_list[0]), point_size, (255,0,0),-1)
		cv2.circle(img, tuple(point_list[1]), point_size, (0,255,0),-1)
		cv2.circle(img, tuple(point_list[2]), point_size, (0,0,255),-1)
		cv2.circle(img, tuple(point_list[3]), point_size, (255,255,0),-1)
	# cv2.imshow("Canvas", img) #6
	# cv2.waitKey(0) #7
	print(img_path)
	cv2.imwrite('../vis/'+ os.path.basename(img_path), img)

for each_img in os.listdir('../images_train/'):
	img_path = '../images_train/'+each_img
	txt_path = '../gt_train/'+'gt_' + each_img.replace(each_img.split('.')[-1],'txt')
	vis(img_path,  txt_path)





# # 测试单张图片
# img_path ='../images_train/img_146.jpg'
# txt_path = '../gt_train/gt_img_146.txt'
# vis(img_path,  txt_path)


# # 分析txt文件里面是否有少于或者多余8个点的情况
# import os
# for each_txt in os.listdir('./gt_train/'):
# 	f = open('./gt_train/'+each_txt,'r',encoding ='utf-8').readlines()
# 	for eachline in f:
# 		if len(eachline.split(','))!=10:
# 			print(eachline.split(','))
# 			print(each_txt)
