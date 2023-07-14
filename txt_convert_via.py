_via_image_id_list = []
_via_data_format_version = "2.0.10"
_via_attributes = {"region": {},"file": {}}
_via_settings= {
        "ui": {
            "annotation_editor_height": 25,
            "annotation_editor_fontsize": 0.8,
            "leftsidebar_width": 18,
            "image_grid": {
                "img_height": 80,
                "rshape_fill": "none",
                "rshape_fill_opacity": 0.3,
                "rshape_stroke": "yellow",
                "rshape_stroke_width": 2,
                "show_region_shape": True,
                "show_image_policy": "all"
            },
            "image": {
                "region_label": "__via_region_id__",
                "region_color": "__via_default_region_color__",
                "region_label_font": "10px Sans",
                "on_image_annotation_editor_placement": "NEAR_REGION"
            }
        },
        "core": {
            "buffer_size": 18,
            "filepath": {},
            "default_filepath": ""
        },
        "project": {
            "name": "1"
        }
    }
_via_img_metadata = {}

lines = open("driver_card_det.txt", "r").readlines()

for line in lines:
    fn = "http://182.160.16.91/m/driver_card_det_jpg/" + line.strip()
    _via_image_id_list.append(fn + "-1")

    polygon_list = []
    txt__line = open("txts_driver/" + line.strip()[:-4] + ".txt", "r", encoding="utf-8").readlines()
    for txt_l in txt__line:
        t_sp = txt_l.split("\t")[0].split(",")
        # print(t_sp)
        t_sp = [int(float(i)) for i in t_sp]
        x = []
        y = []
        for i in range(len(t_sp) //2):
            x.append(t_sp[2*i])
            y.append(t_sp[2*i+1])

        polygon_list.append(               {
                    "shape_attributes": {
                        "name": "polygon",
                        "all_points_x": x,
                        "all_points_y": y
                    },
                    "region_attributes": {}
                })




    _via_img_metadata[fn+"-1"] = {
            "filename": fn,
            "size": -1,
            "regions": polygon_list,
            "file_attributes": {}
        }

save_data = {}

save_data["_via_settings"] = _via_settings
save_data["_via_img_metadata"] = _via_img_metadata
save_data["_via_attributes"] = _via_attributes
save_data["_via_image_id_list"] = _via_image_id_list
save_data["_via_data_format_version"] = _via_data_format_version

print(save_data)

import json
def save_json(dict_data, json_save_path):
    with open(json_save_path, 'w', encoding='utf-8') as f:
        json.dump(dict_data, f, ensure_ascii=False, indent=4)
save_json(save_data, "123.json")
