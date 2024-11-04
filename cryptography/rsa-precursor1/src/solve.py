#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
c, k = [int(i.split('= ')[1]) for i in open("output.txt","r").read().strip().split('\n')]
n = 0x1337
n_inv = pow(n,-1,k)
print(long_to_bytes(c*n_inv % k).decode())

