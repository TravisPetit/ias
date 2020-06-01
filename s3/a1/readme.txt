Open this new file with an image viewer. What is noticeable? How can this be explained?

Observation: The penguin’s outline can still be seen in the new cipher image formed.

Explanation: You have a cipher, that with a key will encrypt 16 bytes of data. And you have some data, that is more than 16 bytes. By using ECB as a mode of encryption
each 16-bytes plaintext block is directly encrypted into a ciphertext block, independently of any other block.
Meaning that under a given key, each identical block of a plaintext gives an identical block of a ciphertext. Which leads to ciphertexts containing some patterns, exposing frequency of symbols in your plaintext.

