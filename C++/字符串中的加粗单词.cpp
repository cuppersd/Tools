#include<iostream>
#include<string>
#include<vector>
using namespace std;
class Solution
{
public:
	string boldWords(vector<string> word,string S) {
		int n = S.size();
		vector<bool> bool_s(n, false);
		string res = "";
		for (string substr : word) {
			int length = substr.size();
			for (int i = 0; i < n-length+1; i++) {
				//cout << substr << ":" << S.substr(i, length) << endl;
				if (substr == S.substr(i, length)) {
					for (int j = i; j < i + length; j++) {
						bool_s[j] = true;
					}
				}
			}
		}

		for (int i = 0; i < n; i++) {
			if (bool_s[i]) {
				if (i == 0 || bool_s[i - 1] == false) {
					res = res + "<b>";
				}
				res=res+S[i];
				if (i == (n - 1) || bool_s[i + 1] == false) {
					res = res + "<\\b>";
				}
			}
			else
			{
				res = res + S[i];
			}
		}
		return res;

	}

};

int main() {
	vector<string> word = { "ab","bc" };
	string S = "asab";
	Solution ss;
	cout << ss.boldWords(word, S) << endl;;
	cin.get();
	return 0;
}