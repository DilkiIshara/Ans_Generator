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

filename = None
result = "" 
linesP = cv.HoughLinesP(None, 1, np.pi / 180, 25, None, 10, 10)  
numberOf_Horizontal = numberOf_Vertical = numberOf_Graph = rows = reduce = 0
maxlength_X = maxlength_Y = maxlength_Graph = 0
X_axis_cordinate = Y_axis_cordinate = graph_cordinate = -1
arr = None             # 0-x1 1-Y1 2-x2 3-y2
X_arr = Y_arr = None   # 0-a  1-length 2-arrIndex
graphs_arr = None      # 0-m  1-C 2-length 3-arrIndex 
cdstP = cdstP2 = allLines = textCoordinate = None
noOfLines = numberOfCharactor = 0
width = height = 0
origin_X = origin_Y = intersection_Xaxis_X = intersection_Xaxis_Y = intersection_Yaxis_X = intersection_Yaxis_Y = numberOfDigitValue = 0
real_intersection_Xaxis_X = real_intersection_Yaxis_Y = 0
pixcelForTicMark_Y = pixcelForTicMark_X = 0
N = 4 # arr (x,y) (x,y) 
graphCrossOrigin = False
ratio_Y_Axis_Value = ratio_X_Axis_Value = 1
found_X = found_Y = False
src = MofologyImg = graphType = None

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
            # getTextCoordinate() 
        # else:
            # getTextCoordinate()
    else:
        # getTextCoordinate()
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
                    arr[j][0] = int(round((value1+arr[j][0])/2))
                    arr[j][1] = int(round((value2+arr[j][1])/2))
                    arr[j][2] = int(round((value3+arr[j][2])/2))
                    arr[j][3] = int(round((value4+arr[j][3])/2))
                    reduce = reduce+1
                    duplicate = 1
            
            if duplicate == 0: 
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
            elif ((x_difference != 0) and (y_difference != 0)):
                m = y_difference/x_difference
                c = y1 - (x1*m) 
                graphs_arr[k][0] = m
                graphs_arr[k][1] = c
                graphs_arr[k][2] = lineLength
                graphs_arr[k][3] = k
                numberOf_Graph = numberOf_Graph + 1
            # else:
            #     print("x_difference =  " + str(x_difference))
            #     print("y_difference =  " + str(y_difference))

def checkGraph():
    global graphType
    if numberOf_Graph > 1 : # check number of lines which are not horizontal or vertical
        negativeG = positiveG = 0
        for i in range(0, len(graphs_arr)):
            m = graphs_arr[i][0]
            if m != 0:
                # print(" graph m " + str(graphs_arr[i][0]))
                if m < 0:
                    negativeG = negativeG + 1
                else: 
                    positiveG = positiveG + 1
        if ((positiveG >= 1) and (negativeG >=1)) : # If have two lines which has positive and negative gradiants
            graphType = "Quadratic"
            print("Quadratic")
        else:
            graphType = "linear"
            print(" linear ")
    else:
        graphType = "linear"
        print(" linear ")   

def getQuadraticGraphCoodinates():
    global graphType, cdstP2
    lengthNegative = lengthPositive = negativeIndex = positiveIndex = 0  
    quadraticType = None
    pm = pc = nm = nc = px = nx = 0
    minMaxY = sx = 0

    for i in range(0, len(graphs_arr)):
        m = graphs_arr[i][0]
        lineLength = graphs_arr[i][2] 
        c = graphs_arr[i][1] 
        if m != 0:
            # print(" graph m " + str(graphs_arr[i][0]))
            # get the line which has negative gradiant and max length
            if m < 0:
                if lengthNegative < lineLength :
                    lengthNegative = lineLength
                    nm = m
                    nc = c
                    negativeIndex = i
            # get the line which has positive gradiant and max length
            else: 
                if lengthPositive < lineLength :
                    lengthPositive = lineLength
                    pm = m
                    pc = c
                    positiveIndex = i

    # Draw the 2 linear lines og Quadratic Graphs
    # print(" Positive Index = " + str(positiveIndex))
    # print(" Negative Index = " + str(negativeIndex))
    cv.line(cdstP, (arr[negativeIndex][0], arr[negativeIndex][1]), (arr[negativeIndex][2], arr[negativeIndex][3]), (5,0,255), 2, cv.LINE_AA)
    cv.line(cdstP, (arr[positiveIndex][0], arr[positiveIndex][1]), (arr[positiveIndex][2], arr[positiveIndex][3]), (128, 0, 128), 2, cv.LINE_AA)
    
    # get x coodinates of line which has positive gradiant
    positiveXcoodinate = 0
    if ((arr[positiveIndex][0]) < (arr[positiveIndex][2])):
        positiveXcoodinate = arr[positiveIndex][0]
    else:
        positiveXcoodinate = arr[positiveIndex][2]
    
    # get x coodinates of line which has negative gradiant
    negativeXcoodinate = 0
    if ((arr[negativeIndex][0]) < (arr[negativeIndex][2])):
        negativeXcoodinate = arr[negativeIndex][0]
    else:
        negativeXcoodinate = arr[negativeIndex][2]
    
    # check quadratic graph hax max or min value
    if (positiveXcoodinate < negativeXcoodinate):
        quadraticType = "min"
        print(" Has Min Value")
    else:
        quadraticType = "max"
        print(" Has MaX Value")

    # take the Y value for both positive and negative lines of quadratic graph
    py = ny = y = 0
    if quadraticType == "min": 
        if (arr[positiveIndex][1] < arr[positiveIndex][3]):
            py = arr[positiveIndex][1]
        else :
            py = arr[positiveIndex][3]

        if (arr[negativeIndex][1] < arr[negativeIndex][3]):
            ny = arr[negativeIndex][1]
        else :
            ny = arr[negativeIndex][3]
        if(ny > py):
            y = ny
        else:
            y = py
        # px = int(round((y - pc )/pm))
        # nx = int(round((y - nc )/nm))
        # print(" px , nx " + str(px) +"fffffffffff" + str(nx))
        # sx = int(round((px+nx))/2)
        # print("sx = " + str(sx)) 
        # for i in range(0, width):
        #     allLines[y,i] = (50, 55, 255)
        #     cdstP[y,i] = (50, 55, 255) 
        # for i in range(0, height): 
        #     allLines[i,sx] = (50, 55, 255)
        #     cdstP[i,sx] = (50, 55, 255)
        # for i in range(0, height): 
        #     allLines[i,px] = (50, 55, 255)
        #     cdstP[i,px] = (50, 55, 255)
        # for i in range(0, height): 
        #     allLines[i,nx] = (50, 55, 255)
        #     cdstP[i,nx] = (50, 55, 255) 

    elif quadraticType == "max": 
        # print("Max")
        # py = ny = y = 0
        if (arr[positiveIndex][1] < arr[positiveIndex][3]):
            py = arr[positiveIndex][3]
        else :
            py = arr[positiveIndex][1]
        if (arr[negativeIndex][1] < arr[negativeIndex][3]):
            ny = arr[negativeIndex][3]
        else :
            ny = arr[negativeIndex][1]
        if(ny > py):
            y = py
        else:
            y = ny

    # get X coodinate of graphs and get the x coodinate of (Samamithika Akshaya )
    px = int(round((y - pc )/pm))
    nx = int(round((y - nc )/nm))
    sx = int(round((px+nx))/2)

    # draw lines (Samamithika akshaya)
    for i in range(0, width):
        cdstP2[y,i] = (50, 55, 255)
        cdstP[y,i] = (50, 55, 255) 
    for i in range(0, height): 
        cdstP2[i,sx] = (50, 55, 255)
        cdstP[i,sx] = (50, 55, 255)
    for i in range(0, height): 
        cdstP2[i,px] = (50, 55, 255)
        cdstP[i,px] = (50, 55, 255)
    for i in range(0, height): 
        cdstP2[i,nx] = (50, 55, 255)
        cdstP[i,nx] = (50, 55, 255) 
    #cv.imshow("Mofology ------" , MofologyImg)

    # Transform source image to gray if it is not already
    if len(MofologyImg.shape) != 2:
        gray = cv.cvtColor(MofologyImg, cv.COLOR_BGR2GRAY)
    else:
        gray = MofologyImg 

    # Set threshold level
    threshold_level = 10

    # Find coordinates of all pixels below threshold
    coords = np.column_stack(np.where(gray < threshold_level))
    np.set_printoptions(threshold=np.inf)
    #print(coords)
     
    # create array to store y coodinates of quadratic graph
    yCordinates = np.arange(height)

    # assign value to 0
    for h in range(0, height):
        yCordinates[h] = 0

    # /*
       # /* This point we can check graph is samamithka on y axis */
       # 
       # 
     
    # store Y coordinates in yCordinates list
    # indexY = 0
    # for i in range(0, len(coords)):
    #     y = coords[i][0]
    #     x = coords[i][1]   
    #     if (x >= sx -2) and (x <= sx +2):
    #         if (indexY < height):
    #             yCordinates[indexY] = y
    #             indexY = indexY + 1
    #         # for j in range(0, 10):
    #         #     cdstP[y+j,x] = ( 50 , 55, 255)
    #         #     print(" X coodinate = " + str(coords[i][1]) + " Y coordinate " + str(coords[i][0]))
    # # for i in range(0, (len(yCordinates)-1)):
    # # y_start = yCordinates[0]

    # # sort array
    # array_sort =  np.sort(yCordinates) 

    # # find max 
    # max = 0  
    # for i in range(0, (len(yCordinates))): 
    #     currentY = yCordinates[i]
    #     if (currentY > max):
    #         max = currentY

    # # find min value
    # min = max
    # for i in range(0, (len(yCordinates))): 
    #     currentY = yCordinates[i]
    #     if ((currentY != 0) and (currentY < min) ):
    #         min = currentY

    # # print(" max Current value ====  "+ str(max))
    # # print(" min Current value ====  "+ str(min))
    
    # # identify Y coordinate of min/max point of quadratic eqation
    # if ((max - min) <= 10):
    #     minMaxY = int(round((max+min)/2))

    # # if we cant idntify Y coordinate of min/max point of quadratic eqation expand the X coodinate range

    # # elif((max-min) > pixcelForTicMark_Y):
    # elif((max-min) > 10):
        # print (" sx -------------------" + str(sx))

    xYCoodinareOfQuadraticGraph = [[0] * 2 for i in range(100)] # 0- X coodinate 1- Y coodinate
    # yCordinatesOfQuadraticGraph = np.arange(height)
    yCordinatesOfQuadraticGraph = np.arange(height)

    # assign value to 0
    for h in range(0, height):
        yCordinatesOfQuadraticGraph[h] = 0

    # get the y coodinate of Graphs by considering mor X coordinates
    index = 0 
    indexY = 0
    for i in range(sx-30, sx + 30):
        cX = i
        c = 1
        min = max = 0
        total_Y = 0
        count = 0
        for p in range(0, len(coords)):
            y = coords[p][0]
            x = coords[p][1]  
            # allLines[x,y] = (255, 255, 0)
            if (x == cX and y != 0):
                total_Y = total_Y + y
                count = count + 1
                if c == 1:
                    min = max = y
                elif c > 1:
                    if (y > max ):
                        max = y
                    if (y < min):
                        min = y
                c = c + 1
        # print("Min ++++++++++++" + str(min) + "Max ++++++++++++" + str(max) )
        #print (" Total Y " + str(total_Y ) + " Count " + str(count)+ "******** ")
        if (count != 0 and total_Y != 0 and (max - min) < 10):
            # print (" Total Y " + str(total_Y ) + " Count " + str(count))
            yCordinatesOfQuadraticGraph[indexY] = int(round(total_Y/count))
            indexY = indexY + 1
            cdstP2[y,x] = (255, 0, 0)
            print (" Y coodinate  " + str(int(round(total_Y/count))) + " ******" +" indexY " + str(indexY))
       
    # length = len(yCordinatesOfQuadraticGraph) 
    # print(" Length " + str(length))
    
    for i in range(0, len(yCordinatesOfQuadraticGraph) ):
        y = yCordinatesOfQuadraticGraph[i]
        if (y != 0):
            print("y coordinate   " + str(y) )
        
    # sort array
    array_sort =  np.sort(yCordinatesOfQuadraticGraph) 

    maxY = yCordinatesOfQuadraticGraph[0]
    for i in range(0, len(yCordinatesOfQuadraticGraph)):
        y = yCordinatesOfQuadraticGraph[i]
        if ( y > maxY):
            maxY = y

    minY = maxY
    for i in range(0, len(yCordinatesOfQuadraticGraph)):
        y = yCordinatesOfQuadraticGraph[i]
        if ( y < minY and y != 0):
            minY = y
        
    if quadraticType == "max": 
        minMaxY = minY
    elif quadraticType == "min":
        minMaxY = maxY
 
    for i in range(sx - 5 , sx + 5):
        for j in range(minMaxY - 5, minMaxY +5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                cdstP2[j,i] = (255, 0, 0)
                cdstP2[j,i] = (255, 0, 0)


def draw_X_Axis():
    global maxlength_X
    global X_axis_cordinate
    global origin_Y, allLines 

    # get the maxmum lenth horizontal line
    # for h in range(0, len(linesP)):
    #     l = X_arr[h][1] 
    #     if l > maxlength_X : 
    #         X_axis_cordinate = h
    #         maxlength_X = l  
    # print(" Length of X Axis  : " + str(maxlength_X))

    sameLine = 0
    for h in range(0, len(linesP)):
        l = X_arr[h][1] 
        if l == maxlength_X or (l > maxlength_X - (maxlength_X * 0.1)) : 
            sameLine = sameLine + 1
    print(" Same Lines : " + str(sameLine))

    if (sameLine > 1): 
        # find_X_Axis_Using_Mofology() 
        find_X_Axis() 

def addMofologyToImage():
    global MofologyImg
    # Transform source image to gray if it is not already
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src

    # Apply adaptiveThreshold at the bitwise_not of gray
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C,  cv.THRESH_BINARY, 15, -2)
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols // 10
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)

   
    # Specify size on vertical axis
    rows = vertical.shape[0]
    verticalsize = rows // 10
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalStructure)

    test2 = bw - vertical - horizontal 

    # smooth
    graph = cv.bitwise_not(test2) 
    edges = cv.adaptiveThreshold(graph, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    kernel = np.ones((2, 2), np.uint8)
    edges = cv.dilate(edges, kernel)
    smooth = np.copy(graph)
    smooth = cv.blur(smooth, (2, 2))
    (rows, cols) = np.where(edges != 0)
    graph[rows, cols] = smooth[rows, cols] 
    
    # final result
    MofologyImg = graph
    # cv.imshow("Mofology ", MofologyImg)  

def find_X_Axis():
    global maxlength_X
    global X_axis_cordinate
    global pixcelForTicMark_X 
 
    half_pixcelForTicMark_X = 10
    minLen_X_Axis = maxlength_X
    min_X_axis_cordinate = 0 
    
    # Identify Shorted horizontal Line
    for h in range(0, len(linesP)):
        l = X_arr[h][1] 
        if ((l < minLen_X_Axis) and (l != 0)) : 
            min_X_axis_cordinate = h
            minLen_X_Axis = X_arr[h][1]   
    min_XAxis_Ycordinate = arr[min_X_axis_cordinate][1] 
    cv.line(cdstP, (arr[min_X_axis_cordinate][0], arr[min_X_axis_cordinate][1]), (arr[min_X_axis_cordinate][2], arr[min_X_axis_cordinate][3]), (255,0,0), 2, cv.LINE_AA)
    
    print(" Identify x using Shortest line  =  " +str(min_X_axis_cordinate))

    # for h in range(0, len(linesP)):
    #     if (X_arr[h][1] <= (minLen_X_Axis +5) and  (X_arr[h][0] <= (min_XAxis_Ycordinate+3)) and (X_arr[h][0] >= (min_XAxis_Ycordinate-3))) : 
    #         min_XAxis_Ycordinate = (X_arr[h][0] + min_XAxis_Ycordinate)/2 
    
    if (pixcelForTicMark_X == 0):
        identifyTicMarks_X_Axis()
    
    if(pixcelForTicMark_X != 0):
        half_pixcelForTicMark_X = pixcelForTicMark_X/2 
    
    # identify all the legthly lane which are near
    count = 0
    for h in range(0, len(linesP)):
        X_axis_Y_cordinate = arr[h][1]
        length_Of_X_Axis = X_arr[h][1]   
        if ((X_axis_Y_cordinate <= (min_XAxis_Ycordinate+half_pixcelForTicMark_X) + 5) and (X_axis_Y_cordinate >= (min_XAxis_Ycordinate-half_pixcelForTicMark_X - 5))) :     
            if ((length_Of_X_Axis == maxlength_X) or (length_Of_X_Axis > (maxlength_X-(maxlength_X*0.1)))) : 
                count = count + 1
                X_axis_cordinate = h 

    if (count > 1):
        for h in range(0, len(linesP)):
            X_axis_Y_cordinate = arr[h][1]
            length_Of_X_Axis = X_arr[h][1]   
            if ((X_axis_Y_cordinate <= (min_XAxis_Ycordinate+20)) and (X_axis_Y_cordinate >= (min_XAxis_Ycordinate-20))) :   
                if ((length_Of_X_Axis == maxlength_X  or (length_Of_X_Axis > (maxlength_X-(maxlength_X*0.05)))) and (X_axis_Y_cordinate <= (min_XAxis_Ycordinate)) ) :  
                    X_axis_cordinate = h 
                   
def draw_Y_Axis():
    global maxlength_Y
    global origin_X
    global Y_axis_cordinate
    global pixcelForTicMark_Y

    # find the maximum length
    # for h in range(0, len(linesP)):
    #     l = Y_arr[h][1] 
    #     if l > maxlength_Y : 
    #         Y_axis_cordinate = h
    #         maxlength_Y = Y_arr[h][1]   

    sameLine = 0
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l == maxlength_Y  or (l > maxlength_Y - (maxlength_Y * 0.1)): 
            sameLine = sameLine + 1
    print(" Same Lines : " + str(sameLine))
    
    if (sameLine > 1):
        find_Y_Axis() 


def find_Y_Axis():
    global maxlength_Y
    global Y_axis_cordinate
    global pixcelForTicMark_Y 
 
    half_pixcelForTicMark_Y = 10
    minLen_Y_Axis = maxlength_Y
    min_Y_axis_cordinate = 0

    # identify verical line which has mimum length
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if ((l < minLen_Y_Axis) and (l != 0)) : 
            min_Y_axis_cordinate = h
            minLen_Y_Axis = Y_arr[h][1] 
            # print("start Find" + str(minLen_Y_Axis)) 
    x =  arr[min_Y_axis_cordinate][0] 
    # print("min_Y_axis_X_cordinate " + str(x))
    cv.line(cdstP, (arr[min_Y_axis_cordinate][0], arr[min_Y_axis_cordinate][1]), (arr[min_Y_axis_cordinate][2], arr[min_Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA) 
    min_YAxis_Xcordinate = arr[min_Y_axis_cordinate][0]
    # print("max Length Value " + str(maxlength_Y))
    
    if (pixcelForTicMark_Y == 0):
        identifyTicMarks_Y_Axis()
    
    if(pixcelForTicMark_Y != 0):
        half_pixcelForTicMark_Y = pixcelForTicMark_Y/2 

    # identify verical line which is near to shortest line
    count = 0
    for h in range(0, len(linesP)):
        Y_axis_X_cordinate = arr[h][0]
        length_Of_Y_Axis = Y_arr[h][1]    
        if ((Y_axis_X_cordinate <= (min_YAxis_Xcordinate+half_pixcelForTicMark_Y)) and (Y_axis_X_cordinate >= (min_YAxis_Xcordinate-half_pixcelForTicMark_Y))) :    
            if (length_Of_Y_Axis == maxlength_Y or (length_Of_Y_Axis > maxlength_Y - (maxlength_Y * 0.1))): 
                Y_axis_cordinate = h 
                count = count + 1 
    
    # get the left side line as Y axis
    if (count > 1):
        for h in range(0, len(linesP)):
            Y_axis_X_cordinate = arr[h][0]
            length_Of_Y_Axis = Y_arr[h][1]    
            if ((Y_axis_X_cordinate <= (min_YAxis_Xcordinate+20)) and (Y_axis_X_cordinate >= (min_YAxis_Xcordinate-20))) :  
                if ((length_Of_Y_Axis == maxlength_Y or (length_Of_Y_Axis > maxlength_Y - (maxlength_Y * 0.1))) and (Y_axis_X_cordinate < min_YAxis_Xcordinate )) : 
                    Y_axis_cordinate = h  
            
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
            if(i > 0 and i < width and j > 0 and j < height ): 
                allLines[j,i] = (255, 255, 255)
                cdstP[j,i] = (255, 255, 255)         

def identifyIntersection():
    global intersection_Xaxis_Y, intersection_Xaxis_X, intersection_Yaxis_Y, intersection_Yaxis_X, graphCrossOrigin
  
    m = graphs_arr[graph_cordinate][0] 
    c = graphs_arr[graph_cordinate][1] 
      
    intersection_Xaxis_Y = origin_Y
    if (m != 0):
        intersection_Xaxis_X = int(round((intersection_Xaxis_Y - c)/m))
    intersection_Yaxis_X = origin_X  
    intersection_Yaxis_Y = int(round((m* intersection_Yaxis_X) + c))

    if ( (intersection_Yaxis_X <= (origin_X + 3)) and (intersection_Yaxis_X >= (origin_X - 3)) and (intersection_Yaxis_Y <= (origin_Y + 3)) and (intersection_Yaxis_Y >= (origin_Y - 3))):
        graphCrossOrigin = True
        print(" Go through Origin")
    
    # elif((intersection_Xaxis_X <= (origin_X + 3)) and (intersection_Xaxis_X >= (origin_X - 3)) and (intersection_Xaxis_Y <= (origin_Y + 3)) and (intersection_Xaxis_Y >= (origin_Y - 3))):
    #     graphCrossOrigin = True
    #     print(" Go through Origin")

    print(" Y axis intersection ---------->("+str(intersection_Yaxis_X) +","+ str(intersection_Yaxis_Y) +")")    
    print(" X axis intersection ---------->("+str(intersection_Xaxis_X) +","+ str(intersection_Xaxis_Y) +")")

    # draw intersection of x axis
    for i in range(intersection_Xaxis_X - 5 , intersection_Xaxis_X + 5):
        for j in range(intersection_Xaxis_Y - 5 , intersection_Xaxis_Y + 5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                allLines[j,i] = (200, 20, 100) 
                cdstP[j,i] = (200, 20, 100)  
    
    for i in range(intersection_Yaxis_X - 5 , intersection_Yaxis_X + 5):
        for j in range(intersection_Yaxis_Y - 5 , intersection_Yaxis_Y + 5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                allLines[j,i] = (0,50,100)
                cdstP[j,i] = (0, 50, 100 )   

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

        # ticMark = 1
        # for ticMark in range(1 , 10):
        #     for i in range(origin_Y-15 , origin_Y+15) : 
        #         x1 = origin_X + (pixcelForTicMark_X*ticMark)
        #         x2 = origin_X - (pixcelForTicMark_X*ticMark)
        #         if ((i > 0) and (i < height)):
        #             if((x1 > 0) and (x1 < width)):
        #                 allLines[i,x1] = (255,252,0)  
        #                 cdstP[i,x1] = (255,252,0)  
        #             if((x2 > 0) and (x2<width)):
        #                 allLines[i,x2] = (255,252,0)  
        #                 cdstP[i,x2] = (255,252,0) 
    # print("Pixcels between Tic marks (X axis)  ------------->   : " + str(pixcelForTicMark_X))

def draw_TicMark_X_Axis():
    global origin_X, origin_Y, pixcelForTicMark_X, width, height
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

        # ticMark = 1
        # for ticMark in range(1 , 10):
        #     for i in range(origin_X-15 , origin_X+15) : 
        #         y1 = origin_Y + (pixcelForTicMark_Y*ticMark)
        #         y2 = origin_Y - (pixcelForTicMark_Y*ticMark)
        #         if( i > 0 and i < width):
        #             if((y1 > 0) and (y1<height) and (i > 0) and (i< width)):
        #                 allLines[y1,i] = (0,252,0)  
        #                 cdstP[y1,i] = (200,252,0)  
        #             if((y2 > 0) and (y2<height) and (i > 0) and (i< width)):
        #                 allLines[y2,i] = (0,252,0)  
        #                 cdstP[y2,i] = (200,252,0)  
    # print("Pixcels between Tic marks (Y axis)  ------------->   : " + str(pixcelForTicMark_Y))

def draw_TicMark_Y_Axis():
    global pixcelForTicMark_Y, origin_X, origin_Y, width, height
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
            real_intersection_Xaxis_X = int(round((intersection_Xaxis_X - origin_X)/ pixcelForTicMark_X)) * ratio_X_Axis_Value 
    else:
        if (pixcelForTicMark_X != 0) : 
            real_intersection_Xaxis_X = int(round((origin_X - intersection_Xaxis_X)/ pixcelForTicMark_X)*(-1)) * ratio_X_Axis_Value
    
    if((origin_Y <= intersection_Yaxis_Y + 5) and (origin_Y >= intersection_Yaxis_Y - 5)) :
        real_intersection_Yaxis_Y = 0 
    elif (origin_Y < intersection_Yaxis_Y):  
        if (pixcelForTicMark_Y != 0) :
            real_intersection_Yaxis_Y = int(round((intersection_Yaxis_Y - origin_Y)/ pixcelForTicMark_Y)*(-1)) * ratio_Y_Axis_Value
    else: 
        if (pixcelForTicMark_Y != 0) : 
            real_intersection_Yaxis_Y = int(round((origin_Y - intersection_Yaxis_Y)/ pixcelForTicMark_Y)) * ratio_Y_Axis_Value

    print(" Real Coordinates of X intersectio Point  = " + str(real_intersection_Xaxis_X))
    print(" Real Coordinates of Y intersectio Point  = " + str(real_intersection_Yaxis_Y))

def equationIP(): 
    c = real_intersection_Yaxis_Y 
    if (real_intersection_Yaxis_Y != 0 and real_intersection_Xaxis_X != 0):
        m = (real_intersection_Yaxis_Y/-(real_intersection_Xaxis_X))
        print(" Eqation : y =  " +str(m)+"x + " + str(c) )

def getTextCoordinate():
    global textCoordinate, filename, ratio_Y_Axis_Value, ratio_X_Axis_Value, numberOfCharactor, numberOfDigitValue

    ratio_X_Axis_Value_Array = ratio_Y_Axis_Value_Array = np.arange(5) 
    # ratio_Y_Axis_Value_Array =  np.arange(5) 
    total_ratio_X_Axis_Value = total_ratio_Y_Axis_Value = ratio_Y_Axis_Index = ratio_X_Axis_Index = 0

    # run tesseract, returning the bounding boxes
    boxes = pytesseract.image_to_boxes(Image.open(filename)) # also include any config options you use
    numberOfCharactor = int(len(boxes.splitlines()))
 
    textCoordinate = [[0] * 4 for i in range(numberOfCharactor)] 
    
    # store values into textCoordinate array
    i = 0
    ratio_X_Axis_Value = ratio_Y_Axis_Value = 0
    numberOf_Tic_Mark_X_Axis = 0

    for b in boxes.splitlines():
        b = b.split(' ')
        # print("Charactor of  " + b[0] + "  =  "+b[1]+ ","+b[2]+ ","+b[3]+ ","+b[4])  # (x1, y1, X2, y2) 
        if (b[0].isdigit() and (int(b[0]) != 0) ):
            textCoordinate[i][0] = int(b[0]) # store Charactor
            textCoordinate[i][1] = round((int(b[1]) + int(b[3]))/2) # store X Coordinate
            textCoordinate[i][2] = round(((height - int(b[2])) + (height - int(b[4])))/2) # store Y Coordinate
            i = i + 1
            numberOfDigitValue = i
     

def identifyNumbersRelated_X_Y_Axis():
    global  ratio_X_Axis_Value, ratio_Y_Axis_Value 
    ratio_X_Axis_Value = ratio_Y_Axis_Value = 0
    ratio_X_Axis_Value_Array = ratio_Y_Axis_Value_Array = np.arange(5) 
    # ratio_Y_Axis_Value_Array =  np.arange(5) 
    total_ratio_X_Axis_Value = total_ratio_Y_Axis_Value = ratio_Y_Axis_Index = ratio_X_Axis_Index = 0
    numberOf_Tic_Mark_X_Axis = numberOf_Tic_Mark_Y_Axis = 0
    
    if numberOfCharactor > 0:
        for i in range(0, numberOfCharactor):
        # for i in range(0, len(textCoordinate)):
            character_X_Cordinate = textCoordinate[i][1]
            character_Y_Cordinate = textCoordinate[i][2]
            if(((textCoordinate[i][1]) <= (origin_X+pixcelForTicMark_X)) and ((textCoordinate[i][1]) >= (origin_X-pixcelForTicMark_X))):
                textCoordinate[i][3] = -1  # Its is a tic mark coordinate of Y axis
                # cv.rectangle(cdstP, (int(b[1]), height - int(b[2])), (int(b[3]), height - int(b[4])), (0, 255, 0), 2)
               
                if (character_Y_Cordinate > origin_Y):
                    numberOf_Tic_Mark_Y_Axis = round((character_Y_Cordinate - origin_Y)/ pixcelForTicMark_Y)

                elif (character_Y_Cordinate < origin_Y):
                    numberOf_Tic_Mark_Y_Axis = round((origin_Y - character_Y_Cordinate)/ pixcelForTicMark_Y) 

                if ((ratio_Y_Axis_Index < 5) and (numberOf_Tic_Mark_Y_Axis > 0)):
                    # print(" X coodinate" + str(character_X_Cordinate))
                    ratio_y  = round(int(textCoordinate[i][0]) / numberOf_Tic_Mark_Y_Axis )
                    if (ratio_y > 0) :
                        ratio_Y_Axis_Value_Array[ratio_Y_Axis_Index] = ratio_y
                        ratio_Y_Axis_Index = ratio_Y_Axis_Index + 1

            elif(((character_Y_Cordinate) <= (origin_Y+pixcelForTicMark_Y)) and ((character_Y_Cordinate) >= (origin_Y-pixcelForTicMark_Y))):
                textCoordinate[i][3] = 1  # Its is a tic mark coordinate of X axis
                # cv.rectangle(cdstP, (int(b[1]), height - int(b[2])), (int(b[3]), height - int(b[4])), (255, 0, 0), 2)

                if(character_X_Cordinate > origin_X):
                    numberOf_Tic_Mark_X_Axis = round((character_X_Cordinate - origin_X)/ pixcelForTicMark_X)

                elif (character_X_Cordinate < origin_X):
                    numberOf_Tic_Mark_X_Axis = round((origin_X - character_X_Cordinate)/ pixcelForTicMark_X)

                if ((ratio_X_Axis_Index < 5) and (numberOf_Tic_Mark_X_Axis > 0)):
                    ratio  = round(int(textCoordinate[i][0]) / numberOf_Tic_Mark_X_Axis )
                    if (ratio > 0) : 
                        ratio_X_Axis_Value_Array[ratio_X_Axis_Index] = ratio
                        ratio_X_Axis_Index = ratio_X_Axis_Index + 1 

    for h in range(0, ratio_X_Axis_Index ):
        total_ratio_X_Axis_Value = total_ratio_X_Axis_Value + ratio_X_Axis_Value_Array[h] 
        # print(" total_ratio_X_Axis_Value " + str(total_ratio_X_Axis_Value))

    for h in range(0, ratio_Y_Axis_Index ):
        total_ratio_Y_Axis_Value = total_ratio_X_Axis_Value + ratio_Y_Axis_Value_Array[h]   
        # print(" total_ratio_X_Axis_Value " + str(total_ratio_Y_Axis_Value))  
    
    if (total_ratio_X_Axis_Value > 0):
        ratio_X_Axis_Value = round(total_ratio_X_Axis_Value/(ratio_X_Axis_Index))
        print("Ratio_X_Axis_Value " + str(ratio_X_Axis_Value))

    if (total_ratio_Y_Axis_Value > 0):
        ratio_Y_Axis_Value = round(total_ratio_Y_Axis_Value/(ratio_Y_Axis_Index))
        print("Ratio_Y_Axis_Value " + str(ratio_Y_Axis_Value))    
    
    # print charactor X coodinate and Y coodinate
    # for h in range(0, numberOfCharactor ):
    #     print(" Charactor  = "+ str(textCoordinate[h][0]) + " X Coordinate = " + str(textCoordinate[h][1]) + " Y coordinate = " + str(textCoordinate[h][2]))
    
    if ((ratio_X_Axis_Value == 0) and (ratio_Y_Axis_Value == 0)):
        ratio_X_Axis_Value = ratio_Y_Axis_Value = 1
    elif ((ratio_X_Axis_Value == 0) and (ratio_Y_Axis_Value != 0)):
        ratio_X_Axis_Value = ratio_Y_Axis_Value
    elif ((ratio_X_Axis_Value != 0) and (ratio_Y_Axis_Value == 0)):
        ratio_Y_Axis_Value = ratio_X_Axis_Value

def indentify_Y_UsingValues():
    global Y_axis_cordinate, X_axis_cordinate, found_X, maxlength_Y, textCoordinate, found_Y

    count_X =  [[0] * 2 for i in range(numberOfCharactor)] # List  to store charactor X coordinate and frequency of that value
    maxlength_Y = max_Count_X = x_coordinate = maxlength_Y = 0

    # store charactor Y coordinate and frequency of that value
    for i in range(0, numberOfCharactor):
        x_val = textCoordinate[i][1]
        count = 0
        if x_val != 0 :
            for h in range(0 , numberOfCharactor):
                val = textCoordinate[h][1]
                if ((val <= x_val+5 ) and (val >= x_val-5)):
                    count = count + 1
        count_X[i][0] = x_val
        count_X[i][1] = count

    # print charactor X coordinate and frequency of that value
    # for i in range(0, numberOfCharactor ):
    #     print(" =========== " + str(  count_X[i][0] ) + "_--------------------  " + str(count_X[i][1]))

    # get the maximum frequency of the x coordinate
    for i in range(0, numberOfCharactor):
        c = count_X[i][1]
        if (c > max_Count_X):
            max_Count_X = c
            x_coordinate = count_X[i][0]
    # print(" X coordinate --------------------"+str(x_coordinate))

    # get the vertical line which has maximum length
    for h in range(0, noOfLines):
        l = Y_arr[h][1] 
        if l > maxlength_Y : 
            Y_axis_cordinate = h
            maxlength_Y = l  
    # print(" Length of Y Axis  : " + str(maxlength_Y))
    
     # identify y axis considering line length and text
    for h in range(0, noOfLines):
        len = Y_arr[h][1]
        x = arr[h][1]
        if (len == maxlength_Y) or (len >= maxlength_Y - (maxlength_Y * 0.1)):
            if ( (x_coordinate <= x + 15) and ( x_coordinate >= x-15)):     
                Y_axis_cordinate = h
                found_Y = True
                return found_Y
    return found_Y        

def indentify_X_Axis_UsingValues():
    global Y_axis_cordinate, X_axis_cordinate, found_X, maxlength_X, numberOfDigitValue

    count_Y =  [[0] * 2 for i in range(numberOfCharactor)]  # List  to store charactor Y coordinate and frequency of that value  
    max_Count_Y = y_coordinate = 0 

    # store charactor Y coordinate and frequency of that value 
    for i in range(0, numberOfDigitValue):
        y_val = textCoordinate[i][2]
        count = 0
        if y_val != 0 :
            for h in range(0 , numberOfDigitValue):
                val = textCoordinate[h][2]
                if ((val <= y_val+5 ) and (val >= y_val-5)):
                    count = count + 1
        count_Y[i][0] = y_val
        count_Y[i][1] = count

    # print charactor Y coordinate and frequency of that value
    # for i in range(0, numberOfCharactor ):
    #     print("      " + str(  count_Y[i][0] ) + "_--------------------  " + str(count_Y[i][1]))
    
    # get the maximum frequency of the y coordinate
    for i in range(0, numberOfCharactor): 
        c = count_Y[i][1]
        if (c > max_Count_Y):
            max_Count_Y = c
            y_coordinate = count_Y[i][0]
    # print(" Y coordinate --------------------"+str(y_coordinate))

    # get the horizontal line which has maximum length
    for h in range(0, noOfLines):
        l = X_arr[h][1] 
        if l > maxlength_X : 
            X_axis_cordinate = h
            maxlength_X = l  
    # print(" Length of X Axis  : " + str(maxlength_X))

    # identify x axis considering line length and text
    if numberOfDigitValue > 0:
        for h in range(0, noOfLines):
            len = X_arr[h][1]
            y = arr[h][1]
            if (len == maxlength_X) or (len >= maxlength_X - (maxlength_X * 0.1)):
                if ( (y_coordinate <= y + 15) and ( y_coordinate >= y-15)):     
                    X_axis_cordinate = h 
                    found_X = True
                    return found_X 
    return found_X 

def main(argv):
    
    global cdstP, cdstP2, allLines, linesP, arr, X_arr, Y_arr, graphs_arr, noOfLines, origin_X, origin_Y, height, width, filename, src

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
    # print("Image width : " + str(width))
    # print("Image height : " + str(height))
    
    # Edge detection
    #dst = cv.Canny(src, 20, 200, None, 3) 
    dst = cv.Canny(resized, 20, 200, None, 3) 

    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    allLines = np.copy(cdst)  
    cdstP2 = np.copy(cdst)
    
    # Get Text
    global result
    result = pytesseract.image_to_string(Image.open(cv.samples.findFile(filename)))
    print(" Result : " + str(result))

    if result: 
        # Generate Eqation Using Given Coodinates
        getEqationByUsingCoordinate() 

        # store value cordinate
        getTextCoordinate()
        # if result != "":

    else:
        print("Text cannot Read")
     
    # Probabilistic Line Transform
    # linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 0, 10) 
    # linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 4, 15) 
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 0, 15) 
    noOfLines = len(linesP) 
    
    if linesP is not None: # Check there are lines

        # store value cordinate
        if result != "":
            getTextCoordinate()

        # Draw the lines
        displayAlllines()

        # add mofology
        addMofologyToImage()

        # Store Lines Coordinate
        storeLineCoordinate()
            
        # Separate X axis Y axis and Graphs
        separateX_Y_Graph()

        # Check graph is quadratic or Linear
        checkGraph()

        # x axis
        check_X = indentify_X_Axis_UsingValues()
        print(" Have we fond x axis using text : " + str(check_X))
        # Identify X Axis Considering lenth If X Axis not found using text
        if(check_X != True): 
            draw_X_Axis()
        # draw X axis 
        cv.line(cdstP, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
        print ("X  axis -------------->("+str(arr[X_axis_cordinate][0])+","+str(arr[X_axis_cordinate][1])+")       ("+str(arr[X_axis_cordinate][2])+","+str(arr[X_axis_cordinate][3])+")")
        
        # y axis
        check_Y = indentify_Y_UsingValues()
        print(" Have we fond Y axis using text : " + str(check_Y))
        if(check_Y != True): 
            draw_Y_Axis()
        cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
        print ("Y  axis -------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")

        # Graph
        draw_Graph() 

        # identify origin
        origin()

        # identify X axis Ticmarks
        if (pixcelForTicMark_X == 0 ):
            identifyTicMarks_X_Axis() 

        # identify Y axis Ticmarks
        if (pixcelForTicMark_Y == 0):
            identifyTicMarks_Y_Axis() 
        
        # draw tic mark of Y axis
        draw_TicMark_Y_Axis()

        # draw tic mark of X axis
        draw_TicMark_X_Axis()

        if graphType == "Quadratic": 
            getQuadraticGraphCoodinates()

        # identify X and Y axis intersection point
        identifyIntersection()
         
        # identifyNumbersRelated_X_Y_Axis()
        
        # get real coordinates of y axis and X intersection point without OCR
        if ( pixcelForTicMark_Y !=0 and pixcelForTicMark_X != 0) :
            getRealCoordianatesWithoutOCR()

        # generate equation using Image processing without OCR
        equationIP()

    # cv.imshow("Resized image", resized) 
    # cv.imshow("Source", src) 
    cv.imshow("Probabilistic Line Transform", cdstP) 
    cv.imshow("Min Max", cdstP2) 
    cv.imshow("Detected All Lines" , allLines )
    cv.waitKey()
    return 0  

if __name__ == "__main__":
    main(sys.argv[1:]) 