// ConsoleApplication16.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include<string>
#include<vector>
#include<fstream>
#include <Windows.h>
using namespace std;
vector<string> SplitString(const string &s, const string &seperator) {
	vector<string> result;  // 结果保存
	typedef string::size_type string_size;  //简化定义
	string_size i = 0;
	while (i != s.size()) {
		//找到字符串中首个不等于分隔符的字母；
		int flag = 0;
		while (i != s.size() && flag == 0) {
			flag = 1;
			for (string_size x = 0; x < seperator.size(); ++x)
				if (s[i] == seperator[x]) {
					++i;
					flag = 0;
					break;
				}
		}
		//找到又一个分隔符，将两个分隔符之间的字符串取出；
		flag = 0;
		string_size j = i;
		while (j != s.size() && flag == 0) {
			for (string_size x = 0; x < seperator.size(); ++x)
				if (s[j] == seperator[x]) {
					flag = 1;
					break;
				}
			if (flag == 0)
				++j;
		}
		if (i != j) {
			result.push_back(s.substr(i, j - i));
			i = j;
		}
	}
	return result;
}

vector<string> SplitStringOne(const string& s, const string& c)
{
	vector<string> v;
	string::size_type pos1, pos2;
	pos2 = s.find(c);
	pos1 = 0;
	while (string::npos != pos2)
	{
		v.push_back(s.substr(pos1, pos2 - pos1));

		pos1 = pos2 + c.size();
		pos2 = s.find(c, pos1);
	}
	if (pos1 != s.length())
		v.push_back(s.substr(pos1));
	return v;
}

int main()
{
	ifstream infile; // 读出到屏幕的文件
	ofstream outfile;  // 写入到文件
	infile.open("1菜单_1菜单_1536044904.045982.txt",ios::binary);  // 打开文件
	outfile.open("22.txt",ios::binary); // 打开文件
	string line;  // 读取一行
	if (infile) // 判断 文件是否成功打开
	{
		while (getline(infile, line)){
			cout << line << endl;
			string newline("");
			vector<string> v = SplitStringOne(line, ",");
			for (vector<string>::size_type i = 0; i!= v.size()-1; ++i)
			{
				newline += v[i]+"\t";
			}
			outfile << newline;
			
		}

	}
	else {
		cout << "Sorry, no files!" << endl;
	
	}

	infile.close();
	outfile.close();
	string s("123,12333333,444");
	//getline(cin, s);
	vector<string> v = SplitStringOne(s, ","); //可按多个字符来分隔;
	while (1);
	return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
