import cv2
import numpy as np
import uuid  # for unique filenames

# constants
CSPACE_LABELS = ['BGR', 'HSV', 'HLS', 'Lab',
                 'Luv', 'YCrCb', 'XYZ', 'Grayscale']
CONVERT_CODES = {'HSV': cv2.COLOR_BGR2HSV, 'HLS': cv2.COLOR_BGR2HLS,
                 'Lab': cv2.COLOR_BGR2Lab, 'Luv': cv2.COLOR_BGR2Luv,
                 'YCrCb': cv2.COLOR_BGR2YCrCb, 'XYZ': cv2.COLOR_BGR2XYZ,
                 'Grayscale': cv2.COLOR_BGR2GRAY}


class FilterWindow:

    def __init__(self, name, image):

        # general params
        self.name = name
        self.image = image          # displayed image; modify this
        self._image = image.copy()  # input image; don't modify

        # parameters for thresholding
        self._lowerb = np.array([0, 0, 0])
        self._upperb = np.array([255, 255, 255])
        self.cspace = 'BGR'
        self.mask = 255 * np.ones(image.shape[:2], dtype=np.uint8)
        self.applied_mask = image.copy()
        self.display_mask = False

    def _initialize_window(self, cspace):
        cv2.namedWindow(self.name)

        # Define trackbar names (NOTE: see known issues in README)
        trackbar_names = ['Ch 1 min ', 'Ch 1 max', 'Ch 2 min  ',
                          'Ch 2 max ', 'Ch 3 min ', 'Ch 3 max']
        start_vals = [0, 255, 0, 255, 0, 255]
        max_vals = [255, 255, 255, 255, 255, 255]

        # lambdas used because createTrackbar only wants the handle of a single
        # parameter function (passing the position), but want to send more info
        cv2.createTrackbar(
            trackbar_names[0], self.name, start_vals[0], max_vals[0],
            lambda pos: self._update_lowerb(pos, 0))
        cv2.createTrackbar(
            trackbar_names[1], self.name, start_vals[1], max_vals[1],
            lambda pos: self._update_upperb(pos, 0))
        cv2.createTrackbar(
            trackbar_names[2], self.name, start_vals[2], max_vals[2],
            lambda pos: self._update_lowerb(pos, 1))
        cv2.createTrackbar(
            trackbar_names[3], self.name, start_vals[3], max_vals[3],
            lambda pos: self._update_upperb(pos, 1))
        cv2.createTrackbar(
            trackbar_names[4], self.name, start_vals[4], max_vals[4],
            lambda pos: self._update_lowerb(pos, 2))
        cv2.createTrackbar(
            trackbar_names[5], self.name, start_vals[5], max_vals[5],
            lambda pos: self._update_upperb(pos, 2))

    def _update_lowerb(self, pos, channel):
        if channel == 0 and (self.cspace == 'HSV' or self.cspace == 'HLS'):
            self._lowerb[channel] = int(179*pos/255)
        else:
            self._lowerb[channel] = pos

        self._update_window()

    def _update_upperb(self, pos, channel):
        if channel == 0 and (self.cspace == 'HSV' or self.cspace == 'HLS'):
            self._upperb[channel] = int(179*pos/255)
        else:
            self._upperb[channel] = pos

        self._update_window()

    def _update_window(self):
        if self.cspace == 'Grayscale':
            lowerb, upperb = int(self._lowerb[0]), int(self._upperb[0])
            self.mask = cv2.inRange(self.image, lowerb, upperb)
        else:
            self.mask = cv2.inRange(self.image, self._lowerb, self._upperb)

        self.applied_mask = cv2.bitwise_and(
            self._image, self._image, mask=self.mask)

        if self.display_mask:
            cv2.imshow(self.name, self.mask)
        else:
            cv2.imshow(self.name, self.applied_mask)

    def _flip_mask_display(self):
        self.display_mask = not self.display_mask
        self._update_window()
        if self.verbose:
            if self.display_mask:
                print('Displaying mask')
            else:
                print('Displaying applied mask')

    def _cspace_change(self, cspace):
        if self.cspace not in ['HSV', 'HLS'] and cspace in ['HSV', 'HLS']:
            # changing *into* HSV/HLS
            self._lowerb[0] = int(179*self._lowerb[0]/255)
            self._upperb[0] = int(179*self._upperb[0]/255)
        elif self.cspace in ['HSV', 'HLS'] and cspace not in ['HSV', 'HLS']:
            # changing *out of* HSV/HLS
            self._lowerb[0] = int(255*self._lowerb[0]/179)
            self._upperb[0] = int(255*self._upperb[0]/179)

        if cspace == 'BGR':
            self.image = self._image
        else:
            self.image = cv2.cvtColor(self._image, CONVERT_CODES[cspace])
        self.cspace = cspace
        self._update_window()

        if self.verbose:
            print('Thresholding in', cspace)

    def _print_bounds(self):
        if self.cspace == 'Grayscale':
            print('Lower bound:', self._lowerb[0])
            print('Upper bound:', self._upperb[0])
        else:
            print('Lower bounds:', self._lowerb)
            print('Upper bounds:', self._upperb)

    def _save(self):

        if self.display_mask:
            filename = 'mask_' + uuid.uuid1().hex + '.png'
            cv2.imwrite(filename, self.mask)
        else:
            filename = 'applied_mask_' + uuid.uuid1().hex + '.png'
            cv2.imwrite(filename, self.applied_mask)
        if self.verbose:
            print('Saved image as', filename)

    def _close(self):
        if self.verbose:
            print('Closing window')
            print('\n--------------------------------------')
            print('Colorspace:', self.cspace)
            if self.cspace == 'Grayscale':
                print('Lower bound:', self._lowerb[0])
                print('Upper bound:', self._upperb[0])
            else:
                print('Lower bounds:', self._lowerb)
                print('Upper bounds:', self._upperb)
            print('--------------------------------------\n')

        cv2.destroyWindow(self.name)

    @property
    def bounds(self):
        if self.cspace == 'Grayscale':
            return [self._lowerb[0], self._upperb[0]]
        return [self._lowerb, self._upperb]

    @property
    def colorspace(self):
        return self.cspace

    def show(self, verbose=False):
        # create window, trackbars, and event callbacks
        self._initialize_window(self.cspace)
        self.verbose = verbose

        print('Press [1] thru [8] (inclusive) to switch between colorspaces')
        if verbose:
            print('    [1]: BGR    [2]: HSV      [3]: HLS    [4]: Lab')
            print('    [5]: Luv    [6]: YCrCb    [7]: XYZ    [8]: Grayscale')
        print('Press [m] to switch between displaying mask and applied mask')
        print('Press [b] to print current lower and upper bounds')
        print('Press [s] to save the currently displayed image')
        print('Press [q] or [esc] to close the window')
        print('------------------------------------------------------------\n')
        if verbose:
            print('Thresholding in BGR')
            print('Displaying applied mask')

        # display the image and wait for a keypress or trackbar change
        cv2.imshow(self.name, self.applied_mask)
        while(True):

            k = cv2.waitKey() & 0xFF
            if k == ord('q') or k == 27:  # 27 is [esc]
                self._close()
                break
            elif k == ord('m'):
                self._flip_mask_display()
            elif k == ord('b'):
                self._print_bounds()
            elif k == ord('s'):
                self._save()
            elif k in range(ord('1'), ord('9')):  # [1, 8] inclusive
                cspace = CSPACE_LABELS[k-49]  # 1-8 are 49-57 on kbd input
                self._cspace_change(cspace)
