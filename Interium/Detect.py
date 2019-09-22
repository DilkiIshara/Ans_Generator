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

result = "" 
linesP = cv.HoughLinesP(None, 1, np.pi / 180, 25, None, 10, 10)  
numberOf_Horizontal = numberOf_Vertical = numberOf_Graph = rows = reduce = 0
maxlength_X = maxlength_Y = maxlength_Graph = 0
X_axis_cordinate = Y_axis_cordinate = graph_cordinate = -1
arr = None             # 0-x1 1-Y1 2-x2 3-y2
X_arr = Y_arr = None   # 0-a  1-length 2-arrIndex
graphs_arr = None      # 0-m  1-C 2-length 3-arrIndex 
cdstP = allLines = None
noOfLines = 0
origin_X = origin_Y = 0
N = 4 # arr (x,y) (x,y) 

def getEqationByUsingCoordinate():
    print("result       :  " + result) 
    number2 = re.findall('\(([^)]+)', result)
    length = len(number2)  
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

        #print("Cordinate 1   :    " + str(li[0]) +" , " + str(li[1]))
        #print("Cordinate 2   :     " + str(li2[0]) +" , " + str(li2[1]))

        x =  li2[0] - li[0]
        y =  li2[1] - li[1]

        if x!=0 and y!=0:
            m = y/x
            c = li[1] - (m * li[0])
            #print ("Equation is  :    y = " + str(m)+"x  + " + str(c))  
    else:
        print("coodinates does not read properly")

def displayAlllines() :
    for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(allLines, (l[0], l[1]), (l[2], l[3]), (5,0,255), 2, cv.LINE_AA)

def storeLineCoordinate() :
    global reduce, arr
    arr = [[0] * N for i in range(noOfLines)] 
    for i in range(0, len(linesP)): 
        l = linesP[i][0] 
        #Store Values in a 2D array 
        if i == 0 : 
            arr[0][0] = l[0]
            arr[0][1] = l[1]
            arr[0][2] = l[2]
            arr[0][3] = l[3]  
        else : 
            value1 = l[0]
            value2 = l[1]
            value3 = l[2]
            value4 = l[3]

            duplicate = 0 
            y = 0 
            x = i - reduce

            for j in range(0,x): 
                if arr[j][0]-3 <= value1 and value1 <= arr[j][0]+3 and arr[j][1]-3 <= value2 and value2 <= arr[j][1]+3 and arr[j][2]-3 <= value3 and value3 <= arr[j][2]+3 and arr[j][3]-3 <= value4 and value4 <= arr[j][3]+3 : 
                    arr[j][0] = int((value1+arr[j][0])/2)
                    arr[j][1] = int((value2+arr[j][1])/2)
                    arr[j][2] = int((value3+arr[j][2])/2)
                    arr[j][3] = int((value4+arr[j][3])/2)
                    reduce = reduce+1
                    duplicate = 1  
                if duplicate == 0: 
                    arr[i-reduce][0] = value1
                    arr[i-reduce][1] = value2
                    arr[i-reduce][2] = value3
                    arr[i-reduce][3] = value4

def separateX_Y_Graph():
    global numberOf_Horizontal, numberOf_Vertical, numberOf_Graph, X_arr, Y_arr, graphs_arr
    X_arr = [[0] * 3 for i in range(noOfLines)]
    Y_arr = [[0] * 3 for i in range(noOfLines)]
    graphs_arr = [[0] * 4 for i in range(noOfLines)] 
    for k in range(0, len(linesP)):  
        if not(arr[k][0] == 0 and arr[k][1] == 0 and arr[k][2] == 0 and arr[k][3] == 0) :
            x1 = arr[k][0]
            y1 = arr[k][1]
            x2 = arr[k][2]
            y2 = arr[k][3]

            #print ("("+str(x1)+","+str(y1)+")       ("+str(x2)+","+str(y2)+")")
            y_difference =  y2 - y1
            if y_difference < 0 :
                y_difference = -1 * y_difference
            #print("y difference       " + str(y_difference))

            x_difference = x2 - x1
            if x_difference < 0 :
                x_difference = -1 * x_difference
            #print("X difference" + str(x_difference))

            slide_1 = pow(y_difference, 2) 
            slide_2 = pow(x_difference, 2)
            total = slide_1 + slide_2
            lineLength = pow(total, 0.5)

            # x axises
            if y_difference == 0:     
                X_arr[k][0] = y1
                X_arr[k][1] = lineLength
                X_arr[k][2] = k
                numberOf_Horizontal = numberOf_Horizontal + 1 
            # y axises 
            elif x_difference == 0:    
                Y_arr[k][0] = x1
                Y_arr[k][1] = lineLength
                Y_arr[k][2] = k
                numberOf_Vertical = numberOf_Vertical + 1 
            # graph
            else :
                m = y_difference/x_difference
                c = y1 - (x1*m) 
                graphs_arr[k][0] = m
                graphs_arr[k][1] = c
                graphs_arr[k][2] = lineLength
                graphs_arr[k][3] = k
                numberOf_Graph = numberOf_Graph + 1

def draw_X_Axis():
    global maxlength_X
    global X_axis_cordinate
    global origin_Y, allLines
    for h in range(0, len(linesP)):
        l = X_arr[h][1]
        # print("Max axix Length  " + str(l))
        if l > maxlength_X : 
            X_axis_cordinate = h
            maxlength_X = l  
    cv.line(cdstP, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
    print ("X  axis -------------->("+str(arr[X_axis_cordinate][0])+","+str(arr[X_axis_cordinate][1])+")       ("+str(arr[X_axis_cordinate][2])+","+str(arr[X_axis_cordinate][3])+")")

def draw_Y_Axis():
    global maxlength_Y
    global origin_X
    global Y_axis_cordinate
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l > maxlength_Y : 
            Y_axis_cordinate = h
            maxlength_Y = Y_arr[h][1]   
    cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
    print ("Y  axis ------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")

def draw_Graph():
    global maxlength_Graph
    global graph_cordinate
    for h in range(0, len(linesP)): 
        l = graphs_arr[h][2]
        print("Max Graph Length  " + str(l))
        if l > maxlength_Graph : 
            graph_cordinate = h
            maxlength_Graph = l 
    # Draw Graph
    cv.line(cdstP, (arr[graph_cordinate][0], arr[graph_cordinate][1]), (arr[graph_cordinate][2], arr[graph_cordinate][3]), (0,252,0), 2, cv.LINE_AA)

def origin():
    global origin_X, origin_Y
    # generate y axis cordinate
    origin_X = Y_arr[Y_axis_cordinate][0]
    # generate x axis cordinate
    origin_Y = X_arr[X_axis_cordinate][0]
    
    print(" Origin ---------->("+str(origin_X) +","+ str(origin_Y) +")")
    for i in range(origin_X - 5 , origin_X + 5):
        for j in range(origin_Y - 5, origin_Y +5):
            allLines[j,i] = (255, 255, 255)
            cdstP[j,i] = (255, 255, 255)

def main(argv):
    
    global cdstP, allLines, linesP, arr, X_arr, Y_arr, graphs_arr, noOfLines, origin_X, origin_Y

    # Loads an image
    default_file = 'g1.jpg' 
    filename = argv[0] if len(argv) > 0 else default_file

    # Convert to gray Scale
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    # Check if image is loaded fine or not
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1 
    
    # resize image
    scale_percent = 220 # percent of original size
    # width = int(src.shape[1] * scale_percent / 100)
    # height = int(src.shape[0] * scale_percent / 100)
    width = int(500)
    height = int(500)
    dim = (width, height)
    resized = cv.resize(src, dim, interpolation = cv.INTER_AREA)

    # Edge detection
    #dst = cv.Canny(src, 20, 200, None, 3) 
    dst = cv.Canny(resized, 20, 200, None, 3) 

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    allLines = np.copy(cdst)  
    
    # Get Text
    global result
    result = pytesseract.image_to_string(Image.open(default_file))

    if result: 
        # Generate Eqation Using Given Coodinates
        getEqationByUsingCoordinate() 
    else:
        print("Text cannot Read")
     
    # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 10, 10) 
    noOfLines = len(linesP) 
    
    if linesP is not None: # Check there are lines

        # Draw the lines
        displayAlllines()

        # Store Lines Coordinate
        storeLineCoordinate()
            
        # Separate X axis Y axis and Graphs
        separateX_Y_Graph()

        # x axis
        draw_X_Axis()
        
        # y axis
        draw_Y_Axis()

        # Graph
        draw_Graph() 

        # identify origin
        origin()

        # identify X axis intersection point
        m = graphs_arr[graph_cordinate][0] 
        c = graphs_arr[graph_cordinate][1]

        intersection_Xaxis_Y = origin_Y
        intersection_Xaxis_X = int((intersection_Xaxis_Y - c)/m)
        
        print(" X axis intersection ---------->("+str(intersection_Xaxis_X) +","+ str(intersection_Xaxis_Y) +")")
        
        for i in range(intersection_Xaxis_X - 10 , intersection_Xaxis_X + 10):
            for j in range(intersection_Xaxis_Y - 10 , intersection_Xaxis_Y + 10):
                allLines[j,i] = (255, 255, 255)

    print(arr)      

    cv.imshow("Resized image", resized) 
    cv.imshow("Source", src) 
    cv.imshow("Probabilistic Line Transform", cdstP) 
    cv.imshow("Detected All Lines" , allLines )
    cv.waitKey()
    return 0  

if __name__ == "__main__":
    main(sys.argv[1:]) 