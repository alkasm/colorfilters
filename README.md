# colorfilters

Threshold your images in any colorspace!

* BGR (RGB)
* HSV
* HLS (HSL)
* Lab (CIELAB/L\*a\*b\*)
* Luv (L\*u\*v\*)
* YCrCb (YCbCr/YCC)
* XYZ (CIEXYZ)
* Grayscale (single channel)

![Example Image][readme-example.png]

## Getting Started

Install into a Python virtual environment, as you would any other Python project.

```sh
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install git+https://github.com/alkasm/cspaceFilterPython
```

Run the module as a script on any image you want:

```sh
(venv) $ python3 -m colorfilters path/to/image.png hsv
```

## Usage

You can always check the `--help` flag when running the module as a script for more info:

```sh
(venv) $ python3 -m colorfilters --help
```

Use inside your own Python projects:

```python
>>> from colorfilters import HSVFilter
>>> import cv2 as cv
>>> 
>>> img = cv.imread("lane.jpg")
>>> window = HSVFilter(img)
>>> window.show()
>>> 
>>> print(f"Image filtered in HSV between {window.lowerb} and {window.upperb}.")
```

The window object has a few properties you might be interested in after successfully filtering your image:

```python
>>> window.lowerb     # lower bound used for cv.inRange()
>>> window.upperb     # upper bound used for cv.inRange()
>>> window.mask       # mask from cv.inRange()
>>> window.masked     # image with mask applied
>>> window.img        # image input into the window
>>> window.converted  # image converted into the corresponding colorspace
```