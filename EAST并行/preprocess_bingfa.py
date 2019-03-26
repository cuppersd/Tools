import numpy as np
from PIL import Image, ImageDraw
import os
import random
from tqdm import tqdm
import multiprocessing
import cfg
from label import shrink


def batch_reorder_vertexes(xy_list_array):
    reorder_xy_list_array = np.zeros_like(xy_list_array)
    for xy_list, i in zip(xy_list_array, range(len(xy_list_array))):
        reorder_xy_list_array[i] = reorder_vertexes(xy_list)
    return reorder_xy_list_array


def reorder_vertexes(xy_list):  # 调整顺序
    reorder_xy_list = np.zeros_like(xy_list)  # 存放调整顺序后的坐标点
    # determine the first point with the smallest x, 调整最小的点必须是x最小的
    # if two has same x, choose that with smallest y, 如果两个点的x相同则，取y小的
    ordered = np.argsort(xy_list, axis=0)  # 按照列进行排序，排序的是索引
    xmin1_index = ordered[0, 0]
    xmin2_index = ordered[1, 0]
    if xy_list[xmin1_index, 0] == xy_list[xmin2_index, 0]:
        if xy_list[xmin1_index, 1] <= xy_list[xmin2_index, 1]:
            reorder_xy_list[0] = xy_list[xmin1_index]
            first_v = xmin1_index
        else:
            reorder_xy_list[0] = xy_list[xmin2_index]
            first_v = xmin2_index
    else:
        reorder_xy_list[0] = xy_list[xmin1_index]
        first_v = xmin1_index
    # connect the first point to others, the third point on the other side of
    # the line with the middle slope
    others = list(range(4))  # 对四个点编号
    others.remove(first_v)  # 移除第一个点的编号
    k = np.zeros((len(others),))  # 初始化一个numpy来保存k
    for index, i in zip(others, range(len(others))):
        k[i] = (xy_list[index, 1] - xy_list[first_v, 1]) \
                    / (xy_list[index, 0] - xy_list[first_v, 0] + cfg.epsilon)   # cfg.epsilon防止除以0
    k_mid = np.argsort(k)[1]  # 三个点排序后取中间的
    third_v = others[k_mid]
    reorder_xy_list[2] = xy_list[third_v]  # 到此处第三个点找出来
    # determine the second point which on the bigger side of the middle line
    others.remove(third_v)
    b_mid = xy_list[first_v, 1] - k[k_mid] * xy_list[first_v, 0]
    second_v, fourth_v = 0, 0
    for index, i in zip(others, range(len(others))):
        # delta = y - (k * x + b)
        delta_y = xy_list[index, 1] - (k[k_mid] * xy_list[index, 0] + b_mid)
        if delta_y > 0:
            second_v = index
        else:
            fourth_v = index
    reorder_xy_list[1] = xy_list[second_v]
    reorder_xy_list[3] = xy_list[fourth_v]
    # compare slope of 13 and 24, determine the final order
    k13 = k[k_mid]
    k24 = (xy_list[second_v, 1] - xy_list[fourth_v, 1]) / (
                xy_list[second_v, 0] - xy_list[fourth_v, 0] + cfg.epsilon)
    if k13 < k24:
        tmp_x, tmp_y = reorder_xy_list[3, 0], reorder_xy_list[3, 1]
        for i in range(2, -1, -1):
            reorder_xy_list[i + 1] = reorder_xy_list[i]
        reorder_xy_list[0, 0], reorder_xy_list[0, 1] = tmp_x, tmp_y
    return reorder_xy_list


def resize_image(im, max_img_size=cfg.max_train_img_size):  # 对图片进行resize
    im_width = np.minimum(im.width, max_img_size)
    if im_width == max_img_size < im.width:
        im_height = int((im_width / im.width) * im.height)
    else:
        im_height = im.height
    o_height = np.minimum(im_height, max_img_size)
    if o_height == max_img_size < im_height:
        o_width = int((o_height / im_height) * im_width)
    else:
        o_width = im_width
    d_wight = o_width - (o_width % 32)
    d_height = o_height - (o_height % 32)
    return d_wight, d_height


def preprocess(o_img_fname,origin_image_dir,origin_txt_dir,train_image_dir,train_label_dir,draw_gt_quad,show_gt_image_dir,show_act_image_dir,train_val_set):
    with Image.open(os.path.join(origin_image_dir, o_img_fname)) as im:
        # d_wight, d_height = resize_image(im)
        # 在这里需要转化为736x736大小的
        d_wight, d_height = cfg.max_train_img_size, cfg.max_train_img_size
        scale_ratio_w = d_wight / im.width
        scale_ratio_h = d_height / im.height
        im = im.resize((d_wight, d_height), Image.NEAREST).convert('RGB')  # im.shape=(736,736)
        show_gt_im = im.copy()  # 用于绘制gt
        # draw on the img
        draw = ImageDraw.Draw(show_gt_im)
        with open(os.path.join(origin_txt_dir,
                               o_img_fname[:-4] + '.txt'), 'r',encoding='utf-8') as f:
            anno_list = f.readlines()
        xy_list_array = np.zeros((len(anno_list), 4, 2))  # xy_list_array为（多少行，四个点，两个坐标）
        for anno, i in zip(anno_list, range(len(anno_list))):
            anno_colums = anno.strip().split(',')
            anno_array = np.array(anno_colums)
            xy_list = np.reshape(anno_array[:8].astype(float), (4, 2))  # 前8个数转化为4行2列
            xy_list[:, 0] = xy_list[:, 0] * scale_ratio_w  # 需要乘以一个倍数，因为图片做了缩放
            xy_list[:, 1] = xy_list[:, 1] * scale_ratio_h
            xy_list = reorder_vertexes(xy_list)  # 调整顺序（四个坐标点调整顺序）
            xy_list_array[i] = xy_list  # xy_list是调整好顺序后的一个numpy数组
            _, shrink_xy_list, _ = shrink(xy_list, cfg.shrink_ratio)  # 将矩形框向内部搜索
            shrink_1, _, long_edge = shrink(xy_list, cfg.shrink_side_ratio)  # 长边往内部收缩后形成的矩形框
            if draw_gt_quad:
                draw.line([tuple(xy_list[0]), tuple(xy_list[1]),
                           tuple(xy_list[2]), tuple(xy_list[3]),
                           tuple(xy_list[0])
                           ],
                          width=2, fill='green')  # 这是绘制的原始框
                draw.line([tuple(shrink_xy_list[0]),
                           tuple(shrink_xy_list[1]),
                           tuple(shrink_xy_list[2]),
                           tuple(shrink_xy_list[3]),
                           tuple(shrink_xy_list[0])
                           ],
                          width=2, fill='blue')  # 往内部收缩后的框
                vs = [[[0, 0, 3, 3, 0], [1, 1, 2, 2, 1]],
                      [[0, 0, 1, 1, 0], [2, 2, 3, 3, 2]]]
                for q_th in range(2):
                    draw.line([tuple(xy_list[vs[long_edge][q_th][0]]),  # 代表resize原始框的的第一个坐标
                               tuple(shrink_1[vs[long_edge][q_th][1]]),  # 代表长边收缩框的第一个坐标
                               tuple(shrink_1[vs[long_edge][q_th][2]]),  # 代表长边收缩框的第二个坐标
                               tuple(xy_list[vs[long_edge][q_th][3]]),  # 代表resize原始框的的第二个坐标
                               tuple(xy_list[vs[long_edge][q_th][4]])],  # 代表resize原始框的的第一个坐标
                              width=3, fill='yellow')
        if cfg.gen_origin_img:  # 这里是保存resize后的原图
            im.save(os.path.join(train_image_dir, o_img_fname))  # 保存resize后的图片
        np.save(os.path.join(
            train_label_dir,
            o_img_fname[:-4] + '.npy'),
            xy_list_array)  # 保存resize后，调整顺序后的标注结果
        if draw_gt_quad:
            show_gt_im.save(os.path.join(show_gt_image_dir, o_img_fname))
        train_val_set.append('{},{},{}\n'.format(o_img_fname,
                                                 d_wight,
                                                 d_height))  # 将所有图片的文件名，宽度和高度加入集合，注意后面有个回车



if __name__ == '__main__':
    data_dir = cfg.data_dir  # 读取数据的根目录 data_dir = './icpr/'
    origin_image_dir = os.path.join(data_dir, cfg.origin_image_dir_name)  # 原始图片路径
    origin_txt_dir = os.path.join(data_dir, cfg.origin_txt_dir_name)  # 原始txt路径
    train_image_dir = os.path.join(data_dir, cfg.train_image_dir_name)  # 训练图片路径
    train_label_dir = os.path.join(data_dir, cfg.train_label_dir_name)  # 训练txt路径
    # 判断存放路径是否存在，不存在需要创建
    if not os.path.exists(train_image_dir):
        os.mkdir(train_image_dir)
    if not os.path.exists(train_label_dir):
        os.mkdir(train_label_dir)
    draw_gt_quad = cfg.draw_gt_quad  # 是否把groundtruth绘制出来
    # 判断act和gt是否存在不存在则创建
    show_gt_image_dir = os.path.join(data_dir, cfg.show_gt_image_dir_name)
    if not os.path.exists(show_gt_image_dir):
        os.mkdir(show_gt_image_dir)
    show_act_image_dir = os.path.join(cfg.data_dir, cfg.show_act_image_dir_name)
    if not os.path.exists(show_act_image_dir):
        os.mkdir(show_act_image_dir)
    # 原始图片文件名列表
    o_img_list = os.listdir(origin_image_dir)
    print('found %d origin images.' % len(o_img_list))  # 打印发现多少张图
    train_val_set = []
    for o_img_fname, _ in zip(o_img_list, tqdm(range(len(o_img_list)))):  # tqdm是一个进度条的控件
        pool = multiprocessing.Pool(processes=1)
        pool.apply_async(preprocess, (o_img_fname,origin_image_dir,origin_txt_dir,train_image_dir,train_label_dir,draw_gt_quad,show_gt_image_dir,show_act_image_dir,train_val_set))


    train_img_list = os.listdir(train_image_dir)
    print('found %d train images.' % len(train_img_list))
    train_label_list = os.listdir(train_label_dir)
    print('found %d train labels.' % len(train_label_list))

    random.shuffle(train_val_set)  # 打乱顺序
    val_count = int(cfg.validation_split_ratio * len(train_val_set))  # 验证集的数量
    with open(os.path.join(data_dir, cfg.val_fname), 'w') as f_val:
        f_val.writelines(train_val_set[:val_count])  # 这样很简洁，值得学习
    with open(os.path.join(data_dir, cfg.train_fname), 'w') as f_train:
        f_train.writelines(train_val_set[val_count:])
