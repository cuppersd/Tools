# -*- coding: utf-8 -*-
import os
import glob
import mmcv
import os.path as osp

name_dict = {'province': 1, 'city': 2, 'nik': 3, 'nama': 4, 'tempat': 5, 'jenis': 6, 'gol': 7, 'alamat': 8, 'rtrw': 9, 'kel': 10, 'kecamatan': 11, 'agama': 12, 'status': 13, 'pekerjaan': 14, 'kewarganegaraan': 15, 'berlaku': 16, 'photocity': 17, 'phototime': 18}
categories_dict = []
for k, v in name_dict.items():
    categories_dict.append({"id":v-1, "name":k})



def via_convert_coco(path):
    fn_list = list(glob.glob(path + "*.json"))
    annotations = []
    images = []
    obj_count = 0
    for idx, json_path in enumerate(fn_list):
        data_infos = mmcv.load(json_path)
        filename = data_infos['filename']
        img_path = osp.join(path, filename)
        height, width = mmcv.imread(img_path).shape[:2]
        images.append(dict(
            id=idx,
            file_name=filename,
            height=height,
            width=width))

        bboxes = []
        labels = []
        masks = []
        for reg in data_infos['regions']:
            if 'key' not in reg['region_attributes'].keys():
                print("no labels:", json_path)
                # print(reg)
                continue
            if 'rect' == reg['shape_attributes']['name']:
                x = reg['shape_attributes']['x']
                y = reg['shape_attributes']['y']
                width = reg['shape_attributes']['width']
                height = reg['shape_attributes']['height']
                line = [x, y, x + width, y, x + width, y + height, x, y + height]
                data_anno = dict(
                    image_id=idx,
                    id=obj_count,
                    category_id=name_dict[reg['region_attributes']['key']] - 1,
                    bbox=[x, y, width, height],
                    area=width * height,
                    segmentation=[line],
                    iscrowd=0)
                annotations.append(data_anno)
                obj_count += 1

            elif 'polygon' == reg['shape_attributes']['name']:
                if len(reg['shape_attributes']["all_points_x"]) < 4:
                    print("polygon error:", json_path)
                obj = reg['shape_attributes']
                px = obj['all_points_x']
                py = obj['all_points_y']
                poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
                poly = [p for x in poly for p in x]

                x_min, y_min, x_max, y_max = (
                    min(px), min(py), max(px), max(py))

                data_anno = dict(
                    image_id=idx,
                    id=obj_count,
                    category_id=name_dict[reg['region_attributes']['key']] - 1,
                    bbox=[x_min, y_min, x_max - x_min, y_max - y_min],
                    area=(x_max - x_min) * (y_max - y_min),
                    segmentation=[poly],
                    iscrowd=0)
                annotations.append(data_anno)
                obj_count += 1
            else:
                print("error:", json_path)
                print(reg)

    coco_format_json = dict(
        images=images,
        annotations=annotations,
        categories=categories_dict)
    mmcv.dump(coco_format_json, "./text_line_det_coco.json")



if __name__ == "__main__":
    path = "C:/Users/jiezh/Desktop/indone_coco/imgs/"
    via_convert_coco(path)