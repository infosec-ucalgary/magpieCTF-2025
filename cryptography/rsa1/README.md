# RSA1
## Category: Cryptography 1
### Author: Christina He (tomato_tomatoes)

## Description
A simple RSA to start off.

## Hints
https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Security_and_practical_considerations
Sagemath has some good functions for factoring: https://sagecell.sagemath.org/

## Solution
1. Factor n into p*q
2. Compute phi=(p-1)*(q-1)
3. Compute private key d=e^{-1} \mod phi
4. Recover message m=c^{d} \mod n
5. Convert m into bytes

## Flag
magpieCTF{sm@ll_n_uns@f3}
