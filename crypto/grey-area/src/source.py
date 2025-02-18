#!/usr/bin/env python3
from secret import flag
from Crypto.Util.number import getPrime,bytes_to_long
p=getPrime(100)
q=getPrime(100)
n=p*q
e=0x10001
m=bytes_to_long(flag)

with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"c = {pow(m,e,n)}")
    f.close()

