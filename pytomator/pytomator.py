# -*- coding: UTF-8 -*-
# Copyright (c) 2014 Daniele Ciriello. All Rights Reserved.

# This file is part of PyTomator.

# PyTomator is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation version 2 and no later version.

# PyTomator is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.
#See the GNU General Public License version 2 for more details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc. 51 Franklin
# St, Fifth Floor, Boston, MA 02110-1301 USA.

import time
import LaunchServices
from Cocoa import NSURL
from Quartz import CGImageDestinationCreateWithURL
from Quartz import kCGImagePropertyDPIWidth
from Quartz import kCGImagePropertyDPIHeight
from Quartz import CGImageDestinationAddImage
from Quartz import CGImageDestinationFinalize
from keyboard import PyKeyboard
import Quartz.CoreGraphics as CG
import cv2
from cv2 import cv
import numpy as np
import os

#
keyboard = PyKeyboard()


dpi = 72  # My screen dpi
box = 0, 0, 1680, 1050  # My screen pixles

'''
  .oooooo.                                         .
 d8P'  `Y8b                                      .o8
888      888    oooo  oooo   .oooo.   oooo d8b .o888oo   oooooooo
888      888    `888  `888  `P  )88b  `888""8P   888    d'""7d8P
888      888     888   888   .oP"888   888       888      .d8P'
`88b    d88b     888   888  d8(  888   888       888 .  .d8P'  .P
 `Y8bood8P'Ybd'  `V88V"V8P' `Y888""8o d888b      "888" d8888888P
'''


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
    '''
    This function moves the mouse pixel by pixel
    '''
    current_x, current_y = mouse_position()
    ix = sign(current_x, posx)
    iy = sign(current_y, posy)
    rx = range(int(current_x), int(posx), ix)
    ry = range(int(current_y), int(posy), iy)
    m = max(len(rx), len(ry))
    rx = rx + rx[-1:] * (m - len(rx))
    ry = ry + ry[-1:] * (m - len(ry))

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


def mousedrag_visive(posx, posy):  # TODO
    mouseEvent(CG.kCGEventLeftMouseDragged, posx, posy)


def clickndrag(posx, posy, fposx, fposy):
    mouseclickdown(posx, posy)
    mousedrag(fposx, fposy)
    mouseclickup(fposx, fposy)


def screenshot(path=None, region=None, box=None):
    '''
    region should be a CGRect, something like:

    >>> import Quartz.CoreGraphics as CG
    >>> region = CG.CGRectMake(0, 0, 100, 100)

    The default region is CG.CGRectInfinite (captures the full screen)
    takes a screenshot and save to path if ain't None
    if region is None an entire screenshot is taken
    '''

    if region is None:
        if box is None:
            region = CG.CGRectInfinite
        else:
            if box[2] - box[0] < (box[3] - box[1]) * 1.6:
                region = CG.CGRectMake(box[0], box[1], (
                    box[3] - box[1]) * 1.6, box[3] - box[1])
            else:
                region = CG.CGRectMake(box[0], box[1], box[2] - box[0], (
                    box[2] - box[0]) / 1.6)

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


'''
ooooo      ooo                               ooooooooo.
`888b.     `8'                               `888   `Y88.
 8 `88b.    8  oooo  oooo  ooo. .oo.  .oo.    888   .d88' oooo    ooo
 8   `88b.  8  `888  `888  `888P"Y88bP"Y88b   888ooo88P'   `88.  .8'
 8     `88b.8   888   888   888   888   888   888           `88..8'
 8       `888   888   888   888   888   888   888            `888'
o8o        `8   `V88V"V8P' o888o o888o o888o o888o            .8'
                                                          .o..P'
                                                          `Y8P'
'''


def get_img_array(data):
    '''
    returns nparray so cv2 can call the matchTemplate function
    '''
    pixel_size = len(data) / 4
    nparr = np.fromstring(data, np.uint8)
    nparr = np.reshape(nparr, (-1, 4))
    nparr = np.delete(nparr, 3, 1)

    # it seems there are problems when using a box instead of infinite

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


'''
  .oooooo.                                      .oooooo.   oooooo     oooo
 d8P'  `Y8b                                    d8P'  `Y8b   `888.     .8'
888      888 oo.ooooo.   .ooooo.  ooo. .oo.   888            `888.   .8'
888      888  888' `88b d88' `88b `888P"Y88b  888             `888. .8'
888      888  888   888 888ooo888  888   888  888              `888.8'
`88b    d88'  888   888 888    .o  888   888  `88b    ooo       `888'
 `Y8bood8P'   888bod8P' `Y8bod8P' o888o o888o  `Y8bood8P'        `8'
              888
             o888o
'''


def match(small_image_path, large_image=None, all_matches=None):
    '''
    returns center coordinates of the matched image(s)
    if large_image is none a screenshot is taken
    if all_matches is not none a list of points (x,y) representing the center
    coordinates of all the matched images is returned
    '''
    if os.path.isfile(small_image_path):
        small_image = cv2.imread(small_image_path)
    else:
        raise Exception('Error! File: ' + small_image_path + " not found!")
    # Get the size of the template. This is the same size as the match.
    trows, tcols = small_image.shape[:2]

    if all_matches:
        method = cv2.TM_CCOEFF_NORMED
    else:
        method = cv.CV_TM_SQDIFF_NORMED

    # Get nparray of the screenshot
    if large_image is None:
        large_image = screenshot()

    result = cv2.matchTemplate(small_image, large_image, method)

    if all_matches:
        threshold = 0.7 #953  # reduce this variable to find similiar Templates
        tenthr = 10 * threshold
        loc = np.where(result >= threshold)
        centers = []
        for pt in zip(*loc[::-1]):
            center = [pt[0] + (tcols / 2), pt[1] + (trows / 2)]
            go_on = True
            # if is a duplicate match we don't need it
            for point in centers:
                # check if there is already a neighbor point
                if (((
                        (point[0] + tenthr) > center[0]) and (
                        (point[0] - tenthr) < center[0])) and ((
                        (point[1] + tenthr) > center[1]) and (
                        (point[1] - tenthr) < center[1]))):
                    go_on = False
                    break
            if go_on:
                centers.append(center)
                # test purpose
                cv2.rectangle(large_image, pt,
                              (pt[0] + tcols, pt[1] + trows), (0, 0, 255), 2)
        # test purpose
        #cv2.imshow('output', large_image)
        #cv2.waitKey(0)
        return centers

    # We want the minimum squared difference
    # the get the best match fast use this:
    minx, maxy, min_loc, max_loc = cv2.minMaxLoc(result)

    # Extract the coordinates of our best match
    MPx, MPy = min_loc
    # calculate the center coordinates and return them
    centerx, centery = (MPx + (tcols / 2)), (MPy + (trows / 2))
    return [centerx, centery]


'''
                             o8o
                             `"'
ooo. .oo.  .oo.    .oooo.   oooo  ooo. .oo.
`888P"Y88bP"Y88b  `P  )88b  `888  `888P"Y88b
 888   888   888   .oP"888   888   888   888
 888   888   888  d8(  888   888   888   888
o888o o888o o888o `Y888""8o o888o o888o o888o
'''


# Testing Purpose
if __name__ == '__main__':
    x, y = match("purple.png", all_matches=True)
    mouseclick_visive(x, y)
    time.sleep(1)
    keyboard.press_key('d')
    keyboard.release_key('d')

    # try:
    #     x, y = match("small_image.png")#, all_matches=True)
    #     centers = [(x, y)]
    #     for i in centers:
    #         mouseclick_visive(i[0], i[1])  # x, y)
    # except Exception, e:
    #     print e
