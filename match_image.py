"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       match_by_image.py
Description:
Provide two images and feed to histogramMatch() function.
Get LUT's for both images and used reference image LUT to
update specified LUT and return to give specified image
features of reference image.
"""

import sys
import cv2 as cv
import numpy as np
from files import fileSearch
from histo_match import histogramMatch


def matching_by_image(args):
    if len(args) <= 1:
        print("Please provide two images!")
        sys.exit(1)
    elif len(args) > 2:
        print("Too many images provided!")
        sys.exit(1)

    img_to_transform_path = args[0]
    ref_image_path = args[1]
    search = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"

    # get absolute path to images
    img_to_transform = fileSearch(img_to_transform_path, search)
    ref_image = fileSearch(ref_image_path, search)

    try:
        img_2_trans = cv.imread(img_to_transform, cv.IMREAD_GRAYSCALE)
        ref_img = cv.imread(ref_image, cv.IMREAD_GRAYSCALE)
    except cv.error as err:
        print(err)
        sys.exit(1)

    # get matched histogram look up table
    new_LUT = histogramMatch(img1=img_2_trans, img2=ref_img)
    R, C = img_2_trans.shape[:2]
    new_image = np.zeros((R, C), dtype="uint8")

    for i in range(R):
        for j in range(C):
            new_image[i][j] = new_LUT[img_2_trans[i][j]]
    try:
        cv.imshow("original image", img_2_trans)
        cv.imshow("reference image", ref_img)
        cv.imshow("matched image", new_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
    except cv.error as err:
        print(err)
        sys.exit(1)
