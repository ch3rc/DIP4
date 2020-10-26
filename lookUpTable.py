"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       lookUpTable.py
Description:
Feed an image to get_lut() function and get an equalized
histogram look up table.
"""


def get_Lut(image):
    # made LUT its own function so i could reuse it for the
    # other histogram functions.
    transformation = [0 for x in range(256)]
    LUT = [0 for x in range(256)]

    R, C = image.shape[:2]
    # get counts of unique pixel values
    for i in range(R):
        for j in range(C):
            transformation[image[i][j]] += 1

    # equalize pixel values and place in Look Up Table
    for i in range(len(transformation)):
        transformation[i] = transformation[i] / image.size
        if i > 0:
            transformation[i] += transformation[i - 1]

    for i in range(len(transformation)):
        LUT[i] = int(transformation[i] * 255)

    return LUT