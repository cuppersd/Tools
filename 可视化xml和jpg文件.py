import xml.etree.ElementTree as ET
import os

from PIL import Image, ImageDraw, ImageFont
im = Image.open('170927_064449997_Camera_5.jpg')
draw = ImageDraw.Draw(im)




# ## 绘制小圆点
# from PIL import Image, ImageDraw, ImageFont
# im = Image.open('4960377fb6919a1e.jpg')
# draw = ImageDraw.Draw(im)
# point_size=50 # 点的大小
# for cor in [[311, 238], [326, 292]]:  # [x,y]代表一个点
# 	x,y=cor
# 	draw.ellipse((x-point_size, y-point_size,x+point_size, y+point_size),fill = (0, 255, 0)) # fill是填充颜色
# im.show()
filename='170927_064449997_Camera_5.xml'
list_file = open('train.txt', 'w')  # 存放的文件
# for filename in os.listdir('./'):  # 遍历xml文件夹
# 	if filename.endswith('.xml'):  # 判断后缀是否是.xml
in_file = open(filename)  # 打开.xml文件夹
tree=ET.parse(in_file)  # 解析.xml文件
root = tree.getroot()  # 获取root最大的标签
for obj in root.iter('object'):  # 遍历root标签下的object子标签

	clsss = obj.find('name').text  # 获取类别属性，并且给每个类别属性编号
	if clsss=='container':
		clsss=0
	if clsss=='cruise ship':
		clsss=1
	if clsss=='drilling platform':
		clsss=2
	if clsss=='Lighthouse':
		clsss=3
	if clsss=='Sailboat':
		clsss=4
	if clsss=='yacht':
		clsss=5

	xmlbox = obj.find('bndbox')  # 寻找每个object下面的bndbox标签，也就是四个坐标值
	draw.rectangle([(int(xmlbox.find('xmin').text),int(xmlbox.find('ymin').text)),(int(xmlbox.find('xmax').text),int(xmlbox.find('ymax').text))],outline=123)  # 参数说明:[(x1,y1),(x2,y2)],绘制矩形
	b = xmlbox.find('xmin').text + ',' + xmlbox.find('ymin').text + ',' + xmlbox.find('xmax').text + ',' + xmlbox.find('ymax').text + ',' + str(clsss) + '\n'
	list_file.write('./'+filename.replace('.xml','.jpg')+' '+b)
list_file.close()
im.show()