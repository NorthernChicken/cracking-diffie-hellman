# bob.py
import random

# Bob picks a secret number (never shared)
def generate_SB():
    SB = random.randint(0, 10000)
    print(f"Bob's secret number: {SB}")
    return SB

# Bob makes a new number (TB) using his secret number
def generate_TB(alpha, SB, p):
    TB = pow(alpha, SB, p)
    print(f"Bob's number (TA): {TB}")
    return TB
# These numbers (TA and TB) are shared, and Eve can see them

# Bob makes the final key
def find_key(TA, SB, p):
    KeyB = pow(TA, SB, p)
    print(f"Bob's final key: {KeyB}")
    return KeyB
# Bob makes the final key too, Eve can't see this

'''
Removed extra quotes.
Fixed spelling of "calculate" to "make" in comments.
Used easier f-strings to show text and numbers.
Made sure spacing was even.
Removed extra blank spaces at the end of lines.
Made comments shorter and easier to understand.
I did some formatting and clarity in the script.
'''
