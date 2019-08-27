import cv2   
import numpy as np
import copy


def merge_counter(counters):
    k = 0
    merge_cnt = copy.deepcopy(counters)
    while k < len(merge_cnt)-1:
        left1, top1, w1, h1 = cv2.boundingRect(merge_cnt[k])
        right1 = left1 + w1
        bot1 = top1 + h1
        left2, top2, w2, h2 = cv2.boundingRect(merge_cnt[k+1])
        right2 = left2 + w2
        bot2 = top2 + h2
        top_max = max(top1, top2)
        bot_min = min(bot1, bot2)
        left_max = max(left1, left2)
        right_min = min(right1, right2)
        if left1 <= left2 and right1 >= right2 and top1 <= top2 and bot1 >= bot2:
            merge_cnt.pop(k+1)
            k = k-1
        elif left1 >= left2 and right1 <= right2 and top1 >= top2 and bot1 <= bot2:
            merge_cnt.pop(k)
            k = k-1
        elif bot_min > top_max and right_min > left_max:
            repetition_area = (right_min - left_max)*(bot_min - top_max)
            area1 = w1*h1
            area2 = w2*h2
            if repetition_area < min(area1, area2)*4//5:
                merge_cnt[k] = np.vstack((merge_cnt[k], merge_cnt[k+1]))  # 将两个边缘合并
                merge_cnt.pop(k+1)
                k = k-1
        k = k+1
    return merge_cnt


def remove_seal(img):
    img_copy = img.copy()
    img_red = img_copy.copy()

    # 装换成HSV空间
    img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    img_h, img_s, img_v = cv2.split(img_hsv)
    # 获取BGR三通道
    if len(cv2.split(img_copy)) > 3:
        b, g, r, alpha = cv2.split(img_copy)
    else:
        b, g, r = cv2.split(img_copy)
    # 对H通道进行二值化操作，大于155-180为红色色度分布范围
    ret, h_thresh = cv2.threshold(img_h, 100, 255, cv2.THRESH_BINARY)
    
    # 对二值图进行开运算，去除噪声
    kernel = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(h_thresh, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(opening, kernel, iterations=1)
    img_close = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel2)
    
    # 寻找轮廓
    contours, hierarchy = cv2.findContours(img_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 筛选面积大于10000的轮廓
    arr = []
    for i in range(len(contours)-1):
        cnt = contours[i]
        x, y, w, h = cv2.boundingRect(contours[i])
        area = w*h
        if area > 100:
            arr.append(cnt)
           
    # 在筛选后的轮廓中寻找面积最大的轮廓
    maxcnt = 0
    maxcntloc = 0
    if len(arr) == 0:
        return img_red
    for i in range(len(arr)-1):
        cnt = arr[i]
        area = cv2.contourArea(cnt)
        if maxcnt < area:
            maxcnt = area
            maxcntloc = i       
    
    x, y, w, h = cv2.boundingRect(arr[maxcntloc])
    # 获取最大面积红色区域上下左右四点坐标，并进行适当扩展
    left = x-w//4 if x-w//4 >= 0 else 0
    right = x+w*5//4 if x+w*5//4 <= img_h.shape[1] else img_h.shape[1]
    top = y-h//4 if y-h//4 >= 0 else 0
    bottom = y+h*5//4 if y+h*5/4 <= img_h.shape[0] else img_h.shape[0]
    # 计算V通道阈值
    # img_small=cv2.resize(img_copy,(int(width),int(height)),fy=2,interpolation=cv2.INTER_AREA)
    sum_rv = 0
    num_r = 0
    sum_bv = 0
    num_b = 0
    
    for i in range(top, bottom, 5):
        for j in range(left, right, 5):
            if r[i, j] > b[i, j] and r[i, j] > g[i, j]*5//4 and r[i, j] > 80:  # 获取红色区域V通道的平均值
                sum_rv = sum_rv+img_v[i, j]
                num_r = num_r+1
            elif r[i, j] < 80 and g[i, j] < 80 and b[i, j] < 80:  # 获取黑色区域V通道平均值
                sum_bv = sum_bv+img_v[i, j]
                num_b = num_b+1
    ave_rv = sum_rv//num_r
    ave_bv = sum_bv//num_b
    ave_th = ave_bv+(ave_rv-ave_bv)*3//4  # 计算V通道阈值，其中红色区域部分V通道的数值较大
    merge_arr = merge_counter(arr)
    for k in range(0, len(merge_arr)):
        x, y, w, h = cv2.boundingRect(merge_arr[k])
        left = x-w//4 if x-w//4 >= 0 else 0
        right = x+w*5//4 if x+w*5//4 <= img_h.shape[1] else img_h.shape[1]
        top = y-h//4 if y-h//4 >= 0 else 0
        bottom = y+h*5//4 if y+h*5/4 <= img_h.shape[0] else img_h.shape[0]
        for i in range(top, bottom):
            for j in range(left, right):
                if img_v[i, j] < ave_th or r[i, j] < b[i, j] or r[i, j] < g[i, j]:
                    img_red[i, j] = img_copy[i, j]
                else:
                    img_red[i, j] = [255, 255, 255]
    return img_red


def remove_seal_main(image):
    img_non_seal = remove_seal(image)
    return img_non_seal


if __name__ == '__main__':
    img_filename = '0005.jpg'
    img_filename = cv2.imread(img_filename)

    img_non_seal = remove_seal_main(img_filename)
    cv2.imwrite('img_non_seal1.jpg',img_non_seal)
    # cv2.imshow('GRAY', img_non_seal)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows().cvtColor()