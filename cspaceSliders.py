import argparse
import cv2
import numpy as np
import cspaceThreshImg



__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"



"""Global variable"""



REDISPLAY = False



"""Private helper functions"""



def __set_redisplay(x):
    """Called whenever a trackbar position is moved.
    
    Sets the global variable REDISPLAY to True.
    """
    global REDISPLAY
    REDISPLAY = True

    pass


def __initialize_window():
    """Initializes the window and trackbars"""
    window = 'Thresholded Image' # create window
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)

    # Define trackbar names (NOTE: see TRACKBAR BUG at the bottom of this file)
    bar_start = [0,0,100,0,100,0,100]
    bar_end = [7,100,100,100,100,100,100]
    bars = ['Switch space','Ch 1 min ','Ch 1 max  ','Ch 2 min','Ch 2 max','Ch 3 min','Ch 3 max']
    for i in range(0,7):
        cv2.createTrackbar(bars[i], window, bar_start[i], bar_end[i], __set_redisplay)

    return window, bars



"""Main public function"""



def display(img):
    """Public function to display the image and color thresholding trackbars."""

    # initialize window and trackbars
    window, sliders = __initialize_window()

    # create colorspace labels to be displayed
    cspace_labels = {0:'BGR',1:'HSV',2:'HLS',3:'Lab',4:'Luv',5:'YCrCb',6:'XYZ',7:'Gray'}
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    fontcolor = [0,0,0] # black text
    strokecolor = [255,255,255] # stroke around the text

    # initializations
    cspace = 0 # starting in BGR
    disp_img = img # display the original image until a trackbar has been changed
    global REDISPLAY

    # display window with trackbar values that can be changed
    print('Exit with [q] or [esc].')
    while(True):

        # display the image
        REDISPLAY = False
        cv2.imshow(window, disp_img)
        k = cv2.waitKey(200) & 0xFF # large wait time to remove freezing
        if k == 113 or k == 27:
            break

        # get positions of the sliders
        slider_pos = [cv2.getTrackbarPos(sliders[i], window) for i in range(0,7)]
        cspace = slider_pos.pop(0) # take the colorspace value out of the positions

        # update threshold image
        if REDISPLAY: # global variable which is modified when a trackbar position moves
            disp_img,_,_,_ = cspaceThreshImg.main(img, cspace_labels[cspace], slider_pos)

            cv2.putText(disp_img, cspace_labels[cspace], (5,30), fontface, 1, strokecolor, 5) # outline
            cv2.putText(disp_img, cspace_labels[cspace], (5,30), fontface, 1, fontcolor, 2) # text

    cv2.destroyAllWindows()

    # return a new thresholded image without label
    out_img, cspace, lowerb, upperb = cspaceThreshImg.main(img, cspace_labels[cspace], slider_pos)

    return out_img, cspace, lowerb, upperb

