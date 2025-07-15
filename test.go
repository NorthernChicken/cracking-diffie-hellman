package main

import (
	"fmt"
	"math/rand/v2"
)

func main() {

	// Random number tester in Go
	var SA int = rand.IntN(10000)
	var SB int = rand.IntN(10000)

	fmt.Println(SA, SB)
}
