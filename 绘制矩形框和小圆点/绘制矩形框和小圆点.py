## 绘制矩形框和小圆点，用于可视化bbox，和人脸关键点和人体关键点

## 绘制矩形框框
from PIL import Image, ImageDraw, ImageFont
im = Image.open('4960377fb6919a1e.jpg')
draw = ImageDraw.Draw(im)
draw.rectangle([(877,1242),(1087,1549)],outline=123)  # 参数说明:[(x1,y1),(x2,y2)],绘制矩形
im.show()


## 绘制小圆点
from PIL import Image, ImageDraw, ImageFont
im = Image.open('4960377fb6919a1e.jpg')
draw = ImageDraw.Draw(im)
point_size=50 # 点的大小
for cor in [[311, 238], [326, 292]]:  # [x,y]代表一个点
	x,y=cor
	draw.ellipse((x-point_size, y-point_size,x+point_size, y+point_size),fill = (0, 255, 0)) # fill是填充颜色
im.show()

