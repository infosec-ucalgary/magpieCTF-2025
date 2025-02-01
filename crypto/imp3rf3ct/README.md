# Imp3rf3ct
## Category: Cryptography
### Author: Christina He (tomato_tomatoes)

## Description
I’ve always believed in the power of innovation, but lately, I’ve started questioning what that really means. In my latest project, I created a system designed for efficiency above all else. It's simple, fast, and perfect for situations where speed is critical. But, as much as I tell myself it’s a breakthrough, I can’t shake the feeling that it’s a step back in some ways. Sure, it’s lightning fast, but the truth is, it’s not secur3. But I can’t ignore the fact that it’s not my best work. It’s a quick fix, not the kind of solution I’ve always strived for. But maybe that’s what the world needs right now. A little less perfection, a little more practicality. Professor Richard would spot this easily, a righteous person like him would sure stop me from publishing this imperfect invention of mine...hopefully. 

## Hints
https://en.wikipedia.org/wiki/Coppersmith%27s_attack
https://ask.sagemath.org/question/10730/is-there-a-simple-way-to-deal-with-computing-real-nth-roots-for-n-a-natural-number/

## Solution
Since e=3 is small, n is 1024 bits and m is 255 bits from the hint, c is only 255*3=765 bits. Hence, n didn't have much use here. If we take cube root of c, we can recover m.
See solve.sage for actual implementation

## Flag
magpieCTF{3ff1c13nt_n0t_s3cur3}
