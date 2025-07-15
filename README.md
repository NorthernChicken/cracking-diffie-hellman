# Cracking Diffie-Hellman
Capstone Project for ICSSA Cybersecurity.

Project is based on the premise that we have a man in the middle of a Diffie-Hellman key exchange and not only can read by intercept and potentially modify all the messages sent between Alice and Bob over a noisy channel.

Project was originally written in Go but it lacks the ease of data type transfer of something like python, and I don't want to have to use bigint to deal with the large prime numbers.