import cv2
import os
import numpy as np
import PIL

#abspath = "/Users/johannpally/Documents/GitHub/HydraBot/vis_processing/hydra_sample_imgs/00049.jpg"
#note we are in the vis_processing folder already
#PIL.Image.open(path)

path = os.getcwd() + "/hydra_sample_imgs/00054.jpg"
img = cv2.imread(path)
c_img = cv2.imread(path)

#==============GEOMETRY MASKS===================
# start result mask with circle mask

ww, hh = img.shape[:2]
r = 173
xc = hh // 2
yc = ww // 2
cv2.circle(c_img, (xc - 10, yc + 2), r, (255, 255, 255), -1)
hsv_cir = cv2.cvtColor(c_img, cv2.COLOR_BGR2HSV)

l_w = np.array([0,0,0])
h_w = np.array([0,0,255])
result_mask = cv2.inRange(hsv_cir, l_w, h_w)

#===============COLOR MASKS====================
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#(hMin = 7 , sMin = 66, vMin = 124), (hMax = 19 , sMax = 255, vMax = 237)
# Threshold of orange in HSV space output from the HSV picker tool
l_orange = np.array([7, 66, 125])
h_orange = np.array([19, 255, 240])
orange_mask = cv2.inRange(hsv_img, l_orange, h_orange)
orange_res = cv2.bitwise_and(img, img, mask = orange_mask)

#===============COMBINE MASKS====================
result_mask &= orange_mask
c_o_res = cv2.bitwise_and(img, img, mask=result_mask)

#===============BOXING============================
# We have to use gray image (1 Channel) to use cv2.findContours
gray = cv2.cvtColor(c_o_res, cv2.COLOR_RGB2GRAY)
contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

minAreaSize = 150
for contour in contours:
    if cv2.contourArea(contour) > minAreaSize:
        #Rectangle Bounding box Drawing Option
        rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        print(x+1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # FINDING CONTOURS CENTERS
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # DRAW CENTERS
        cv2.circle(img, (cX, cY), radius=0, color=(255, 0, 255), thickness=5)

        # DRAW
        cv2.drawContours(img, contour, -1, (0, 255, 0), 1)

#==============DISPLAY========================
cv2.imshow('final result', img)
cv2.imshow('res', c_o_res)
cv2.waitKey(0)
cv2.destroyAllWindows()


#Threshold of black in HSV
#maybe try using in the future
l_black = np.array([0,0,0])
h_black = np.array([360,255,50])
black_mask = cv2.inRange(hsv_img, l_black, h_black)
black_res = cv2.bitwise_and(img, img, mask=black_mask)
