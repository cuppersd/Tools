import xml.etree.ElementTree as ET
import os

list_file = open('train.txt', 'w')  # 存放的文件
for filename in os.listdir('./'):  # 遍历xml文件夹
	if filename.endswith('.xml'):  # 判断后缀是否是.xml
		in_file = open(filename)  # 打开.xml文件夹
		tree=ET.parse(in_file)  # 解析.xml文件
		root = tree.getroot()  # 获取root最大的标签
		for obj in root.iter('item'):  # 遍历root标签下的object子标签

			clsss = obj.find('name').text  # 获取类别属性，并且给每个类别属性编号
			if clsss=='yz':
				clsss=0


			xmlbox = obj.find('bndbox')  # 寻找每个object下面的bndbox标签，也就是四个坐标值

			b = xmlbox.find('xmin').text + ',' + xmlbox.find('ymin').text + ',' + xmlbox.find('xmax').text + ',' + xmlbox.find('ymax').text + ',' + str(clsss) + '\n'
			list_file.write('./data/'+filename.replace('.xml','.jpg')+' '+b)
list_file.close()