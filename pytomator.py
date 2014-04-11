# -*- coding: UTF-8 -*-
import time
import LaunchServices
from Cocoa import NSURL
from Quartz import CGImageDestinationCreateWithURL
from Quartz import kCGImagePropertyDPIWidth
from Quartz import kCGImagePropertyDPIHeight
from Quartz import CGImageDestinationAddImage
from Quartz import CGImageDestinationFinalize
import Quartz.CoreGraphics as CG
import cv2
from cv2 import cv
import numpy as np

dpi = 72  # My screen dpi
box = 0, 0, 1680, 1050  # My screen pixles


def get_img_array(data):
    '''
    returns nparray so cv2 can call the matchTemplate function
    '''
    pixel_size = len(data) / 4
    nparr = np.fromstring(data, np.uint8)
    nparr = np.reshape(nparr, (-1, 4))
    nparr = np.delete(nparr, 3, 1)

    if box[2] - box[0] < (box[3] - box[1]) * 1.6:
        nparr = np.reshape(
            nparr, (box[3] - box[1], pixel_size / (box[3] - box[1]), 3))
        nparr = nparr[0:box[3] - box[1], 0:box[2] - box[0]]
    else:
        nparr = np.reshape(
            nparr, ((box[2] - box[0]) / 1.6, pixel_size / (
                box[2] - box[0]) * 1.6, 3))
        nparr = nparr[0:box[3] - box[1], 0:box[2] - box[0]]
    return nparr


def screenshot(path=None, region=None):
    '''
    takes a screenshot and save to path if ain't None
    if region is None an entire screenshot is taken
    '''

    if region is None:
        region = CG.CGRectInfinite

    # Create screenshot as CGImage
    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)

    if not path:

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        _data = CG.CGDataProviderCopyData(prov)

        # Get width/height of image
        #width = CG.CGImageGetWidth(image)
        #height = CG.CGImageGetHeight(image)

        return get_img_array(_data)

    url = NSURL.fileURLWithPath_(path)

    dest = CGImageDestinationCreateWithURL(
        url,
        LaunchServices.kUTTypePNG,  # file type
        1,  # 1 image in file
        None
    )

    properties = {
        kCGImagePropertyDPIWidth: dpi,
        kCGImagePropertyDPIHeight: dpi,
    }

    # Add the image to the destination, characterizing the image with
    # the properties dictionary.
    CGImageDestinationAddImage(dest, image, properties)

    # When all the images (only 1 in this example) are
    # added to the destination,
    # finalize the CGImageDestination object.
    CGImageDestinationFinalize(dest)


def mouse_position():
    return CG.CGEventGetLocation(CG.CGEventCreate(None))


def mouseEvent(type, posx, posy):
    theEvent = CG.CGEventCreateMouseEvent(
        None, type, (posx, posy), CG.kCGMouseButtonLeft)
    CG.CGEventPost(CG.kCGHIDEventTap, theEvent)


def mousemove(posx, posy):
    mouseEvent(CG.kCGEventMouseMoved, posx, posy)

def sign(n1, n2):
    if n1 < n2:
        return 1
    else:
        return -1

def mousemove_visive(posx, posy):
    current_x, current_y = mouse_position()
    ix = sign(current_x, posx)
    iy = sign(current_y, posy)
    rx = range(int(current_x), int(posx), ix)
    ry = range(int(current_y), int(posy), iy)
    m  = max(len(rx), len(ry))
    rx = rx + rx[-1:]*(m-len(rx))
    ry = ry + ry[-1:]*(m-len(ry))

    for x, y in zip(rx, ry):
        mouseEvent(CG.kCGEventMouseMoved, x, y)
        time.sleep(0.001)
    mousemove(posx, posy)


def mouseclick(posx, posy):
    mouseEvent(CG.kCGEventLeftMouseDown, posx, posy)
    mouseEvent(CG.kCGEventLeftMouseUp, posx, posy)


def mouseclick_visive(posx, posy):
    mousemove_visive(posx, posy)
    mouseclick(posx, posy)


def mouseclickdown(posx, posy):
    mouseEvent(CG.kCGEventLeftMouseDown, posx, posy)


def mouseclickup(posx, posy):
    mouseEvent(CG.kCGEventLeftMouseUp, posx, posy)


def mousedrag(posx, posy):
    mouseEvent(CG.kCGEventLeftMouseDragged, posx, posy)


def mousedrag_visive(posx, posy):
    mouseEvent(CG.kCGEventLeftMouseDragged, posx, posy)


def clickndrag(posx, posy, fposx, fposy):
    mouseclickdown(posx, posy)
    mousedrag(fposx, fposy)
    mouseclickup(fposx, fposy)


def match(small_image_path, large_image=None):
    '''
    returns center coordinates of the matched image
    if large_image is none a screenshot is taken
    '''
    st = time.time()
    small_image = cv2.imread(small_image_path)
    method = cv.CV_TM_SQDIFF_NORMED

    # Get nparray of the screenshot
    if not large_image:
        large_image = screenshot()

    large_image = large_image
    small_image = small_image
    result = cv2.matchTemplate(small_image, large_image, method)
    print 'secs: ', time.time() - st
    # We want the minimum squared difference
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    # Extract the coordinates of our best match
    MPx, MPy = mnLoc

    # Get the size of the template. This is the same size as the match.
    trows, tcols = small_image.shape[:2]

    centerx, centery = (MPx + (tcols / 2)), (MPy + (trows / 2))

    return centerx, centery


if __name__ == '__main__':
    # Capture full screen
    # screenshot("testscreenshot_full.png")

    # Capture region (100x100 box from top-left)
    # region = CG.CGRectMake(0, 0, 100, 100)
    # screenshot("testscreenshot_partial.png", region=region)

    x, y = match("small_image.png")
    mouseclick_visive(x, y)
