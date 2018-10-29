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

### [1. VS2017图像处理OpenCV](https://blog.csdn.net/sinat_36264666/article/details/73135823?ref=myread)
