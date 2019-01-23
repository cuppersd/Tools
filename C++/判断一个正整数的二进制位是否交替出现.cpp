// 输入一个正整数n，将其转化为二进制，判断0,1是否是交替出现

#include<iostream>
using namespace std;
class Solution
{
public:
	bool hasAlternatingBit(int n) {
		int bit = -1;
		while (n>0)
		{
			if (n & 1 == 1) {
				if (bit == 1) {
					return false;
				}
				bit = 1;
			}
			else
			{
				if (bit == 0) {
					return false;
				}
				bit = 0;
			}
			n = n >> 1;
		}
		return true;
	}
};

int main() {
	Solution solution;
	cout.setf(ios::boolalpha);
	cout << solution.hasAlternatingBit(3) << endl;

	cin.get();
	return 0;
}