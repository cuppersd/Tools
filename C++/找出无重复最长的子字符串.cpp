#include<iostream>
#include<vector>
#include<string>
#include<unordered_map>
#include<cmath>
#include<algorithm>
using namespace std;
//class Solution
//{
//public:
//	int lengthOfLongestSubstring(string s) {
//		unordered_map<>
//	}
//
//};

//class Solution {
//public:
//	int lengthOfLongestSubstring(string s) {
//		int res = 0, left = -1, n = s.size();
//		unordered_map<int, int> m;
//		for (int i = 0; i < n; ++i) {
//			if (m.count(s[i]) && m[s[i]] > left) {
//				left = m[s[i]];
//			}
//			m[s[i]] = i;
//			res = max(res, i - left);
//		}
//		return res;
//	}
//};
//
//int main() {
//	//string s = "pwwkew";
//	//Solution ss;
//
//	//cout << ss.lengthOfLongestSubstring(s) << endl;
//	unordered_map<int, int> dd;
//	dd['a'] = 1;
//	dd['f'] = 1;
//	dd['e'] = 2;
//	cout << dd.count(1) << endl;
//	cin.get();
//	return 0;
//}


#include<iostream>
#include<unordered_map>
#include<algorithm>
#include<string>
using namespace std;
class Solution
{
public:
	int lengthOfLongestSubstring(string s) {
		int res = 0, left = -1;
		unordered_map<int, int> m;
		for (int i = 0; i < s.size(); i++) {
			if (m.count(s[i]) && m[s[i]] > left) {
				left = m[s[i]];
			}
			m[s[i]] = i;
			res = max(res, i - left);
			cout << s.substr(res,(i - left)) << endl;;	
		}
		
		return res;
	}

};


int main() {
	string s = "pwwkew";
	Solution dd;
	cout << dd.lengthOfLongestSubstring(s) << endl;
	cin.get();
	return 0;
}
