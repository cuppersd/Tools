from PIL import Image, ImageDraw
import numpy as np
import os
from termcolor import colored


def show_boxes(img, anno, rotate=None):
    """读取标注文件, 在图片上显示多边形"""
    if rotate:
        with rotate_im(img, rotate) as im_rotated:
            with Image.open(img) as im:
                im_size = im.size
            draw = ImageDraw.Draw(im_rotated)
            for coords, _ in iter_anno(anno):
                coords_rotated = rotate_coords(coords, im_size, rotate)
                draw.polygon(coords_rotated, outline='lime')
            im_rotated.show()
    else:
        with Image.open(img) as im:
            draw = ImageDraw.Draw(im)
            for coords, _ in iter_anno(anno):
                draw.polygon(coords, outline='lime')
            im.show()


def iter_anno(anno):
    """读取标注文件返回coords的生成器"""
    with open(anno, encoding='utf-8') as f:
        data = f.read().strip().split('\n')
        for line in data:
            line_split = line.split(',', maxsplit=8)
            coords = list(map(int, line_split[:8]))
            extra = line_split[8] if len(line_split) > 8 else None
            yield coords, extra


def rotate_im(img, angle):
    """(逆时针)旋转图片"""
    with Image.open(img) as im:
        im_rotated = im.transpose(angle)
        return im_rotated


def rotate_coords(coords_raw, im_size, angle):
    """(逆时针)旋转坐标"""
    coords = np.array(coords_raw, dtype=int).reshape(-1, 2)
    if angle == Image.ROTATE_90:
        coords_rotated = (coords * np.array([-1, 1]))[:, ::-1] + np.array([0, im_size[0]])  # (x,y) -> (y,w-x)
    elif angle == Image.ROTATE_180:
        coords_rotated = np.array(im_size) - coords  # (x,y) -> (w-x,h-y)
    elif angle == Image.ROTATE_270:
        coords_rotated = (coords * np.array([1, -1]))[:, ::-1] + np.array([im_size[1], 0])  # (x,y) -> (h-y,x)
    else:
        return
    return coords_rotated.flatten().tolist()


def prefix_save(path, prefix, to_create=False):
    """获取保存的路径"""
    dirname, filename = os.path.split(path)
    dir_prefixed = os.path.join(dirname)
    if not os.path.isdir(dir_prefixed) and to_create:
        os.mkdir(dir_prefixed)
        print(colored('created:', 'blue'), dir_prefixed)
    return os.path.join(dir_prefixed, prefix + '_' + filename)


def proc_rotate(img, anno, angle, save_img=False, save_anno=False):
    with Image.open(img) as im:
        im_size = im.size
    if angle == Image.ROTATE_90:
        prefix = 'ROTATE_90'
    elif angle == Image.ROTATE_180:
        prefix = 'ROTATE_180'
    elif angle == Image.ROTATE_270:
        prefix = 'ROTATE_270'
    else:
        return
    if save_img:
        save_img_to = prefix_save(img, prefix=prefix, to_create=True)
        with rotate_im(img, angle) as im_rotated:
            im_rotated.save(save_img_to, quality=90)
        print(colored('img saved:', 'blue'), save_img_to)
    if save_anno:
        save_anno_to = prefix_save(anno, prefix=prefix, to_create=True)
        with open(save_anno_to, 'w', encoding='utf-8') as f:
            for coords, extra in iter_anno(anno):
                coords_rotated = rotate_coords(coords, im_size, angle)
                line = ','.join(map(str, coords_rotated))
                if extra:
                    line += ',' + extra
                f.write(line + '\n')
        print(colored('anno saved:', 'blue'), save_anno_to)


if __name__ == '__main__':
    # img_path = '/Users/Kee/Public/archive/EAST_big/anno_images/1550402964.379332.jpg'
    # anno_path = '/Users/Kee/Public/archive/EAST_big/anno_boxes/1550402964.379332.txt'
    # show_boxes(img_path, anno_path)
    # show_boxes(img_path, anno_path, rotate=Image.ROTATE_270)
    # proc_rotate(img_path, anno_path, angle=Image.ROTATE_90, save_img=True, save_anno=True)

    root_img = './image_10000/'
    root_anno = './txt_10000/'
    for img_f in os.listdir(root_img):
        img_name, img_ext = os.path.splitext(img_f)
        if img_ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
            continue
        img_path = os.path.join(root_img, img_f)
        anno_path = os.path.join(root_anno, '{}.txt'.format(img_name))
        if not os.path.isfile(anno_path):
            print(colored('not exists:', 'red'), anno_path)
            continue

        for angle in [Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]:
            proc_rotate(img_path, anno_path, angle=angle, save_img=True, save_anno=True)
