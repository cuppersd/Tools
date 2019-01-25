#include<iostream>
#include<queue>
#include<vector>
#include<string>
using namespace std;
class Solution
{
public:
	vector<string> letterCasePermutation(string s) {
		vector<string> res{ "" };
		for (char c : s) {
			int length = res.size();
			if (c >= '0' && c <= '9') {
				for (string& str : res) {
					str.push_back(c);
				}
			}
			else {
				for (int i = 0; i < length; i++) {
					res.push_back(res[i]);
					res[i].push_back(tolower(c));
					res[i + length].push_back(toupper(c));
				}
			}
		}
		for (string ss : res) {
			cout << ss << endl;
		}
		return res;
	}
};


int main() {
	string sss = "asd2f";
	Solution su;
	vector<string> ddd=su.letterCasePermutation(sss);
	cin.get();
	return 0;
}