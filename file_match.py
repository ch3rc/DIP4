"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       file_match.py
Description:
Read in normalized histogram probabilites and convert to
equalized histogram and insert into LUT and add features
to specified image.
"""

from lookUpTable import get_Lut
from histo_match import histogramMatch
import numpy as np


def readAndMatch(image, file):
    # get normalized histogram
    with open(file, "r") as f:
        nums = f.readlines()
        real_nums =[]
        for i in range(len(nums)):
            real_nums.append(float(nums[i].strip("\n")))
    f.close()

    # get original image look up table
    LUT1 = get_Lut(image)
    # equalize normalized histogram
    LUT2 = [0 for x in range(256)]
    for i in range(len(real_nums)):
        if i > 0:
            real_nums[i] += real_nums[i - 1]

    for i in range(len(real_nums)):
        LUT2[i] = int(real_nums[i] * 255)

    # histogram matching
    matched_histogram = histogramMatch(LUT1=LUT1, LUT2=LUT2)

    # insert new values into image for histogram matched image
    R, C = image.shape[:2]
    new_image = np.zeros((R, C), dtype="uint8")

    for i in range(R):
        for j in range(C):
            new_image[i][j] = matched_histogram[image[i][j]]

    return new_image