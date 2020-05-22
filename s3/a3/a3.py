import sys
import base64
from aead import AEAD as a
import os
import logging

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


os.system("head -c 54 tux.bmp >> header")
os.system("tail -c +54 tux.bmp >> body")

cryptor = a("Gzb9X-EAiZsk5-7OVZe0KrwIiLxySqYWfJFyyDtPf4w=")

header = read_file("header")
body = read_file("body")

cipher_text = cryptor.encrypt(body, header)
cipher_text = base64_decode(cipher_text)

write(cipher_text, "out")
os.system("touch img.bmp")
os.system("cat header >> img.bmp")
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


os.system("rm out")
os.system("rm header")
os.system("rm body")
