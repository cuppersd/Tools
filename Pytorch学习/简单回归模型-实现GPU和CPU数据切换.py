import torch
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt
from torch import nn
from torch import optim

# numpy 格式的数据， 注意：指明数据类型，不然后面会报错
x_train = np.array([[3.3],[4.4],[5.5],[6.71],[6.93],[4.168],[9.779],[6.182],[7.59],[2.167],[7.042],[10.791],[5.313],[7.997],[3.1]],dtype=np.float32)
y_train = np.array([[1.7],[2.76],[2.09],[3.19],[1.694],[1.573],[3.366],[2.596],[2.53],[1.221],[2.827],[3.465],[1.65],[2.904],[1.3]],dtype=np.float32)
# 转化为pytorch格式的Tensor
x_train_torch = torch.from_numpy(x_train).float()
y_train_torch = torch.from_numpy(y_train).float()


# 模型搭建
class LinearRegression(nn.Module):
	"""docstring for LinearRegression"""
	def __init__(self):
		super(LinearRegression, self).__init__()
		self.linear = nn.Linear(1,1)

	def forward(self,x):
		out = self.linear(x)
		return out

# 判断是否有GPU存在，若存在模型放在GPU上，若不存在模型放在CPU
if torch.cuda.is_available(): 
	model = LinearRegression().cuda()
else:
	model = LinearRegression()

# 损失函数的定义
criterion = nn.MSELoss()
# 优化器的定义
optimizer = optim.SGD(model.parameters(), lr=0.003)

num_epochs = 1000
for epoch in range(num_epochs):
	if torch.cuda.is_available(): # 判断GPU是否存在，若存在输入和输出都放在GPU
		inputs = Variable(x_train_torch).cuda()
		target = Variable(y_train_torch).cuda()
	else:
		inputs = Variable(x_train_torch)
		target = Variable(y_train_torch)		

	out = model(inputs)
	loss = criterion(out, target)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()

# 用模型做验证，先要申明一下	
model.eval()
predict = model(Variable(x_train_torch).cuda()).cpu() # 模型在GPU上，验证的时候输入也要放在GPU上，但是作图的时候需要放在cup上，故后面加上cpu
plt.plot(x_train, y_train, 'ro', label='original data')		
plt.plot(x_train, predict.data.numpy(), 'bo', label='Fitting Line')		
plt.show()