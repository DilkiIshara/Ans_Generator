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

def hello():
    print("Hello")

def main(argv):

    ## [load]
    default_file = 'uu.png' 
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
    # dst = cv.Canny(resized, 20, 200, None, 3) 
    dst = cv.Canny(src, 20, 200, None, 3) 

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
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 10, 10) 

    rows, cols = (len(linesP),4)
    # # arr = [[0]*cols]*rows
    # arr = [[]*cols]*rows
    
    noOfLines = 0
    p = 0
    q = 0
    r = 0
    #N = 4
    N = 5
    M = len(linesP)
    
    maxlength_X = 0
    X_axis_cordinate = -1

    maxlength_Y = 0
    Y_axis_cordinate = -1
    arr = [[0] * N for i in range(M)]
    Xarr = [[0] * 3 for i in range(M)]   #0-Y 1-length 2-arrIndex
    Yarr = [[0] * 3 for i in range(M)]   #0-X 1-length 2-arrIndex
    graphsarr = [[0] * 4 for i in range(M)]  # 0-m  1-C 2-length 3-arrIndex

    print(arr)

    reduce = 0

    # Draw the lines
    if linesP is not None:
        for i in range(0, len(linesP)): 
            l = linesP[i][0]
            #cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (5,0,255), 2, cv.LINE_AA)
            # print("("+ str(l[0]) + " ," + str(l[1]) +") , " + "("+ str(l[2]) + " ," + str(l[3]) +") , " )  ---------------/

            #Store Values in a 2D array
            if i == 0 : 
                arr[0][0] = l[0]
                arr[0][1] = l[1]
                arr[0][2] = l[2]
                arr[0][3] = l[3]  
            else :
                # print(i) ---------------------------/ # arr[i][0] = l[0] # arr[i][1] = l[1] # arr[i][2] = l[2] # arr[i][3] = l[3]
                value1 = l[0]
                value2 = l[1]
                value3 = l[2]
                value4 = l[3]

                duplicate = 0 
                y = 0 
                x = i - reduce
                for j in range(0,x):
                    #print(j)
                    # print(arr[j][0])
                    # print(arr[j][1])
                    # print(arr[j][2])
                    # print(arr[j][3])
                    if arr[j][0]-3 <= value1 and value1 <= arr[j][0]+3 and arr[j][1]-3 <= value2 and value2 <= arr[j][1]+3 and arr[j][2]-3 <= value3 and value3 <= arr[j][2]+3 and arr[j][3]-3 <= value4 and value4 <= arr[j][3]+3 :
                    # if arr[j][0]-3 <= value1 and value1 <= arr[j][0]+3:  
                        arr[j][0] = int((value1+arr[j][0])/2)
                        arr[j][1] = int((value2+arr[j][1])/2)
                        arr[j][2] = int((value3+arr[j][2])/2)
                        arr[j][3] = int((value4+arr[j][3])/2)
                        reduce = reduce+1
                        duplicate = 1 
                        # print(arr) ------------------------------/
                if duplicate == 0: 
                    arr[i-reduce][0] = value1
                    arr[i-reduce][1] = value2
                    arr[i-reduce][2] = value3
                    arr[i-reduce][3] = value4
            
        # Get the Size of the Array element
        for k in range(0, len(linesP)): 
            # print(" Inside arr ") -------------------/
            if not(arr[k][0] == 0 and arr[k][1] == 0 and arr[k][2] == 0 and arr[k][3] == 0) :
                x1 = arr[k][0]
                y1 = arr[k][1]
                x2 = arr[k][2]
                y2 = arr[k][3]

                print ("("+str(x1)+","+str(y1)+")       ("+str(x2)+","+str(y2)+")")
                y_difference =  y2 - y1
                if y_difference < 0 :
                    y_difference = -1 * y_difference
                print("y difference       " + str(y_difference))

                x_difference = x2 - x1
                if x_difference < 0 :
                    x_difference = -1 * x_difference
                print("X difference" + str(x_difference))

                slide_1 = pow(y_difference, 2) 
                slide_2 = pow(x_difference, 2)
                total = slide_1 + slide_2
                lineLength = pow(total, 0.5)

                print("gap Betwwen two points" + str(lineLength))

                if y_difference == 0:    # x axises
                    # Xarr[p][0] = y1
                    # Xarr[p][1] = lineLength
                    # Xarr[p][2] = k
                    Xarr[k][0] = y1
                    Xarr[k][1] = lineLength
                    Xarr[k][2] = k
                    p = p + 1
                    print(" P :" + str(p))

                if x_difference == 0:    # y axises
                    # Yarr[q][0] = y1
                    # Yarr[q][1] = lineLength
                    # Yarr[q][2] = k
                    Yarr[k][0] = y1
                    Yarr[k][1] = lineLength
                    Yarr[k][2] = k
                    q = q + 1
                    print(" q :" + str(q))

                else :
                    m = y_difference/x_difference
                    c = y1 - (x1*m)
                    graphsarr[r][0] = m
                    graphsarr[r][1] = c
                    graphsarr[r][2] = lineLength
                    graphsarr[r][3] = k
                    r = r + 1
                    print(" r :" + str(r))
                    print("a")
                print("b")
            print("c")

        # x axis
        for h in range(0, len(linesP)):
            l = Xarr[h][1]
            print("Length "+ str(l))
            if l > maxlength_X : 
                X_axis_cordinate = h
                maxlength_X = Xarr[h][1]
                print("YES")
        
        # y axis
        for h in range(0, len(linesP)):
            l = Yarr[h][1]
            print("Length "+ str(l))
            if l > maxlength_Y : 
                Y_axis_cordinate = h
                maxlength_Y = Yarr[h][1]
                print("YES")

        
                
        #cv.line(cdstP, (74, 204) , (74, 0) , (255,255,0), 2, cv.LINE_AA)

        # #Check y axis
        # for k in range(0, len(linesP)) : 
        #     l = Yarr[k][1]
        #     if l > maxlength_Y :
        #         Y_axis_cordinate = k
        #         maxlength_Y = Xarr[k][1]
                

        #Draw x Axies
        cv.line(cdstP, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (127,255,0), 2, cv.LINE_AA)
        #cv.line(cdstP, (74, 204) , (74, 0) , (255,255,0), 2, cv.LINE_AA)

        #Draw y Axies
        cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)

                
    print("ttttttttttttttttttttttttttttt")
    print(arr)      


    cv.imshow("Resized image", resized)

    # Show results
    cv.imshow("Source", src) 
    cv.imshow("Probabilistic Line Transform", cdstP)
    cv.waitKey()
    return 0  

if __name__ == "__main__":
    main(sys.argv[1:])