import torch
from torch import nn, optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 超参数设置
batch_size = 64
learning_rata = 1e-3
num_epoches = 1

# 神经网络设置
class Batch_Net(nn.Module):
	"""docstring for Batch_Net"""
	def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
		super(Batch_Net, self).__init__()
		self.layer1 = nn.Sequential(nn.Linear(in_dim,n_hidden_1), nn.BatchNorm1d(n_hidden_1), nn.ReLU(True))
		self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.BatchNorm1d(n_hidden_2), nn.ReLU(True))
		self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, out_dim))

	def forward(self, x):
		x = self.layer1(x)
		x = self.layer2(x)
		x = self.layer3(x)
		return x
		
# 数据预处理方法
data_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5],[0.5])])
# 下载打包训练和测试数据
train_dataset = datasets.MNIST(root='./data', train=True, transform=data_tf, download=False)
test_dataset = datasets.MNIST(root='./data', train=False, transform=data_tf, download=True)
# 加载训练和测试数据
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)
# 实例化模型
if torch.cuda.is_available():
	model = Batch_Net(28 * 28, 300, 100, 10).cuda()
else:
	model = Batch_Net(28 * 28, 300, 100, 10)
# 设置损失函数和优化方法
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rata)
# 开启训练，每一个epoch打印loss
for epoch in range(num_epoches):
	for x_train,y_train in train_loader:
		x_train = x_train.view(x_train.size(0), -1).cuda()
		y_train = y_train.cuda()
		prediction = model(x_train)
		loss = criterion(prediction, y_train)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
	print("loss:{:.6f}".format(loss.data))

# 验证训练模型
model.eval()
# 验证损失值和准确率
eval_loss = 0
eval_acc = 0
for test_data in test_loader:
	test_img, test_label = test_data
	test_img = test_img.view(test_img.size(0), -1).cuda()
	test_label = test_label.cuda()
	out = model(test_img)
	loss = criterion(out, test_label)

	eval_loss += loss.item() * test_label.size(0)  # tensor只有一个元素时，tensor.item(),否则不可用
	_, pred = torch.max(out, 1) 
	num_correct = (pred==test_label).sum().cpu()
	eval_acc += num_correct.item()
print('loss:{:.6f},acc:{:.6f}'.format(eval_loss/len(test_dataset), eval_acc/len(test_dataset)))

