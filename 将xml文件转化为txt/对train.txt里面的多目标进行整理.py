f = open('train.txt','r').readlines()
ff = open('train.txt','r').readlines()
fff = open('train11.txt','w')
my = {}
# 初始化
for x in f:
	x = x[:-1].split(' ')
	my[x[0]] = x[0]

for xx in ff:
	xx = xx[:-1].split(' ')
	my[xx[0]] = my[xx[0]] + ' ' + xx[1]


for xxx in my.keys():
	fff.write(my[xxx] + '\n')
fff.close()
print(my)