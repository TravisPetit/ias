#!/bin/bash

# script that converts the output of the encryption tool into an image

# save the first 54 bytes of the file tux.bmp
# into a new file called image.bmp
head -c 54 tux.bmp >> image.bmp

# save all but the first 54 bytes of the output
# file (MUST BE CALLED output) into
# the file body
tail -c +54 output >> body

# append the body to the end of the image
cat body >> image.bmp

#delete the body file
rm body
