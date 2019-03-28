import tensorflow as tf
# # 声明两个变量
# v1 = tf.Variable(tf.random_normal([1, 2]), name="v1")
# v2 = tf.Variable(tf.random_normal([2, 3]), name="v2")
# init_op = tf.global_variables_initializer() # 初始化全部变量
# saver = tf.train.Saver() # 声明tf.train.Saver类用于保存模型
# with tf.Session() as sess:
#     sess.run(init_op)
#     print("v1:", sess.run(v1)) # 打印v1、v2的值一会读取之后对比
#     print("v2:", sess.run(v2))
#     saver_path = saver.save(sess, "save/model.ckpt")  # 将模型保存到save/model.ckpt文件
#     print("Model saved in file:", saver_path)
# saver = tf.train.import_meta_graph('./save/model.ckpt.meta', clear_devices=True)
# graph = tf.get_default_graph() # 获得默认的图
# input_graph_def = graph.as_graph_def()  # 返回一个序列化的图代表当前的图
# print(help(input_graph_def ))
# print(input_graph_def.node)
import os
from tensorflow.python import pywrap_tensorflow
checkpoint_path = os.path.join('./save/', "captcha-900")
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
for key in var_to_shape_map:
    print("tensor_name: ", key)
    print(reader.get_tensor(key)) # Remove this is you want to print only variable names