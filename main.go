// Don't use this it doesn't work. Use the python main.py. 

package main

import (
	"fmt"
	"math"
	"math/rand/v2"
)

func main() {
	// Alice announces these, Eve intercepts them before passing them to Bob.
	var p int = 1000000007
	var alpha int = 5

	// Alice and Bob choose SA and SB respectively (secret, never transmitted)
	var SA int = rand.IntN(10000)
	fmt.Println("Alice's secret is:", SA)
	var SB int = rand.IntN(10000)
	fmt.Println("Bob's secret is:", SB)

	// Alice and Bob caluclate TA and TB respecitvely based on alpha, p, and their secret number.
	TA := int(math.Pow(float64(alpha), float64(SA))) % p // have to convert from int to float to int for this because Go is fucking stupid.
	fmt.Println("TA calculated by Alice is:", TA)
	TB := int(math.Pow(float64(alpha), float64(SB))) % p
	fmt.Println("TB calculated by Bob is:", TB)
	// These values TA and TB are sent to each other (and pass through Eve first, who can manipulate them)

	// Alice caluclates the shared key.
	KeyA := int(math.Pow(float64(TB), float64(SA))) % p
	fmt.Println("Alice calculates the shared key to be:", KeyA)
	// Bob does the same on his end. These steps aren't visible to Eve.
	KeyB := int(math.Pow(float64(TA), float64(SB))) % p
	fmt.Println("Bob calculates the shared key to be:", KeyB)

	// We check if the keys match for debugging. IRL this wouldn't happen, much less on a noisy channel.
	KeysMatch := "undefined"
	if KeyA == KeyB {
		KeysMatch = "true"
	} else {
		KeysMatch = "false"
	}

	fmt.Println("Keys Match:", KeysMatch)

}
