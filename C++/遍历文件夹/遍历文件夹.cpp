// ConsoleApplication11.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <io.h>  // 必须使用这个头文件
#include <string>
#include<iostream>


void listdir(std::string inpath) {   //  输入的path   std::string inpath = "C://*";
	long handle;  // 一个句柄
	struct _finddata_t fileinfo;  //  声明一个结构体，用于存放文件信息
	handle = _findfirst(inpath.c_str(), &fileinfo);  //  将结构体绑架在句柄上
	//  如果句柄为-1说明路径错误
	if (handle == -1) {  
		std::cout << "The path is error！";
	}
	do {
		std::cout << fileinfo.name << std::endl;

	} while (!_findnext(handle, &fileinfo));
	_findclose(handle);
}




int main()
{
	std::string inpath = "C://*";
	listdir(inpath);
	system("pause");
	return 0;
}
