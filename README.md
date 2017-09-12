## cspaceFilter
Python module to quickly test colorspace thresholding values on color images.

## files
    .gitignore          ignore all images other than the example `lane.jpg`
    LICENSE             MIT License
    README.md           this file
    cspaceSliders.py    module containing FilterWindow class that displays the thresholded image with sliders
    example.py          an example of how you might use the functions
    lane.jpg            an included example image; try filtering out the sky or obtaining the lane lines
    
## use

    import cv2
    from cspaceSliders import FilterWindow
    image = cv2.imread('lane.jpg')
    window = FilterWindow('Filter Window', image)
    window.show(verbose=True)

While the window is showing, there is a number of keyboard shortcuts to change the thresholding operations and to modify what's being displayed:

Press <kbd>1</kbd> thru <kbd>8</kbd> (inclusive) to switch between colorspaces.  
Colorspaces: <kbd>1</kbd>: BGR, <kbd>2</kbd>: HSV, <kbd>3</kbd>: HLS    <kbd>4</kbd>: Lab, <kbd>5</kbd>: Luv, <kbd>6</kbd>: YCrCb, <kbd>7</kbd>: XYZ, <kbd>8</kbd>: Grayscale  
Press <kbd>m</kbd> to switch between displaying mask and applied mask  
Press <kbd>b</kbd> to print current lower and upper bounds  
Press <kbd>s</kbd> to save the currently displayed image  
Press <kbd>q</kbd> or <kbd>esc</kbd> to close the window

The class properties are updated during `.show()` and if you want to grab them after closing the window (or during window display) you can get the current colorspace, upper and lower bounds, mask, and applied mask with:

    colorspace = window.colorspace
    lowerb, upperb = window.bounds
    mask = window.mask
    applied_mask = window.applied_mask
    
Lastly, the `.show()` method has an optional argument, `verbose` which is `False` by default. A value of `True` will print out every time the displayed image is switched from `mask` to `applied_mask`, will print every time the colorspace is changed, and will print the colorspace and bounds when the image is closed. A value of `False` still prints instructions when the image is first displayed, but doesn't print any more after that (unless <kbd>b</kbd> is pressed to print the current bounds).

## web app
With another friend, I am currently developing a web application to do the same thing but through your browser (locally as well as on the internet) for a nicer interface and easy use for all who might not be using Python. Additionally trackbars sometimes get placed in a weird order (see known issues below), so the slider script could be annoying to use. Finally, OpenCV does not have a robust UI at all---it only has the bare minimum. The web app will enable much better interactivity. You can check out the current working version [here](https://alkasm.github.io/cspaceFilter/). The interface isn't finished yet, but it works.

## known issues
Depending on your build of OpenCV, the sliders (trackbars) get placed in a weird order. This is a [known bug](https://github.com/opencv/opencv/issues/5056). For those with the issue, ordering of them is somehow dependant on their name. I've added a couple spaces to some of my trackbar names to get them in a satisfactory order on my machine---I have no idea if others with this issue will have them in my same order or not. If not, at least the trackbars are labeled.

If the image height is larger than your screen resolution (minus the trackbar size, and window borders), then the trackbars will be displayed on top of your image. Simply resize the image before sending it through, and double check that they work on the larger image after by using the `lowerb` and `upperb` return values with `cv2.inRange(image, lowerb, upperb)`.

## possible updates
Morphological operations such as erosion, dilation, opening, or closing are often done in-tandem with colorspace range thresholding to remove spurious bits. It would be nice to include views of these steps along with the thresholding since they also have tunable parameters (height and width of the kernel, number of iterations). However, it seems difficult to implement as these are often done in different orders. This might be easier to complete for a browser-based implementation.

## contribute
Please report any errors you find, and open a pull request if you fix. Alternatively, if you would like to port these scripts to another language which uses OpenCV, please feel free to do so.

Thank you!
