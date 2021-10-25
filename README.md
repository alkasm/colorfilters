# colorfilters

Threshold your images in OpenCV's colorspaces.

* BGR (RGB)
* HSV
* HLS (HSL)
* Lab (CIELAB/L\*a\*b\*)
* Luv (L\*u\*v\*)
* YCrCb (YCbCr/YCC)
* XYZ (CIEXYZ)
* Grayscale (single channel)

![Example Image](readme-example.png)

## Getting Started

```sh
$ pip install git+https://github.com/alkasm/colorfilters
```

Run the tool on any image you want:

```sh
$ colorfilter path/to/image.png hsv
```

## Usage

```sh
$ colorfilter --help
usage: test color thresholding of images in different colorspaces
       [-h] image {bgr,hsv,hls,lab,luv,ycc,xyz,gray}

positional arguments:
  image                 path to image
  {bgr,hsv,hls,lab,luv,ycc,xyz,gray}
                        colorspace to filter in

optional arguments:
  -h, --help            show this help message and exit
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
Image filtered in HSV between [51, 0, 183] and [63, 255, 255].
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
