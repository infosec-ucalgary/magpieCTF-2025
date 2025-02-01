# RSA Precursor 1
## Category: Cryptography
### Author: Christina He (tomato_tomatoes)

## Description
My relationship with Professor Richard Hash is defined by an "inverse" dynamic—where our approaches to cryptography couldn’t be more opposite. While I believe in innovation and adaptability, he is firmly rooted in tradition, advocating for methods that have stood the test of time. Where I see flexibility and evolution, he sees instability and risk. Our perspectives mirror each other’s in a way: he’s focused on maintaining a static, tried-and-true system, while I push for constant progress, knowing that staying the same in the face of growing threats is the real danger. In this inverse, our work complements yet challenges one another—he strives for preservation, and I, for transformation. But ultimately, it’s this very contrast that drives the future of cryptography forward.


## Hints

If you're not familiar with modulo arithmetics or congruency, check out https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic.

In math, identity is importance. Usually we denote identity as e, or you can think about 1 in our specific case.
Given an integer m>1, for any integer k, 0<=k<m, k*1=1*k=k. Identity doesn't change your input.

Now, here is the concept of a multiplicative inverse (or you can think about the reverse card in uno).
Usually we denote inverse of integer k, 0<=k<m under m as k^{-1}. Here is the definition of k^{-1}:
k^{-1}k=kk^{-1}=1 mod m. Here we see that the inverse undoes what changes k did.

So given an integer 0<=h<m, k^{-1}kh=kk^{-1}h=khk^{-1}=h as multiplication is commutative in modular arithmetics and k^{-1} undoes changes made by k.

## Solution
By taking the inverse of 0x1337 and multiply with c we get 0x1337^{-1}c=0x1337^{-1}0x1337m=m \mod k. Since k is larger than than the bits of 0x1337 and m combined, we know m is the original plaintext value.

## Flag
magpieCTF{1nv3rs3_cr34t3s_fr1ct10n}
