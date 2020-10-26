"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/26/20
File:       files.py
Description:
Provide fileSearch() function with the name of the file you wish
to search for and a starting patch. The function will return the
full path for the specified file if it exists.
"""

import os
import sys


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