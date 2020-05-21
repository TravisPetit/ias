#!/bin/python3

import argparse
from Crypto.Cipher import AES               # requires 'pycrypto' package
from Crypto.Util.Padding import pad, unpad  # requires 'pycrypto' package

#AES is a block cipher, setting the block size to 16 means that ...
block_size = 16           


# AES is also a symmetric cipher, key contrais the secret key, which is ...
key = b'!pre-shared-key!'


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

	# we set the mode of operation to ECB, this means that ...
	cipher = AES.new(key, AES.MODE_ECB)

	# we read the input bytes from a plaintext file
	plain_text = read_plain(args.input)

	# then we pad it such that it is fit for 'block_size'
	# this means that we add some redundant bits at the
	# end of the file until the number of bytes in the file
	# is a factor of block size.
	# so for instance if the block size is 5 bits,
	# but the message is 12 bits long, we add 3 redundant bits
	# at the end, that way we can divide the text into
	# 3 whole blocks when performing AES.
	# we want to split this in blocks because ...
	padded_plain_text = pad(plain_text, block_size)

	# we are now ready to encrypt the message
	# the cipher.encrypt method takes the padded_plain_text
	# as an input and returns ...
	cipher_text = cipher.encrypt(padded_plain_text)

	# which is then written to the file whose name is the
	# value of args.output
	write_encrypted(cipher_text, args.output)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Alice-Bob Encryption')
	parser.add_argument('-i', '--input', type=str, help="Path to plain file", required=True)
	parser.add_argument('-o', '--output', type=str, help="Path of encrypted file (should not exist)", required=True)
	args = parser.parse_args()
	main(args)
