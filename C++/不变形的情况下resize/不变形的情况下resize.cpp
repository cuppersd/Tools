#include<opencv2/opencv.hpp>
#include<iostream>
#include<vector>
using namespace cv;
void letterbox_image(Mat& image, Mat& dst,Size size);
int main() {
	Mat src = imread("C:/Users/Study/Desktop/12.jpg");
	Mat dst;
	letterbox_image(src, dst, Size(416, 416));
	imshow("as", dst);
	waitKey(0);
	return 0;
}

void letterbox_image(Mat& image, Mat& dst, Size size) {
	int row = image.rows, col = image.cols;  // 获取图像矩阵的高度和宽度row高度，col宽度
	float scale = min((float)size.width/row,(float)size.height/col);
	int nw = (int)(row*scale), nh = (int)(col*scale);  // resize后的图片尺寸
	resize(image, dst, Size(nh, nw), 0, 0, INTER_CUBIC);
	Mat image1(size.width, size.height, CV_8UC3, Scalar(128, 128, 128));
	dst.copyTo(image1(Range((size.width-nw)/2, nw+ (size.width - nw) / 2), Range((size.height-nh)/2, nh+ (size.height - nh) / 2)));
	dst = image1;
}