"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       histo_match.py
Description:
IF you provide two images get the Look up tables and then you
create a new look up table that manipulates the specified image
look up table from the occurences of the grayscale intensities
from the reference image look up table and then return the new LUT.

If you provide two look up tables you create a new look up table and
take the features of the reference look up table and update the
specified look up table with the occurences of the reference look up table.
"""

from lookUpTable import get_Lut


def histogramMatch(img1=None, img2=None, LUT1=None, LUT2=None):
    # reused function for histogram matching with file and image
    if img1 is not None and img2 is not None:
        LUT1 = get_Lut(img1)
        LUT2 = get_Lut(img2)
    else:
        LUT1 = LUT1
        LUT2 = LUT2
    # create new map
    new_map = [0 for x in range(256)]

    j = 0
    for i in range(len(LUT1)):
        temp = LUT1[i]
        while True:
            # zero case
            if temp < LUT2[j]:
                if j > 0:
                    j -= 1
                    new_map[i] = j
                    # print(f"gray level {i} ==> original {temp} ==> lut2: {LUT2[j]} ==> {j} ==> new_map[{i}]: {new_map[i]}")
                    j = 0
                    break
            # find next lowest number if temp is not in reference look up table
            elif j == 255 and temp != LUT2[j]:
                j = 0
                temp -= 1
            elif temp == LUT2[j]:
                new_map[i] = j
                # print(f"gray level {i} ==> original {temp} ==> lut2: {LUT2[j]} ==> {j} ==> new_map[{i}]: {new_map[i]}")
                j = 0
                break
            j += 1

    return new_map