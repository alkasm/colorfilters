## cspaceThresh
Python scripts to quickly test colorspace thresholding values on color images.

## files
    .gitignore          ignore all images other than the example  `lane.jpg`
    README.md           this file
    cspaceSliders.py    script that displays the thresholded image with sliders
    cspaceThreshImg.py  script that runs the thresholding operations
    example.py          an example of how you might use the functions
    lane.jpg            an included example image; try filtering out the sky or obtaining the lane lines
    
## use
The script `cspaceSliders.py` is the main script to include and use for your own images. Simply `import cspaceSliders` in your script and pass your `image` into the provided function `cspaceSliders.display(image)`. This function gives four outputs: the thresholded image, the colorspace used for thresholding, and the lower bounds and upper bounds of the thresholding operation. The full use line would be `binary_image, colorspace, lower_bound, upper_bound = cspaceSliders.display(image)`.

The keys `[q]` and `[esc]` will close the window with sliders and will send the output through to your variables.

The script `cspaceThreshImg.py` is simply used as a subroutine for `cspaceSliders.py` and simply contains functions to threshold the image in different colorspaces and modify the slider values into the proper ranges for that colorspace.

## web app
With another friend, I am currently developing a web application to do the same thing but through your browser (locally as well as on the internet) for a nicer interface and easy use for all who might not be using Python. Additionally [trackbars sometimes get placed in a weird order](https://github.com/opencv/opencv/issues/5056), so the slider script could be annoying to use. You can check out the current status of the repo [here](https://github.com/alkasm/cspaceThreshWeb).

## contribute
Please report any errors you find, and open a pull request if you fix. Alternatively, if you would like to port these scripts to another language which uses OpenCV, please feel free to do so and open a pull request!

## known issues
Depending on your build of OpenCV, the sliders (trackbars) get placed in a weird order. This is a [known bug](https://github.com/opencv/opencv/issues/5056). For those with the issue, ordering of them is somehow dependant on their name. I've added a couple spaces to some of my trackbar names to get them in a satisfactory order on my machine---I have no idea if others with this issue will have them in my same order or not. If not, at least the trackbars are labeled.

If the image height is larger than your screen resolution (minus the trackbar size, and window borders), then the trackbars will be displayed on top of your image. Simply resize the image before sending it through `cspaceSliders.display(image)` to find good values, and double check that they work on the larger image after by using the `lowerb` and `upperb` return values with `cv2.inRange(image, lowerb, upperb).
