#coding:utf-8
import cv2
import numbers
import random
import math
import numpy as np
from skimage.util import random_noise

# 图像均为cv2读取
class DataAugment():
    def __init__(self):
        pass

    def trans_color_image(self, img):
        '''
        颜色通道转换
        '''
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def add_noise(self, im):
        """
        对图片加噪声
        :param img: 图像array
        :return: 加噪声后的图像array,由于输出的像素是在[0,1]之间,所以得乘以255
        """
        return (random_noise(im, mode='gaussian', clip=True) * 255).astype(im.dtype)

    def random_scale(self, im, text_polys, scales = [0.7, 0.8, 0.9, 1.1, 1.2]):
        """
        从scales中随机选择一个尺度，对图片和文本框进行缩放
        :param im: 原图
        :param text_polys: 文本框
        :param scales: 尺度
        :return: 经过缩放的图片和文本
        """
        tmp_text_polys = text_polys.copy().astype(np.float32)
        rd_scale = float(np.random.choice(scales))
        im = cv2.resize(im, dsize=None, fx=rd_scale, fy=rd_scale)
        tmp_text_polys *= rd_scale
        return im, tmp_text_polys.astype(np.int32)

    def random_crop_img_bboxes(self, im, text_polys, max_tries=50):
        """
        从图片中裁剪出 cropsize大小的图片和对应区域的文本框
        :param im: 图片
        :param text_polys: 文本框
        :param max_tries: 最大尝试次数
        :return: 裁剪后的图片和文本框
        """
        h, w, _ = im.shape
        text_polys[:,:,0]=np.clip(text_polys[:,:,0],1,w-2)
        text_polys[:,:,1]=np.clip(text_polys[:,:,1],1,h-2)
        
        pad_h = h // 10
        pad_w = w // 10
        h_array = np.zeros((h + pad_h * 2), dtype=np.int32)
        w_array = np.zeros((w + pad_w * 2), dtype=np.int32)
        for poly in text_polys:
            poly = np.round(poly, decimals=0).astype(np.int32)  # 四舍五入取整
            
            minx = np.min(poly[:, 0])
            maxx = np.max(poly[:, 0])
            w_array[minx + pad_w:maxx + pad_w] = 1  # 将文本区域的在w_array上设为1，表示x轴方向上这部分位置有文本
            miny = np.min(poly[:, 1])
            maxy = np.max(poly[:, 1])
            h_array[miny + pad_h:maxy + pad_h] = 1  # 将文本区域的在h_array上设为1，表示y轴方向上这部分位置有文本
        # 在两个轴上 拿出背景位置去进行随机的位置选择，避免选择的区域穿过文本
        h_axis = np.where(h_array == 0)[0]
        w_axis = np.where(w_array == 0)[0]
        if len(h_axis) == 0 or len(w_axis) == 0:
            # 整张图全是文本的情况下，直接返回
            return im, text_polys
        for i in range(max_tries):
            xx = np.random.choice(w_axis, size=2)
            # 对选择区域进行边界控制
            xmin = np.min(xx) - pad_w
            xmax = np.max(xx) - pad_w
            xmin = np.clip(xmin, 1, w - 2)
            xmax = np.clip(xmax, 1, w - 2)
            yy = np.random.choice(h_axis, size=2)
            ymin = np.min(yy) - pad_h
            ymax = np.max(yy) - pad_h
            ymin = np.clip(ymin, 1, h - 2)
            ymax = np.clip(ymax, 1, h - 2)
            if xmax - xmin < 0.1 * w or ymax - ymin < 0.1 * h:
                # 选择的区域过小
                # area too small
                continue
            if text_polys.shape[0] != 0:  # 这个判断不知道干啥的
                poly_axis_in_area = (text_polys[:, :, 0] >= xmin) & (text_polys[:, :, 0] <= xmax) \
                                    & (text_polys[:, :, 1] >= ymin) & (text_polys[:, :, 1] <= ymax)
                selected_polys = np.where(np.sum(poly_axis_in_area, axis=1) == 4)[0]
            else:
                selected_polys = []
            if len(selected_polys) == 0:
                # 区域内没有文本
                continue
            im = im[ymin:ymax + 1, xmin:xmax + 1, :]
            polys = text_polys[selected_polys]
            # 坐标调整到裁剪图片上
            polys[:, :, 0] -= xmin
            polys[:, :, 1] -= ymin
            return im, polys
        return im, text_polys

    # 随机旋转图片
    def random_rotate_img_bbox(self, img, text_polys, degrees, same_size=False):
        """
        从给定的角度中选择一个角度，对图片和文本框进行旋转
        :param img: 图片
        :param text_polys: 文本框
        :param degrees: 角度，可以是一个数值,比如180
        :param same_size: 是否保持和原图一样大
        :return: 旋转后的图片和角度
        """
        if isinstance(degrees, numbers.Number):
            if degrees < 0:
                raise ValueError("If degrees is a single number, it must be positive.")
            degrees = (-degrees, degrees)
        elif isinstance(degrees, list) or isinstance(degrees, tuple) or isinstance(degrees, np.ndarray):
            if len(degrees) != 2:
                raise ValueError("If degrees is a sequence, it must be of len 2.")
            degrees = degrees
        else:
            raise Exception('degrees must in Number or list or tuple or np.ndarray')
        # ---------------------- 旋转图像 ----------------------
        w = img.shape[1]
        h = img.shape[0]
        angle = np.random.uniform(degrees[0], degrees[1])

        if same_size:
            nw = w
            nh = h
        else:
            # 角度变弧度
            rangle = np.deg2rad(angle)
            # 计算旋转之后图像的w, h
            nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w))
            nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w))
        # 构造仿射矩阵
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, 1)
        # 计算原图中心点到新图中心点的偏移量
        rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
        # 更新仿射矩阵
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # 仿射变换
        rot_img = cv2.warpAffine(img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=np.mean(img))

        # ---------------------- 矫正bbox坐标 ----------------------
        # rot_mat是最终的旋转矩阵
        # 获取原始bbox的四个中点，然后将这四个点转换到旋转后的坐标系下
        rot_text_polys = list()
        for bbox in text_polys:
            # bbox = bbox.reshape(4,2)
            point1 = np.dot(rot_mat, np.array([bbox[0, 0], bbox[0, 1], 1]))
            point2 = np.dot(rot_mat, np.array([bbox[1, 0], bbox[1, 1], 1]))
            point3 = np.dot(rot_mat, np.array([bbox[2, 0], bbox[2, 1], 1]))
            point4 = np.dot(rot_mat, np.array([bbox[3, 0], bbox[3, 1], 1]))
            rot_text_polys.append([point1, point2, point3, point4])
        return rot_img, np.array(rot_text_polys, dtype=np.float32)

    def random_rotate_img_bbox_90(self, img, text_polys, same_size=False):
        """
        从给定的角度中选择一个角度，对图片和文本框进行旋转
        :param img: 图片
        :param text_polys: 文本框
        :param degrees: 角度，可以是一个数值,比如180
        :param same_size: 是否保持和原图一样大
        :return: 旋转后的图片和角度
        """
        w = img.shape[1]
        h = img.shape[0]
        angle = 90

        if same_size:
            nw = w
            nh = h
        else:
            # 角度变弧度
            rangle = np.deg2rad(angle)
            # 计算旋转之后图像的w, h
            nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w))
            nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w))
        # 构造仿射矩阵
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, 1)
        # 计算原图中心点到新图中心点的偏移量
        rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
        # 更新仿射矩阵
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # 仿射变换
        rot_img = cv2.warpAffine(img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=np.mean(img))

        # ---------------------- 矫正bbox坐标 ----------------------
        # rot_mat是最终的旋转矩阵
        # 获取原始bbox的四个中点，然后将这四个点转换到旋转后的坐标系下
        rot_text_polys = list()
        for bbox in text_polys:
            # bbox = bbox.reshape(4,2)
            point1 = np.dot(rot_mat, np.array([bbox[0, 0], bbox[0, 1], 1]))
            point2 = np.dot(rot_mat, np.array([bbox[1, 0], bbox[1, 1], 1]))
            point3 = np.dot(rot_mat, np.array([bbox[2, 0], bbox[2, 1], 1]))
            point4 = np.dot(rot_mat, np.array([bbox[3, 0], bbox[3, 1], 1]))
            rot_text_polys.append([point1, point2, point3, point4])
        return rot_img, np.array(rot_text_polys, dtype=np.float32)


    def add_padding(self, im, text_polys, input_size):
        """
        对图片和文本框进行resize
        :param im: 图片
        :param text_polys: 文本框
        :param input_size: resize尺寸,数字或者list的形式，如果为list形式，就是[w,h]
        :param keep_ratio: 是否保持长宽比
        :return: resize后的图片和文本框
        """
        # 将图片短边pad到和长边一样
        h, w, c = im.shape
        long_edge = float(max(h, w))
        if long_edge > input_size:
            w_scale = input_size*1.0 / long_edge
            h_scale = input_size*1.0 / long_edge
            im = cv2.resize(im, (0, 0), fx=w_scale, fy=h_scale)
        else:
            w_scale = 1
            h_scale = 1

        im_padded = np.ones((input_size, input_size, c), dtype=np.uint8) * np.mean(im).astype(np.uint8)
        h_, w_= im.shape[:2]
        start_h = random.randint(0, input_size - h_)
        start_w = random.randint(0, input_size - w_)
        im_padded[start_h:start_h + h_, start_w:start_w + w_] = im.copy()
        im = im_padded
        text_polys = text_polys.astype(np.float32)
        text_polys[:, :, 0] *= w_scale
        text_polys[:, :, 1] *= h_scale
        text_polys[:, :, 0] += start_w
        text_polys[:, :, 1] += start_h
        return im, text_polys

    def flip(self, image, text_polys, horiz=False, vert=False):
        if horiz:
            code = 1
        if vert:
            code = 0
        image = cv2.flip(image, code)
        if horiz:
            text_polys[:, :, 0] = image.shape[1] - text_polys[:, :, 0]
        else:
            text_polys[:, :, 1] = image.shape[0] - text_polys[:, :, 1]
        return image, text_polys


    def augment(self,img,bbox):
        prob = np.random.random()
        if prob > 0.5:
            img, bbox = self.random_rotate_img_bbox_90(img, bbox)
        prob = np.random.random()
        if prob > 0.5:
            img, bbox = self.random_scale(img, bbox,)
        prob = np.random.random()
        if prob>0.5:
            img = self.trans_color_image(img)
        prob = np.random.random()
        if prob>0.5:
            img = self.add_noise(img)
        prob = np.random.random()
        if prob > 0.5:
            img, bbox = self.random_rotate_img_bbox(img, bbox, 20)
        prob = np.random.random()
        if prob > 0.5:
            img, bbox = self.random_crop_img_bboxes(img, bbox, 50)
        prob = np.random.random()
        if prob > 0.8:
            img, bbox = self.flip(img, bbox, horiz=True)
        prob = np.random.random()
        if prob > 0.8:
            img, bbox = self.flip(img, bbox, vert=True)
        return img, bbox

def test(filename):
    import uuid
    img = cv2.imread(filename)
    txt = open(filename.replace('.jpg','.txt')).readlines()
    cor = []
    for each_line in txt:
        each_line = np.array(each_line.split(',')[:8]).reshape(4,2)
        cor.append(each_line.astype(np.int32))
    cor = np.array(cor)
    aug = DataAugment()

    t_im, t_text_polys = aug.augment(img, cor)
    t_text_polys = t_text_polys.astype(np.int32)
    for point in t_text_polys:
        cclor = (55, 5, 55)
        cv2.line(t_im, tuple(point[0]), tuple(point[1]), cclor, 2)
        cv2.line(t_im, tuple(point[1]), tuple(point[2]), cclor, 2)
        cv2.line(t_im, tuple(point[2]), tuple(point[3]), cclor, 2)
        cv2.line(t_im, tuple(point[3]), tuple(point[0]), cclor, 2)
        # cv2.namedWindow(name, 0)  # 1表示原图
        # cv2.moveWindow(name, 0, 0)
        # cv2.resizeWindow(name, 1200, 800)  # 可视化的图片大小
    filename = './'+str(uuid.uuid1()) + '1.jpg'
    cv2.imwrite(filename, t_im)
    print(filename,t_text_polys.shape,t_im.shape)
if __name__ == '__main__':
    for i in range(60):
        file = '1540426112.693826.jpg'
        test(file)
