from colorfilters import *
import cv2 as cv
import argparse

choices = {
    "bgr": BGRFilter,
    "hsv": HSVFilter,
    "hls": HLSFilter,
    "lab": LabFilter,
    "luv": LuvFilter,
    "ycrcb": YCrCbFilter,
    "xyz": XYZFilter,
    "gray": GrayscaleFilter,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="path to image")
    parser.add_argument(
        "colorspace", choices=list(choices.keys()), help="colorspace to filter in"
    )
    args = parser.parse_args()

    img = cv.imread(args.image)
    if img is None or img.size == 0:
        raise Exception(f"Unable to read image {args.image}. Please check the path.")
    window = choices[parser.colorspace]()
    window.show()
