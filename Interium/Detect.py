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
width = height = 0
origin_X = origin_Y = intersection_Xaxis_X = intersection_Xaxis_Y = intersection_Yaxis_X = intersection_Yaxis_Y = 0
real_intersection_Xaxis_X = real_intersection_Yaxis_Y = 0
pixcelForTicMark_Y = pixcelForTicMark_X = 0
N = 4 # arr (x,y) (x,y) 

def getEqationByUsingCoordinate():
    # print("result       :  " + result) 
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
            print ("Equation is  :    y = " + str(m)+"x  + " + str(c))  
    else:
        print("coodinates does not read properly")

def displayAlllines() :
    for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(allLines, (l[0], l[1]), (l[2], l[3]), (5,0,255), 2, cv.LINE_AA)

def storeLineCoordinate() :
    global reduce, arr
    arr = [[0] * N for i in range(noOfLines)] 

    index = 1
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
                if arr[j][0]-5 <= value1 and value1 <= arr[j][0]+5 and arr[j][1]-5 <= value2 and value2 <= arr[j][1]+5 and arr[j][2]-5 <= value3 and value3 <= arr[j][2]+5 and arr[j][3]-5 <= value4 and value4 <= arr[j][3]+5 : 
                    # arr[j][0] = int((value1+arr[j][0])/2)
                    # arr[j][1] = int((value2+arr[j][1])/2)
                    # arr[j][2] = int((value3+arr[j][2])/2)
                    # arr[j][3] = int((value4+arr[j][3])/2)
                    arr[j][0] = int(round((value1+arr[j][0])/2))
                    arr[j][1] = int(round((value2+arr[j][1])/2))
                    arr[j][2] = int(round((value3+arr[j][2])/2))
                    arr[j][3] = int(round((value4+arr[j][3])/2))
                    reduce = reduce+1
                    duplicate = 1
            

            if duplicate == 0: 
                    # arr[i-reduce][0] = value1
                    # arr[i-reduce][1] = value2
                    # arr[i-reduce][2] = value3
                    # arr[i-reduce][3] = value4
                arr[index][0] = value1
                arr[index][1] = value2
                arr[index][2] = value3
                arr[index][3] = value4
                index = index + 1
                    
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

            y_difference =  y2 - y1 
            x_difference = x2 - x1 

            slide_1 = pow(y_difference, 2) 
            slide_2 = pow(x_difference, 2)
            total = slide_1 + slide_2
            lineLength = pow(total, 0.5)

            # x axises
            if (((y_difference >= -5) and (y_difference <= 5))  and (x_difference != 0)) :     
                X_arr[k][0] = y1
                X_arr[k][1] = lineLength
                X_arr[k][2] = k
                numberOf_Horizontal = numberOf_Horizontal + 1 
            # y axises 
            elif (((x_difference >= -5) and (x_difference <= 5)) and (y_difference != 0)) :    
                Y_arr[k][0] = x1
                Y_arr[k][1] = lineLength
                Y_arr[k][2] = k
                numberOf_Vertical = numberOf_Vertical + 1 
            # graph
            else:
            # elif ((x_difference != 0) and (y_difference != 0)):
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
        if l > maxlength_X : 
            X_axis_cordinate = h
            maxlength_X = l  
    sameLine = 0
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l == maxlength_Y : 
            sameLine = sameLine + 1
    print(" Same Lines : " + str(sameLine))

    if (sameLine > 1):
        find_X_Axis()
        cv.line(cdstP, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
        print("---------------------------------------")
        print ("X  axis -------------->("+str(arr[X_axis_cordinate][0])+","+str(arr[X_axis_cordinate][1])+")       ("+str(arr[X_axis_cordinate][2])+","+str(arr[X_axis_cordinate][3])+")")
    else :
        cv.line(cdstP, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
        print ("X  axis -------------->("+str(arr[X_axis_cordinate][0])+","+str(arr[X_axis_cordinate][1])+")       ("+str(arr[X_axis_cordinate][2])+","+str(arr[X_axis_cordinate][3])+")")

def find_X_Axis():
    global maxlength_X
    global X_axis_cordinate
    global pixcelForTicMark_X 
 
    half_pixcelForTicMark_X = 10
    minLen_X_Axis = maxlength_X
    min_X_axis_cordinate = 0

    for h in range(0, len(linesP)):
        l = X_arr[h][1] 
        if ((l < minLen_X_Axis) and (l != 0)) : 
            min_X_axis_cordinate = h
            minLen_X_Axis = X_arr[h][1]  
    # x =  arr[min_X_axis_cordinate][0]  
    # cv.line(cdstP, (arr[min_X_axis_cordinate][0], arr[min_X_axis_cordinate][1]), (arr[min_X_axis_cordinate][2], arr[min_X_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA) 
    min_XAxis_Ycordinate = arr[min_X_axis_cordinate][1] 
    
    if (pixcelForTicMark_X == 0):
        identifyTicMarks_X_Axis()
    
    if(pixcelForTicMark_X != 0):
        half_pixcelForTicMark_X = pixcelForTicMark_X/2 

    for h in range(0, len(linesP)):
        X_axis_Y_cordinate = arr[h][1]
        length_Of_X_Axis = X_arr[h][1]    
        if ((X_axis_Y_cordinate <= (min_XAxis_Ycordinate+15)) and (X_axis_Y_cordinate >= (min_XAxis_Ycordinate-15))) :  
            if (length_Of_X_Axis == maxlength_X): 
                print("4444444444444444444444444444444444")
                X_axis_cordinate = h
    # cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
    # print ("Y  axis ------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")
    

def draw_Y_Axis():
    global maxlength_Y
    global origin_X
    global Y_axis_cordinate
    global pixcelForTicMark_Y
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l > maxlength_Y : 
            Y_axis_cordinate = h
            maxlength_Y = Y_arr[h][1]   
    sameLine = 0
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l == maxlength_Y : 
            sameLine = sameLine + 1
    # print(" Same Lines : " + str(sameLine))
    
    if (sameLine > 1):
        find_Y_Axis()
        cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
        print ("Y  axis ------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")
    else :
        cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
        print ("Y  axis ------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")

def find_Y_Axis():
    global maxlength_Y
    global Y_axis_cordinate
    global pixcelForTicMark_Y 
 
    half_pixcelForTicMark_Y = 10
    minLen_Y_Axis = maxlength_Y
    min_Y_axis_cordinate = 0

    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if ((l < minLen_Y_Axis) and (l != 0)) : 
            min_Y_axis_cordinate = h
            minLen_Y_Axis = Y_arr[h][1] 
            # print("start Find" + str(minLen_Y_Axis)) 
    x =  arr[min_Y_axis_cordinate][0] 
    # print("min_Y_axis_X_cordinate " + str(x))
    # cv.line(cdstP, (arr[min_Y_axis_cordinate][0], arr[min_Y_axis_cordinate][1]), (arr[min_Y_axis_cordinate][2], arr[min_Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA) 
    min_YAxis_Xcordinate = arr[min_Y_axis_cordinate][0]
    # print("max Length Value " + str(maxlength_Y))
    
    # if (pixcelForTicMark_Y == 0):
    #     identifyTicMarks_Y_Axis()
    
    if(pixcelForTicMark_Y != 0):
        half_pixcelForTicMark_Y = pixcelForTicMark_Y/2 

    for h in range(0, len(linesP)):
        Y_axis_X_cordinate = arr[h][0]
        length_Of_Y_Axis = Y_arr[h][1]    
        if ((Y_axis_X_cordinate <= (min_YAxis_Xcordinate+15)) and (Y_axis_X_cordinate >= (min_YAxis_Xcordinate-15))) :  
            if (length_Of_Y_Axis == maxlength_Y): 
                Y_axis_cordinate = h
    # cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
    # print ("Y  axis ------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")
    
def draw_Graph():
    global maxlength_Graph
    global graph_cordinate
    for h in range(0, len(linesP)): 
        l = graphs_arr[h][2]
        # print("Max Graph Length  " + str(l))
        if l > maxlength_Graph : 
            graph_cordinate = h
            maxlength_Graph = l 
    # Draw Graph
    cv.line(cdstP, (arr[graph_cordinate][0], arr[graph_cordinate][1]), (arr[graph_cordinate][2], arr[graph_cordinate][3]), (0,252,0), 2, cv.LINE_AA)
    print ("Graph    ------------->("+str(arr[graph_cordinate][0])+","+str(arr[graph_cordinate][1])+")       ("+str(arr[graph_cordinate][2])+","+str(arr[graph_cordinate][3])+")")

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

def identifyIntersection():
    global intersection_Xaxis_Y, intersection_Xaxis_X, intersection_Yaxis_Y, intersection_Yaxis_X
    y1 = -(arr[graph_cordinate][1])
    y2 = -(arr[graph_cordinate][3])

    m = graphs_arr[graph_cordinate][0] 
    c = graphs_arr[graph_cordinate][1] 
    # print(" Y axis intersection ---------->("+str(m) +","+ str(c) +")")    
    intersection_Xaxis_Y = origin_Y
    intersection_Xaxis_X = int(round((intersection_Xaxis_Y - c)/m))
    intersection_Yaxis_X = origin_X  
    intersection_Yaxis_Y = int(round((m* intersection_Yaxis_X) + c))
    print(" Y axis intersection ---------->("+str(intersection_Yaxis_X) +","+ str(intersection_Yaxis_Y) +")")    
    print(" X axis intersection ---------->("+str(intersection_Xaxis_X) +","+ str(intersection_Xaxis_Y) +")")

    
    for i in range(intersection_Xaxis_X - 5 , intersection_Xaxis_X + 5):
        for j in range(intersection_Xaxis_Y - 5 , intersection_Xaxis_Y + 5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                allLines[j,i] = (255, 255, 255) 
                cdstP[j,i] = (255, 255, 255)  
    
    for i in range(intersection_Yaxis_X - 5 , intersection_Yaxis_X + 5):
        for j in range(intersection_Yaxis_Y - 5 , intersection_Yaxis_Y + 5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                allLines[j,i] = (0,252,0)
                cdstP[j,i] = (255, 255, 255)   

def take(elem):
    return elem

def identifyTicMarks_X_Axis():
    global pixcelForTicMark_X, width
    # Create Array
    X_Axis_Intersections = np.arange(len(linesP))

    # assign value to zero
    for h in range(0, len(linesP)):
        X_Axis_Intersections[h] = 0

    # Insert values to array
    i = 0
    for h in range(0, len(linesP)):
        x = Y_arr[h][0] 
        X_Axis_Intersections[i] = x 
        i = i + 1      

    # sort array
    array_sort =  np.sort(X_Axis_Intersections) 
    # print(array_sort)

    indexOfOriginX = 0
    for h in range(0, i):
        if(array_sort[h] == origin_X) :
            indexOfOriginX = h

    # create array to store distance from origin to tic mark
    distance = np.arange(i+1)

    # assign value to 0
    for h in range(0, i+1):
        distance[h] = 0

    modify_array_sort =  np.arange(len(linesP)) 

    # assign value to zero
    for h in range(0, len(linesP)):
        modify_array_sort[h] = 0
        
    increment = 1
    for h in range(0, len(linesP)):
        d = array_sort[h]
        if(h == 0):
            modify_array_sort[h] = d
        else : 
            dup = 0
            for k in range(0, len(linesP)):
                val = modify_array_sort[k]
                if(((val-5) <= d) and ((val+5)>= d)):
                    modify_array_sort[k] = int(round((val+d)/2))
                    dup = 1
                
            if (dup == 0 ):
                modify_array_sort[increment] = d
                increment = increment + 1

    # print(modify_array_sort)
    j = 0
    for h in range(0, len(linesP)):
        d = modify_array_sort[h]
        if(h > 0):
            d1 = modify_array_sort[h-1]
            if (d1 > 0) : 
                d2 = d - d1
                if (d2 > 10) :
                    distance[j] = d2
                    j = j + 1 

    # print(distance)
    count_arr = [[0] * 2 for i in range(j)]
    average_dis = 0

    for h in range(0, j ):
        d = distance[h] 
        if (d != 0) : 
            count = 0
            for i in range(0, j ):  
                if ((distance[i] >= d - 10) and (distance[i] <= d + 10) )  : 
                    count = count +1
            count_arr[h][0]  = d
            count_arr[h][1]  = count
    # print(count_arr)
 
    # Check max count
    maxCount = 0
    for h in range(0, len(count_arr) ): 
        c = count_arr[h][1] 
        if (c > maxCount) : 
            maxCount = c   
        
    equalCount = [[0] * 3 for i in range(j)] 
    index = 0
    m = 0

    for h in range(0, len(count_arr) ):
        total = 0
        c = count_arr[h][1]                 # count
        value = count_arr[h][0]             # value
        if c == maxCount  or c == (maxCount - 1) or c == (maxCount+1):
            equalCount[m][0] = value        # value
            equalCount[m][1] = c            # count

            for k in range(0, len(count_arr) ):
                val =  count_arr[k][0]  
                #if (val > (value - 10))  and (val < (value + 10)):
                if (val > (value - 10))  and (val < (value + 10)):
                    total = total + val
                # print("Total           ============ "+ str(total))

            equalCount[m][2] = total/c  # average value
            m = m+1 

    total_avg = 0
    for h in range(0, m ):
        total_avg = total_avg + equalCount[h][2] 
        
    if total_avg != 0 :
        aveg = total_avg/m
        pixcelForTicMark_X = int(round(aveg))

        ticMark = 1
        for ticMark in range(1 , 10):
            for i in range(origin_Y-15 , origin_Y+15) : 
                x1 = origin_X + (pixcelForTicMark_X*ticMark)
                x2 = origin_X - (pixcelForTicMark_X*ticMark)
                if ((i > 0) and (i < height)):
                    if((x1 > 0) and (x1 < width)):
                        allLines[i,x1] = (255,252,0)  
                        cdstP[i,x1] = (255,252,0)  
                    if((x2 > 0) and (x2<width)):
                        allLines[i,x2] = (255,252,0)  
                        cdstP[i,x2] = (255,252,0) 
    print("Pixcels between Tic marks (X axis)  ------------->   : " + str(pixcelForTicMark_X))

def identifyTicMarks_Y_Axis():
    global pixcelForTicMark_Y, height
    # Create Array
    Y_Axis_Intersections = np.arange(len(linesP))

    # assign value to zero
    for h in range(0, len(linesP)):
        Y_Axis_Intersections[h] = 0 

    # Insert values to array
    i = 0
    for h in range(0, len(linesP)):
        y = X_arr[h][0] 
        Y_Axis_Intersections[i] = y 
        i = i + 1      

    # sort array
    array_sort =  np.sort(Y_Axis_Intersections) 
    # print(array_sort)

    indexOfOriginY = 0
    for h in range(0, i):
        if(array_sort[h] == origin_Y) :
            indexOfOriginY = h

    # create array to store distance from origin to tic mark
    distance = np.arange(i+1)

    # assign value to 0
    for h in range(0, i+1):
        distance[h] = 0

    modify_array_sort =  np.arange(len(linesP)) 

    # assign value to zero
    for h in range(0, len(linesP)):
        modify_array_sort[h] = 0
        
    increment = 1
    for h in range(0, len(linesP)):
        d = array_sort[h]
        if(h == 0):
            modify_array_sort[h] = d
        else : 
            dup = 0
            for k in range(0, len(linesP)):
                val = modify_array_sort[k]
                if(((val-5) <= d) and ((val+5)>= d)):
                    modify_array_sort[k] = int(round((val+d)/2))
                    dup = 1
                
            if (dup == 0 ):
                modify_array_sort[increment] = d
                increment = increment + 1

    # print(modify_array_sort)
    j = 0
    for h in range(0, len(linesP)):
        d = modify_array_sort[h]
        if(h > 0):
            d1 = modify_array_sort[h-1]
            if (d1 > 0) : 
                d2 = d - d1
                if (d2 > 10) :
                    distance[j] = d2
                    j = j + 1 

    # print(distance)
    count_arr = [[0] * 2 for i in range(j)]
    average_dis = 0

    for h in range(0, j ):
        d = distance[h] 
        if (d != 0) : 
            count = 0
            for i in range(0, j ):  
                if ((distance[i] >= d - 10) and (distance[i] <= d + 10) )  : 
                    count = count +1
            count_arr[h][0]  = d
            count_arr[h][1]  = count
    # print(count_arr)
 
    # Check max count
    maxCount = 0
    for h in range(0, len(count_arr) ): 
        c = count_arr[h][1] 
        if (c > maxCount) : 
            maxCount = c   
        
    equalCount = [[0] * 3 for i in range(j)] 
    index = 0
    m = 0

    for h in range(0, len(count_arr) ):
        total = 0
        c = count_arr[h][1]                 # count
        value = count_arr[h][0]             # value
        if c == maxCount or c == (maxCount - 1) or c == (maxCount+1):
            equalCount[m][0] = value        # value
            equalCount[m][1] = c            # count

            for k in range(0, len(count_arr) ):
                val =  count_arr[k][0]  
                #if (val > (value - 10))  and (val < (value + 10)):
                if (val > (value - 10))  and (val < (value + 10)):
                    total = total + val
                # print("Total           ============ "+ str(total))

            equalCount[m][2] = total/c  # average value
            m = m+1 

    total_avg = 0
    for h in range(0, m ):
        total_avg = total_avg + equalCount[h][2] 
        
    if total_avg != 0 :
        aveg = total_avg/m
        pixcelForTicMark_Y = int(round(aveg)) 

        ticMark = 1
        for ticMark in range(1 , 10):
            for i in range(origin_X-15 , origin_X+15) : 
                y1 = origin_Y + (pixcelForTicMark_Y*ticMark)
                y2 = origin_Y - (pixcelForTicMark_Y*ticMark)
                if( i > 0 and i < width):
                    if((y1 > 0) and (y1<height) and (i > 0) and (i< width)):
                        allLines[y1,i] = (0,252,0)  
                        cdstP[y1,i] = (200,252,0)  
                    if((y2 > 0) and (y2<height) and (i > 0) and (i< width)):
                        allLines[y2,i] = (0,252,0)  
                        cdstP[y2,i] = (200,252,0)  
    print("Pixcels between Tic marks (Y axis)  ------------->   : " + str(pixcelForTicMark_Y))

def getRealCoordianatesWithoutOCR():
    global origin_X, origin_Y 
    global intersection_Xaxis_X, intersection_Yaxis_Y
    global real_intersection_Xaxis_X, real_intersection_Yaxis_Y

    # print("Pixcels between Tic marks (Y axis)  : " + str(pixcelForTicMark_Y))
    # print("Pixcels between Tic marks (X axis)  : " + str(pixcelForTicMark_X))

    if((origin_X <= intersection_Xaxis_X + 5) and (origin_X >= intersection_Xaxis_X - 5)): 
        real_intersection_Xaxis_X = 0
    elif (origin_X < intersection_Xaxis_X): 
        if (pixcelForTicMark_X != 0) :
            real_intersection_Xaxis_X = int(round((intersection_Xaxis_X - origin_X)/ pixcelForTicMark_X))
    else:
        if (pixcelForTicMark_X != 0) : 
            real_intersection_Xaxis_X = int(round((origin_X - intersection_Xaxis_X)/ pixcelForTicMark_X)*(-1))

    
    if((origin_Y <= intersection_Yaxis_Y + 5) and (origin_Y >= intersection_Yaxis_Y - 5)) :
        real_intersection_Yaxis_Y = 0 
    elif (origin_Y < intersection_Yaxis_Y):  
        if (pixcelForTicMark_Y != 0) :
            real_intersection_Yaxis_Y = int(round((intersection_Yaxis_Y - origin_Y)/ pixcelForTicMark_Y)*(-1))
            # print("origin " + str(origin_Y))
            # print("y  " + str(intersection_Yaxis_Y))
    else: 
        if (pixcelForTicMark_Y != 0) : 
            real_intersection_Yaxis_Y = int(round((origin_Y - intersection_Yaxis_Y)/ pixcelForTicMark_Y))
            # print("origin " + str(origin_Y))
            # print("y  " + str(intersection_Yaxis_Y))

    print(" Real Coordinates of X intersectio Point  = " + str(real_intersection_Xaxis_X))
    print(" Real Coordinates of Y intersectio Point  = " + str(real_intersection_Yaxis_Y))

def equationIP(): 
    c = real_intersection_Yaxis_Y
    if (real_intersection_Yaxis_Y != 0 and real_intersection_Xaxis_X != 0):
        m = (real_intersection_Yaxis_Y/-(real_intersection_Xaxis_X))
        print(" Eqation : y =  " +str(m)+"x + " + str(c) )

def main(argv):
    
    global cdstP, allLines, linesP, arr, X_arr, Y_arr, graphs_arr, noOfLines, origin_X, origin_Y, height, width 

    # Loads an image
    default_file = 'x2.png' 
    filename = argv[0] if len(argv) > 0 else default_file

    # Convert to gray Scale
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # img = cv.imread(cv.samples.findFile(filename))
    # src = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

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

    resized = src
    height = np.size(resized, 0)
    width = np.size(resized, 1)
    print("Image width : " + str(width))
    print("Image height : " + str(height))
    
    # Edge detection
    #dst = cv.Canny(src, 20, 200, None, 3) 
    dst = cv.Canny(resized, 20, 200, None, 3) 

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    allLines = np.copy(cdst)  
    
    # Get Text
    global result
    result = pytesseract.image_to_string(Image.open(cv.samples.findFile(filename)))
    print(" Result : " + str(result))

    if result: 
        # Generate Eqation Using Given Coodinates
        getEqationByUsingCoordinate() 
    else:
        print("Text cannot Read")
     
    # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 0, 10) 
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

        # identify X and Y axis intersection point
        identifyIntersection()
        
        # identify X axis Ticmarks
        if (pixcelForTicMark_X == 0 ):
            identifyTicMarks_X_Axis()
        
        # identify Y axis Ticmarks
        if (pixcelForTicMark_Y == 0):
            identifyTicMarks_Y_Axis()

        print("Tic Mark Distance " + str(pixcelForTicMark_Y))

        # get real coordinates of y axis and X intersection point without OCR
        if ( pixcelForTicMark_Y !=0 and pixcelForTicMark_X != 0) :
            getRealCoordianatesWithoutOCR()

        # generate equation using Image processing without OCR
        equationIP()

    cv.imshow("Resized image", resized) 
    cv.imshow("Source", src) 
    cv.imshow("Probabilistic Line Transform", cdstP) 
    cv.imshow("Detected All Lines" , allLines )
    cv.waitKey()
    return 0  

if __name__ == "__main__":
    main(sys.argv[1:]) 