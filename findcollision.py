#!/usr/bin/env python

import sys
import string
import random
import struct

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl.backend import backend

# Print a random string with uppercase and digits of length str_len
def random_string(str_len):
    char_array = string.ascii_uppercase + string.digits
    rand_str = ""
    for i in range(str_len):
        rand_str += random.choice(char_array)
    return rand_str
    #print(string.ascii_uppercase)

# find either a weak or strong collision decided by "collision_type" parameter
def find_collision(trials, collision_type, guesses, str_len):
    results = []

    for i in range(trials):
        # Create a random string for each trial.
        string_to_hash = random_string(str_len).encode('utf-8')

        # Using an MD5 hash because it has a short (128 bit) space
        mhash = hashes.Hash(hashes.MD5(), backend)
        m_hash_str = mhash.update(string_to_hash)
        m_hash_str = mhash.finalize()
        print(m_hash_str[0:3])

        # Guess integers, convert to bytes.  This assures that all combinations
        # of bytes form 0-guesses are covered (in theory)
        for i in range(guesses):
            # convert the integer to bytes using struct.pack()
            guess = struct.pack("<l", i)

            # Initialize Hash object
            mhash_guess = hashes.Hash(hashes.MD5(), backend)
            # Create a hash of the raw bytes.
            hash_str = mhash_guess.update(guess)
            hash_str = mhash_guess.finalize()

            if (collision_type == 'w'):
                # Weak collision
                if m_hash_str[0:3] == hash_str[0:3]:
                    print("Found weak collision: " + hash_str[0:3])
                    print("Trials: " + str(i))
                    break
            elif (collision_type == 's'):
                # Strong collision
                if (m_hash_str[0:3] == hash_str[0:3]) and (string_to_hash != guess):
                    print("Found strong collision: " + hash_str[0:3])
                    print("Trials: " + str(i))
                    print("Original string: " + string_to_hash[0:3])
                    print("Collision string: " + guess[0:3])
                    break

def main():
    find_collision(1, 'w', 20000000, 5)

if __name__=="__main__":
    main()
guesses = {}
