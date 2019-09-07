"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image 
import re

def main(argv):

    ## [load]
    default_file = 'line.jpg' 
    filename = argv[0] if len(argv) > 0 else default_file

    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1 
    
    # resize image
    scale_percent = 220 # percent of original size
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(src, dim, interpolation = cv.INTER_AREA)

    # Edge detection
    dst = cv.Canny(resized, 20, 200, None, 3)  

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)   
    
    # Get Text
    result = pytesseract.image_to_string(Image.open(default_file))

    if result: 
        print("result  " + result) 
        number2 = re.findall('\(([^)]+)', result)
        length = len(number2) 
        # print(number2[0])
        if length > 1:
            if ' ' in number2[0]:
                cordinate1 = number2[0].replace(" ", "")
            else: 
                cordinate1 = number2[0]
            if ' ' in number2[1]:
                cordinate2 = number2[1].replace(" ", "")
            else: 
                cordinate2 = number2[1] 

        print(cordinate1)
        print(cordinate2)
        list1 = cordinate1.split (",") 
        list2 = cordinate2.split (",") 

        # convert each element as integers
        li = []
        for i in list1:
	        li.append(int(i))

        li2 = []
        for i in list2:
	        li2.append(int(i))

        print("Cordinate 1   :    " + str(li[0]) +" , " + str(li[1]))
        print("Cordinate 2   :     " + str(li2[0]) +" , " + str(li2[1]))

        x =  li2[0] - li[0]
        y =  li2[1] - li[1]

        if x!=0 and y!=0:
            m = y/x
            c = li[1] - (m * li[0])
            print ("Equation is  :    y = " + str(m)+"x  + " + str(c))
        
        else:
            print("coodinates does not read properly")
    else:
        print("Text cannot Read")
     
    # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 10, 10) 

    # Draw the lines
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (5,0,255), 2, cv.LINE_AA)
 
    cv.imshow("Resized image", resized)

    # Show results
    cv.imshow("Source", src) 
    cv.imshow("Probabilistic Line Transform", cdstP)
    cv.waitKey()
    return 0  

if __name__ == "__main__":
    main(sys.argv[1:])