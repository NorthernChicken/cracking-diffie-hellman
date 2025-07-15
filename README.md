# Cracking Diffie-Hellman
Capstone Project for ICSSA Cybersecurity.

Project is based on the premise that we are a man in the middle of a Diffie-Hellman key exchange and not only can read but intercept and potentially modify all the messages sent between Alice and Bob over a noisy channel. Our goal is to figure out the key that is generated as a result of the exchange.

Project was originally written in Go but it lacks the ease of data type transfer of something like python, and I don't want to have to use bigint to deal with the large prime numbers.

# To-do

- Generate a large prime and alpha primitve root
- Code a system for Eve to create a shared private key with Bob and Alice seperately to create seperate shared private keys with each