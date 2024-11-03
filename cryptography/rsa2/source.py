#!/usr/bin/env python3
from secret import flag
from Crypto.Util.number import getPrime,bytes_to_long
from Crypto.Util.Padding import pad
p=getPrime(512)
q=getPrime(512)
n=p*q
e=3
m=bytes_to_long(pad(flag,16))


with open("output.txt", "w") as f:
    f.write(f"n = {n}\n")
    f.write(f"c = {pow(m,e,n)}")
    f.close()

