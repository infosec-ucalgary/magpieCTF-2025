# Grey Area
## Category: Cryptography 1
### Author: Christina He (tomato_tomatoes)

## Description
I’ve always believed in pushing boundaries, in seeing beyond what’s already been done. But lately, as I dig deeper into this new factor—exploring encryption beyond the rigid structures I’ve known—I feel a creeping doubt. The lines between black and white, between what’s secure and what’s vulnerable, are starting to fade. It’s as if I’m trapped between two worlds. 

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
magpieCTF{wh1tp_n_blqck}
