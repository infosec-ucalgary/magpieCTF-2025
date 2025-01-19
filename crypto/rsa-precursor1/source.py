from secret import flag
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import getPrime

m=bytes_to_long(flag)
bits=len(bin(m)[2:])
k=getPrime(bits+16)
n=0x1337
with open("output.txt",'w') as f:
    f.write(f"c = {m*n%k}\n")
    f.write(f"k = {k}")
    f.close()
