import cv2
import numpy as np
img = cv2.imread("q2.png")

# [gray]
# Transform source image to gray if it is not already
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
if len(img.shape) != 2:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
else:
    gray_img = img

# template = cv2.imread("1.png", cv2.IMREAD_GRAYSCALE)
# [gray]
# Transform source image to gray if it is not already 

# create array to store Images(template)
# templates = np.arange()
templates = [[0] * 2 for i in range(12)]

# # assign value to 0
# for h in range(0, i+1):
#     distance[h] = 0

templates[0][0] = "c0.png"
templates[0][1] = 0

templates[1][0] = "c1.png"
templates[1][1] = 1

templates[2][0] = "c2.png"
templates[2][1] = 2

templates[3][0] = "c3.png"
templates[3][1] = 3

templates[4][0] = "c4.png"
templates[4][1] = 4

templates[5][0] = "c5.png"
templates[5][1] = 5

templates[6][0] = "c6.png"
templates[6][1] = 6

templates[7][0] = "c7.png"
templates[7][1] = 7

templates[8][0] = "c8.png"
templates[8][1] = 8

templates[9][0] = "c9.png"
templates[9][1] = 9

templates[10][0] = "c10.png"
templates[10][1] = 10

templates[11][0] = "c20.png"
templates[11][1] = 20

img2 = templates[11][0]
print(" Image " + img2)

for i in range(0 , 12):
    curretTemplate = templates[i][0]
    src = cv2.imread(curretTemplate)
    if len(src.shape) != 2:
        template = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    else:
        template = src

    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.7)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

cv2.imshow("img", img)
# gaussianRemove=cv2.GaussaianBlur(Image,(5,5),0)
# noiseRemove = cv2.fastNlMeansDenoising(Image,None,10,7,21)
cv2.waitKey(0)
cv2.destroyAllWindows()

