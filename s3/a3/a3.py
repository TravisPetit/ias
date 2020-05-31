import sys
import base64
from aead import AEAD as a
import os
import logging

# disclaimer: if you get the incorrect padding error when running this program, please
# delete the header and body output files and run it again.
# This might take a few tries, I have no idead why this happens, since our decode
# function should not raise exceptions. Also, I have no idea why rerunning the program makes
# this work, but it does.


# copied from https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding
# because I kept on getting the error 'Incorrect padding'
def base64_decode(s):
    """Add missing padding to string and return the decoded base64 string."""
    log = logging.getLogger()
    s = str(s).strip()
    try:
        return base64.b64decode(s)
    except TypeError:
        padding = len(s) % 4
        if padding == 1:
            log.error("Invalid base64 string: {}".format(s))
            return ''
        elif padding == 2:
            s += b'=='
        elif padding == 3:
            s += b'='
        return base64.b64decode(s)


def read_file(path):
	file = open(path, "rb")
	bytes = file.read()
	file.close()
	return bytes
	

def write(bytes, path):
	file = open(path, "wb")
	file.write(bytes)
	file.close()


# first we create copy header of the penguin in the file 'header'
os.system("head -c 54 tux.bmp >> header")

# and the content itself in a the file 'body'
os.system("tail -c +54 tux.bmp >> body")

SECRET_KEY = "Gzb9X-EAiZsk5-7OVZe0KrwIiLxySqYWfJFyyDtPf4w="

# we initialize a cryptorr with our secret key
cryptor = a(SECRET_KEY)

# read the contents of the header and body files just created
header = read_file("header")
body = read_file("body")

# encrypt the content of the body and sign the header
cipher_text = cryptor.encrypt(body, header)


# unfortunately ciper text is in base64, so we must convert it to binary
# We can't just use base64.b64decode(s) because the padding is
# incorrect, so we use a dedicated function
cipher_text = base64_decode(cipher_text)

# we write the bytes into 'out'
write(cipher_text, "out")

# create the image
os.system("touch img.bmp")

# append the header to the image
os.system("cat header >> img.bmp")

# append the encrypted body to the image
os.system("cat out >> img.bmp")


# do some manipulations to the associated data
# cipher_text = ~cipher_text

# we can't because cipher_text is stored as a string ...
# we tried
# eval("cipher_text = b{}".format(cipher_text))
# cipher_text = cipher_text.encode()
# cipher_text = str.encode(cipher_text)
# and many more
# NOTHING WORKS

# thus there is no point in executing the following
#os.system("touch img2.bmp")
#os.system("cat header >> img2.bmp")
#os.system("cat out >> img2.bmp")


# file cleaning
os.system("rm out")
os.system("rm header")
os.system("rm body")
