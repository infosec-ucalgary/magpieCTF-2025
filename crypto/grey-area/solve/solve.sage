from Crypto.Util.number import long_to_bytes
n,c = [int(i.split("= ")[1]) for i in open("output.txt", 'r').read().split("\n")]
p,q=[i[0] for i in list(factor(n))]
e=0x10001
phi=(p-1)*(q-1)
d=pow(e,-1,phi)
print(long_to_bytes(pow(c,d,n)).decode())
