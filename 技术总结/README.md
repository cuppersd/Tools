# 技术总结
### [1. tensorflow 报错 libcusolver.so.8.0: cannot open shared object file: No such file or directory](https://blog.csdn.net/u012223913/article/details/78675284)
`echo $LD_LIBRARY_PATH`

`/usr/local/cuda-8.0/lib64`

* 解决方案，执行以下命令：

`sudo ldconfig /usr/local/cuda-8.0/lib64`

### 2. Python 安装模块更换源
`pip3 install django -i http://pypi.douban.com/simple --trusted-host pypi.douban.com`

### 3. Python 后台启动服务，启动后不关闭
`nohup python manage.py runserver 0.0.0.0:8330 &`

### 4. ffmpeg 将视频转化为gif图片
* 将视频 MP4 转化为 GIF

`ffmpeg -i small.mp4 small.gif`

* 转化视频中的一部分为 GIF，从视频中第二秒开始，截取时长为3秒的片段转化为 gif

`ffmpeg -t 3 -ss 00:00:02 -i small.webm small-clip.gif`

* 转化高质量 GIF，默认转化是中等质量模式，若要转化出高质量的 gif，可以修改比特率

`ffmpeg -i 2.mp4 -b 2048k small.gif`

### [5. VS2017图像处理OpenCV](https://blog.csdn.net/sinat_36264666/article/details/73135823?ref=myread)


### [6. CTPN（原始）](https://blog.csdn.net/sinat_36264666/article/details/73135823?ref=myread), [CTPN（定位加识别）](https://github.com/YCG09/chinese_ocr)

[其中的一段代码需要编译，以下是编译步骤](https://github.com/eragonruan/text-detection-ctpn/issues/73)

my environment is:

windows10 ,

python3.6 ,

tensorflow1.3 ,

vs2015(ps:vs2013 not support python3.6 when compile)

step 1:make some change

change "np.int_t " to "np.intp_t" in line 25 of the file lib\utils\cython_nms.pyx

otherwise appear " ValueError: Buffer dtype mismatch, expected 'int_t' but got 'long long' " in step 6.

step 2:updata c file

execute:cd your_dir\text-detection-ctpn-master\lib\utils

execute:cython bbox.pyx

execute:cython cython_nms.pyx

step 3:builf setup file as setup_new.py

import numpy as np

from distutils.core import setup

from Cython.Build import cythonize

from distutils.extension import Extension

numpy_include = np.get_include()

setup(ext_modules=cythonize("bbox.pyx"),include_dirs=[numpy_include])

setup(ext_modules=cythonize("cython_nms.pyx"),include_dirs=[numpy_include])

step 4:build .pyd file

execute:python setup_new.py install

copy bbox.cp36-win_amd64.pyd and cython_nms.cp36-win_amd64.pyd to your_dir\text-detection-ctpn-master\lib\utils

step 5:make some change

(1) Set "USE_GPU_NMS " in the file \ctpn\text.yml as "False"

(2) Set the "_C.USE_GPU_NMS" in the file \lib\fast_rcnn\config.py as "False";

(3) Comment out the line "from lib.utils.gpu_nms import gpu_nms" in the file \lib\fast_rcnn\nms_wrapper.py;

(4) Comment out the line "from . import gpu_nms" in the file \lib\utils_init.py;

(5) change "base_name = image_name.split('/')[-1]" to "base_name = image_name.split('\')[-1]" in line 24 of the file ctpn\demo.py

step 6:run demo

execute:cd your_dir\text-detection-ctpn-master

execute:python ./ctpn/demo.py

### 7. [Ubuntu显卡驱动安装与更新](https://blog.csdn.net/seymour163/article/details/78798419)

ctrl+alt+f1进入tty

1 第一句删除掉之前nv文件，不执行这句可能执行后面的也能进得去系统，最好执行

`sudo apt-get purge nvidia*`

2 Add the graphics-driver PPA

`sudo add-apt-repository ppa:graphics-drivers`

3 And update

`sudo apt-get update`

`sudo apt-get install nvidia-375`

4 375相对我原来的381可能更稳吧,有个后话，我试了更新的驱动，比如387也进来系统了，或许是别的原因导致进不来的，还不清楚原因。

### 8. [Ubuntu远程桌面的安装](https://blog.csdn.net/sinolover/article/details/78673625)

### 9. [Ubuntu用户添加删除权限管理](https://blog.csdn.net/cugxyy6/article/details/80690768)

### 10. [最新CRNN代码](https://blog.csdn.net/Sierkinhane/article/details/82857572)

### 11. 通配符删文件 for i in ROTATE_*; do rm -f ${i}; done

### 12. cv2.imread('1.jpg',cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)

### 13. Tensorflow serving部署。
官网教程：https://tensorflow.google.cn/tfx/serving/docker?hl=RU
代码教程1：https://medium.com/tensorflow/training-and-serving-ml-models-with-tf-keras-fd975cc0fa27
代码教程2：https://gist.github.com/asimshankar/000b8d276f211f972168afa138eb3cc7

### 14. NVIDIA DOCKER的安装：https://github.com/NVIDIA/nvidia-docker | 在tensorflow serving 部署之前必须要安装NVIDIA DOCKER才可以GPU部署docker run --runtime=nvidia -t --rm -p 8501:8501 -e CUDA_VISIBLE_DEVICES=3    -v "$TESTDATA/saved_model_half_plus_two_gpu:/models/half_plus_two"     -e MODEL_NAME=half_plus_two     tensorflow/serving:latest-gpu &

