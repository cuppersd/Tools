import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

max_steps=1000 # 训练最大步数
learning_rate=0.001 # 设置学习率
dropout=0.9 # 神经元保留比例
data_dir='./MNIST_data' # 数据存放路径  百度网盘下载 链接: https://pan.baidu.com/s/13M8TYuw77D_cH0tnLU4O4g 密码: xa2w
log_dir='./' # 日志保存路径


# 初始化权重函数
  # We can't initialize these variables to 0 - the network will get stuck.
def weight_variable(shape):
  """Create a weight variable with appropriate initialization."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

# 初始化偏置函数
def bias_variable(shape):
  """Create a bias variable with appropriate initialization."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

# 将某个变量写入tensorboard
def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean) # 写入均值
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean))) # 写入方差
    tf.summary.scalar('stddev', stddev) # 写入方差
    tf.summary.scalar('max', tf.reduce_max(var)) # 写入最大值
    tf.summary.scalar('min', tf.reduce_min(var)) # 写入最小值
    tf.summary.histogram('histogram', var)  # 绘制直方图

def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
  """Reusable code for making a simple neural net layer.
  It does a matrix multiply, bias add, and then uses relu to nonlinearize.
  It also sets up name scoping so that the resultant graph is easy to read,
  and adds a number of summary ops.
  """
  # Adding a name scope ensures logical grouping of the layers in the graph.
  with tf.name_scope(layer_name):
    # This Variable will hold the state of the weights for the layer
    with tf.name_scope('weights'):
      weights = weight_variable([input_dim, output_dim])
      variable_summaries(weights) # 记录变量
    with tf.name_scope('biases'):
      biases = bias_variable([output_dim])
      variable_summaries(biases) # 记录变量
    with tf.name_scope('Wx_plus_b'):
      preactivate = tf.matmul(input_tensor, weights) + biases
      tf.summary.histogram('pre_activations', preactivate) # 激活前的直方图
    activations = act(preactivate, name='activation')
    tf.summary.histogram('activations', activations) # 激活后的直方图，观察激活前后的直方图变化
    return activations




  # Import data
mnist = input_data.read_data_sets(data_dir,one_hot=True)
sess = tf.InteractiveSession()


#-----------------------------------------------------------------------------------------------------------
  # Create a multilayer model.
  # Input placeholders
  # 创建输入
with tf.name_scope('input'):
  x = tf.placeholder(tf.float32, [None, 784], name='x-input')
  y_ = tf.placeholder(tf.float32, [None, 10], name='y-input')

  # 对创建的输入进行reshape。
with tf.name_scope('input_reshape'):
  image_shaped_input = tf.reshape(x, [-1, 28, 28, 1])
  tf.summary.image('input', image_shaped_input, 10)
# 该部分主要用于在tensorboard中展示图片

hidden1 = nn_layer(x, 784, 500, 'layer1')
with tf.name_scope('dropout'):
  keep_prob = tf.placeholder(tf.float32) # 此变量需要run时feed进来
  tf.summary.scalar('dropout_keep_probability', keep_prob) # 记录keep_prob随着训练步数的变化曲线
  dropped = tf.nn.dropout(hidden1, keep_prob) # 将第一层的结果进行dropout
  # Do not apply softmax activation yet, see below.

y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

# 此部分是整个模型框架，包括输入每一层的搭建需要feed(x-input,y-input,keep-prob)
#-----------------------------------------------------------------------------------------------------------

with tf.name_scope('cross_entropy'):
    # The raw formulation of cross-entropy,
    #
    # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
    #                               reduction_indices=[1]))
    #
    # can be numerically unstable.
    #
    # So here we use tf.nn.softmax_cross_entropy_with_logits on the
    # raw outputs of the nn_layer above, and then average across
    # the batch.
  diff = tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_)
  with tf.name_scope('total'):
    cross_entropy = tf.reduce_mean(diff) # 求取平均值

tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'): # 执行训练
  train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

with tf.name_scope('accuracy'): # 执行准确率
  with tf.name_scope('correct_prediction'):
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  with tf.name_scope('accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)
 
  # Merge all the summaries and write them out to /tmp/mnist_logs (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(log_dir + '/train', sess.graph)
test_writer = tf.summary.FileWriter(log_dir + '/test')
tf.global_variables_initializer().run()
  # Train the model, and also write summaries.
  # Every 10th step, measure test-set accuracy, and write test summaries
  # All other steps, run train_step on training data, & add training summaries

def feed_dict(train):
  """Make a TensorFlow feed_dict: maps data onto Tensor placeholders."""
  if train:
    xs, ys = mnist.train.next_batch(100)
    k = dropout
  else:
    xs, ys = mnist.test.images, mnist.test.labels
    k = 1.0
  return {x: xs, y_: ys, keep_prob: k}

saver = tf.train.Saver()  # 用于保存模型文件

for i in range(max_steps): # 一共训练的step数目
  # 记录测试结果
  if i % 10 == 0:  # Record summaries and test-set accuracy # 每隔10次测试一次准确率，并写入summary
    summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False)) # 运行准确率，并且记录summary
    test_writer.add_summary(summary, i) # 将所有要记录的变量写入summary
    print('Accuracy at step %s: %s' % (i, acc)) # 输出准确率
  
  # 每隔100个step记录训练结果，保存模型文件
  else:  # Record train set summaries, and train
    if i % 100 == 99:  # Record execution stats
      run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
      run_metadata = tf.RunMetadata() # 这两行代码是记录运行状态的
      summary, _ = sess.run([merged, train_step],
                            feed_dict=feed_dict(True),
                            options=run_options,
                            run_metadata=run_metadata)
      train_writer.add_run_metadata(run_metadata, 'step%03d' % i)
      train_writer.add_summary(summary, i)
      saver.save(sess, log_dir+"./model/model.ckpt", i)
      print('Adding run metadata for', i)
    else:  # Record a summary
      summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
      train_writer.add_summary(summary, i)
train_writer.close()
test_writer.close()

