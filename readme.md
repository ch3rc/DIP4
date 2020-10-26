##How to run
___
python3 histo.py [-h, --help] -[m 1,2, or 3] [img_file] [img_file or histogram_probabilities]
___
- -h --help: brings up a help message
- -m --sampling_method: 1, 2 or 3 [default: 1]
    - Equalized Histogram: Provide an image and return equalized version of image [method: 1]
    - Histogram Matching: Provide specified image and reference image and return specified image with equalized histogram of reference image [method: 2]
    - Histogram Matching By File: Read in a file of 256 normalized probabilities and convert to equalized histogram and return specified image with equalized histogram features [method: 3]
___
##Known issues
___
No Known issues at this time
___
##links
___
- [github](www.https://github.com/ch3rc/DIP4 "github account") for code and logs under master branch
- contact me at my [UMSL email](ch3rc@umsystem.edu) if you have any questions