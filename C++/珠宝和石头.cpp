#include<iostream>
#include<string>
#include<unordered_set>
#include<vector>
using namespace std;
class Solution
{
public:
	int numJewellsInStone(string J,string S) {
		int res = 0;
		unordered_set<char> ss;
		for (char c : J) {
			ss.insert(c);
		}
		for (char dd : S) {
			if (ss.count(dd)) {
				res = res + 1;
			}
		}
		return res;
	}
};


int main() {
	string J = "aac";
	string S = "wdecasca";
	Solution su;
	cout << su.numJewellsInStone(J, S) << endl;
	cin.get();
	return 0;
}