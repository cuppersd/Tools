import json
import os
import numpy as np
from PIL import Image

def get_directed_area(polygon: np.ndarray) -> float:
    """计算多边形的有向面积: 顺时针为负, 逆时针为正"""
    p = polygon.reshape(-1, 2)  # 右下坐标系
    n_sides = p.shape[0]  # 多边形端点数
    sides = np.zeros(n_sides)
    for i in range(n_sides):
        j = i + 1 if i + 1 < n_sides else 0
        side = (p[j][0] - p[i][0]) * (p[j][1] + p[i][1]) / 2  # 投射在x轴上梯形的有向面积
        sides[i] = side
    return sides.sum()

def sort_loc(loc: np.ndarray) -> np.ndarray:
    """将多边形的端点从左上角的点开始, 按顺时针排列"""
    loc = loc.reshape(-1, 2)
    idx_top_left = np.argmin(loc.sum(axis=1))  # 左上角的点以横纵坐标之和最小确定
    da = get_directed_area(loc)  # 求有向面积
    if da < 0:  # 顺时针
        pts_sorted = np.vstack([loc[idx_top_left:], loc[:idx_top_left]])
    elif da > 0:  # 逆时针
        pts_sorted = np.vstack([loc[idx_top_left::-1], loc[:idx_top_left:-1]])
    else:
        raise ValueError('directed_area == 0')
    return pts_sorted

class Dataset:
    def __init__(self, root_img, root_txt, txt_prefix='', invalid_ok=True):
        self.root_img = root_img
        self.root_txt = root_txt
        self.txt_prefix = txt_prefix
        self.invalid_ok = invalid_ok
        self.loaded = False
        self.output = {}

    def _proc_data(self):
        for img_f in os.listdir(self.root_img):
            print(img_f)
            fname, ext = os.path.splitext(img_f)
            if ext.lower() not in ['.jpg', '.png', '.jpeg','.gif']:
                continue
            size = self._get_img_bytes(self.root_img, img_f)
            img_size = self._get_img_size(self.root_img, img_f)
            txt_f = 'gt_' + img_f[:-3]+'txt'
            try:
                regions = self._parse_txt(root_txt, txt_f, img_size, invalid_ok=self.invalid_ok)
            except:
                print(img_f,"----------------")
                continue

            k = '{}{}'.format(img_f, size)
            self.output[k] = dict(fileref='',
                                  size=size,
                                  filename=img_f,
                                  base64_img_data='',
                                  file_attributes={},
                                  regions=regions)

    @staticmethod
    def _get_img_bytes(root_img, fname):
        img_path = os.path.join(root_img, fname)
        with open(img_path, 'rb') as f:
            size = len(f.read())
        return size

    @staticmethod
    def _get_img_size(root_img, fname):
        img_path = os.path.join(root_img, fname)
        with Image.open(img_path) as img:
            return img.size

    @staticmethod
    def _parse_txt(root_txt, fname, img_size, invalid_ok=True):
        txt_path = os.path.join(root_txt, fname)
        output = {}
        idx = 0
        with open(txt_path, encoding='utf-8') as f:
            for line in f:
                line_split = line.strip().split(',', maxsplit=9)
                coords = list(map(int, line_split[:8]))
                script, text = line_split[-2:]
                is_valid = (script != 'None' and text != '###')
                if not invalid_ok and not is_valid:
                    continue
                coords = sort_loc(np.array(coords))
                coords = np.clip(coords, a_min=[0, 0], a_max=img_size)  # 防止边界超出框
                coords = coords.astype(int).flatten().tolist()
                shape_attributes = dict(name='polygon',
                                        all_points_x=coords[0::2],
                                        all_points_y=coords[1::2])
                output[str(idx)] = dict(shape_attributes=shape_attributes,
                                        region_attributes={})
                idx += 1
        return output

    def load(self):
        if self.loaded:
            print('>>> already loaded')
            return
        else:
            self._proc_data()
            self.loaded = True
            print('>>> loaded')

    def save(self, save_path, **kwargs):
        if not self.loaded:
            print('>>> data not loaded')
            return
        else:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.output, f, ensure_ascii=False, **kwargs)
            print('>>> saved:', save_path)


if __name__ == '__main__':
    root_img = './img'
    root_txt = './gt'
    save_to = 'via_region_data.json'
    dataset = Dataset(root_img, root_txt, txt_prefix='gt_', invalid_ok=True)
    dataset.load()
    dataset.save(save_to)
