#!/bin/python3

import argparse
from Crypto.Cipher import AES               # requires 'pycrypto' package
from Crypto.Util.Padding import pad, unpad  # requires 'pycrypto' package

# AES is a block cipher; As symmetric cryptography is subdivided into types based on
# the amount of information it can encrypt or decrypt at a time, Block cipher is one of the types in which it
# divides the plaintext into blocks of bits and uses a specially constructed function 
# which mixes a block of the plaintext with the secret key to produce a block of the ciphertext.
# Block ciphers operate with a fixed transformation on large blocks of plaintext data.
# Therefore, they operate on blocks of fixed length data (in this code length is 16 bits).
# Since the plaintext to be encrypted can be of any length, there are encryption modes that are
# used for encrypting messages larger than the block size (such as ECB and CBC).
block_size = 16           

# AES is a symmetric cipher, In symmetric cryptography or private-key cryptography, the same key is used for both
# encryption and decryption. This means that the encryption key must be shared between the two parties before any messages can be decrypted. 
# Symmetric cryptography can be used to transmit information over an insecure public channel and ensures strong mutual authentication.
# Key must be exchanged with the receivers every time the key is changed for encryption. So, the key is not changed often.
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

	# We set the mode of encryption to Electronic codebook mode (ECB). In this mode, a plaintext is divided into fixed size blocks 
	# each of the plaintext blocks is directly encrypted into a ciphertext block, independently of any other block.
	# This enables parallelism in encrypting the plaintext blocks and decrypting the ciphertext blocks,
	# which yields high performance.
	cipher = AES.new(key, AES.MODE_ECB)

	# we read the input bytes from a plaintext file. The message to be encrypted is called a plaintext 
	plain_text = read_plain(args.input)

	# then we pad it such that it is fit for 'block_size'
	# this means that we add some redundant bits at the
	# end of the file until the number of bytes in the file
	# is a factor of block size.
	# so for instance if the block size is 5 bits,
	# but the message is 12 bits long, we add 3 redundant bits
	# at the end, that way we can divide the text into
	# 3 whole blocks when performing AES.
	padded_plain_text = pad(plain_text, block_size)

	# we are now ready to encrypt the message
	# the cipher.encrypt method takes the padded_plain_text
	# as an input and and the output of the encryption process is called a ciphertext.
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
