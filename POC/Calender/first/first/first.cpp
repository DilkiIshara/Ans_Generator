// first.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <stdio.h>
#include <iostream>
#include <opencv\cv.h>
#include <opencv\highgui.h>  
#include <opencv\cv.h>
#include "opencv2/imgproc.hpp"
#include <opencv\cxcore.h>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp" 
#include "opencv2/highgui.hpp" 
#include "opencv2/imgcodecs.hpp" 
   
using namespace cv;
using namespace std;

int main(int argc, char** argv)
{
	// Declare the output variables
	Mat dst, cdst, cdstP , graph;
	int y_cordinates[100];
	int x_cordinates[100];
	const char* default_file = "../data/sudoku.png";
	const char* filename = argc >= 2 ? argv[1] : default_file;

	// Loads an image
	Mat src = imread(filename, IMREAD_GRAYSCALE);

	// Check if image is loaded fine
	if (src.empty()) {
		printf(" Error opening image\n");
		printf(" Program Arguments: [image_name -- default %s] \n", default_file);
		return -1;
	}

	// Edge detection
	Canny(src, dst, 50, 200, 3);

	// Copy edges to the images that will display the results in BGR
	cvtColor(dst, cdst, COLOR_GRAY2BGR);
	cdstP = cdst.clone();
	graph = cdst.clone();

	// Standard Hough Line Transform
	vector<Vec2f> lines; // will hold the results of the detection
	HoughLines(dst, lines, 1, CV_PI / 180, 150, 0, 0); // runs the actual detection

	// Draw the lines
	for (size_t i = 0; i < lines.size(); i++)
	{
		float rho = lines[i][0], theta = lines[i][1];
		Point pt1, pt2;
		double a = cos(theta), b = sin(theta);
		double x0 = a * rho, y0 = b * rho;
		pt1.x = cvRound(x0 + 1000 * (-b));
		pt1.y = cvRound(y0 + 1000 * (a));
		pt2.x = cvRound(x0 - 1000 * (-b));
		pt2.y = cvRound(y0 - 1000 * (a));
		line(cdst, pt1, pt2, Scalar(0, 0, 255), 3, LINE_AA);
	}


	// Probabilistic Line Transform
	vector<Vec4i> linesP; // will hold the results of the detection
	HoughLinesP(dst, linesP, 1, CV_PI / 180, 50, 50, 10); // runs the actual detection

	int y_cordinate = 0;
	int x_cordinate = 0;
	int start_x = 0;
	int start_y = 0;
	int end_x = 0;
	int end_y = 0;

	// Draw the lines
	for (size_t i = 0; i < linesP.size(); i++)
	{
		Vec4i l = linesP[i];
		line(cdstP, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 3, LINE_AA);
		int x1 = l[0];
		int y1 = l[1];
		int x2 = l[2];
		int y2 = l[3]; 

		cout << i << " is a horizontal line with" << x1 << ", " << y1 << " , " << x2 << " , " << y2 << endl;

		if ((y2 - y1) == 0) {
			y_cordinates[y_cordinate] = y1;
			y_cordinate = y_cordinate + 1;

			x_cordinates[x_cordinate] = x1;
			x_cordinate = x_cordinate + 1;
		}

		if ((x2-x1) != 0 && (y2 - y1) != 0)
		{   
			start_x = x1;
			start_y = y1;
			end_x = x2;
			end_y = y2;
			line(graph, Point(x1, y1), Point(x2, y2), Scalar(0, 0, 255), 3, LINE_AA);
		}
	}

	for (int i = 0; i < 100; i++) {
		cout << y_cordinates[i] << endl;
		int slpoe = (end_y - start_y) / (end_x - end_y);
		int slpoe2 = (end_y - y_cordinates[i]) / (end_x - x_cordinates[i]);
		if (slpoe = slpoe2) {
			cout << x_cordinates[i] << " " << y_cordinates[i] << endl;
			cout << start_x << " " << start_y << endl;
		}
	}

	// Show results
	imshow("Source", src);
	imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst);
	imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP);
	imshow("Detected Graph (in red) - Probabilistic Line Transform", graph);
	// Wait and Exit
	waitKey();
	return 0;
}