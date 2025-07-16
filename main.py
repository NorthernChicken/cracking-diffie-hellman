import random

# Alice shares these numbers, but Eve can see them.
p = 1000000007
alpha = 5

# Alice and Bob each pick a secret number (never shared)
# F-strings allows you to format strings quicker instead of the format() method.
SA = random.randint(0, 10000)
print(f"Alice's secret number: {SA}")
SB = random.randint(0, 10000)
print(f"Bob's secret number: {SB}")

# Alice and Bob make new numbers (TA and TB) using their secret numbers. 
# "Pow" function is used to calculate the power of a number. pow(base, exponent)
TA = pow(alpha, SA, p)
print(f"Alice's number (TA): {TA}")
TB = pow(alpha, SB, p)
print(f"Bob's number (TB): {TB}")
# These numbers (TA and TB) are shared, and Eve can see them

# Alice creates the final key
KeyA = pow(TB, SA, p)
print(f"Alice's final key: {KeyA}")
# Bob creates the final key, Eve can't see this
KeyB = pow(TA, SB, p)
print(f"Bob's final key: {KeyB}")

# Check if the keys are the same
KeysMatch = KeyA == KeyB
print(f"Are the keys the same? {KeysMatch}")

'''
What was fixed?

Removed extra quotes.
Fixed spelling of "calculate" to "make" in comments.
Used easier f-strings to show text and numbers.
Even spacing.
Removed extra blank spaces at the end of lines.
Made comments shorter and easier to understand.
Fixed formatting and clarity issues in the script.

'''
