#include "stdafx.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<iostream>

// 测试字符串
#define STRING_X "SUN333DA122Y"
#define STRING_Y "SATURasdasdasdDAY"

#define SENTINEL (-1)
#define EDIT_COST (1)

inline
int min(int a, int b) {
	return a < b ? a : b;
}
// Returns Minimum among a, b, c
int Minimum(int a, int b, int c)
{
	return min(min(a, b), c);
}
// Strings of size m and n are passed.
// Construct the Table for X[0...m, m+1], Y[0...n, n+1]
int EditDistanceDP(char X[], char Y[])
{
	// Cost of alignment
	int cost = 0;
	int leftCell, topCell, cornerCell;
	int m = strlen(X) + 1;
	int n = strlen(Y) + 1;
	// T[m][n]
	int *T = (int *)malloc(m * n * sizeof(int));
	// Initialize table
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++)
			*(T + i * n + j) = SENTINEL;
	// Set up base cases
	// T[i][0] = i
	for (int i = 0; i < m; i++)
		*(T + i * n) = i;
	// T[0][j] = j
	for (int j = 0; j < n; j++)
		*(T + j) = j;
	// Build the T in top-down fashion
	for (int i = 1; i < m; i++)
	{
		for (int j = 1; j < n; j++)
		{
			// T[i][j-1]
			leftCell = *(T + i*n + j - 1);
			leftCell += EDIT_COST; // deletion
			// T[i-1][j]
			topCell = *(T + (i - 1)*n + j);
			topCell += EDIT_COST; // insertion
			// Top-left (corner) cell
			// T[i-1][j-1]
			cornerCell = *(T + (i - 1)*n + (j - 1));
			// edit[(i-1), (j-1)] = 0 if X[i] == Y[j], 1 otherwise
			cornerCell += (X[i - 1] != Y[j - 1]); // may be replace
			// Minimum cost of current cell
			// Fill in the next cell T[i][j]
			*(T + (i)*n + (j)) = Minimum(leftCell, topCell, cornerCell);
		}
	}
	// 结果存储在 T[m][n]
	cost = *(T + m*n - 1);
	free(T);
	return cost;
}

// 递归方法实现
int EditDistanceRecursion(char *X, char *Y, int m, int n)
{
	// 基本情况
	if (m == 0 && n == 0)
		return 0;
	if (m == 0)
		return n;
	if (n == 0)
		return m;
	// Recurse
	int left = EditDistanceRecursion(X, Y, m - 1, n) + 1;
	int right = EditDistanceRecursion(X, Y, m, n - 1) + 1;
	int corner = EditDistanceRecursion(X, Y, m - 1, n - 1) + (X[m - 1] != Y[n - 1]);
	return Minimum(left, right, corner);
}

int main()
{
	char X[100]; // vertical
	char Y[100]; // horizontal
	std::cout << "请输入第一个字符串：";
	std::cin >> X;
	std::cout << "请输入第二个字符串：";
	std::cin >> Y;
	printf("Minimum edits required to convert %s into %s is %d\n",
		X, Y, EditDistanceDP(X, Y));
	printf("Minimum edits required to convert %s into %s is %d by recursion\n",
		X, Y, EditDistanceRecursion(X, Y, strlen(X), strlen(Y)));
	system("pause");
	return 0;
}