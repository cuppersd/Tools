//#include<iostream>
//#include<vector>
//using namespace std;
//int main() {
//	vector<int> list = {3,3,5,1,5};
//	int res = 0;
//	for (auto num : list) {
//		
//		cout << res<<"^"<<num << "="<<(res ^ num)<<endl;
//		res = res ^ num;
//	}
//	cout << res << endl;
//	cin.get();
//	return 0;
//}


#include<iostream>
#include<vector>
using namespace std;
class Solution
{
public:
	int singleNumber(vector<int>& nums) {
		int res = 0;
		for (auto num : nums) {
			res = res ^ num;
		}
		return res;
	}
};
int main() {
	vector<int> list = { 5,2,3,6,3,5,2 };
	Solution s;
	cout << s.singleNumber(list) << endl;
	cin.get();
	return 0;
}