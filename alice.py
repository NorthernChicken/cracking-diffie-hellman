import random

# Alice initiates the exchange so she generates the prime and alpha.
def generate_p():
    p = 1000000007
    return p
def generate_alpha():
    alpha = 5
    return alpha

# Alice picks a secret number (never shared)
def generate_SA():
    SA = random.randint(0, 10000)
    print(f"Alice's secret number: {SA}")
    return SA

# Alice makes a new number (TA) using her secret number
def generate_TA(alpha, SA, p):
    TA = pow(alpha, SA, p)
    print(f"Alice's number (TA): {TA}")
    return TA
# TA and TB are shared, and Eve can see them

# Alice makes the final key
def find_key(TB, SA, p):
    KeyA = pow(TB, SA, p)
    print(f"Alice's final key: {KeyA}")
    return KeyA

'''
Removed extra quotes.
Fixed spelling of "calculate" to "make" in comments.
Used easier f-strings to show text and numbers.
Made sure spacing was even.
Removed extra blank spaces at the end of lines.
Made comments shorter and easier to understand.
I did some formatting and clarity in the script.
'''
