import cv2
import numpy as np
import pytesseract
from PIL import Image
import sys
import math
import cv2 as cv
import numpy as np
import pytesseract
from .pytesseract import image_to_string
 
 default_file = 'g1.jpg'
    filename = argv[0] if len(argv) > 0 else default_file

    # Loads an image
    img = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    #img = cv2.imread('line.jpg')
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    # cv2.imwrite(src_path + "removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    # cv2.imwrite(src_path + "thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open("line.jpg"))

    print("hhhhh" + result)
    # Remove template file
    #os.remove(temp)

    #return result


print ("--- Start recognize text from image ---")
#print get_string('D:/4th - Project/Interium/line.jpg')

print ("------ Done -------")