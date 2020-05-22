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


def main(args):
	# first we read the ciphertext
	cipher_text = read_plain(args.input)

	# we also read the initialization vector,
	# remember this is public knowledge so it is not
	# encrypted
	iv = read_plain("iv.txt")

	# now we create cipher instance with the CBC
	# mode of operation, and our initialization vector
	# and the key that is shared between alice and bob
	cipher = AES.new(key, AES.MODE_CBC, iv)

	# now we use the cipher to decrypt our ciphertext
	# and we unpad (remove unecessary bytes that were added
	# to make the message length a multiple of the 
	# block size)
	plain_text = unpad(cipher.decrypt(cipher_text), 16)

	# we may print the output to STDOUT
	action = input("Print the file as a string?[y/n]")
	if action == "y":
		# decode() converts a byte object into a string
		s = plain_text.decode()
		print(s)

	# and we write the output to the value of args.output
	write_encrypted(plain_text, args.output)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Alice-Bob Encryption')
	parser.add_argument('-i', '--input', type=str, help="Path to plain file", required=True)
	parser.add_argument('-o', '--output', type=str, help="Path of encrypted file (should not exist)", required=True)
	args = parser.parse_args()
	main(args)
