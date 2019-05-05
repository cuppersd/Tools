from PIL import Image
import os
path_dir = './PNG/'
for filename in os.listdir(path_dir):	
	image_file = Image.open(path_dir+filename)
	image_file = image_file.convert('RGB') # convert image to black and white
	image_file.save(filename.replace(filename.split('.')[-1],'jpg'))
	print(filename)