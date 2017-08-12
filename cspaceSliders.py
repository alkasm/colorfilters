import argparse
import cv2
import numpy as np
import cspaceThreshImg


"""Globals"""


# variable
redisplay = False

# constants
CSPACE_LABELS = ['BGR', 'HSV', 'HLS', 'Lab', 'Luv', 'YCrCb', 'XYZ', 'Gray']
STROKE_FONT = ((5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 5)
LABEL_FONT = ((5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 0], 2)


"""Private helper functions"""


def __set_redisplay(x):
    """Called whenever a trackbar position is moved.

    Sets the global variable redisplay to True.
    """
    global redisplay
    redisplay = True


def __initialize_sliders(window_name):
    """Initializes the trackbars"""
    cv2.resizeWindow(window_name, 600, 25)

    # Define trackbar names (NOTE: see known issues in README)
    bar_start = [0, 0, 100, 0, 100, 0, 100]
    bar_end = [7, 100, 100, 100, 100, 100, 100]
    bars = ['Switch space', 'Ch 1 min ', 'Ch 1 max  ',
            'Ch 2 min', 'Ch 2 max', 'Ch 3 min', 'Ch 3 max']
    for i in range(0, 7):
        cv2.createTrackbar(bars[i], window_name, bar_start[i], bar_end[i], __set_redisplay)

    return bars


def __initialize_font():
    pass


def __multi_window(img):
    """Display mask, applied mask, and filtering trackbars in three windows."""

    # initialize window and trackbars
    mask_window = "Binary mask"
    masked_window = "Masked image"
    slider_window = "Thresholding ranges"
    cv2.namedWindow(mask_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(masked_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(slider_window, cv2.WINDOW_NORMAL)
    sliders = __initialize_sliders(slider_window)

    # initializations
    cspace = 0
    mask = np.ones(img.shape[:2], dtype=np.uint8)
    masked_img = img
    global redisplay

    # display window with trackbar values that can be changed
    print('Exit with [q] or [esc].')
    while(True):

        # display the image
        redisplay = False
        cv2.imshow(mask_window, mask)
        cv2.imshow(masked_window, masked_img)
        k = cv2.waitKey(200) & 0xFF  # large wait time to remove freezing
        if k == 113 or k == 27:
            break

        # get positions of the sliders
        slider_pos = [cv2.getTrackbarPos(sliders[i], slider_window)
                      for i in range(0, 7)]
        cspace = slider_pos.pop(0)  # take the colorspace value out

        # update threshold image
        if redisplay:  # global variable; modified on trackbar position change
            mask, _, _, _ = cspaceThreshImg.main(
                img, CSPACE_LABELS[cspace], slider_pos)
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            cv2.putText(mask, CSPACE_LABELS[cspace], *STROKE_FONT)  # outline
            cv2.putText(mask, CSPACE_LABELS[cspace], *LABEL_FONT)   # text

    cv2.destroyAllWindows()

    return cspace, slider_pos


def __uni_window(img):
    """Display mask, applied mask, and filtering trackbars in one window."""

    # initialize window and trackbars
    window = "Mask and Applied Mask with Thresholding"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    sliders = __initialize_sliders(window)

    # initializations
    cspace = 0
    h, w = img.shape[:2]
    mask = np.ones((h, w), dtype=np.uint8) * 255
    masked_img = img
    combo_img = np.zeros((h, 2*w, 3), dtype=np.uint8)
    global redisplay

    # display window with trackbar values that can be changed
    print('Exit with [q] or [esc].')
    while(True):

        # display the image
        redisplay = False

        combo_img[:h, :w] = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
        combo_img[:h, w:2*w] = masked_img
        cv2.imshow(window, combo_img)
        k = cv2.waitKey(200) & 0xFF  # large wait time to remove freezing
        if k == 113 or k == 27:
            break

        # get positions of the sliders
        slider_pos = [cv2.getTrackbarPos(sliders[i], window)
                      for i in range(0, 7)]
        cspace = slider_pos.pop(0)  # take the colorspace value out

        # update threshold image
        if redisplay:  # global variable; modified on trackbar position change
            mask, _, _, _ = cspaceThreshImg.main(
                img, CSPACE_LABELS[cspace], slider_pos)
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            cv2.putText(mask, CSPACE_LABELS[cspace], *STROKE_FONT)  # outline
            cv2.putText(mask, CSPACE_LABELS[cspace], *LABEL_FONT)   # text

    cv2.destroyAllWindows()

    return cspace, slider_pos


"""Main public function"""


def display(img, multi_window=False):
    """Public function to display the image and filtering trackbars.

    Parameters
    ----------
    img : array_like
        image to filter/threshold.
    multi_window: bool, optional
        when set to True, displays image, applied mask, and trackbars
        each in separate windows at full size; when False (default),
        resizes the image by half until it is under 600x600 and
        displays in a single window with trackbars on the top.

    Returns
    -------
    mask : ndarray
        single channel binary image, same size as input `img`, where
        white (255) corresponds to that pixel being inside the bounds
        defined by the trackbars, and black (0) is outside the bounds.
    masked_img : ndarray
        the mask applied to the input `img`
    cspace : string
        colorspace the mask was produced in
    lowerb : uint8
        three lower bound trackbar values as a list
    upperb : uint8
        three upper bound trackbar values as a list
    """

    h, w = img.shape[:2]

    # create windows
    if multi_window:
        # run with full size images
        cspace, slider_pos = __multi_window(img)
    else:
        # resize image until it's under 600x600
        max_h, max_w = 600, 600
        rsz_img = img
        while (h > max_h) or (w > max_w):
            rsz_img = cv2.pyrDown(rsz_img)
            h, w = rsz_img.shape[:2]
        cspace, slider_pos = __uni_window(rsz_img)

    # return a new thresholded image, full size, without label
    mask, cspace, lowerb, upperb = cspaceThreshImg.main(
        img, CSPACE_LABELS[cspace], slider_pos)
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    return mask, masked_img, cspace, lowerb, upperb

