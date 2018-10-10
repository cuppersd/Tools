from PIL import Image, ImageDraw


def main():
    im = Image.open('1_Handshaking_Handshaking_1_940.jpg')  # 读取目标图片
    x1,y1,x2,y2=464,104,662,396  # 框的四个坐标值
    ss = im  # 将图片复制一份
    im = im.crop((x1, y1, x2, y2))  # 对图片进行裁剪
    im = im.convert('RGBA')  # 裁剪图片进行转化，增加透明通道

    # 制造一个和im一样大小的纯色图片
    im2 = Image.new("RGBA", (im.size[0], im.size[1]))  # 生成一张裁剪后大小的图片
    draw2 = ImageDraw.Draw(im2)
    draw2.rectangle((0, 0, im.size[0], im.size[1]), fill=(255, 0, 0))

    # 将裁剪出来的图片和纯色图片进行混合
    print(im.size, im2.size)
    blend = Image.blend(im, im2, 0.4)
    ss.paste(blend,(x1,y1))
    ss.save("blend.png")


if __name__ == '__main__':
    main()