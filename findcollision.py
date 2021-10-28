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

	if (collision_type == 'w'):
		print("Looking for " + str(trials) + " weak collisions")
	elif (collision_type == 's'):
		print("Looking for " + str(trials) + " strong collisions")
		
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

			# Search for weak collisions
			if (collision_type == 'w'):
				if m_hash_str[0:3] == hash_str[0:3]:
					print("Found weak collision: " + str(hash_str[0:3]))
					print("Trials: " + str(i))
					results.append(i)
					break
			# Search for strong collisions
			elif (collision_type == 's'):
				if (m_hash_str[0:3] == hash_str[0:3]) and (string_to_hash != guess):
					print("Found strong collision: " + str(hash_str[0:3]))
					print("Trials: " + str(i))
					print("Original string: " + str(string_to_hash[0:3]))
					print("Collision string: " + str(guess[0:3]))
					results.append(i)
					break
	
	print("Found " + str(len(results)) + "/" + str(trials) + " collisions")
	print(results)
	print("Average number of trials: " + str(sum(results) / len(results)))	
	

def main():	
	# specify what collision type to look for
	collision_type = sys.argv[1]
	# specify how many collisions to look for
	num_trials = int(sys.argv[2])
	# specify how many times ot guess for each collision
	num_guesses = int(sys.argv[3])
	# specify the string length to use to generate the hash
	str_len = int(sys.argv[4])
	find_collision(num_trials, collision_type, num_guesses, str_len)

if __name__=="__main__":
	main()
