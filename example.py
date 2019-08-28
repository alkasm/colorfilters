from colorfilters import HSVFilter
import cv2 as cv

img = cv.imread("lane.jpg")
window = HSVFilter(img)
window.show()

print(f"Image filtered in HSV between {window.lowerb} and {window.upperb}.")
