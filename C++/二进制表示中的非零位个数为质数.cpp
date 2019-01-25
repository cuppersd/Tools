#include<iostream>
#include<vector>
using namespace std;
class Solution
{
public:
	vector<int> countPrimeSetBits(int L, int R) {
		vector<int> res;
		for (int i = L; i <= R; i++) {
			int count = 0,p=i;
			while (p > 0) {
				if (p & 1) {
					count++;
				}
				p = p >> 1;
			}
			bool flag = true;
			for (int j = 2; j <= sqrt(count); j++) {
				if ((count%j) == 0) {
					flag = false;
					break;
				}
			}
			if (flag && (count>1)) {
				res.push_back(i);
				cout << i << ":" << count << endl;
			}
		}
		return res;
	}

};

int main() {
	int L = 10, R = 15;
	Solution ss;
	vector<int> dd = ss.countPrimeSetBits(L, R);
	for (int de : dd) {
		cout << de << endl;
	}
	cin.get();
	return 0;
}