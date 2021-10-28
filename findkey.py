#!/usr/bin/env python
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import padding
import binascii

# Get the key from the first command line argument, should be file with a single
# line.  Strip the newline character if there is any. Encode the plaintext to
# bytes-like object with utf-8.  plaintext_bytes will be used with the
# cryptography library function.
plaintext_file = open(sys.argv[1], 'r')
plaintext = plaintext_file.readline()
plaintext.strip('\n')
plaintext_bytes = plaintext.encode('utf-8')

# Get the ciphertext as a string from the command line.  Convert the string to
# a bytes-like object using unhexlify from the binascii library.
ciphertext = sys.argv[2]
ciphertext_bytes = binascii.unhexlify(ciphertext)

# initialize the padder for padding the plaintext
padder = padding.PKCS7(128).padder()
padded_plaintext = padder.update(plaintext_bytes)
padded_plaintext += padder.finalize()


# Fill the initialization vector with 16 zero bytes.
iv = b'\x00' * 16

# Open the file to be used as a list of words, read into words
words_file = open(sys.argv[3], 'r')
words = words_file.readlines()

# Iterate through the words list
for word in words:
    # Get a word from the list of words, remove the newline
    key = word.strip('\n')

    # Only use words that are less that 16 letters
    if len(key) < 16:
        # Pad the key with spaces (ASCII values 32 or 0x20)
        for i in range(0, (16 - len(key))):
            key += '\x20'
        # Encode the key so it can be used with Cipher()
        key_bytes = str.encode(key)

        # Encrypt the plaintext with the key, store the resulting ciphertext
        # as ctext
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend)
        encryptor = cipher.encryptor()
        ctext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Compare the ciphertext encoded with the key from the words list
        # (ctext) to the ciphertext we provided in the commandline
        # (ciphertext_bytes)
        if (ctext == ciphertext_bytes):
            # if equal, we found the key. Print it and exit the loops.
            print("FOUND! key: " + str(ctext))

            # Check that ctext will decrypt into the plaintext.  This is more
            # of a sanity check for myself.
            decryptor = cipher.decryptor()
            decrypted_ctext = decryptor.update(ctext) + decryptor.finalize()

            assert decrypted_ctext.strip() == plaintext
            break;


