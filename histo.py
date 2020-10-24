"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/23/20
File:       histo.py
"""

import getopt
import sys
import os
import cv2 as cv
import numpy as np


def help():
    print("\t\tHELP")
    print("-m: [m=1] Histogram Equalization [default]")
    print("-m: [m=2] Histogram Matching with image")
    print("-m: [m=3] Histogram Matching with file")


def fileSearch(filename, search):
    # search through files and return path of image
    result = []
    for root, dirs, files in os.walk(search):
        if filename in files:
            result.append(os.path.join(root, filename))
    if len(result) == 0:
        print("Could not find file!")
        sys.exit(0)

    return result[0]


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
        img = cv.imread(img_path, 0)
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


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["help", "method"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    # histogram method
    method = 1

    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit(1)
        elif o in ("-m", "--method"):
            method = int(a)
            if method > 3 or method < 1:
                print("Must use numbers 1 through 3\n")
                help()
                sys.exit(1)
        else:
            assert False, "Unhandled Option!"

    if method == 1:
        equalization(args)
    elif method == 2:
        matching_by_image(args)
    elif method == 3:
        matching_by_file(args)


if __name__ == "__main__":
    main()