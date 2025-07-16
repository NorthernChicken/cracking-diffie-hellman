# main.py
import alice, bob, eve

# Alice: 'Hey Bob, let's do Diffie Hellman! Here is a large prime and a primitive root mod that prime!'
p = alice.generate_p()
alpha = alice.generate_alpha()

# Alice: 'I'm going to generate a secret number... you do too.'
SA = alice.generate_SA()

# Eve, pretending to be Bob: 'OK, I generated a secret number.'
SE_with_Alice = eve.generate_SE()

# Eve, pretending to be Alice: 'Hey Bob, let's do Diffie Hellman! Here is a large prime and a primitive root mod that prime!'
p_eve = eve.generate_p()
alpha_eve = eve.generate_alpha()

# Eve, pretending to be Alice: 'Let's generate secret numbers, Bob'
SE_with_Bob = eve.generate_SE()

# Bob, thinking he's talking to Alice: 'OK'
SB = bob.generate_SB()

# Eve says to both Alice and Bob: 'Generate your T value and give me it so we can create a shared key.'
# Eve also generates two seperate keys for each of them.
TE_with_Alice = eve.generate_TE(alpha, SE_with_Alice, p)
TE_with_Bob = eve.generate_TE(alpha, SE_with_Bob, p)

TA = alice.generate_TA(alpha, SA, p)
TB = bob.generate_TB(alpha, SB, p)

# Eve pretending to be Alice: 'Alright Bob, here is my TE. Give me your TB and we can make a shared key.'
KeyE_with_Bob = eve.find_key(TB, SE_with_Bob, p)

# Eve pretending to be Bob: 'Alright Alice, here is my TE. Give me your TA and we can make a shared key.'
KeyE_with_Alice = eve.find_key(TA, SE_with_Alice, p)

# Alice and Bob each find the key on their ends:
KeyA = alice.find_key(TE_with_Alice, SA, p)
KeyB = bob.find_key(TE_with_Bob, SB, p)

KeysMatch = KeyA == KeyB
print(f"Do Alice and Bob's keys match? {KeysMatch}")
# They shouldn't because Alice and Bob didn't actually make a key with each other,
# they both made a key with Eve.

Alice_and_Eve_match = KeyA == KeyE_with_Alice
print(f"Does Eve have Alice's key? {Alice_and_Eve_match}")

Bob_and_Eve_match = KeyB == KeyE_with_Bob
print(f"Does Eve have Bob's key? {Bob_and_Eve_match}")