# 技术总结
### [1. tensorflow 报错 libcusolver.so.8.0: cannot open shared object file: No such file or directory](https://blog.csdn.net/u012223913/article/details/78675284)
`echo $LD_LIBRARY_PATH`

`/usr/local/cuda-8.0/lib64`

* 解决方案，执行以下命令：

`sudo ldconfig /usr/local/cuda-8.0/lib64`
