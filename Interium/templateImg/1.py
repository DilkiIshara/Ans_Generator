import cv2
import numpy as np
img = cv2.imread("q1.png")

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
src = cv2.imread("\templateImg\x\2.png")
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

