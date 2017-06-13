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

# web app
With another friend, I am currently developing a web application to do the same thing but through your browser (locally as well as on the internet) for a nicer interface and easy use for all. You can check out the current status of the repo [here](https://github.com/alkasm/cspaceThreshWeb).
