#include<iostream>
#include<vector>
using namespace std;
class Solution
{
public:
	int dominantIndex(vector<int> nums) {
		int max_one = INT_MIN, max_two = INT_MIN, index;
		for (int i = 0; i < nums.size();i++) {
			if (nums[i] > max_one) {
				max_two = max_one;
				max_one = nums[i];
				index = i;
			}else if (nums[i] > max_two) {
				max_two= nums[i];
			}
		}
		cout << max_one << ":" << max_two << endl;
		if (max_one - max_two >= max_two) {
			return index;
		}
		else {
			return -1;
		}
		
	}

};
int main() {
	vector<int> list = { 3,1,0,6 };
	Solution ss;
	cout << ss.dominantIndex(list) << endl;;
	
	cin.get();
	return 0;
}