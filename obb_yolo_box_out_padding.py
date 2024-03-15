# 该文件用于旋转目标检测，标注框超出图片范围，通过padding将四个角点都放在图片内


import cv2
import numpy as np
import os




img_file_name = "K:/mm-code/ultralytics_train/data/nin_paper/images/val/"
txt_file_name = "K:/mm-code/ultralytics_train/data/nin_paper/labels/val_original/"

image_list = os.listdir(img_file_name)

for fn in image_list:
    if fn.startswith("rotate"):
        continue
    txt_p = txt_file_name + fn[:-4] + ".txt"
    img_p = img_file_name + fn

    np_im = cv2.imread(img_p)
    height, width = np_im.shape[:2]

    lines = open(txt_p, "r", encoding="utf-8").readlines()
    f_n = open("./padding/"+fn[:-4] + ".txt", "w", encoding="utf-8")

    for line in lines:
        
        cords = line.split(" ")[:8]
        cords = [int(i) for i in cords]
        x_list = [cords[i] for i in range(8) if i%2==0]
        y_list = [cords[i] for i in range(8) if i%2==1]
        left_a = 0
        up_a = 0
        down_a = 0
        right_a = 0
        if min(x_list) <= 0:
            left_a = -min(x_list)

        if min(y_list) <= 0:
            up_a = -min(y_list)

        if max(y_list) - height >= 0:
            down_a = max(y_list) - height

        if max(x_list) - width >= 0:
            right_a = max(x_list) - width

        if max([up_a, down_a, left_a, down_a]) > 0:
            print(fn)
            print("old:", line)

        up_a = up_a + 1
        down_a = down_a + 1
        left_a = left_a + 1
        right_a = right_a + 1
        n_image = cv2.copyMakeBorder(np_im, up_a, down_a, left_a, right_a, cv2.BORDER_CONSTANT, value=(127, 127, 127))
        x_list = [i+left_a for i in x_list]
        y_list = [i+up_a for i in y_list]
        cv2.imwrite("./padding/" + fn, n_image)
        w_cords = []
        for x, y in zip(x_list, y_list):
            w_cords.append(x)
            w_cords.append(y)

        f_n.write(" ".join([str(i) for i in w_cords]) + " card 0\n")
        max_cords = np.array(w_cords)
        n_image = cv2.polylines(n_image, [max_cords.reshape(-1,1,2).astype(np.int32)], isClosed=True, color=(255,0,0),thickness=6)
        # print("new:", " ".join([str(i) for i in w_cords]) + " card 0\n")
        cv2.imwrite("./padding/" + "vis_" + fn, n_image)



    # break