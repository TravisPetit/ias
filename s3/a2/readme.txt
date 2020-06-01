A2:
ab-encrypt/decrypt are not information theoretically secure. A cipher is information theoretically secure if it is impossible to decrypt its ciphertext without having the secret key(s), even with an unlimited amount of computational power. It is easy to see that this is not the case here, an attacker could just go over all of the possible secret keys and try to use AES to decrypt the message, if the output is gibberish, disregard it and continue, otherwise they would be done.

Authenticity is not guaranteed, after decrypting the message, everything Bob gets is the plaintext Alice sent her. Since Alice did not add a signature to her text, and since AES does not create one automatically, Authenticity is not guaranteed.
In Order to guarantee it, one solution could be to use another approach like AEAD where the text would get signed, so Bob would either know 1: Alice wrote the text or 2: the signature does not match the text, so some attacker tried to edit it, and it is not Alice‘s text anymore.

Confidentiality is not fully guaranteed, because ab-encrypt uses ECB, so if 2 messages are identical, this is reflected directly in the ciphertext, and this can be used to reverse-engineer some critical data from the ciphertext (as we have showed with the penguin image on ex. 1). A solution for this would be to use a safer mode of operation like the galois counter mode or CBC.

Reliable Delivery is not guaranteed in ab-encrypt  because in symmetric cryptography the receiver also has the same secret key, so there's no way for the receiver to prove that the sender and not the receiver signed the message.
The solution depends on whether the shared key is public or not. If the parties agree to a public source (third party) for their shared key there is non-repudiation of origin, so in that case asymmetric cryptography could be used to guarantee a reliable delivery.

In terms of data and network security integrity is guaranteed, as symmetric cryptography used in ab-encrypt uses one key, assures that the information can only be accessed or modified by those authorized to do so.
Information cannot be altered in storage, or in transit between the sender and
the intended receiver, without the alteration being detected. 







