"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       match_by_file.py
Description:
Read in 256 grayscale intensity probability numbers and create LUT.
Use newly created LUT to transform image to equalized histogram from
LUT.
"""

import sys
import cv2 as cv
from files import fileSearch
from file_match import readAndMatch


def matching_by_file(args):
    if len(args) == 0:
        print("No files provided!")
        sys.exit(1)
    elif len(args) < 2:
        print("Need both image path and normalized histogram path!")
        sys.exit(1)
    elif len(args) > 2:
        print("Too many arguments provided!")
        sys.exit(1)

    image_name = args[0]
    histogram_file = args[1]
    search = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"

    # get absolute file paths of image and normalized histogram text file
    img_path = fileSearch(image_name, search)
    histogram_path = fileSearch(histogram_file, search)

    try:
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    except cv.error as err:
        print(err)
        sys.exit(1)

    # get matched histogram image
    matched_image = readAndMatch(img, histogram_path)

    try:
        cv.imshow("orginal image", img)
        cv.imshow("matched image", matched_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
    except cv.error as err:
        print(err)
        sys.exit(1)