from PIL import Image
 
class image_aspect():
 
    def __init__(self, image_file, aspect_width, aspect_height):
        self.img = Image.open(image_file)  # 打开图片
        self.aspect_width = aspect_width  # 目标宽度
        self.aspect_height = aspect_height  # 目标高度
        self.result_image = None
 
    def change_aspect_rate(self):
        img_width = self.img.size[0]  # 读取图像宽度
        img_height = self.img.size[1]  # 读取图像高度
 
        if (img_width / img_height) > (self.aspect_width / self.aspect_height):
            rate = self.aspect_width / img_width
        else:
            rate = self.aspect_height / img_height

        rate = round(rate, 1)
        print(rate)
        self.img = self.img.resize((int(img_width * rate), int(img_height * rate)))  # 对图像进行resize操作
        return self
 
    def past_background(self):
        self.result_image = Image.new("RGB", [self.aspect_width, self.aspect_height], (127, 127, 127, 255)) # 生成一张目标大小的灰色图像，指定填充颜色
        self.result_image.paste(self.img, (int((self.aspect_width - self.img.size[0]) / 2), int((self.aspect_height - self.img.size[1]) / 2)))  # 将图像粘贴在中央
        return self
 
    def save_result(self, file_name):
        self.result_image.save(file_name)  # 保存图像
 
 
if __name__ == "__main__":
    filename="219.jpg"
    image_aspect(filename, 500, 500).change_aspect_rate().past_background().save_result(filename+"-resize.jpg")
