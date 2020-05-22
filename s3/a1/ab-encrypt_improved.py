#!/bin/python3

import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from base64 import b64encode
from Crypto.Random import get_random_bytes

block_size = 16

# We now use a 32-byte long key
# this is the safest variant of the AES algorithm
# the longer the key, the safer the algorithm
key = b"b\x12\xcf\xc4\x87\x1e\x00\x99RF\xa1l\xf1\x17Q\x90\x08'\xcb\x94P\x90Ja\xb88\xea\x86\x9d\xda\x8d3"


def read_plain(path):
	file = open(path, "rb")
	bytes = file.read()
	file.close()
	return bytes


def write_encrypted(bytes, path):
	file = open(path, "wb")
	file.write(bytes)
	file.close()


# we now use CBC mode instead of ECB
# we already mentioned the problems of ECB
# CBC fiexes that where every output of an
# encryption block gets masked to the the input
# of the next encryption block: that way no
# 2 identical inputs yield identical outputs
# ECB works as follows
#
#   m1        m2
#   |         |
#   |         |
#  AES       AES    ...
#   |         |
#   |         |
#   c1        c2
#
# So if m1 == m2 then c1 == c2, this is NOT GOOD
# so CBC fixes this as follows
#
#   m1
#   |
#   |
#  AES    m2
#   |     |
#   |     v
#   c1-->XOR   ...
#         |
#         v
#        AES
#         |
#         |
#         c2
#
# There is also the problem that if two distinct ciphertext message
# have the same first amout of header bytes, then m1 of plaintext 1
# m1 of plaintext 2 are yield the same c1. This is what iv is for
# and is explained below
#
def encrypt(padded_data):
	# this is the initialization vector,
	# it is the vector that gets XOR'd with the
	# first block of the chain and only then it is
	# entered as an input to AES
	# the reason this is used is to make it
	# such that no two first messages
	# generate the same output, since that could
	# be used to reverse engineer some of
	# the plaintext.
	# Of course this is only needed for the first
	# message, since all the other ones
	# are masked with the result of the previous AES
	# output
	# it is very important for iv to be random
	# it is also public knowledge, so it is just printed
	# in STDOOUT and saved in the file iv.txt
	iv = get_random_bytes(16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	output = cipher.encrypt(padded_data)
	write_encrypted(iv, "iv.txt")
	print("using iv = {}".format(iv))
	return output


def main(args):
	plain_text = read_plain(args.input)
	padded_plain_text = pad(plain_text, block_size)

	cipher_text = encrypt(padded_plain_text)
	write_encrypted(cipher_text, args.output)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Alice-Bob Encryption')
	parser.add_argument('-i', '--input', type=str, help="Path to plain file", required=True)
	parser.add_argument('-o', '--output', type=str, help="Path of encrypted file (should not exist)", required=True)
	args = parser.parse_args()
	main(args)
