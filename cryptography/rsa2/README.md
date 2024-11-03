# RSA 2
## Category: Cryptography
### Author: Christina He (tomato_tomatoes)

## Description
I fixed the size of the primes, it should be good right?

## Hints
https://en.wikipedia.org/wiki/Coppersmith%27s_attack
https://ask.sagemath.org/question/10730/is-there-a-simple-way-to-deal-with-computing-real-nth-roots-for-n-a-natural-number/

## Solution
Since e=3 is small, n is 1024 bits and m is 255 bits from the hint, c is only 255*3=765 bits. Hence, n didn't have much use here. If we take cube root of c, we can recover m.
See solve.sage for actual implementation

## Flag
magpieCTF{3ff1c13nt_n0t_s3cur3}
