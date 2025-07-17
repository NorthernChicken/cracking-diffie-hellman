package main

import (
	"math/big"
	"math/rand"
)

// This is our random 'secret number' which we never share.
func Generate_secret_number() *big.Int {
	random_number := rand.Int63n(1000000)
	return big.NewInt(random_number)
}

// Our public key that we share with the world.
func Generate_public_key(alpha *big.Int, secret_number *big.Int, p *big.Int) *big.Int {
	// This function returns alpha to the power of our secret number, modulo p (alpha^secret%p)
	public_key := new(big.Int).Exp(alpha, secret_number, p)
	return public_key
}

// Both people who run this should get the same private key.
func Find_private_key(other_persons_public_key *big.Int, secret_number *big.Int, p *big.Int) *big.Int {
	// Same function as before (other_persons_public_key^secret_number%p)
	private_key := new(big.Int).Exp(other_persons_public_key, secret_number, p)
	return private_key
}
