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
    default_file = 'Capture3.png'
    #default_file = '29.png'
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
    print("result  " + result)
    # number = re.search('\(([^)]+)', result) 
    number2 = re.findall('\(([^)]+)', result)
    # print(number) 

    print(number2[0])
    cordinate1 = number2[0].replace(" ", "")
    cordinate2 = number2[1].replace(" ", "")
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
    # print(result)
    # total = str(int(currentline[0]) + int(currentline[1]) + int(currentline [2])) + "\n"
    # print(number) 
    # print(number2)
    # print(total) 

    # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 100, None, 10, 10) 

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



# import cv2
# import sys
# import math 
# import numpy as np

# import numpy as np

# img = cv2.imread('line.jpg')
# dst = cv2.imread('line.jpg')

# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray,50,100,apertureSize = 3)
# #edges = cv2.Canny(img, 75, 150)
# minLineLength = 5
# maxLineGap = 5
# lines = cv2.HoughLinesP(edges,1,np.pi/180,10,10,50)
# #lines = cv2.HoughLinesP(edges, 5, np.pi/180, 11, maxLineGap = 15)
# for x1,y1,x2,y2 in lines[0]:
#     cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


# linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, 0, 50, 10) 
#     if linesP is not None:
#         for i in range(0, len(linesP)):
#             l = linesP[i][0]
#             cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)


# cv2.imshow('image2',dst)          
# cv2.imshow('image',img)
# cv2.imwrite('3.jpg',img)
# cv2.waitKey(0)
