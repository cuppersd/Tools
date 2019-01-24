//#include<iostream>
//#include<vector>
//#include<unordered_map>
//using namespace std;
//class solution
//{
//public:
//	vector<int> twoSum(vector<int>& nums, int target) {
//		unordered_map<int, int> m;
//		vector<int> res;
//		for (int i = 0; i < nums.size(); i++)
//		{
//			m[nums[i]] = i;
//		}
//
//		
//		for (int i = 0; i < nums.size(); i++)
//		{
//			int t = target - nums[i];
//			if (m.count(t) != 0 && t!=nums[i]) {
//				res.push_back(i);
//				res.push_back(m[t]);
//			}
//			else {
//				continue;
//			}
//		}
//		return res;
//	}
//
//};
//
//int main() {
//	vector<int> list = { 1,8,2,7,11,8,15 };
//	solution ss;
//	vector<int> xx = ss.twoSum(list, 9);
//	for (int i = 0; i < xx.size(); i++) {
//		cout << xx[i] << endl;
//		if (i % 2 == 1) {
//			cout << "--------------------------------" << endl;
//		}
//	}
//	cin.get();
//	return 0;
//}


#include<iostream>
#include<unordered_map>
using namespace std;
class Solution
{
public:
	vector<int> twoSum(vector<int> nums, int target) {
		unordered_map<int, int> m;
		vector<int> res = {};
		for (int i = 0; i < nums.size(); i++)
		{
			if (m.count(target-nums[i])) {
				res.push_back(i);
				res.push_back(m[nums[i]]);
			}
			m[nums[i]] = i;
		}
		return res;
	}
};

int main() {
	vector<int> list = { 1,8,2,7,11,8,15 };
	Solution ss;
	vector<int> xx = ss.twoSum(list, 9);
	for (int i = 0; i < xx.size(); i++) {
		cout << xx[i] << endl;
		if (i % 2 == 1) {
			cout << "--------------------------------" << endl;
		}
	}
	cin.get();
	return 0;
}