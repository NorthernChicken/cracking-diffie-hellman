import random
'''
Converting to Python because Go sucks
'''

# Alice announces these, Eve intercepts them before passing them to Bob.
p = 1000000007
alpha = 5

# Alice and Bob choose SA and SB respectively (secret, never transmitted)
SA = random.randint(0, 10000)
print("Alice's secret is: " + str(SA))
SB = random.randint(0, 10000)
print("Bob's secret is: " + str(SB))

# Alice and Bob caluclate TA and TB respecitvely based on alpha, p, and their secret number.
TA = pow(alpha, SA, p)
print("TA calculated by Alice is: " + str(TA))
TB = pow(alpha, SB, p)
print("TB calculated by Bob is: " + str(TB))
# These values TA and TB are sent to each other (and pass through Eve first, who can manipulate them)

# Alice calculates the shared key.
KeyA = pow(TB, SA, p)
print("Alice calculates the shared key to be: " + str(KeyA))
# Bob does the same on his end. These steps aren't visible to Eve.
KeyB = pow(TA, SB, p)
print("Bob calculates the shared key to be: " + str(KeyB))

KeysMatch = KeyA == KeyB
print("Do the keys match? " + str(KeysMatch))