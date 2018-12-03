#include "stdafx.h"
#include<iostream>
// 将n个从x移动到z，借助y，起点：X（n） ，介质：Y，终点：Z，-->起点：X ，介质：Y，终点：Z（n）
void towerhannoi(int n,char x,char y,char z) {
	if (n) {
		towerhannoi(n - 1, x, z, y); // 起点：X（n） ，介质：Y，终点：Z -->起点：X（1） ，介质：Y(n-1)，终点：Z
		std::cout << x << "->" << z << std::endl; //起点：X（1） ，介质：Y(n-1)，终点：Z -->起点：X ，介质：Y(n-1)，终点：Z(1)
		towerhannoi(n - 1, y, x , z);
	
	}
}
int main()
{
	towerhannoi(3,'X','Y','Z');
	while (1);

    return 0;
}

