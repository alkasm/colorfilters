import abc
from functools import partial
import cv2 as cv
import numpy as np


MIN_SUFFIX = " min"
MAX_SUFFIX = " max"


class BaseFilter(abc.ABC):
    """Base class for filter window.

    Implement the abstract methods/properties to use the class.
    """

    @staticmethod
    @abc.abstractmethod
    def converter(img):
        pass

    @property
    @abc.abstractmethod
    def channel_names(self):
        pass

    @property
    @abc.abstractmethod
    def channel_mins(self):
        pass

    @property
    @abc.abstractmethod
    def channel_maxes(self):
        pass

    def __init__(self, img, name="Filter Window"):
        self.name = name
        self.img = img.copy()
        self.converted = self.converter(img)
        self.lowerb = np.array(self.channel_mins)
        self.upperb = np.array(self.channel_maxes)

    def _update_lowerb(self, channel, pos):
        self.lowerb[channel] = pos
        self._update()

    def _update_upperb(self, channel, pos):
        self.upperb[channel] = pos
        self._update()

    def _update(self):
        """Update the image inside the window."""
        self.mask = cv.inRange(self.converted, self.lowerb, self.upperb)
        self.masked = cv.bitwise_and(self.img, self.img, mask=self.mask)
        cv.imshow(self.name, self.masked)

    def _initialize_window(self):
        """Create the window and add trackbars."""
        cv.namedWindow(self.name)
        for i, (chname, min_, max_) in enumerate(
            zip(self.channel_names, self.channel_mins, self.channel_maxes)
        ):
            cv.createTrackbar(
                chname + MIN_SUFFIX,
                self.name,
                min_,
                max_,
                partial(self._update_lowerb, i),
            )
            cv.setTrackbarMin(chname + MIN_SUFFIX, self.name, min_)
            cv.createTrackbar(
                chname + MAX_SUFFIX,
                self.name,
                max_,
                max_,
                partial(self._update_upperb, i),
            )
        self._update()

    def show(self):
        """Draw the filter window. This method is blocking."""
        self._initialize_window()
        while True:
            print("Press [q] or [esc] to close the window.")
            k = cv.waitKey() & 0xFF
            if k in (ord("q"), ord("\x1b")):
                cv.destroyWindow(self.name)
                break


class BGRFilter(BaseFilter):
    converter = staticmethod(lambda img: img)
    channel_names = ("B", "G", "R")
    channel_mins = (0, 0, 0)
    channel_maxes = (255, 255, 255)


class HSVFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2HSV))
    channel_names = ("H", "S", "V")
    channel_mins = (0, 0, 0)
    channel_maxes = (180, 255, 255)


class HLSFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2HLS))
    channel_names = ("H", "L", "S")
    channel_mins = (0, 0, 0)
    channel_maxes = (180, 255, 255)


class LabFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2Lab))
    channel_names = ("L", "a", "b")
    channel_mins = (0, 1, 1)
    channel_maxes = (255, 255, 255)


class LuvFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2Luv))
    channel_names = ("L", "u", "v")
    channel_mins = (0, 1, 1)
    channel_maxes = (255, 255, 255)


class YCrCbFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2YCrCb))
    channel_names = ("Y", "Cr", "Cb")
    channel_mins = (0, 0, 0)
    channel_maxes = (255, 255, 255)


class XYZFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2XYZ))
    channel_names = ("X", "Y", "Z")
    channel_mins = (0, 0, 0)
    channel_maxes = (255, 255, 255)


class GrayscaleFilter(BaseFilter):
    converter = staticmethod(partial(cv.cvtColor, code=cv.COLOR_BGR2GRAY))
    channel_names = ("L",)
    channel_mins = (0,)
    channel_maxes = (255,)
