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
from math import modf
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
cdstP = cdstP2 = allLines = textCoordinate = cdstP_Linear = MofologyImg_2 = None
noOfLines = numberOfCharactor = 0
width = height = 0
origin_X = origin_Y = intersection_Xaxis_X = intersection_Xaxis_Y = intersection_Yaxis_X = intersection_Yaxis_Y = numberOfDigitValue = 0
real_intersection_Xaxis_X = real_intersection_Yaxis_Y = 0
pixcelForTicMark_Y = pixcelForTicMark_X = 0
N = 4 # arr (x,y) (x,y) 
numberOf_Xaxis = numberOf_Yaxis = None # 0 - number 1 - coordinate
graphCrossOrigin = False
ratio_Y_Axis_Value = ratio_X_Axis_Value = 1
found_X = found_Y = passfromTem_Y = passfromTem_X = False
src = src2 = MofologyImg = graphType = srcTemplate = temSrc = cdstP_X_Y = resized_img = None
tem_y_arr =  tem_x_arr =  tem_Matching_Coordinates  = None
xIndex = yIndex = 0 # for Identify X, Y using template maching 
numberOf_Yaxis =  numberOf_Xaxis  = xy_arr =  None

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
    # else:
    #     # getTextCoordinate()
    #     print("coodinates does not read properly")

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
    if numberOf_Graph >= 1 : # check number of lines which are not horizontal or vertical
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
            print(" This is a Quadratic Graph")
        else:
            graphType = "linear"
            print(" This is a linear Graph")
    else:
        graphType = "linear"
        print(" This is a linear Graph which is Parallel to X or Y Axis ")   
        return

def getQuadraticGraphCoodinates():
    global graphType, cdstP2, MofologyImg
    lengthNegative = lengthPositive = negativeIndex = positiveIndex = 0  
    quadraticType = None
    pm = pc = nm = nc = px = nx = pny = 0 # pm - positive line gtadiant / pc - c of positive line / 
    qa = qb = qc = 0
    minMaxY = sx = 0
    hasRealRoots = False  
    solveUsingRealRoots = False

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

    # Draw the 2 linear lines of Quadratic Graphs 
    cv.line(cdstP, (arr[negativeIndex][0], arr[negativeIndex][1]), (arr[negativeIndex][2], arr[negativeIndex][3]), (5,0,255), 2, cv.LINE_AA)
    cv.line(cdstP, (arr[positiveIndex][0], arr[positiveIndex][1]), (arr[positiveIndex][2], arr[positiveIndex][3]), (128, 0, 128), 2, cv.LINE_AA)
    
    # get x coodinates of line which has positive gradiant (get the min x coordinate)
    positiveXcoodinate = 0
    if ((arr[positiveIndex][0]) < (arr[positiveIndex][2])):
        positiveXcoodinate = arr[positiveIndex][0]
    else:
        positiveXcoodinate = arr[positiveIndex][2]
    
    # get x coodinates of line which has negative gradiant (get the min x coordinate)
    negativeXcoodinate = 0
    if ((arr[negativeIndex][0]) < (arr[negativeIndex][2])):
        negativeXcoodinate = arr[negativeIndex][0]
    else:
        negativeXcoodinate = arr[negativeIndex][2]
    
    # check quadratic graph hax max or min value
    if (positiveXcoodinate < negativeXcoodinate):
        quadraticType = "min"
        print(" This Quadratic Graph has Minimum Value")
    else:
        quadraticType = "max"
        print(" This Quadratic Graph has Maximum Value")

    # take the Y value for both positive and negative lines of quadratic graph
    py = ny = y = 0
    if quadraticType == "min": 
        # print("Min-----------------------------")
        if (arr[positiveIndex][1] < arr[positiveIndex][3]): # get the min Y coordinate of positive line
            py = arr[positiveIndex][1]
        else :
            py = arr[positiveIndex][3]

        if (arr[negativeIndex][1] < arr[negativeIndex][3]): # get the min Y coordinate of negative line
            ny = arr[negativeIndex][1]
        else :
            ny = arr[negativeIndex][3]

        if(ny > py): #  get the max Y coordinate out of two
            y = ny
        else:
            y = py 

    elif quadraticType == "max": 
        # print("Max----------------------------")
        # py = ny = y = 0
        if (arr[positiveIndex][1] < arr[positiveIndex][3]): # get the max Y coordinate of positive line
            py = arr[positiveIndex][3]
        else :
            py = arr[positiveIndex][1]

        if (arr[negativeIndex][1] < arr[negativeIndex][3]): # get the max Y coordinate of negative line
            ny = arr[negativeIndex][3]
        else :
            ny = arr[negativeIndex][1]

        if(ny > py): # get the min Y coordinate 
            y = py
        else:
            y = ny


    # get X coodinate of graphs and get the x coodinate of symmetric line
    if pm != 0:
        px = int(round((y - pc )/pm))
    if nm != 0:   
        nx = int(round((y - nc )/nm))
    sx = int(round((px+nx))/2)
    pny = y

    # draw positive line point
    for i in range (px-5, px+5):
        for j in range(pny - 5,pny +5 ):
            if(i > 0 and i < width and j > 0 and j < height ): 
                # if(i<width and j< height):
                cdstP2[j,i] = (0, 255, 0)
                cdstP[j,i] = (0, 255, 0) 

    # draw negative line point
    for i in range (nx-5, nx+5):
        for j in range(pny - 5,pny +5 ):
            if(i > 0 and i < width and j > 0 and j < height ): 
                # if(i<width and j< height):
                cdstP2[j,i] = (0, 255, 0)
                cdstP[j,i] = (0, 255, 0) 


    # draw lines (Samamithika akshaya)
    for i in range(0, width):
        cdstP2[y,i] = (50, 55, 255)
        cdstP[y,i] = (50, 55, 255) 
    for i in range(0, height): 
        cdstP2[i,sx] = (50, 55, 255)
        cdstP[i,sx] = (50, 55, 255)
        MofologyImg_2[i,sx] = (50, 55, 255)
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

    xYCoodinareOfQuadraticGraph = [[0] * 2 for i in range(100)] # 0- X coodinate 1- Y coodinate
    # create array to store y coodinates of quadratic graph
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
        # print (" Total Y " + str(total_Y ) + " Count " + str(count)+ "******** ")
        if (count != 0 and total_Y != 0 and (max - min) < 10 and (indexY >= 0 and indexY < height)):
            # print (" Total Y " + str(total_Y ) + " Count " + str(count))
            yCordinatesOfQuadraticGraph[indexY] = int(round(total_Y/count))
            indexY = indexY + 1
            cdstP2[y,x] = (255, 0, 0)
            # print (" Y coodinate  " + str(int(round(total_Y/count))) + " ******" +" indexY " + str(indexY))
       
    yCordinates_and_Counts = [[0] * 2 for i in range(len(yCordinatesOfQuadraticGraph))] 
    yCordinates_and_Counts_Index = 0

    for i in range(0, len(yCordinatesOfQuadraticGraph) ):
        y = yCordinatesOfQuadraticGraph[i]
        count = 0
        if y != 0:
            for j in range(0, len(yCordinatesOfQuadraticGraph) ):
                current_y = yCordinatesOfQuadraticGraph[j]
                if current_y != 0:
                    if ((current_y >= (y - 20)) and (current_y <= (y + 20))):
                        count = count + 1
            yCordinates_and_Counts[yCordinates_and_Counts_Index][0] = y
            yCordinates_and_Counts[yCordinates_and_Counts_Index][1] = count
            yCordinates_and_Counts_Index = yCordinates_and_Counts_Index + 1
    
    yCordinatesOfQuadraticGraph_New = np.arange(height)

    for i in range(0, len(yCordinatesOfQuadraticGraph_New)):
        yCordinatesOfQuadraticGraph_New[i] = 0

    max_count = 0
    min_count = 100
    for i in range(0, yCordinates_and_Counts_Index):
        if yCordinates_and_Counts[i][1] != 0 and yCordinates_and_Counts[i][0] != 0:
            c_count = yCordinates_and_Counts[i][1]
            # print("y coordinate   " + str(yCordinates_and_Counts[i][0]) + " count " + str(yCordinates_and_Counts[i][1]) )
            if c_count > max_count:
                max_count = c_count
            if min_count > c_count:
                min_count = c_count
    #### print("y coordinate _ max_count " + str(max_count))
    #### print("y coordinate _ min_count " + str(min_count))

    avg_count = round((max_count-min_count)/2)
    yCordinatesOfQuadraticGraph_New_Index = 0
    for i in range(0, yCordinates_and_Counts_Index):
        if yCordinates_and_Counts[i][1] != 0 and yCordinates_and_Counts[i][0] != 0 and yCordinates_and_Counts[i][1] > avg_count :
            yCordinatesOfQuadraticGraph_New[yCordinatesOfQuadraticGraph_New_Index] = yCordinates_and_Counts[i][0]
            yCordinatesOfQuadraticGraph_New_Index = yCordinatesOfQuadraticGraph_New_Index + 1

    # print the Y coodinate of graph
    # for i in range(0, len(yCordinatesOfQuadraticGraph_New) ):
    #     y = yCordinatesOfQuadraticGraph_New[i]
    #     if (y != 0):
    #         print("y coordinate   " + str(y) )

    # find the max of the Y coodinate of graph
    maxY = yCordinatesOfQuadraticGraph_New[0]
    for i in range(0, len(yCordinatesOfQuadraticGraph_New)):
        y = yCordinatesOfQuadraticGraph_New[i]
        if ( y > maxY):
            maxY = y

    # find the min of the Y coodinate of graph
    minY = maxY
    for i in range(0, len(yCordinatesOfQuadraticGraph_New)):
        y = yCordinatesOfQuadraticGraph_New[i]
        if ( y < minY and y != 0):
            minY = y

    # if graph is max one take the min y coodinate and graph is min one take the max y coodinate   
    if quadraticType == "max": 
        minMaxY = minY
    elif quadraticType == "min":
        minMaxY = maxY

    # # print the Y coodinate of graph
    # for i in range(0, len(yCordinatesOfQuadraticGraph) ):
    #     y = yCordinatesOfQuadraticGraph[i]
    #     if (y != 0):
    #         print("y coordinate   " + str(y) )

        
    # # sort array
    # array_sort =  np.sort(yCordinatesOfQuadraticGraph) 
    
    # # find the max of the Y coodinate of graph
    # maxY = yCordinatesOfQuadraticGraph[0]
    # for i in range(0, len(yCordinatesOfQuadraticGraph)):
    #     y = yCordinatesOfQuadraticGraph[i]
    #     if ( y > maxY):
    #         maxY = y
    
    # # find the min of the Y coodinate of graph
    # minY = maxY
    # for i in range(0, len(yCordinatesOfQuadraticGraph)):
    #     y = yCordinatesOfQuadraticGraph[i]
    #     if ( y < minY and y != 0):
    #         minY = y

    # # if graph is max one take the min y coodinate and graph is min one take the max y coodinate   
    # if quadraticType == "max": 
    #     minMaxY = minY
    # elif quadraticType == "min":
    #     minMaxY = maxY
 
    # draw min or max point
    for i in range(sx - 5 , sx + 5):
        for j in range(minMaxY - 5, minMaxY +5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                cdstP2[j,i] = (255, 0, 0)
                cdstP2[j,i] = (255, 0, 0)
                MofologyImg_2[j,i] = (255, 255, 0)
    
    if ((quadraticType == "min") and (minMaxY > origin_Y)) or ((quadraticType == "max") and (minMaxY < origin_Y)) :
        hasRealRoots = True

    py = pny
    ny = pny + 1
    qa_before = (1/(sx - nx)) * (((py - minMaxY)/(px - sx)) - ((ny - py)/(nx - px)))
    qa = (1/(sx - nx)) * (((minMaxY - py)/(sx - px)) - ((py - ny )/(px - nx)))
    # qb_before = (1/(nx - sx)) * ((((pny - minMaxY)*(px + nx ))/(nx - sx)) - (((1)*(px + sx ))/(nx - px)))
    qb_before = ((py - minMaxY)/(px - sx)) - (qa_before*(px + sx))
    qb = ((minMaxY - py)/(sx-px)) - (qa * (sx+px))
    qc_before = ((nx/(sx - nx))*(((minMaxY*px)-(pny*sx))/(sx - px))) - ((sx/(sx - nx))*(((pny*nx)-(pny*px))/(px - nx)))
    qc = minMaxY - (qa*pow(sx,2)) - (qb*sx)

    if ( hasRealRoots == True):
        print(" Have Real Roots ----------------->>>>>")
        solveUsingRealRoots = True
        b24ac = pow(qb, 2) - (4*qa*(qc - origin_Y))
        x1 = ((-1*qb) + pow(b24ac, 0.5))/(2*qa)
        x2 = ((-1*qb) - pow(b24ac, 0.5))/(2*qa)
        x4 = int(np.nan_to_num(x2))
        x3 = int(np.nan_to_num(x1))
        # draw root
        for i in range(x3 - 5 , x3 + 5):
            for j in range(origin_Y - 5, origin_Y +5):
                if(i > 0 and i < width and j > 0 and j < height ): 
                    cdstP2[j,i] = (255, 0, 0)
                    cdstP2[j,i] = (255, 0, 0)
                    MofologyImg_2[j,i] = (255, 0, 0)
        # draw root
        for i in range(x4 - 5 , x4 + 5):
            for j in range(origin_Y - 5, origin_Y +5):
                if(i > 0 and i < width and j > 0 and j < height ): 
                    cdstP2[j,i] = (255, 0, 0)
                    cdstP2[j,i] = (255, 0, 0)
                    MofologyImg_2[j,i] = (255, 0, 0)
        
        root_1 = x3
        root_2 = x4 
        real_val_1 = real_val_2 = 0 

        # take number in floting point
        real_val_1_float = -1*((origin_X-root_1)/ pixcelForTicMark_X)
        real_val_2_float = -1*((origin_X-root_2)/ pixcelForTicMark_X)
        # print(" Real value floating points ----> " + str(real_val_1_float))
        # print(" Real value floating points ----> " + str(real_val_2_float))

        # round the floating point number in to one decimal point
        real_val_1_D1 = round(real_val_1_float,1)
        real_val_2_D1 = round(real_val_2_float,1)
        # print(" Real value in one Decimal point ----> " + str(real_val_1_D1))
        # print(" Real value in one decimal point ----> " + str(real_val_2_D1))
        
        # Separate the Integer Part and Floating part
        a = modf(real_val_1_D1)
        d1 = round(a[0],1)
        # print(" ----> " + str(a[0])) # floating part
        # print(" ----> " + str(a[1])) # integer part
        b = modf(real_val_2_D1)
        d2 = round(b[0],1)
        
        # print(" ----> " + str(b[0])) # floating part
        # print(" ----> " + str(b[1])) # integer part
        # print(" Decimal Point 1 ----> " + str(a[0]))
        # print(" Decimal Point 2 ----> " + str(b[0]))

        if (d1 < 0) :
            d1 = (-1)*d1
            # print(" Decimal Point 1 ----> " + str(d1))
        if (d2 < 0) :
            d2 = (-1)*d2
            # print(" Decimal Point 2 ----> " + str(d2))
        
        if ( (d1 <= 0.25  or d1>=0.75) and (d2 <= 0.25  or d2>=0.75)):   
            real_val_1 = int(round(-1*((origin_X-root_1)/ pixcelForTicMark_X)))
            real_val_2 = int(round(-1*((origin_X-root_2)/ pixcelForTicMark_X)))



            # needed........................


            # if ((quadraticType == "min") and ((real_val_1 != 0) or (real_val_1 != 0))):
            #     # print("Graph Equation --- > " + " ( X - " + str(real_val_1) + ") ( X - " + str(real_val_2) + ")")
            #     print("Graph Equation consider Real Roots --- > " + " ( X - " + str(real_val_1) + ") ( X - " + str(real_val_2) + ")")
            # elif ((quadraticType == "max") and ((real_val_1 != 0) or (real_val_1 != 0))):
            #     print("Graph Equation consider Real Roots --- > " + " - ( X - " + str(real_val_1) + ") ( X - " + str(real_val_2) + ")")
        
        
        
        
        else:
            if ( pixcelForTicMark_X != 0):
                real_sx = int(round((sx-origin_X)/pixcelForTicMark_X))
                rsx = real_sx
                lsx = real_sx - 1
                # print(" Real Sx ------>  " + str(real_sx))
            solveUsingRealRoots = False 
          
    else : 
        print(" This Quadratic Graph Does not have real Roots ")

    # if (solveUsingRealRoots == False) :
    real_sx = int(round((sx-origin_X)/pixcelForTicMark_X))
    rsx = real_sx
    lsx = real_sx - 1
    X_Y_Coordinate = [[0] * 2 for i in range(10)] # 0- X coordinate / 1 - Y Coordinate
    X_Y_Coordinate_n = [[0] * 2 for i in range(10)] # 0- X coordinate / 1 - Y Coordinate
    count = count_2 = totalCount =  0
        # print(" Real Sx ------>  " + str(real_sx))
        # color tic mark right hand side of thesamamiyjika axis
    for k in range(0, 25):
        rsx_coordinate = origin_X + (pixcelForTicMark_X*(rsx+k))
        lsx_coordinate = origin_X + (pixcelForTicMark_X*(lsx-k))

        rsy_coordinate = int(round(((qa*(pow(rsx_coordinate,2))) + (qb*rsx_coordinate) + qc)))
        lsy_coordinate = int(round(((qa*(pow(lsx_coordinate,2))) + (qb*lsx_coordinate) + qc)))
            
            
        rsy = ((origin_Y-rsy_coordinate)/pixcelForTicMark_Y)
        rsy_D1 = round(rsy,1)
        c = modf(rsy_D1)
        d3 = round(c[0],1)
        if (d3 < 0) :
            d3 = (-1)*d3
            # print(" D_33333333333 ----> " + str(d3)) 
        if (d3 <= 0.2  or d3>=0.8) :
            ry = int(round(rsy_D1))
            if (count < 10):
                X_Y_Coordinate[count][0] = rsx+k
                X_Y_Coordinate[count][1] = ry
                count = count + 1
                totalCount = totalCount + 1



        lsx_coordinate= origin_X + (pixcelForTicMark_X*(lsx-k))
        lsy_coordinate = int(round(((qa*(pow(lsx_coordinate,2))) + (qb*lsx_coordinate) + qc)))
        lsy = ((origin_Y-lsy_coordinate)/pixcelForTicMark_Y)
        lsy_D1 = round(lsy,1)
        d = modf(lsy_D1)
        d4 = round(d[0],1)
        if (d4 < 0) :
            d4 = (-1)*d4
            # print(" D_33333333333 ----> " + str(d4))
        if (d4 <= 0.2  or d4>=0.8) :
            ly = int(round(lsy_D1)) 
            if (count_2 < 10):
                X_Y_Coordinate_n[count_2][0] = lsx-k
                X_Y_Coordinate_n[count_2][1] = ly
                count_2 = count_2 + 1
                totalCount = totalCount + 1 
             
        # draw
        for i in range(lsx_coordinate - 5 , lsx_coordinate + 5):
            for j in range(lsy_coordinate - 5, lsy_coordinate +5):
                if(i > 0 and i < width and j > 0 and j < height ): 
                    cdstP2[j,i] = (0, 0, 255)  
        for i in range(rsx_coordinate - 5 , rsx_coordinate + 5):
            for j in range(rsy_coordinate - 5, rsy_coordinate +5):
                if(i > 0 and i < width and j > 0 and j < height ): 
                    cdstP2[j,i] = (255, 255, 150)
 
    if totalCount < 3:
        for k in range(0, 50):
            rsx_coordinate = origin_X + (pixcelForTicMark_X*(rsx+k))
            lsx_coordinate = origin_X + (pixcelForTicMark_X*(lsx-k))

            rsy_coordinate = int(round(((qa*(pow(rsx_coordinate,2))) + (qb*rsx_coordinate) + qc)))
            lsy_coordinate = int(round(((qa*(pow(lsx_coordinate,2))) + (qb*lsx_coordinate) + qc)))
            
            
            rsy = ((origin_Y-rsy_coordinate)/pixcelForTicMark_Y)
            rsy_D1 = round(rsy,1)
            c = modf(rsy_D1)
            d3 = round(c[0],1)
            if (d3 < 0) :
                d3 = (-1)*d3
                # print(" D_33333333333 ----> " + str(d3)) 
            if (d3 <= 0.3  or d3>=0.7) :
                ry = int(round(rsy_D1))
                if (count < 10):
                    X_Y_Coordinate[count][0] = rsx+k
                    X_Y_Coordinate[count][1] = ry
                    count = count + 1
                    totalCount = totalCount + 1

    if totalCount > 3:
        if count_2 > 0 and count > 2:
            x1 = X_Y_Coordinate[0][0] * ratio_X_Axis_Value
            y1 = X_Y_Coordinate[0][1] * ratio_Y_Axis_Value
            x2 = X_Y_Coordinate[1][0] * ratio_X_Axis_Value
            y2 = X_Y_Coordinate[1][1] * ratio_Y_Axis_Value
            x3 = X_Y_Coordinate_n[0][0] * ratio_X_Axis_Value
            y3 = X_Y_Coordinate_n[0][1] * ratio_Y_Axis_Value
        if count_2 == 1 and count > 2:
            x1 = X_Y_Coordinate[0][0] * ratio_X_Axis_Value
            y1 = X_Y_Coordinate[0][1] * ratio_Y_Axis_Value
            x2 = X_Y_Coordinate[1][0] * ratio_X_Axis_Value
            y2 = X_Y_Coordinate[1][1] * ratio_Y_Axis_Value
            x3 = X_Y_Coordinate[2][0] * ratio_X_Axis_Value
            y3 = X_Y_Coordinate[2][1] * ratio_Y_Axis_Value

        print(" 1. Point on Graph ---> (" + str(x1) + " , " + str(y1) +")")
        print(" 2. Point on Graph ---> (" + str(x2) + " , " + str(y2) +")")
        print(" 3. Point on Graph ---> (" + str(x3) + " , " + str(y3) +")")

        a = (1/(x1 - x3)) * (((y1 - y2)/(x1 - x2)) - ((y2 - y3 )/(x2 - x3)))
        b = ((y1 - y2)/(x1-x2)) - (a * (x1+x2))
        c = y1 - (a*pow(x1,2)) - (b*x1)
            
        a1 = round((1/(x1 - x3)) * (((y1 - y2)/(x1 - x2)) - ((y2 - y3 )/(x2 - x3))), 1)
        a1_O = modf(a1)
        d_a1 = round(a1_O[0],1)
        if (d_a1 < 0) :
            d_a1 = (-1)*d_a1
            # print ("=============================== a " + str(d_a1)) 
        if (d_a1 <= 0.25  or d_a1>= 0.75) :
            a1 = int(round(a1))

        b1 = round(((y1 - y2)/(x1-x2)) - (a * (x1+x2)),1)
        b1_O = modf(b1)
        d_b1 = round(b1_O[0],1)
        if (d_b1 < 0) :
            d_b1 = (-1)*d_b1 
        # print ("===============================  b " + str(d_b1)) 
        if (d_b1 <= 0.25  or d_b1>=0.75) :
            b1 = int(round(b1))

        c1 = round(y1 - (a*pow(x1,2)) - (b*x1),1)
        c1_O = modf(c1)
        d_c1 = round(c1_O[0],1)
        if (d_c1 < 0) :
            d_c1 = (-1)*d_c1 
        if (d_c1 <= 0.25  or d_c1>=0.75) :
            c1 = int(round(c1))
            
        print(" a ----------->" + str(a1))
        print(" b ----------->" + str(b1))
        print(" c ----------->" + str(c1))
        print(" Equation --->  Y = " +str(a1)+"X^2  + "+str(b1)+"X + " +str(c1))

 
        # color tic mark left hand side of thesamamiyjika axis
        # for k in range(0, 20):
        #     lsx_coordinate = origin_X + (pixcelForTicMark_X*(lsx-k))
        #     for i in range(lsx_coordinate - 5 , lsx_coordinate + 5):
        #         for j in range(origin_Y - 5, origin_Y +5):
        #             if(i > 0 and i < width and j > 0 and j < height ): 
        #                 cdstP2[j,i] = (0, 0, 255)    


         


def draw_X_Axis():
    global maxlength_X
    global X_axis_cordinate
    global origin_Y, allLines, passfromTem_X
    
    maxlength_X = 0
    # get the maxmum lenth horizontal line
    for h in range(0, len(linesP)):
        l = X_arr[h][1] 
        if l > maxlength_X : 
            X_axis_cordinate = h
            maxlength_X = l  
    # print(" Length of X Axis  : " + str(maxlength_X))

    sameLine = 0
    for h in range(0, len(linesP)):
        l = X_arr[h][1] 
        if l == maxlength_X or  l >= maxlength_X*0.9: 
            sameLine = sameLine + 1

    if sameLine == 0: 
        for h in range(0, len(linesP)):
            l = X_arr[h][1] 
            if l == maxlength_X  or l >= maxlength_X*0.8: 
                sameLine = sameLine + 1 

    if (sameLine > 1): 
        if passfromTem_X != True:
            passfromTem_X = False
            find_X_Axis() 
    else :
        found_X = True
        return
 

def addMofologyToImage():
    global MofologyImg, MofologyImg_2
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
    MofologyImg_2 = cv.cvtColor(test2, cv.COLOR_GRAY2BGR)

     

def find_X_Axis():
    global maxlength_X
    global X_axis_cordinate
    global pixcelForTicMark_X 
 
    half_pixcelForTicMark_Y = 10
    minLen_X_Axis = maxlength_X
    min_X_axis_cordinate = 0
    min_X_axis_array = [[0] * 2 for i in range(20)] 
    min_X_axis_array_Index = 0
    min_XAxis_Ycordinate = 0

    if (pixcelForTicMark_X == 0):
        identifyTicMarks_X_Axis()

    # Identify Shorted horizontal Line
    for h in range(0, len(linesP)):
        l = X_arr[h][1]  
        if ((l < minLen_X_Axis) and (l != 0)) : 
            min_X_axis_cordinate = h
            minLen_X_Axis = X_arr[h][1]   
            min_XAxis_Ycordinate = X_arr[h][0]
    cv.line(cdstP, (arr[min_X_axis_cordinate][0], arr[min_X_axis_cordinate][1]), (arr[min_X_axis_cordinate][2], arr[min_X_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA) 
    
    
    # get Minimum lines y coordinates
    for h in range(0, len(linesP)):
        l = X_arr[h][1] 
        y =  X_arr[h][0] 
        if (l != 0) and (l <= (minLen_X_Axis + (pixcelForTicMark_X*2))):  
            if min_X_axis_array_Index < 20:
                min_X_axis_array[min_X_axis_array_Index][0] = y
                min_X_axis_array[min_X_axis_array_Index][1] = 0
                min_X_axis_array_Index = min_X_axis_array_Index + 1 

    # get the count of their values
    for i in range(0, 20 ):
        y1 = min_X_axis_array[i][0] 
        count = 0
        if y1 != 0:
            for j in range(0, 20 ):
                y2 = min_X_axis_array[j][0] 
                if y1 <= y2 + (pixcelForTicMark_Y/4) and y1 >= y2 - (pixcelForTicMark_Y/4):
                    count = count + 1
            min_X_axis_array[i][1] = count

    # get max count and get their y coordinate
    maxCount = 0
    for i in range(0, 20 ):
        count  = min_X_axis_array[i][1] 
        # print(" Y coordinate : " + str(min_X_axis_array[i][0] ) + " count " + str(count))
        if count != 0:
            if count > maxCount:
                maxCount = count
                min_XAxis_Ycordinate = min_X_axis_array[i][0] 
    
    
  

    if ( maxCount == 1):
        if passfromTem_X == True:
            draw_X_Axis()
        else:
            min_XAxis_Ycordinate = arr[min_X_axis_cordinate][1]
    # print(" Max Count " + str(maxCount))

    # min_XAxis_Ycordinate = arr[min_X_axis_cordinate][1] 
    # cv.line(cdstP, (arr[min_X_axis_cordinate][0], arr[min_X_axis_cordinate][1]), (arr[min_X_axis_cordinate][2], arr[min_X_axis_cordinate][3]), (255,0,0), 2, cv.LINE_AA)
    
    # print(" Identify x using Shortest line  =  " +str(min_X_axis_cordinate))

    # for h in range(0, len(linesP)):
    #     if (X_arr[h][1] <= (minLen_X_Axis +5) and  (X_arr[h][0] <= (min_XAxis_Ycordinate+3)) and (X_arr[h][0] >= (min_XAxis_Ycordinate-3))) : 
    #         min_XAxis_Ycordinate = (X_arr[h][0] + min_XAxis_Ycordinate)/2 
  
    if(pixcelForTicMark_Y != 0):
        half_pixcelForTicMark_Y = pixcelForTicMark_Y/2 
     
    
    # identify all the legthly lane which are near
    count = 0
    found = False
    for h in range(0, len(linesP)):
        X_axis_Y_cordinate = arr[h][1]
        length_Of_X_Axis = X_arr[h][1]   
        if ((X_axis_Y_cordinate <= (min_XAxis_Ycordinate + half_pixcelForTicMark_Y)) and (X_axis_Y_cordinate >= (min_XAxis_Ycordinate-half_pixcelForTicMark_Y))) :      
          
            if ((length_Of_X_Axis == maxlength_X) or (length_Of_X_Axis > (maxlength_X - (maxlength_X*0.4)))) : 
             
                found = True
                count = count + 1
                X_axis_cordinate = h 
    
    if found == False:
        for h in range(0, len(linesP)):
            X_axis_Y_cordinate = arr[h][1]
            length_Of_X_Axis = X_arr[h][1]   
            if ((X_axis_Y_cordinate <= (min_XAxis_Ycordinate + pixcelForTicMark_Y)) and (X_axis_Y_cordinate >= (min_XAxis_Ycordinate-pixcelForTicMark_Y))) :      
                if ((length_Of_X_Axis == maxlength_X) or (length_Of_X_Axis > (maxlength_X-(maxlength_X*0.4)))) : 
                    found = True
                    count = count + 1
                    X_axis_cordinate = h 

    if (count > 1):
        for h in range(0, len(linesP)):
            X_axis_Y_cordinate = arr[h][1]
            length_Of_X_Axis = X_arr[h][1]   
            if ((X_axis_Y_cordinate <= (min_XAxis_Ycordinate+half_pixcelForTicMark_Y)) and (X_axis_Y_cordinate >= (min_XAxis_Ycordinate-half_pixcelForTicMark_Y))) :   
                if ((length_Of_X_Axis == maxlength_X  or (length_Of_X_Axis > (maxlength_X-(maxlength_X*0.2)))) and (X_axis_Y_cordinate <= (min_XAxis_Ycordinate)) ) :  
                    X_axis_cordinate = h 
                   
def draw_Y_Axis():
    global maxlength_Y
    global origin_X
    global Y_axis_cordinate
    global pixcelForTicMark_Y, found_Y, passfromTem_Y


    maxlength_Y = 0
    # find the maximum length
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l > maxlength_Y : 
            Y_axis_cordinate = h
            maxlength_Y = Y_arr[h][1]   

    sameLine = 0
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if l == maxlength_Y or l >= maxlength_Y*0.9: 
            sameLine = sameLine + 1

    if sameLine == 0:
        for h in range(0, len(linesP)):
            l = Y_arr[h][1] 
            if l == maxlength_Y or l >= maxlength_Y*0.8 : 
                sameLine = sameLine + 1
    print(" Same Lines Y------------------ : " + str(sameLine))
    
    if (sameLine > 1):
        if passfromTem_Y != True:
            passfromTem_Y = False
            find_Y_Axis() 
    else: 
        found_Y = True
        return


def find_Y_Axis():
    global maxlength_Y
    global Y_axis_cordinate
    global pixcelForTicMark_Y 
    global passfromTem_Y
 
    half_pixcelForTicMark_X = 10
    minLen_Y_Axis = maxlength_Y
    min_Y_axis_cordinate = 0
    min_Y_axis_array = [[0] * 2 for i in range(20)] 
    min_Y_axis_array_Index = 0
    min_YAxis_Xcordinate = 0

    if ( pixcelForTicMark_Y == 0):
        identifyTicMarks_Y_Axis()
      

    # identify verical line which has mimum length
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        if ((l < minLen_Y_Axis) and (l != 0)) : 
            min_Y_axis_cordinate = h
            minLen_Y_Axis = Y_arr[h][1] 

    # print ("minLen_Y_Axis " + str(minLen_Y_Axis))
    # get Minimum lines x coordinates
    for h in range(0, len(linesP)):
        l = Y_arr[h][1] 
        x =  Y_arr[h][0] 
        if (l != 0) and (l <= minLen_Y_Axis + (pixcelForTicMark_Y/3)): 
            if min_Y_axis_array_Index < 20:
                min_Y_axis_array[min_Y_axis_array_Index][0] = x
                min_Y_axis_array[min_Y_axis_array_Index][1] = 0
                min_Y_axis_array_Index = min_Y_axis_array_Index + 1 

    # get the count of their values
    for i in range(0, 20 ):
        x1 = min_Y_axis_array[i][0] 
        count = 0
        # print(" X coordinate : " + str(x1))
        if x1 != 0:
            for j in range(0, 20 ):
                x2 = min_Y_axis_array[j][0] 
                if x1 <= x2 + (pixcelForTicMark_X/4) and x1 >= x2 - (pixcelForTicMark_X/4):
                    count = count + 1
            min_Y_axis_array[i][1] = count

    # get max count and get their x coordinate
    maxCount = 0
    for i in range(0, 20 ):
        count  = min_Y_axis_array[i][1] 
        #vprint(" X count : " + str(min_Y_axis_array[i][0]) + " Count "+ str(count))
        if count != 0:
            if count > maxCount:
                maxCount = count
                min_YAxis_Xcordinate = min_Y_axis_array[i][0] 
                
    if ( maxCount == 1):
        if passfromTem_Y == True: 
            draw_Y_Axis()
        else:
            min_YAxis_Xcordinate = arr[min_Y_axis_cordinate][0]
    # min_YAxis_Xcordinate = arr[min_Y_axis_cordinate][0]
    # x =  arr[min_Y_axis_cordinate][0] 

    print("min_Y_axis_X_cordinate " + str(min_YAxis_Xcordinate))

    
   
    # print("max Length Value " + str(maxlength_Y))
    
    if (pixcelForTicMark_X == 0):
        identifyTicMarks_X_Axis()
    
    if(pixcelForTicMark_X != 0):
        half_pixcelForTicMark_X = pixcelForTicMark_X/2 

    cv.line(cdstP, (arr[min_Y_axis_cordinate][0], arr[min_Y_axis_cordinate][1]), (arr[min_Y_axis_cordinate][2], arr[min_Y_axis_cordinate][3]), (0,128,255), 2, cv.LINE_AA) 
    
    # identify verical line which is near to shortest line
    # print (" Count 8888 " + str(maxlength_Y))
    
    count = 0
    found = False
    for h in range(0, len(linesP)):
        Y_axis_X_cordinate = arr[h][0]
        length_Of_Y_Axis = Y_arr[h][1]    
        if ((Y_axis_X_cordinate <= (min_YAxis_Xcordinate + half_pixcelForTicMark_X)) and (Y_axis_X_cordinate >= (min_YAxis_Xcordinate - half_pixcelForTicMark_X)) and (Y_axis_X_cordinate != 0)) :         
            if ((length_Of_Y_Axis == maxlength_Y) or (length_Of_Y_Axis > maxlength_Y - (maxlength_Y * 0.4))):
                found = True
                # print (" Count 8888 " + str(count))
                Y_axis_cordinate = h 
                count = count + 1 

    
    if found == False:
        for h in range(0, len(linesP)):
            Y_axis_X_cordinate = arr[h][0]
            length_Of_Y_Axis = Y_arr[h][1]    
            if ((Y_axis_X_cordinate <= (min_YAxis_Xcordinate + pixcelForTicMark_X)) and (Y_axis_X_cordinate >= (min_YAxis_Xcordinate - pixcelForTicMark_X))) :         
                if ((length_Of_Y_Axis == maxlength_Y) or (length_Of_Y_Axis > maxlength_Y - (maxlength_Y * 0.4))):
                    found = True
                    Y_axis_cordinate = h  
                    count = count + 1
    
    for j in range(0, 100):
        for k in range(min_YAxis_Xcordinate, min_YAxis_Xcordinate + 5):
            cdstP[j,k] = (255, 255, 255)  


    # get the left side line as Y axis
    if (count > 1):
        for h in range(0, len(linesP)):
            Y_axis_X_cordinate = arr[h][0]
            length_Of_Y_Axis = Y_arr[h][1]    
            if ((Y_axis_X_cordinate <= (min_YAxis_Xcordinate + half_pixcelForTicMark_X)) and (Y_axis_X_cordinate >= (min_YAxis_Xcordinate - half_pixcelForTicMark_X))) :  
                if ((length_Of_Y_Axis == maxlength_Y or (length_Of_Y_Axis > maxlength_Y - (maxlength_Y * 0.2))) and (Y_axis_X_cordinate < min_YAxis_Xcordinate )) : 
                    # print (" Count 444   77  " + str(count))
                    Y_axis_cordinate = h  

    cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (0,252,0), 2, cv.LINE_AA)

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
    #### print ("Graph    ------------->("+str(arr[graph_cordinate][0])+","+str(arr[graph_cordinate][1])+")       ("+str(arr[graph_cordinate][2])+","+str(arr[graph_cordinate][3])+")")

def origin():
    global origin_X, origin_Y, MofologyImg_2
    # generate y axis cordinate
    origin_X = Y_arr[Y_axis_cordinate][0]
    # generate x axis cordinate
    origin_Y = X_arr[X_axis_cordinate][0]
    
    # print(" Origin ---------->("+str(origin_X) +","+ str(origin_Y) +")")
    for i in range(origin_X - 5 , origin_X + 5):
        for j in range(origin_Y - 5, origin_Y +5):
            if(i > 0 and i < width and j > 0 and j < height ): 
                allLines[j,i] = (255, 255, 255)
                MofologyImg_2[j,i] = (0, 255, 0)
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
        print(" Linear Grapg Go through Origin")
    
    # elif((intersection_Xaxis_X <= (origin_X + 3)) and (intersection_Xaxis_X >= (origin_X - 3)) and (intersection_Xaxis_Y <= (origin_Y + 3)) and (intersection_Xaxis_Y >= (origin_Y - 3))):
    #     graphCrossOrigin = True
    #     print(" Go through Origin")

    #### print(" Y axis intersection ---------->("+str(intersection_Yaxis_X) +","+ str(intersection_Yaxis_Y) +")")    
    #### print(" X axis intersection ---------->("+str(intersection_Xaxis_X) +","+ str(intersection_Xaxis_Y) +")")

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
    noOfPixcels = np.arange(len(linesP))
    noOfPixcels_Index = 0

    # assign value to zero
    for h in range(0, len(linesP)):
        X_Axis_Intersections[h] = 0
        noOfPixcels[h] = 0

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
        noOfPixcels[h] = 0
        
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
                if ((distance[i] >= d - 5) and (distance[i] <= d + 5) )  : 
                    count = count +1
            count_arr[h][0]  = d
            count_arr[h][1]  = count
    # print(count_arr)
 
    # Check max count
    maxCount = pixcelForTicMark_X_2 = 0
    for h in range(0, len(count_arr) ): 
        c = count_arr[h][1] 
        if (c > maxCount) : 
            maxCount = c   
            noOfPixcels[noOfPixcels_Index] = count_arr[h][0] 
            noOfPixcels_Index = noOfPixcels_Index + 1
            pixcelForTicMark_X_2 = count_arr[h][0] 

    sort_noOfPixcels =  np.sort(noOfPixcels)  
    new_pixcel_array = np.arange(noOfPixcels_Index)
    new_pixcel_array_Index = 0 
    
    for i in range(0, len(sort_noOfPixcels)):
        pixcels = sort_noOfPixcels[i] 
        if pixcels != 0:
            new_pixcel_array[new_pixcel_array_Index] = pixcels
            new_pixcel_array_Index = new_pixcel_array_Index + 1

    if new_pixcel_array_Index > 1:
       index = int(round(new_pixcel_array_Index/2))
       pixcelForTicMark_X = new_pixcel_array[index]
       print(" Tic X  : > 1" )
    elif new_pixcel_array_Index == 1:
       pixcelForTicMark_X = new_pixcel_array[0]
       print(" Tic X  : = 1" )
    else :
       pixcelForTicMark_X = pixcelForTicMark_X_2
       print(" Tic X  " )




    # equalCount = [[0] * 3 for i in range(j)] 
    # index = 0
    # m = 0

    # for h in range(0, len(count_arr) ):
    #     total = 0
    #     c = count_arr[h][1]                 # count
    #     value = count_arr[h][0]             # value
    #     if c == maxCount  or c == (maxCount - 1) :
    #         equalCount[m][0] = value        # value
    #         equalCount[m][1] = c            # count

    #         for k in range(0, len(count_arr) ):
    #             val =  count_arr[k][0]  
    #             #if (val > (value - 10))  and (val < (value + 10)):
    #             if (val > (value - 10))  and (val < (value + 10)):
    #                 total = total + val
    #             # print("Total           ============ "+ str(total))

    #         equalCount[m][2] = total/c  # average value
    #         m = m+1 

    # total_avg = 0
    # for h in range(0, m ):
    #     total_avg = total_avg + equalCount[h][2] 
        
    # if total_avg != 0 :
    #     aveg = total_avg/m
    #     pixcelForTicMark_X = int(round(aveg))
    #     pixcelForTicMark_X = pixcelForTicMark_X_2



def draw_TicMark_X_Axis():
    global origin_X, origin_Y, pixcelForTicMark_X, width, height, MofologyImg_2, cdstP_X_Y
    ticMark = 1
    for ticMark in range(1 , 10):
        for i in range(origin_Y-15 , origin_Y+15) : 
            x1 = origin_X + (pixcelForTicMark_X*ticMark)
            x2 = origin_X - (pixcelForTicMark_X*ticMark)
            if ((i > 0) and (i < height)):
                if((x1 > 0) and (x1 < width)):
                    allLines[i,x1] = (255,252,0)  
                    cdstP[i,x1] = (255,252,0) 
                    MofologyImg_2[i,x1] = (0,255,0) 
                    cdstP_X_Y[i,x1] = (0,255,0)  
                if((x2 > 0) and (x2<width)):
                    allLines[i,x2] = (255,252,0)   
                    cdstP[i,x2] = (255,252,0)
                    MofologyImg_2[i,x2] = (0,255,0) 
                    cdstP_X_Y[i,x2] = (0,255,0)  
    #### print("Pixcels between Tic marks (X axis)  ------------->   : " + str(pixcelForTicMark_X))

def identifyTicMarks_Y_Axis():
    global pixcelForTicMark_Y, height
    # Create Array
    Y_Axis_Intersections = np.arange(len(linesP))
    noOfPixcels = np.arange(len(linesP))
    noOfPixcels_Index = 0

    # assign value to zero
    for h in range(0, len(linesP)):
        Y_Axis_Intersections[h] = 0 
        noOfPixcels[h] = 0

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
        noOfPixcels[h] = 0
        
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
                if ((distance[i] >= d - 5) and (distance[i] <= d + 5) )  : 
                    count = count +1
            count_arr[h][0]  = d
            count_arr[h][1]  = count
    # print(count_arr)
 
    # Check max count
    maxCount = 0
    pixcelForTicMark_Y_2 = 0
    for h in range(0, len(count_arr) ): 
        c = count_arr[h][1] 
        if (c > maxCount) : 
            maxCount = c 
            noOfPixcels[noOfPixcels_Index] = count_arr[h][0] 
            noOfPixcels_Index = noOfPixcels_Index + 1
            pixcelForTicMark_Y_2 = count_arr[h][0] 
        
    sort_noOfPixcels =  np.sort(noOfPixcels)  
    new_pixcel_array = np.arange(noOfPixcels_Index)
    new_pixcel_array_Index = 0 

    for i in range(0, len(sort_noOfPixcels)):
        pixcels = sort_noOfPixcels[i] 
        if pixcels != 0:
            new_pixcel_array[new_pixcel_array_Index] = pixcels
            new_pixcel_array_Index = new_pixcel_array_Index + 1

    if new_pixcel_array_Index > 1:
       index = int(round(new_pixcel_array_Index/2))
       pixcelForTicMark_Y = new_pixcel_array[index]
       print(" Tic Y  : > 1" )
    elif new_pixcel_array_Index == 1:
       pixcelForTicMark_Y = new_pixcel_array[0]
       print(" Tic Y : = 1" )
    else :
       pixcelForTicMark_Y = pixcelForTicMark_Y_2
       print(" Tic Y " )

    # equalCount = [[0] * 3 for i in range(j)] 
    # index = 0
    # m = 0

    # for h in range(0, len(count_arr) ):
    #     total = 0
    #     c = count_arr[h][1]                 # count
    #     value = count_arr[h][0]             # value
    #     if c == maxCount or c == (maxCount - 1):
    #         equalCount[m][0] = value        # value
    #         equalCount[m][1] = c            # count

    #         for k in range(0, len(count_arr) ):
    #             val =  count_arr[k][0]  
    #             #if (val > (value - 10))  and (val < (value + 10)):
    #             if (val > (value - 10))  and (val < (value + 10)):
    #                 total = total + val
    #             # print("Total           ============ "+ str(total))

    #         equalCount[m][2] = total/c  # average value
    #         m = m+1 

    # total_avg = 0
    # for h in range(0, m ):
    #     total_avg = total_avg + equalCount[h][2] 
        
    # if total_avg != 0 :
    #     aveg = total_avg/m
    #     pixcelForTicMark_Y = int(round(aveg)) 
    #     pixcelForTicMark_Y = pixcelForTicMark_Y_2

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
    global pixcelForTicMark_Y, origin_X, origin_Y, width, height, cdstP_X_Y, MofologyImg_2
    ticMark = 1
    for ticMark in range(1 , 10):
        for i in range(origin_X-15 , origin_X+15) : 
            y1 = origin_Y + (pixcelForTicMark_Y*ticMark)
            y2 = origin_Y - (pixcelForTicMark_Y*ticMark)
            if( i > 0 and i < width):
                if((y1 > 0) and (y1<height) and (i > 0) and (i< width)):
                    allLines[y1,i] = (0,252,0)  
                    cdstP[y1,i] = (200,252,0)  
                    MofologyImg_2[y1,i] = (0,255,0) 
                    cdstP_X_Y[y1,i] = (0,255,0)  
                if((y2 > 0) and (y2<height) and (i > 0) and (i< width)):
                    allLines[y2,i] = (0,252,0)  
                    cdstP[y2,i] = (200,252,0) 
                    MofologyImg_2[y2,i] = (0,255,0) 
                    cdstP_X_Y[y2,i] = (0,255,0) 
    #### print("Pixcels between Tic marks (Y axis)  ------------->   : " + str(pixcelForTicMark_Y))


def getRealCoordianatesWithoutOCR():
    global origin_X, origin_Y 
    global intersection_Xaxis_X, intersection_Yaxis_Y
    global real_intersection_Xaxis_X, real_intersection_Yaxis_Y

    # print("Pixcels between Tic marks (Y axis)  : " + str(pixcelForTicMark_Y))
    # print("Pixcels between Tic marks (X axis)  : " + str(pixcelForTicMark_X))

    if((origin_X <= intersection_Xaxis_X + 5) and (origin_X >= intersection_Xaxis_X - 5)): 
        real_intersection_Xaxis_X = 0 
    else:
        if (pixcelForTicMark_X != 0) :
            real_intersection_Xaxis_X = int(round((intersection_Xaxis_X - origin_X)/ pixcelForTicMark_X)) * ratio_X_Axis_Value 
            real_intersection_Xaxis_X_f = round(((intersection_Xaxis_X - origin_X)/ pixcelForTicMark_X) * ratio_X_Axis_Value , 1)
            # print(" real_intersection_Xaxis_X_f "+ str(real_intersection_Xaxis_X_f))
            # print(" intersection_Xaxis_X "+ str(intersection_Xaxis_X))
           #  print("origin_X    " + str(origin_X))
            # print(" pixcelForTicMark_X "+ str(pixcelForTicMark_X))
            # print(" ratio_X_Axis_Value "+ str(ratio_X_Axis_Value))
            # print("check ------------------------")
    # elif (origin_X < intersection_Xaxis_X): 
    #     if (pixcelForTicMark_X != 0) :
    #         real_intersection_Xaxis_X = int(round((intersection_Xaxis_X - origin_X)/ pixcelForTicMark_X)) * ratio_X_Axis_Value 
    # else:
    #     if (pixcelForTicMark_X != 0) : 
    #         real_intersection_Xaxis_X = int(round((origin_X - intersection_Xaxis_X)/ pixcelForTicMark_X)*(-1)) * ratio_X_Axis_Value
    
    if((origin_Y <= intersection_Yaxis_Y + 5) and (origin_Y >= intersection_Yaxis_Y - 5)) :
        real_intersection_Yaxis_Y = 0 
    elif (origin_Y < intersection_Yaxis_Y):  
        if (pixcelForTicMark_Y != 0) :
            real_intersection_Yaxis_Y = int(round((intersection_Yaxis_Y - origin_Y)/ pixcelForTicMark_Y)*(-1)) * ratio_Y_Axis_Value
    else: 
        if (pixcelForTicMark_Y != 0) : 
            real_intersection_Yaxis_Y = int(round((origin_Y - intersection_Yaxis_Y)/ pixcelForTicMark_Y)) * ratio_Y_Axis_Value

    # print(" Real Coordinates of X intersection Point  =  (" + str(real_intersection_Xaxis_X) + ", 0)")
    # print(" Real Coordinates of Y intersection Point  = ( 0 ," + str(real_intersection_Yaxis_Y) + " )")

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
    boxes = pytesseract.image_to_boxes(resized_img) # also include any config options you use
    numberOfCharactor = int(len(boxes.splitlines()))
 
    textCoordinate = [[0] * 4 for i in range(numberOfCharactor)] 
    
    # store values into textCoordinate array
    i = 0  

    for b in boxes.splitlines():
        b = b.split(' ')
        # print("Charactor of  " + b[0] + "  =  "+b[1]+ ","+b[2]+ ","+b[3]+ ","+b[4])  # (x1, y1, X2, y2) 
        if (b[0].isdigit() and (int(b[0]) != 0) ):
            textCoordinate[i][0] = int(b[0]) # store Charactor
            textCoordinate[i][1] = round((int(b[1]) + int(b[3]))/2) # store X Coordinate
            textCoordinate[i][2] = round(((height - int(b[2])) + (height - int(b[4])))/2) # store Y Coordinate
            cv.rectangle(cdstP, ( int(b[1]), int((height - int(b[2])))), (int(b[3]), int((height - int(b[4])))), (255, 255, 0), 2)
            i = i + 1
            numberOfDigitValue = i
     

def identifyNumbersRelated_X_Y_Axis():
    global  ratio_X_Axis_Value, ratio_Y_Axis_Value  
    ratio_Of_XAxis = 1 
    ratio_Of_YAxis = 1
    x_Axis_ratio = y_Axis_ratio = np.arange(30) # ratio of number of X axis 
    x_Axis_Number =  [[0] * 2 for i in range(30)] 
    y_Axis_Number = [[0] * 2 for i in range(30)] 
    x_Axis_Number_Index = y_Axis_Number_Index = 0

    numberOf_Yaxis_remove_Duplicates = numberOf_Xaxis_remove_Duplicates = [[0] * 2 for i in range(30)] # 0 - number 1 Y coordinate  # numbers which are relate to Y Axis
    numberOf_Xaxis_remove_Duplicates_Index = numberOf_Yaxis_remove_Duplicates_Index = 0 

    x_Axis_ratio_Index = y_Axis_ratio_Index = 0
    for j in range(0, 30):
        x_Axis_ratio[j] = 0 
        y_Axis_ratio[j] = 0 

    if numberOfCharactor > 0:
        for i in range(0, numberOfCharactor): 
            character_X_Cordinate = textCoordinate[i][1]
            character_Y_Cordinate = textCoordinate[i][2]
            Number = textCoordinate[i][0] 

            # Identify Y axis numbers
            if((character_X_Cordinate <= (origin_X + pixcelForTicMark_X)) and (character_X_Cordinate >= (origin_X-pixcelForTicMark_X))): 
                if y_Axis_Number_Index < 30:
                    y_Axis_Number[y_Axis_Number_Index][0] = textCoordinate[i][0]   # number
                    y_Axis_Number[y_Axis_Number_Index][1] = textCoordinate[i][2]   #  Y cooordinate
                    y_Axis_Number_Index = y_Axis_Number_Index + 1  

            # Identify Numbers related to X axis
            elif(((character_Y_Cordinate) <= (origin_Y + pixcelForTicMark_Y)) and ((character_Y_Cordinate) >= (origin_Y-pixcelForTicMark_Y))):
                if x_Axis_Number_Index < 30:
                    x_Axis_Number[x_Axis_Number_Index][0] = textCoordinate[i][0]   # number
                    x_Axis_Number[x_Axis_Number_Index][1] = textCoordinate[i][1]   #  X cooordinate
                    x_Axis_Number_Index = x_Axis_Number_Index + 1 


# Identify Ratio of X axis
    if x_Axis_Number_Index > 1:
        for i in range(0, 30): 
            number = x_Axis_Number[i][0]
            x = x_Axis_Number[i][1] 
            haveDuplicate = False
            if number != 0 and x != 0:
                for j in range (0,30):
                    number_dup = numberOf_Xaxis_remove_Duplicates[j][0]
                    x_dup = numberOf_Xaxis_remove_Duplicates[j][1]
                    if number_dup == number and (x >= x_dup - 3 and x <= x_dup + 3):
                        haveDuplicate = True
            if haveDuplicate != True:
                numberOf_Xaxis_remove_Duplicates[numberOf_Xaxis_remove_Duplicates_Index][0] = number
                numberOf_Xaxis_remove_Duplicates[numberOf_Xaxis_remove_Duplicates_Index][1] = x
                numberOf_Xaxis_remove_Duplicates_Index = numberOf_Xaxis_remove_Duplicates_Index + 1
                

        # get The ratio and stotre in a array
        for i in range(0, 30):
            number = numberOf_Xaxis_remove_Duplicates[i][0]
            x = numberOf_Xaxis_remove_Duplicates[i][1]
            haveDuplicate = False
            if number != 0 and x != 0 and pixcelForTicMark_X != 0:
                numberOf_TicMarks = int(round((x - origin_X )/pixcelForTicMark_X))
                if numberOf_TicMarks != 0:
                    ratio = int(round(number/numberOf_TicMarks))
                    if x_Axis_ratio_Index < 30:
                        if (ratio < 0):
                            x_Axis_ratio[x_Axis_ratio_Index] = ratio*(-1)
                        else:
                            x_Axis_ratio[x_Axis_ratio_Index] = ratio
                        x_Axis_ratio_Index = x_Axis_ratio_Index + 1
    
        ratioVsCount = [[0] * 2 for i in range(30)]
        ratioVsCount_Index = 0

        # get the frequency of each ratio
        for i in range(0, 30):
            count = 0
            # print(" X Axis Ratios ===" + str(x_Axis_ratio[i]))
            current_Ratio = x_Axis_ratio[i]
            if current_Ratio != 0 :
                for j in range(0, 30):
                    if current_Ratio == (x_Axis_ratio[j]):
                        count = count + 1
                if (ratioVsCount_Index < 30 ):
                    ratioVsCount[ratioVsCount_Index][0] = current_Ratio
                    ratioVsCount[ratioVsCount_Index][1] = count
                    ratioVsCount_Index = ratioVsCount_Index + 1

        # select the ratio which has the max frequency
        max_count = 0
        for i in range(0, 30):
            count = ratioVsCount[i][1]
            if (max_count < count):
                max_count = count
                if ((ratioVsCount[i][0] >= 1)):
                    ratio_Of_XAxis = ratioVsCount[i][0]

        ratio_X_Axis_Value = ratio_Of_XAxis

# Identify Y axis ratio
    if y_Axis_Number_Index > 1: 
        for i in range(0, 30):
            num = number = y_Axis_Number[i][0]
            y = y_Axis_Number[i][1]
            # print(" Number  YYYYYYYYY   :  " + str(num) + " x cor " + str(y))
            haveDuplicate = False
            if number != 0 and y != 0:
                for j in range (0,30):
                    number_dup = numberOf_Yaxis_remove_Duplicates[j][0]
                    y_dup = numberOf_Yaxis_remove_Duplicates[j][1]
                    if number_dup == number and (y >= y_dup - 3 and y <= y_dup + 3):
                        haveDuplicate = True
            if haveDuplicate != True:
                numberOf_Yaxis_remove_Duplicates[numberOf_Yaxis_remove_Duplicates_Index][0] = number
                numberOf_Yaxis_remove_Duplicates[numberOf_Yaxis_remove_Duplicates_Index][1] = y
                numberOf_Yaxis_remove_Duplicates_Index = numberOf_Yaxis_remove_Duplicates_Index + 1
            

        # get The ratio and stotre in a array
        for i in range(0, 30):
            # number = numberOf_Yaxis[i][0]
            # y = numberOf_Yaxis[i][1]
            number =  numberOf_Yaxis_remove_Duplicates[i][0]                                                #*******
            y =  numberOf_Yaxis_remove_Duplicates[i][1]                                                      #*******
            # print("  Y number ermove ---" + str(number) + str(" Y coordinate "+ str(y)))
            if number != 0 and pixcelForTicMark_Y != 0 and y !=0 : 
                print(" Y : " + str(y))

                for i in range(origin_X - 15 , origin_X + 15):
                    for j in range(y - 5, y +5):
                        if(i > 0 and i < width and j > 0 and j < height ): 
                            allLines[j,i] = (255, 255, 255)
                            MofologyImg_2[j,i] = (0, 255, 0)
                            cdstP[j,i] = (255, 255, 255)  
                print(" origin_Y : " + str(origin_Y))
                print(" pixcelForTicMark_Y : " + str(pixcelForTicMark_Y))                                #*******
                numberOf_TicMarks = int(round((y - origin_Y )/pixcelForTicMark_Y))
                print(" Number of Tic Marks " + str(numberOf_TicMarks))
                if numberOf_TicMarks != 0:
                    ratio = int(round(number/numberOf_TicMarks))
                    # print("  ratio ----- ---" + str(ratio))
                    if y_Axis_ratio_Index < 30:
                        if (ratio < 0):
                            y_Axis_ratio[y_Axis_ratio_Index] = ratio*(-1)
                        else:
                            y_Axis_ratio[y_Axis_ratio_Index] = ratio
                        y_Axis_ratio_Index = y_Axis_ratio_Index + 1 
    
        ratioVsCount = [[0] * 2 for i in range(30)]
        ratioVsCount_Index = 0

        # get the frequency of each ratio
        for i in range(0, 30):
            count = 0
            # print(" Y Axis Ratios ===" + str(y_Axis_ratio[i]))
            current_Ratio = y_Axis_ratio[i]
            if current_Ratio != 0 :
                for j in range(0, 30):
                    if current_Ratio == (y_Axis_ratio[j]):
                        count = count + 1
                if (ratioVsCount_Index < 30 ):
                    ratioVsCount[ratioVsCount_Index][0] = current_Ratio
                    ratioVsCount[ratioVsCount_Index][1] = count
                    ratioVsCount_Index = ratioVsCount_Index + 1

        # select the ratio which has the max frequency
        max_count = 0
        for i in range(0, 30):
            count = ratioVsCount[i][1]
            if (max_count < count):
                max_count = count
                if ((ratioVsCount[i][0] >= 1)):
                    ratio_Of_YAxis = ratioVsCount[i][0]

        ratio_Y_Axis_Value = ratio_Of_YAxis

        print(" X axis Ratio + "+ str(ratio_X_Axis_Value) + " Y axis Ratio + " + str(ratio_Y_Axis_Value))



def indentify_Y_UsingValues():
    global Y_axis_cordinate, X_axis_cordinate, found_X, maxlength_Y, textCoordinate, found_Y

    count_X =  [[0] * 2 for i in range(numberOfCharactor)] # List  to store charactor X coordinate and frequency of that value
    maxlength_Y = max_Count_X = x_coordinate = maxlength_Y = 0

    if (pixcelForTicMark_X == 0):
        identifyTicMarks_X_Axis()
        

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

    

    # get the maximum frequency of the x coordinate
    for i in range(0, numberOfCharactor):
        c = count_X[i][1]
        # print(" =========== " + str(  count_X[i][0] ) + "_--------------------  " + str(count_X[i][1]))
        if (c > max_Count_X):
            max_Count_X = c
            x_coordinate = count_X[i][0]

    # print(" X coordinate --------------------"+str(x_coordinate))
    
    if max_Count_X > 1:
        # get the vertical line which has maximum length
        for h in range(0, noOfLines):
            l = Y_arr[h][1] 
            if l > maxlength_Y : 
                Y_axis_cordinate = h
                maxlength_Y = l  
        # print(" Length of Y Axis  : " + str(maxlength_Y))
        hasError = False

        # identify y axis considering line length and text
        for h in range(0, noOfLines):
            len = Y_arr[h][1]
            x = arr[h][0]
            if (len == maxlength_Y or (len >= maxlength_Y*0.9)): 
                if ( (x_coordinate <= x + (pixcelForTicMark_X/2)) and ( x_coordinate >= x-(pixcelForTicMark_X/2)) and (x_coordinate != 0)):     
                    Y_axis_cordinate = h
                    found_Y = True
                    return found_Y

        # for h in range(0, noOfLines):
        #     len = Y_arr[h][1]
        #     x = arr[h][0]
        #     if (len == maxlength_Y):
        #         hasError = True
        #         if ( (x_coordinate <= x + (pixcelForTicMark_X*(3/4))) and ( x_coordinate >= x-(pixcelForTicMark_X*(3/4)))):     
        #             Y_axis_cordinate = h
        #             found_Y = True
        #             return found_Y 

        count = 0

        for h in range(0, noOfLines):
            len = X_arr[h][1]
            y = arr[h][1] 
            if (len == maxlength_X) or (len >= maxlength_Y - (maxlength_Y * 0.4)):      
                if ( (x_coordinate <= x + (pixcelForTicMark_X/2)) and ( x_coordinate >= x-(pixcelForTicMark_X/2)) and ( x_coordinate != 0)):     
                    Y_axis_cordinate = h
                    # found_Y = True
                    # return found_Y
        
        if count > 1:
            find_Y_Axis()
        elif count ==  1:
            found_Y = True 
            return found_Y


        # for h in range(0, noOfLines):
        #     len = Y_arr[h][1]
        #     x = arr[h][0]
        #     if (len == maxlength_Y) or (len >= maxlength_Y - (maxlength_Y * 0.4)):
        #         if ( (x_coordinate <= x + (pixcelForTicMark_X*(3/4))) and ( x_coordinate >= x- (pixcelForTicMark_X*(3/4)))):     
        #             Y_axis_cordinate = h
        #             found_Y = True
        #             return found_Y
    return found_Y        

def indentify_X_Axis_UsingValues():
    global Y_axis_cordinate, X_axis_cordinate, found_X, maxlength_X, numberOfDigitValue

    count_Y =  [[0] * 2 for i in range(numberOfCharactor)]  # List  to store charactor Y coordinate and frequency of that value  
    max_Count_Y = y_coordinate = 0 

    # 10 identify Y axis Ticmarks
    if (pixcelForTicMark_Y == 0):
        identifyTicMarks_Y_Axis() 
        # print("pixcelForTicMark_Y" + str(pixcelForTicMark_Y))

    # store charactor Y coordinate and frequency of that value 
    for i in range(0, numberOfDigitValue):
        y_val = textCoordinate[i][2]
        count = 0
        if y_val != 0 :
            for h in range(0 , numberOfDigitValue):
                val = textCoordinate[h][2]
                if ((val <= y_val + 5 ) and (val >= y_val - 5)):
                    count = count + 1
        count_Y[i][0] = y_val
        count_Y[i][1] = count
        # print(" Value : " + str(textCoordinate[i][0])+ "  y_val : " + str(y_val) + " count " + str(count))

    # # print charactor Y coordinate and frequency of that value
    # for i in range(0, numberOfCharactor ):
    #     print("      " + str(  count_Y[i][0] ) + "_--------------------  " + str(count_Y[i][1]))
    
    # get the maximum frequency of the y coordinate
    for i in range(0, numberOfCharactor): 
        c = count_Y[i][1]
        if (c > max_Count_Y):
            max_Count_Y = c
            y_coordinate = count_Y[i][0]
    
    if max_Count_Y > 1:
        
        # get the horizontal line which has maximum length
        for h in range(0, noOfLines):
            l = X_arr[h][1] 
            if l > maxlength_X : 
                X_axis_cordinate = h
                maxlength_X = l  
        # print(" Length of X Axis  : " + str(maxlength_X))

        # identify x axis considering line length and text
        if numberOfDigitValue > 0:
            # print(" Max Count --------------------"+str(max_Count_Y))
            hasError = False
            for h in range(0, noOfLines):
                len = X_arr[h][1]
                y = arr[h][1]
                if (len == maxlength_X and len >= maxlength_X*0.9): 
                    if ((y_coordinate <= y + (pixcelForTicMark_Y/2)) and ( y_coordinate >= y - (pixcelForTicMark_Y/2)) and (y_coordinate != 0)):     
                        X_axis_cordinate = h 
                        found_X = True
                        return found_X 
            
            # for h in range(0, noOfLines):
            #     len = X_arr[h][1]
            #     y = arr[h][1]
            #     if (len == maxlength_X) :     
            #         if ((y_coordinate <= y + (pixcelForTicMark_Y*(3/4))) and ( y_coordinate >= y - (pixcelForTicMark_Y*(3/4)))):     
            #             X_axis_cordinate = h 
            #             found_X = True
            #             return found_X 
            
            count = 0 

            for h in range(0, noOfLines):
                len = X_arr[h][1]
                y = arr[h][1]
                if (len == maxlength_X) or (len >= maxlength_X - (maxlength_X * 0.4)):
                    if ((y_coordinate <= y + (pixcelForTicMark_Y/2)) and ( y_coordinate >= y - (pixcelForTicMark_Y/2)) and (y_coordinate != 0)):     
                        X_axis_cordinate = h 
                        # found_X = True
                        # return found_X  
            
            if count > 1:
                find_X_Axis()
            elif count ==  1:
                found_X = True 
                return found_X 

            # for h in range(0, noOfLines):
            #     len = X_arr[h][1]
            #     y = arr[h][1]
            #     if (len == maxlength_X) or (len >= maxlength_X - (maxlength_X * 0.4)):  
            #         if ((y_coordinate <= y + (pixcelForTicMark_Y*(3/4))) and ( y_coordinate >= y - (pixcelForTicMark_Y*(3/4)))):     
            #             X_axis_cordinate = h 
            #             found_X = True
            #             return found_X
            
            
    return found_X 

def generateEquationLinearGraph():
    m = graphs_arr[graph_cordinate][0]
    c = graphs_arr[graph_cordinate][1]
    X_Y_Coordinate = [[0] * 2 for i in range(10)] # 0- X coordinate / 1 - Y Coordinate
    X_Y_Coordinate_n = [[0] * 2 for i in range(10)] # 0- X coordinate / 1 - Y Coordinate
    pointOnGraph_Index = 0
    count = count_2 = totalCount = 0
    current_X = 0
    
    # print(" Check ")

    for k in range(0, 20):
        current_X = origin_X+(k*pixcelForTicMark_X) 
        intersect_y = round((m*current_X) + c,1) 

        real_Y = round(((origin_Y - intersect_y)/pixcelForTicMark_Y) , 1)
        # print(" X Value -->" + str(-k) + " Y Value -->" + str(real_Y) )
        a = modf(real_Y)
        d1 = round(a[0],1)
        if (d1 < 0) :
            d1 = (-1)*d1  
        if (d1 <= 0.2  or d1>=0.8) :
            y = int(round(real_Y))
            if (count < 10):
                X_Y_Coordinate[count][0] = k
                X_Y_Coordinate[count][1] = y
                count = count + 1
                totalCount = totalCount + 1

    # if count < 2:

    for k in range(1, 20):
        current_X = origin_X-(k*pixcelForTicMark_X) 
        intersect_y = round((m*current_X) + c,1)
        real_Y = round(((origin_Y - intersect_y)/pixcelForTicMark_Y) , 1)
        # print(" X Value -->" + str(-k) + " Y Value -->" + str(real_Y) )
        a = modf(real_Y)
        d1 = round(a[0],1)
        if (d1 < 0) :
            d1 = (-1)*d1  
        if (d1 <= 0.2  or d1>=0.8) :
            y = int(round(real_Y)) 
            if (count_2 < 10):
                X_Y_Coordinate_n[count_2][0] = -k
                X_Y_Coordinate_n[count_2][1] = y
                count_2 = count_2 + 1
                totalCount = totalCount + 1

    if (totalCount < 2):
        for k in range(0, 50):
            current_X = origin_X+(k*pixcelForTicMark_X) 
            intersect_y = round((m*current_X) + c,1) 

            real_Y = round(((origin_Y - intersect_y)/pixcelForTicMark_Y),1) 
            a = modf(real_Y)
            d1 = round(a[0],1)
            if (d1 < 0) :
                d1 = (-1)*d1  
            if (d1 <= 0.25 or d1>=0.75) :
                y = int(round(real_Y))
                if (count < 10):
                    X_Y_Coordinate[count][0] = k
                    X_Y_Coordinate[count][1] = y
                    count = count + 1
                    totalCount = totalCount + 1

    if (totalCount > 2):
        
        if count != 0 and count_2 != 0:
            x1 = X_Y_Coordinate[0][0] * ratio_X_Axis_Value
            y1 = X_Y_Coordinate[0][1] * ratio_Y_Axis_Value
            x2 = X_Y_Coordinate_n[0][0] * ratio_X_Axis_Value
            y2 = X_Y_Coordinate_n[0][1] * ratio_Y_Axis_Value
        elif count != 0 and count_2 == 0:
            x1 = X_Y_Coordinate[0][0] * ratio_X_Axis_Value
            y1 = X_Y_Coordinate[0][1] * ratio_Y_Axis_Value
            x2 = X_Y_Coordinate[1][0] * ratio_X_Axis_Value
            y2 = X_Y_Coordinate[1][1] * ratio_Y_Axis_Value
        elif count == 0 and count_2 != 0:
            x1 = X_Y_Coordinate_n[0][0] * ratio_X_Axis_Value
            y1 = X_Y_Coordinate_n[0][1] * ratio_Y_Axis_Value
            x2 = X_Y_Coordinate_n[1][0] * ratio_X_Axis_Value
            y2 = X_Y_Coordinate_n[1][1] * ratio_Y_Axis_Value
        

        print(" 1. Pont on Graph ---> (" + str(x1) + " , " + str(y1) +")")
        print(" 2. Pont on Graph ---> (" + str(x2) + " , " + str(y2) +")")
        if ((x1 - x2) != 0):
            m = round(((y1 - y2)/(x1 - x2)) , 1)
        else:
            m = round(((y1 - y2)) , 1)
        a = modf(m)
        d1 = round(a[0],1)
        if (d1 < 0) :
            d1 = (-1)*d1  
        if (d1 <= 0.15  or d1>=0.85) :
            m = int(round(m))

        c = round((y1 - (m*x1)), 1)
        b = modf(c)
        d2 = round(b[0],1)
        if (d2 < 0) :
            d2 = (-1)*d2
        if (d2 <= 0.15  or d2>=0.85) :
            c = int(round(c))

        print(" Equation ----> " + " Y = " + str(m) + "X + "+ str(c))

    # print
    # for i in range (0, 10):
    #     print(" X Value -->" + str(X_Y_Coordinate[i][0]) + " Y Value -->" + str(X_Y_Coordinate[i][1]) )
       
    # getQuadraticGraphCoodinates

def templateMatching():
    global srcTemplate, numberOf_Xaxis, numberOf_Yaxis, tem_y_arr, tem_x_arr, tem_Matching_Coordinates, xIndex , yIndex, temSrc, xy_arr
    numberOf_Xaxis = [[0] * 3 for i in range(20)] # 0 - number 1 X coordinate 2 count
    numberOf_Yaxis = [[0] * 2 for i in range(20)] # 0 - number 1 Y coordinate
    indexNumberOf_Xaxis = indexNumberOf_Yaxis = 0
    tem_Matching_Coordinates = [[0] * 5 for i in range(30)] # 0 - number 1 - topleft_x/ 2-topleft_y / 3 - bottemRight_x / 4 -bottemRight_y 
    xy_arr = [[0] * 2 for i in range(30)]
    tem_Matching_Coordinates_Index = 0
    tem_x_arr  = [[0] * 2 for i in range(20)]  # np.arange(20)
    tem_y_arr = [[0] * 2 for i in range(20)]  # np.arange(20)
    xIndex = yIndex = 0
    xy_Index = 0

    # assign value to 0
    for h in range(0, 20):
        numberOf_Xaxis[h][0] = numberOf_Xaxis[h][1] = numberOf_Xaxis[h][2] = 0
        numberOf_Yaxis[h][0] = numberOf_Yaxis[h][1] = 0
        # print(" numberOf_Xaxis +  " + str(numberOf_Xaxis[h][0]) + "  , " + str(numberOf_Xaxis[h][1]) )
        # print(" numberOf_Yaxis +  " + str(numberOf_Yaxis[h][0]) + "  , " + str(numberOf_Yaxis[h][1]) )

    img = src

    # Transform source image to gray if it is not already
    if len(img.shape) != 2:
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:
        gray_img = img

    # create array to store Images(template) 
    templates = [[0] * 2 for i in range(27)]

    templates[0][0] = "tem2.5.png"
    templates[0][1] = 2

    templates[1][0] = "tem1.1.png"
    templates[1][1] = 1

    # templates[1][0] = "tem2.4.png"
    # templates[1][1] = 2

    templates[2][0] = "tem2.png"
    templates[2][1] = 2

    templates[3][0] = "tem2.1.png"
    templates[3][1] = 2

    templates[4][0] = "tem3.png"
    templates[4][1] = 3

    templates[5][0] = "tem3.1.png"
    templates[5][1] = 3

    templates[6][0] = "tem4.png"
    templates[6][1] = 4

    templates[7][0] = "tem4.1.png"
    templates[7][1] = 4

    templates[8][0] = "tem5.png"
    templates[8][1] = 5

    templates[9][0] = "tem5.1.png"
    templates[9][1] = 5
    templates[10][0] = "tem6.png"
    templates[10][1] = 6
    templates[11][0] = "tem6.1.png"
    templates[11][1] = 6
    templates[12][0] = "tem8.png"
    templates[12][1] = 8
    templates[13][0] = "tem8.1.png"
    templates[13][1] = 8
    templates[14][0] = "tem10.png"
    templates[14][1] = 10
    templates[15][0] = "tem10.1.png"
    templates[15][1] = 10
    templates[16][0] = "tem15.png"
    templates[16][1] = 15


    templates[17][0] = "tem2.2.png"
    templates[17][1] = 2
    templates[18][0] = "tem3.2.png"
    templates[18][1] = 3
    templates[19][0] = "tem4.2.png"
    templates[19][1] = 4
    templates[20][0] = "tem6.2.png"
    templates[20][1] = 6
    templates[21][0] = "tem8.2.png"
    templates[21][1] = 8
    # templates[22][0] = "tem7.png"
    # templates[22][1] = 7
    templates[22][0] = "tem8.2.png"
    templates[22][1] = 8
    templates[23][0] = "tem5.2.png"
    templates[23][1] = 5
    templates[24][0] = "tem4.3.png"
    templates[24][1] = 4

    templates[25][0] = "tem4.3.png"
    templates[25][1] = 4
    templates[26][0] = "tem4.3.png"
    templates[26][1] = 4


    helfpixcelForTicMark_X = pixcelForTicMark_X/2
    helfpixcelForTicMark_Y = pixcelForTicMark_Y/2

 

    for i in range(1, 27):
        curretTemplate = templates[i][0]
        number = templates[i][1]
        tem = cv.imread(curretTemplate)
        if len(tem.shape) != 2:
            template = cv.cvtColor(tem, cv.COLOR_BGR2GRAY)
        else:
            template = tem
        w, h = template.shape[::-1]
        result = cv.matchTemplate(MofologyImg, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.7)
        for pt in zip(*loc[::-1]):
            topleft_x = pt[0]
            topleft_y = pt[1]
            bottemRight_x = pt[0] + w
            bottemRight_y = pt[1] + h
            cv.rectangle(srcTemplate, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            cv.rectangle(temSrc, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            
            haveDuplicate = False

            x = int(round((topleft_x + bottemRight_x)/2))
            y = int(round((topleft_y + bottemRight_y)/2))

            for k in range(0,30):
                cur_x = xy_arr[k][0]
                if cur_x != 0 and ((xy_arr[k][1]) != 0):
                    # if (cur_x == x) and (y == xy_arr[k][0]):
                    # print ("cur x " + str(cur_x ) + " and y = " + str(xy_arr[k][1]))
                    if (cur_x >= x - 5 and cur_x <= x + 5 ) and (y >= (xy_arr[k][1] - 5) and y <= (xy_arr[k][1] + 5)):
                        haveDuplicate = True

            
            if haveDuplicate != True:
                if xy_Index < 30:
                    xy_arr[xy_Index][0]  = x
                    xy_arr[xy_Index][1]  = y
                    xy_Index = xy_Index +1

                # if (xIndex < 20):
                #     tem_x_arr[xIndex][0] =  x
                #     tem_x_arr[xIndex][1] =  0
                #     xIndex = xIndex + 1
                # if (yIndex < 20):
                #     tem_y_arr[yIndex][0] = y
                #     tem_y_arr[yIndex][1] = 0
                #     yIndex = yIndex + 1

            if tem_Matching_Coordinates_Index < 30:
                tem_Matching_Coordinates[tem_Matching_Coordinates_Index][0] = number 
                tem_Matching_Coordinates[tem_Matching_Coordinates_Index][1] = topleft_x 
                tem_Matching_Coordinates[tem_Matching_Coordinates_Index][2] = topleft_y
                tem_Matching_Coordinates[tem_Matching_Coordinates_Index][3] = bottemRight_x 
                tem_Matching_Coordinates[tem_Matching_Coordinates_Index][4] = bottemRight_y 
                tem_Matching_Coordinates_Index = tem_Matching_Coordinates_Index + 1

            
          
            
        
            
    #         print(" Origin Y " + str(origin_Y)+ " ----------------- y " + str(y) )

    #         if ( y >= (origin_Y - helfpixcelForTicMark_Y)) and ( y <= (origin_Y  + helfpixcelForTicMark_Y)):
    #             print("indexNumberOf_Xaxis "+ str(indexNumberOf_Xaxis))
    #             if ( indexNumberOf_Xaxis < 20):
    #                 numberOf_Xaxis[indexNumberOf_Xaxis][0] = number
    #                 numberOf_Xaxis[indexNumberOf_Xaxis][1] = x
    #                 indexNumberOf_Xaxis = indexNumberOf_Xaxis + 1
    #             cv.rectangle(srcTemplate, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    #         if ( x >= (origin_X - helfpixcelForTicMark_X)) and ( x <= (origin_X + helfpixcelForTicMark_X)):
    #             if ( indexNumberOf_Yaxis < 20):
    #                 numberOf_Yaxis[indexNumberOf_Yaxis][0] = number
    #                 numberOf_Yaxis[indexNumberOf_Yaxis][1] = y
    #                 indexNumberOf_Yaxis = indexNumberOf_Yaxis + 1
    #             cv.rectangle(srcTemplate, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)
    # identify_XAxis_Ratio()

def identify_XAxis_UsingTempalte_Matching(): 
    global X_axis_cordinate
    found_X = False
    y_coordinates = [[0] * 2 for i in range(30)]  # 0 - Y coordinate 1 - count 

    
    # 9 identify X axis Ticmarks
    if (pixcelForTicMark_Y == 0 ):
        identifyTicMarks_Y_Axis() 

    # print x y axis
    for i in range(0, 30): 
        count = 0
        y = xy_arr[i][1]
        # print("**" + str(y) )
        if y != 0:
            for j in range (0, 30): 
                current_y_cor = xy_arr[j][1]
                if current_y_cor != 0:
                    if ( (current_y_cor <= (y + (pixcelForTicMark_Y/3) )) and (current_y_cor >= (y - (pixcelForTicMark_Y/3) ))):
                        count = count +1
                        # print (" cc" + str(y + (pixcelForTicMark_Y/3)))
                        # print (" cc" + str(y - (pixcelForTicMark_Y/3)))
        y_coordinates[i][0] = y
        y_coordinates[i][1] = count
        # print("**********" + str(y) + "count " +str(count))

 
    y_count_max = 0 
    y_coordnate_of_X_Axis = total_y_coordnate_of_X_Axis =  0 

    for i in range (0,20): 
        current_y_count_max = y_coordinates[i][1]
        if current_y_count_max > y_count_max:
            y_count_max = current_y_count_max
            # y_coordnate_of_X_Axis = tem_y_arr[i][0]
    
    count = 0
    for i in range (0,20): 
        current_y_count_max = y_coordinates[i][1]
        # print("/////////////////////" + str(y_coordinates[i][0]) + "count " +str(y_coordinates[i][1]))
        if (current_y_count_max == y_count_max):
            total_y_coordnate_of_X_Axis = total_y_coordnate_of_X_Axis + y_coordinates[i][0]
            count = count + 1

    y_coordnate_of_X_Axis = int(round(total_y_coordnate_of_X_Axis/count))

    # print(" y_count_max " + str(y_count_max) + " y_coordnate_of_X_Axis " + str(y_coordnate_of_X_Axis))
    
    if y_count_max > 1:
        maxlength_X = 0
        # get the horizontal line which has maximum length
        for h in range(0, noOfLines):
            l = X_arr[h][1] 
            if l > maxlength_X : 
                X_axis_cordinate = h
                maxlength_X = l  
        # print(" Length of X Axis  : " + str(maxlength_X))

        # identify x axis considering line length and text
        # if numberOfDigitValue > 0:
        hasErrorin = False
        con = 0
        for h in range(0, noOfLines):
            len = X_arr[h][1]
            y = arr[h][1] 
            if (len == maxlength_X or  (len >= maxlength_X* 0.9)) :
                hasErrorin = True     
                if ( (y_coordnate_of_X_Axis <= y + (pixcelForTicMark_Y/2)) and ( y_coordnate_of_X_Axis >= y-(pixcelForTicMark_Y/2)) and ( y_coordnate_of_X_Axis != 0) ):    
                    X_axis_cordinate = h 
                    con = con + 1

        if con == 1:           
            # print(" Check ======1111")
            found_X = True 
            return found_X  
                    
        # print (" max length " + str(maxlength_X))

        count = 0
        for h in range(0, noOfLines):
            len = X_arr[h][1]
            y = arr[h][1] 
            # print(" Length " + str(len))
            if (len == maxlength_X) or (len >= maxlength_X - (maxlength_X * 0.4)):   
                if ( (y_coordnate_of_X_Axis <= y + (pixcelForTicMark_Y)) and ( y_coordnate_of_X_Axis >= y-(pixcelForTicMark_Y)) and ( y_coordnate_of_X_Axis != 0) ):        
                    X_axis_cordinate = h 
                    # print(" Check ======2222")
                    count = count + 1
                    # found_X = True 
                    # return found_X 
        if count > 1:
            find_X_Axis()
            passfromTem_X = True
            # print(" fROM tEMPLATE TO SHORT x")
        elif count ==  1:
            found_X = True 
            return found_X 


        # for h in range(0, noOfLines):
        #     len = X_arr[h][1]
        #     y = arr[h][1] 
            
        #     if (len == maxlength_X) or (len >= maxlength_X - (maxlength_X * 0.4)):      
        #         if ( (y_coordnate_of_X_Axis <= y + (pixcelForTicMark_Y* (3/4))) and ( y_coordnate_of_X_Axis >= y-(pixcelForTicMark_Y*(3/4))) and ( y_coordnate_of_X_Axis != 0) ):    
        #             X_axis_cordinate = h  
        #             found_X = True 
        #             return found_X 

    return found_X 





def identify_Y_AXis_UsingTempalte_Matching():
    global Y_axis_cordinate, passfromTem_Y
    found_Y = False
    x_coordinates = [[0] * 2 for i in range(30)]  # 0 - Y coordinate 1 - count 

    # 9 identify X axis Ticmarks
    if (pixcelForTicMark_X == 0 ):
        identifyTicMarks_X_Axis() 

    # get the yx coordinate and their count 


    for i in range(0, 30): 
        count = 0
        x = xy_arr[i][0]
        # print(" x cor " + str(x))
        if x != 0:
            for j in range (0, 30): 
                current_x_cor = xy_arr[j][0]
                if current_x_cor != 0:
                    if ( (current_x_cor <= (x + (pixcelForTicMark_X/3) )) and (current_x_cor >= (x - (pixcelForTicMark_X/3)))):
                        count = count +1
        x_coordinates[i][0] = x
        x_coordinates[i][1] = count


    # find max count
    x_count_max = 0
    x_coordnate_of_Y_Axis = total_x_coordnate_of_Y_Axis = 0
        # y_coordnate_of_X_Axis = 0 
    for i in range (0,20):
        # print(" x cor " + str(x_coordinates[i][0]) + " count  " + str(x_coordinates[i][1]))
        current_x_count_max = x_coordinates[i][1]
        if current_x_count_max > x_count_max:
            x_count_max = current_x_count_max
            # x_coordnate_of_Y_Axis = tem_x_arr[i][0]

    count = 0
    for i in range (0,20):
        current_x_count_max = x_coordinates[i][1]
        if (current_x_count_max == x_count_max)  :
            total_x_coordnate_of_Y_Axis = total_x_coordnate_of_Y_Axis + x_coordinates[i][0]
            count = count + 1
    
    x_coordnate_of_Y_Axis = int(round(total_x_coordnate_of_Y_Axis/count))



    # print (" x_count_max " + str(x_count_max)) 
    # print (" x_coordnate_of_Y_Axis " + str(x_coordnate_of_Y_Axis)) 

            # current_y_count_max = tem_y_arr[i][1]
            # if current_y_count_max > y_count_max:
            #     y_count_max = current_y_count_max
            #     y_coordnate_of_X_Axis = tem_y_arr[i][0]
    
    if x_count_max > 1:
        # get the vertical line which has maximum length
        maxlength_Y = 0
        for h in range(0, noOfLines):
            l = Y_arr[h][1]
            # print(" Length of Y Axis *********** : " + str(l)) 
            if l > maxlength_Y : 
                Y_axis_cordinate = h
                maxlength_Y = l  
        # print(" Length of Y Axis  : " + str(maxlength_Y))
     
        # 9 identify X axis Ticmarks
        if (pixcelForTicMark_X == 0 ):
            identifyTicMarks_X_Axis() 

        # identify y axis considering line length and text
        con = 0
        for h in range(0, noOfLines):
            len = Y_arr[h][1]
            x = arr[h][0]
            if (len == maxlength_Y and len >= maxlength_Y*0.9) :     
                if ((x_coordnate_of_Y_Axis <= x + (pixcelForTicMark_X/2)) and ( x_coordnate_of_Y_Axis >= x - (pixcelForTicMark_X/2)) and (x_coordnate_of_Y_Axis != 0)):     
                    Y_axis_cordinate = h 
                    con = con + 1
                    # print (" check 1111")
                     
        if con == 1:
            found_Y = True
            return found_Y 

        count = 0
        for h in range(0, noOfLines):
            len = Y_arr[h][1]
            x = arr[h][0]
            if (len == maxlength_Y) or (len >= maxlength_Y - (maxlength_Y * 0.4)):     
                if ((x_coordnate_of_Y_Axis <= x + (pixcelForTicMark_X)) and ( x_coordnate_of_Y_Axis >= x - (pixcelForTicMark_X)) and (x_coordnate_of_Y_Axis != 0)):     
                    Y_axis_cordinate = h 
                    print (" check 3333")
                    count = count + 1
                    # found_Y = True
                    # return found_Y
        if count > 1:
            passfromTem_Y = True
            find_Y_Axis()
            print(" fROM tEMPLATE TO SHORT y")
        elif count ==  1:
            found_Y = True 
            return found_Y 
    return found_Y      

def seperateTemplateTo_X_Y_Axis():
    global numberOf_Yaxis, numberOf_Xaxis
    
    numberOf_Yaxis = [[0] * 2 for i in range(30)] # 0 - number 1 Y coordinate  # numbers which are relate to Y Axis
    numberOf_Xaxis = [[0] * 2 for i in range(30)] # 0 - number 1 X coordinate  # numbers which are relate to X Axis
    indexNumberOf_Xaxis = indexNumberOf_Yaxis = 0
    ratio_Of_XAxis = 1

    x_Axis_ratio = np.arange(30) # ratio of number of X axis 
    x_Axis_ratio_Index = 0
    for j in range(0, 30):
        x_Axis_ratio[j] = 0

    for i in range(0,30):
        number = tem_Matching_Coordinates[i][0]
        top_x = tem_Matching_Coordinates[i][1]
        top_y = tem_Matching_Coordinates[i][2]
        bottom_x = tem_Matching_Coordinates[i][3]
        bottom_y = tem_Matching_Coordinates[i][4]

        x = int(round((top_x + bottom_x)/2))
        y = int(round((top_y + bottom_y)/2))


        helfpixcelForTicMark_Y = int(round(pixcelForTicMark_Y /2))
        helfpixcelForTicMark_X = int(round(pixcelForTicMark_X / 2))

        # select Template Which are near to X axis
        if ( y >= (origin_Y - helfpixcelForTicMark_Y)) and ( y <= (origin_Y  + helfpixcelForTicMark_Y)): 
            if ( indexNumberOf_Xaxis < 20):
                numberOf_Xaxis[indexNumberOf_Xaxis][0] = number
                numberOf_Xaxis[indexNumberOf_Xaxis][1] = x
                indexNumberOf_Xaxis = indexNumberOf_Xaxis + 1 
                cv.rectangle(cdstP, (top_x,top_y), (bottom_x, bottom_y), (237, 28, 36), 2)
        
        # select Template Which are near to Y axis
        if ( x >= (origin_X - helfpixcelForTicMark_X)) and ( x <= (origin_X + helfpixcelForTicMark_X)):
            if ( indexNumberOf_Yaxis < 20):
                numberOf_Yaxis[indexNumberOf_Yaxis][0] = number
                numberOf_Yaxis[indexNumberOf_Yaxis][1] = y
                indexNumberOf_Yaxis = indexNumberOf_Yaxis + 1 
                cv.rectangle(cdstP, (top_x,top_y), (bottom_x, bottom_y), (0, 250, 36), 2)


def identify_X_Axis_Ratio():
    global ratio_X_Axis_Value

    ratio_Of_XAxis = 1
    x_Axis_ratio = np.arange(30) # ratio of number of X axis 

    numberOf_Xaxis_remove_Duplicates = [[0] * 2 for i in range(30)] # 0 - number 1 Y coordinate  # numbers which are relate to Y Axis
    numberOf_Xaxis_remove_Duplicates_Index = 0 


    x_Axis_ratio_Index = 0
    for j in range(0, 30):
        x_Axis_ratio[j] = 0
    
    # print number and Its x coordinate
    for i in range(0, 30):
        number = numberOf_Xaxis[i][0]
        x = numberOf_Xaxis[i][1]
        #print(" Xnumber---" + str(number) + str(" X coordinate "+ str(x)))

    for i in range(0, 30):
        number = numberOf_Xaxis[i][0]
        x = numberOf_Xaxis[i][1]
        haveDuplicate = False
        if number != 0 and x != 0:
            for j in range (0,30):
                number_dup = numberOf_Xaxis_remove_Duplicates[j][0]
                x_dup = numberOf_Xaxis_remove_Duplicates[j][1]
                if number_dup == number and (x >= x_dup - 3 and x <= x_dup + 3):
                    haveDuplicate = True
        if haveDuplicate != True:
            numberOf_Xaxis_remove_Duplicates[numberOf_Xaxis_remove_Duplicates_Index][0] = number
            numberOf_Xaxis_remove_Duplicates[numberOf_Xaxis_remove_Duplicates_Index][1] = x
            numberOf_Xaxis_remove_Duplicates_Index = numberOf_Xaxis_remove_Duplicates_Index + 1
                




    # get The ratio and stotre in a array
    for i in range(0, 30):
        number = numberOf_Xaxis_remove_Duplicates[i][0]
        x = numberOf_Xaxis_remove_Duplicates[i][1]
        haveDuplicate = False
        if number != 0 and x != 0 and pixcelForTicMark_X != 0:
            numberOf_TicMarks = int(round((x - origin_X )/pixcelForTicMark_X))
            if numberOf_TicMarks != 0:
                ratio = int(round(number/numberOf_TicMarks))
                if x_Axis_ratio_Index < 30:
                    if (ratio < 0):
                        x_Axis_ratio[x_Axis_ratio_Index] = ratio*(-1)
                    else:
                        x_Axis_ratio[x_Axis_ratio_Index] = ratio
                    x_Axis_ratio_Index = x_Axis_ratio_Index + 1
    
    ratioVsCount = [[0] * 2 for i in range(30)]
    ratioVsCount_Index = 0

    # get the frequency of each ratio
    for i in range(0, 30):
        count = 0
        # print(" X Axis Ratios ===" + str(x_Axis_ratio[i]))
        current_Ratio = x_Axis_ratio[i]
        if current_Ratio != 0 :
            for j in range(0, 30):
                if current_Ratio == (x_Axis_ratio[j]):
                    count = count + 1
            if (ratioVsCount_Index < 30 ):
                ratioVsCount[ratioVsCount_Index][0] = current_Ratio
                ratioVsCount[ratioVsCount_Index][1] = count
                ratioVsCount_Index = ratioVsCount_Index + 1

    # select the ratio which has the max frequency
    max_count = 0
    for i in range(0, 30):
        count = ratioVsCount[i][1]
        if (max_count <= count):
            max_count = count
            if ((ratioVsCount[i][0] >= 1)):
                ratio_Of_XAxis = ratioVsCount[i][0]

    ratio_X_Axis_Value = ratio_Of_XAxis

    # print(" Ratio Of Number on X Axis = "+str(ratio_Of_XAxis))


def identify_Y_Axis_Ratio():
    global ratio_Y_Axis_Value

    ratio_Of_YAxis = 1
    y_Axis_ratio = np.arange(30) # ratio of number of X axis 
    numberOf_Yaxis_remove_Duplicates = [[0] * 2 for i in range(30)] # 0 - number 1 Y coordinate  # numbers which are relate to Y Axis
    numberOf_Yaxis_remove_Duplicates_Index = 0 
    
    y_Axis_ratio_Index = 0
    for j in range(0, 30):
        y_Axis_ratio[j] = 0
    
    # print number and Its y coordinate
    for i in range(0, 30):
        number = numberOf_Yaxis[i][0]
        y = numberOf_Yaxis[i][1]

    # remove duplicates  # ********** full method
    for i in range(0, 30):
        number = numberOf_Yaxis[i][0]
        y = numberOf_Yaxis[i][1]
        haveDuplicate = False
        if number != 0 and y != 0:
            for j in range (0,30):
                number_dup = numberOf_Yaxis_remove_Duplicates[j][0]
                y_dup = numberOf_Yaxis_remove_Duplicates[j][1]
                if number_dup == number and (y >= y_dup - 3 and y <= y_dup + 3):
                    haveDuplicate = True
        if haveDuplicate != True:
            numberOf_Yaxis_remove_Duplicates[numberOf_Yaxis_remove_Duplicates_Index][0] = number
            numberOf_Yaxis_remove_Duplicates[numberOf_Yaxis_remove_Duplicates_Index][1] = y
            numberOf_Yaxis_remove_Duplicates_Index = numberOf_Yaxis_remove_Duplicates_Index + 1
                
    

    # get The ratio and stotre in a array
    for i in range(0, 30):
        # number = numberOf_Yaxis[i][0]
        # y = numberOf_Yaxis[i][1]
        number =  numberOf_Yaxis_remove_Duplicates[i][0]                                                #*******
        y =  numberOf_Yaxis_remove_Duplicates[i][1]                                                      #*******
        # print("  Y number ermove ---" + str(number) + str(" Y coordinate "+ str(y)))
        if number != 0 and pixcelForTicMark_Y != 0 and y !=0 :                                          #*******
            numberOf_TicMarks = int(round((y - origin_Y )/pixcelForTicMark_Y))
            if numberOf_TicMarks != 0:
                ratio = int(round(number/numberOf_TicMarks))
                print("  ratio ----- ---" + str(ratio))
                if y_Axis_ratio_Index < 30:
                    if (ratio < 0):
                        y_Axis_ratio[y_Axis_ratio_Index] = ratio*(-1)
                    else:
                        y_Axis_ratio[y_Axis_ratio_Index] = ratio
                    y_Axis_ratio_Index = y_Axis_ratio_Index + 1 
    
    ratioVsCount = [[0] * 2 for i in range(30)]
    ratioVsCount_Index = 0

    # get the frequency of each ratio
    for i in range(0, 30):
        count = 0
        #print(" Y Axis Ratios ===" + str(y_Axis_ratio[i]))
        current_Ratio = y_Axis_ratio[i]
        if current_Ratio != 0 :
            for j in range(0, 30):
                if current_Ratio == (y_Axis_ratio[j]):
                    count = count + 1
            if (ratioVsCount_Index < 30 ):
                ratioVsCount[ratioVsCount_Index][0] = current_Ratio
                ratioVsCount[ratioVsCount_Index][1] = count
                ratioVsCount_Index = ratioVsCount_Index + 1

    # select the ratio which has the max frequency
    max_count = 0
    for i in range(0, 30):
        count = ratioVsCount[i][1]
        if (max_count <= count):
            max_count = count
            # print( " Max Count 8888888888" + str(max_count))
            if ((ratioVsCount[i][0] >= 1)):
                ratio_Of_YAxis = ratioVsCount[i][0]
                # print(" Ratio 88888888" +str(ratio_Of_YAxis))

    ratio_Y_Axis_Value = ratio_Of_YAxis

def main(argv):
    
    global cdstP, src2, cdstP2, cdstP_X_Y, cdstP_Linear, allLines, linesP, arr, X_arr, Y_arr, graphs_arr, noOfLines, origin_X, origin_Y, height, width, filename, src, srcTemplate, resized_img
   
    # Loads an image
    default_file = 'x2.png' 
    filename = argv[0] if len(argv) > 0 else default_file

    # Convert to gray Scale
    # src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE) 
    img = cv.imread(cv.samples.findFile(filename))

    if img is None :
        print(" Cannot Solve this graph")
        return

    i_height = np.size(img, 0)
    i_width = np.size(img, 1)
    resized_img = None
    print (" Width :" + str(i_width) + " height " + str(i_height))

    if(i_height <= 350 and i_width <= 350):
        print(" Resized 1 ")
        r_width = int(350)
        r_height = int(350)
        dim = (r_width, r_height)
        resized_img = cv.resize(img, dim, interpolation = cv.INTER_AREA) 
    elif (i_height <= 650 and i_width <= 900):
        resized_img = img
    else:
        # resize imagex
        print("   Resized //////////////////////////////////////////////////")
        r_width = int(600)
        r_height = int(550)
        dim = (r_width, r_height)
        resized_img = cv.resize(img, dim, interpolation = cv.INTER_AREA) 
  
    src = cv.cvtColor(resized_img, cv.COLOR_BGR2GRAY)

    # Check if image is loaded fine or not
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1 

    src2 = np.copy(src)
    resized = np.copy(src)

    height = np.size(resized, 0)
    width = np.size(resized, 1)
    # print("Image width : " + str(width))
    # print("Image height : " + str(height))
    
    # Edge detection
    #dst = cv.Canny(src, 20, 200, None, 3) 
    dst = cv.Canny(resized, 20, 200, None, 3) 

    cv.imshow("Check Canny", dst)  
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
   
    temSrc = np.copy(src)
    cdstP = np.copy(cdst)
    cdstP_X_Y = np.copy(cdst)
    allLines = np.copy(cdst)  
    cdstP2 = np.copy(cdst)
    cdstP_Linear = np.copy(cdst)
    srcTemplate = np.copy(cdst)
    
    # Get Text
    global result
    result = pytesseract.image_to_string(resized_img)
    print(" Numbers Identify Using OCR  " + str(result))

    if result: 
        # Generate Eqation Using Given Coodinates
        getEqationByUsingCoordinate() 
        # store value cordinate
        getTextCoordinate()
        # if result != "":

    # else:
        # print("Text cannot Read")
     
    # Probabilistic Line Transform
    # linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 0, 10) 
    # linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 4, 15) 
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 25, None, 1, 15) 
    
    
    if linesP is not None: # Check there are lines

        noOfLines = len(linesP) 

        # 1 store value cordinate
        if result != "":
            getTextCoordinate()

        # 2  Draw the lines
        displayAlllines()


        # 3  add mofology
        addMofologyToImage()


        # 4 Store Lines Coordinate
        storeLineCoordinate()
            
        # 5 Separate X axis Y axis and Graphs
        separateX_Y_Graph()

        
        templateMatching()


  
        # 6 x axis
        check_X = indentify_X_Axis_UsingValues()
        print(" Have we fond x axis using text : " + str(check_X))

        # Identify X Axis Considering lenth If X Axis not found using text
        if(check_X != True): 
            check_X_usingTemplateMatching = identify_XAxis_UsingTempalte_Matching()
            print(" Identify X Axis Template ---------->" + str(check_X_usingTemplateMatching))
            if(check_X_usingTemplateMatching != True):
                draw_X_Axis()

        # draw X axis 
        #### print ("X  axis -------------->("+str(arr[X_axis_cordinate][0])+","+str(arr[X_axis_cordinate][1])+")       ("+str(arr[X_axis_cordinate][2])+","+str(arr[X_axis_cordinate][3])+")")
        cv.line(cdstP, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
        cv.line(MofologyImg_2, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
        cv.line(cdstP_X_Y, (arr[X_axis_cordinate][0], arr[X_axis_cordinate][1]), (arr[X_axis_cordinate][2], arr[X_axis_cordinate][3]), (50,0,255), 2, cv.LINE_AA)
        
        # 7 y axis
        check_Y = indentify_Y_UsingValues()
        print(" Have we fond Y axis using text : " + str(check_Y))

        if(check_Y != True): 
            check_Y_usingTemplateMatching = identify_Y_AXis_UsingTempalte_Matching()
            print(" Identify Y Axis Template ---------->" + str(check_Y_usingTemplateMatching))
            if (check_Y_usingTemplateMatching != True):
                # print (" Testing..........................")
                draw_Y_Axis()
        cv.line(cdstP, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
        cv.line(MofologyImg_2, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
        cv.line(cdstP_X_Y, (arr[Y_axis_cordinate][0], arr[Y_axis_cordinate][1]), (arr[Y_axis_cordinate][2], arr[Y_axis_cordinate][3]), (255,128,0), 2, cv.LINE_AA)
        #### print ("Y  axis -------------->("+str(arr[Y_axis_cordinate][0])+","+str(arr[Y_axis_cordinate][1])+")       ("+str(arr[Y_axis_cordinate][2])+","+str(arr[Y_axis_cordinate][3])+")")
        
        # 8 identify origin
        origin()
        
        # 9 identify X axis Ticmarks
        if (pixcelForTicMark_X == 0 ):
            identifyTicMarks_X_Axis() 

        # 10 identify Y axis Ticmarks
        if (pixcelForTicMark_Y == 0):
            identifyTicMarks_Y_Axis() 

        # 11 draw tic mark of Y axis
        draw_TicMark_Y_Axis()

        # 12 draw tic mark of X axis
        draw_TicMark_X_Axis()

        # 13 Check graph is quadratic or Linear
        checkGraph()

        # templateMatching()

        # get the ratio between x and Y axis Values
        if numberOfCharactor > 0:
            identifyNumbersRelated_X_Y_Axis()
 
        seperateTemplateTo_X_Y_Axis()
        if ratio_X_Axis_Value == 1 :
            # print (" Check 555555555555555555555")
            identify_X_Axis_Ratio()

        if ratio_Y_Axis_Value == 1 :
            identify_Y_Axis_Ratio()
        
        print (" Origin Y " + str(origin_Y))
        print(" Ratio Of Number on X Axis = "+str(ratio_X_Axis_Value))
        print(" Ratio Of Number on Y Axis = "+str(ratio_Y_Axis_Value))
        print(" number of pixcles  on X axis " + str(pixcelForTicMark_X))
        print(" number of pixcles  on Y axis " + str(pixcelForTicMark_Y))


        # if graph is a Linear Graph
        if ( graphType == "linear"):
            # Graph
            draw_Graph() 
            # identify X and Y axis intersection point
            identifyIntersection()
            # get real coordinates of y axis and X intersection point without OCR
            if ( pixcelForTicMark_Y !=0 and pixcelForTicMark_X != 0) :
                # getRealCoordianatesWithoutOCR()
                # # generate equation using Image processing without OCR
                # equationIP()
                generateEquationLinearGraph()

        # if graph is a Quadratic Graph
        elif ((graphType == "Quadratic") and (pixcelForTicMark_Y !=0) and (pixcelForTicMark_X != 0)): 
            getQuadraticGraphCoodinates()


        
         
    cv.imshow("Source", src)    
    cv.imshow("Source Template", srcTemplate)  
    cv.imshow("Source", src2) 
    cv.imshow("Source Template", temSrc)
    cv.imshow("X Y Axis", cdstP_X_Y)    
    if ( graphType == "linear"): 
        cv.imshow("Probabilistic Line Transform", cdstP) 
        cv.imshow("Linear graph", cdstP_Linear) 
        cv.imshow("Mofology ", MofologyImg_2) 
    elif (graphType == "Quadratic"): 
        cv.imshow("Mofology ", MofologyImg_2) 
        cv.imshow("Min Max", cdstP2)
        cv.imshow("Probabilistic Line Transform", cdstP) 
        cv.imshow("Edge Detection", cdstP_Linear) 
    cv.imshow("Detected All Lines" , allLines )
    cv.imshow("Source", src)
    cv.waitKey()
    return 0  

    # cv.imshow("Resized image", resized) 
    # cv.imshow("Source", src) 

    #### cv.imshow("Probabilistic Line Transform", cdstP) 
    #### cv.imshow("Min Max", cdstP2) 
    #### cv.imshow("Detected All Lines" , allLines )
    #### cv.waitKey()
    #### return 0  

if __name__ == "__main__":
    main(sys.argv[1:]) 