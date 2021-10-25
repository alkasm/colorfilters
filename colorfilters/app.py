import argparse
import cv2 as cv
from .colorfilters import (
    BGRFilter,
    HSVFilter,
    HLSFilter,
    LabFilter,
    LuvFilter,
    YCrCbFilter,
    XYZFilter,
    GrayscaleFilter,
)

CHOICES = {
    "bgr": BGRFilter,
    "hsv": HSVFilter,
    "hls": HLSFilter,
    "lab": LabFilter,
    "luv": LuvFilter,
    "ycc": YCrCbFilter,
    "xyz": XYZFilter,
    "gray": GrayscaleFilter,
}


def app():
    parser = argparse.ArgumentParser(
        description="Theshold images in different colorspaces"
    )
    parser.add_argument("image", help="path to image")
    parser.add_argument(
        "colorspace", choices=list(CHOICES.keys()), help="colorspace to filter in"
    )
    args = parser.parse_args()

    img = cv.imread(args.image)
    if img is None or img.size == 0:
        raise Exception(f"Unable to read image {args.image}. Please check the path.")
    window = CHOICES[args.colorspace](img)

    window.show()
    cv.destroyAllWindows()
