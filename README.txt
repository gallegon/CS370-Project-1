to run findkey:

if findkey.py is given execute permission

$> chmod u+x findkey.py
$> ./findkey.py [plaintext filename] [ciphertext string] [word list filename]

without giving findkey.py execute permission
$> python findkey.py [plaintext filename] [ciphertext string] [word list filename]

example:
$> ./findkey.py plaintext 8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9 words.txt

***NOTE***: Find collision runs heinously slow, expect up to 10 minutes per
trial on flip.  I would recommend running on a local machine.  It took ~30 mins
on my local machine to attempt to find 10 weak collisions and ~15 mins to
attempt to find 10 strong collisions.  I can do a live demo on my machine if
needed -- email me: gallegon@oregonstate.edu I can demostrate that it does work
properly on my machine.  Looking back, coding this in C would have been the
faster solution. My writeup contains my results.

to run findcollision.py:

if findcollision.py is given execute permission:

$> chmod u+x findcollision.py
$> ./findcollision.py [collision type] [num_trials] [num_guesses] [string length]

collsion type is 'w' for weak collision and 's' for strong collision
num_trials is the number of collsions to find with a random hash input
num_guesses is the number of guesses per hash input
string length is the length of the hash input to use (will be a random
alpha-numeric string)

example:
$> ./findcollision.py w 10 20000000 5
-- attempt to find 10 weak collisions with 20000000 guesses per hash and
-- hash input length 5

$> ./findcollision.py s 20 30000000 5
-- attempt to find 20 strong collisions with 30000000 guesses per hash and
-- hash input length 5
