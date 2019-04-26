import datetime
import json
import os
from PIL import Image
from termcolor import colored


root_images = '/data/zhangjie/MLT_2017/images_train/'
root_annotations = '/data/zhangjie/MLT_2017/gt_train/'
save_to = './anno_COCO_indented.json'


def get_now_date():
    """获取当前日期"""
    now = datetime.datetime.now()
    return now.strftime('%Y/%m/%d')


def get_image_info(file_name):
    image_path = os.path.join(root_images, file_name)
    image_info = {}
    if not os.path.isfile(image_path):
        print(colored('error:', 'red'), '{} not found.'.format(file_name))
        return
    with Image.open(image_path) as im:
        image_info['width'], image_info['height'] = im.size
    return image_info


class COCO:
    """COCO格式数据集"""
    def __init__(self, info: dict):
        self._description = info.get('description')
        self._url = info.get('url')
        self._version = info.get('version', '1.0')
        self._year = info.get('year')
        self._contributor = info.get('contributor')
        self._date_created = info.get('date_created', get_now_date())
        self._info = dict(description=self._description,
                          url=self._url,
                          version=self._version,
                          year=self._year,
                          contributor=self._contributor,
                          date_created=self._date_created)
        self._licenses = []
        self._images = []
        self._annotations = []
        self._categories = []
        self._image2id = {}
        self._dataset = {}

    def add_license(self, name, url):
        idx = self._licenses[-1]['id'] + 1 if len(self._licenses) > 0 else 0
        self._licenses.append(dict(name=name, url=url, id=idx))

    def add_category(self, name):
        idx = self._categories[-1]['id'] + 1 if len(self._categories) > 0 else 0
        self._categories.append(dict(name=name, id=idx))

    def add_image(self, file_name, license_id=None):
        idx = self._images[-1]['id'] + 1 if len(self._images) > 0 else 0
        image = dict(file_name=file_name, id=idx)
        self._image2id[file_name] = idx
        size = get_image_info(file_name)
        if size:
            image.update(size)
        if license_id is not None:
            image['license'] = license_id
        self._images.append(image)

    def add_annotation(self, file_name, bbox: list, text='', category_id=0):
        idx = self._annotations[-1]['id'] + 1 if len(self._annotations) > 0 else 0
        annotation = dict(bbox=bbox, text=text, id=idx, category_id=category_id)
        image_id = self._image2id.get(file_name)
        if image_id is None:
            print(colored('error:', 'red'), '{} not processed.'.format(file_name))
            # return
            raise
        annotation['image_id'] = image_id
        self._annotations.append(annotation)

    def process(self):
        if not all([len(self._images) > 0, len(self._annotations) > 0]):
            print(colored('error:', 'red'), 'wrong size for images or annotations')
            return
        self._dataset = dict(info=self._info,
                             licenses=self._licenses,
                             categories=self._categories,
                             images=self._images,
                             annotations=self._annotations)

    def save(self, save_to: str, **kwargs):
        if not save_to.lower().endswith('.json'):
            print(colored('error:', 'red'), 'wrong format')
            return
        save_to = os.path.abspath(save_to)
        with open(save_to, 'w', encoding='utf-8') as f:
            json.dump(self._dataset, f, ensure_ascii=False, **kwargs)
            print(colored('saved:', 'blue'), save_to)


if __name__ == '__main__':
    info = dict(description='日文数据集',
                url='http://www.aibabel.com',
                version='1.0',
                year=2019,
                contributor='Babel Technology Co., Ltd.')
    coco = COCO(info)
    coco.add_category('text')  # category_0

    for image_f in os.listdir(root_images):
        if not image_f.lower().endswith('.jpg'):
            continue
        coco.add_image(image_f)

    # for anno_f in os.listdir(root_annotations):
    #     if not anno_f.lower().endswith('.txt'):
    #         continue
        anno_f = image_f.replace('.jpg', '.txt')
        anno_path = os.path.join(root_annotations, anno_f)
        # image_f = anno_f.replace('.txt', '.jpg')
        with open(anno_path, encoding='utf-8') as f:
            anno_data = f.read().strip().split('\n')
        for line in anno_data:
            line_split = line.split(',', maxsplit=8)
            line_bbox = list(map(int, line_split[:8]))
            line_text = line_split[-1] if len(line_split) > 8 else ''
            if line_text.startswith('\"') and line_text.endswith('\"'):
                line_text = json.loads(line_text)
            try:
                coco.add_annotation(image_f, line_bbox, line_text, 0)
            except:
                print(image_f)
            

    coco.process()
    coco.save(save_to, indent=2)
