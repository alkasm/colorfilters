import cspaceSliders
import cspaceThreshImg
import cv2
import numpy as np

img = cv2.imread('lane.jpg')

mask, masked_img, cspace_label, lowerb, upperb = cspaceSliders.display(img, multi_window=False)

cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.imshow("Applied Mask", masked_img)
cv2.waitKey(0)

print(
    '\nColorspace:', cspace_label,
    '\nLower bound:', lowerb,
    '\nUpper bound:', upperb)