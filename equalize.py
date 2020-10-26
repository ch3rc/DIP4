"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       equalize.py
Description:
Feed an image to equalization() function and get equalized
histogram look up table. Update the image with the equalized
look up table.
"""

import cv2 as cv
import sys
import numpy as np
from files import fileSearch
from lookUpTable import get_Lut


def equalization(args):
    if len(args) > 1:
        print("Too many arguments, only need one image name!")
        sys.exit(1)
    elif len(args) <= 0:
        print("Too few arguments, need an image!")
        sys.exit(1)

    image_name = args[0]
    search = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"

    # get absolute path of image
    image = fileSearch(image_name, search)

    try:
        img = cv.imread(image, cv.IMREAD_GRAYSCALE)
    except cv.error as err:
        print(err)
        sys.exit(1)

    # get equalized histogram look up table
    LUT = get_Lut(img)
    R, C = img.shape[:2]
    new_image = np.zeros((R, C), dtype="uint8")

    # fill new image with correlated LUT values
    for i in range(R):
        for j in range(C):
            new_image[i][j] = LUT[img[i][j]]

    try:
        cv.imshow("orginal image", img)
        cv.imshow("equalized image", new_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
    except cv.error as err:
        print(err)
        sys.exit(1)
