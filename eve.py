import random

# Eve can generate all the same numbers as Bob and Alice.

def generate_p():
    p = 1000000007
    return p
def generate_alpha():
    alpha = 5
    return alpha

def generate_SE():
    SE = random.randint(0, 10000)
    print(f"Eve's secret number: {SE}")
    return SE

def generate_TE(alpha, SE, p):
    TE = pow(alpha, SE, p)
    print(f"Eve's number (TE): {TE}")
    return TE

# In this case, T could be either Alice's TA or Bob's TB.
def find_key(T, SE, p):
    KeyE = pow(T, SE, p)
    print(f"Eve's final key: {KeyE}")
    return KeyE

'''
Removed extra quotes.
Fixed spelling of "calculate" to "make" in comments.
Used easier f-strings to show text and numbers.
Made sure spacing was even.
Removed extra blank spaces at the end of lines.
Made comments shorter and easier to understand.
I did some formatting and clarity in the script.
'''
