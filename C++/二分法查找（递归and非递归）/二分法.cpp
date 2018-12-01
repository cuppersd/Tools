//  非递归实现二分查找
#include "stdafx.h"
#include<iostream>
int BinarySearch(int *arr, int length, int target) {
	if (arr == NULL || length <= 0) {
		return -1;
	}
	int low, high, mid;
	low = 0;
	high = length - 1;
	while (low <= high) {
		mid = (high + low) / 2;
		if (arr[mid] == target) {
			return mid;
		}
		else if (arr[mid] > target) {
			high = mid - 1;
		}
		else {
			low = mid + 1;
		}
	}
	return -1;
}
//  递归实现二分查找
int BinarySearchRecursive(int* array, int low, int high, int target) {
	if (low > high) {
		return -1;
	}
	int mid = (low + high) / 2;
	if (array[mid] == target) {
		return mid;
	}
	else if (array[mid] > target) {
		BinarySearchRecursive(array, low, mid - 1, target);
	}
	else {
		BinarySearchRecursive(array, low+1, high, target);
	}
}

int main()
{
	int s[] = { 1,3,4,65,77,898,9999 };
	int length = sizeof(s) / sizeof(s[0]);
	std::cout << BinarySearch(s, length, 77) << std::endl;
	std::cout << BinarySearchRecursive(s, 0,length-1, 4);
	while (1);
    return 0;
}

