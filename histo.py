"""
Author:     Cody Hawkins
Class:      CS5420
Date:       10/23/20
File:       histo.py
"""

import getopt
import sys
from equalize import equalization
from match_image import matching_by_image
from match_by_file import matching_by_file


def help():
    print("\t\tHELP")
    print("-m: [m=1] Histogram Equalization [default]")
    print("-m: [m=2] Histogram Matching with image")
    print("-m: [m=3] Histogram Matching with file")


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