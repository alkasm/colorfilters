import cspaceSliders
import cv2

img = cv2.imread('lane.jpg')
blur = cv2.GaussianBlur(img, (5,5), 1)

out_img, cspace_label, lowerb, upperb = cspaceSliders.display(img)

cv2.imshow("Output", out_img)
cv2.waitKey(0)
out_path = 'output.png'
cv2.imwrite(out_path, out_img)

print('Output:', out_path,
    '\nColorspace:', cspace_label,
    '\nLower bound:', lowerb,
    '\nUpper bound:', upperb)