from Crypto.Util.number import long_to_bytes
print(long_to_bytes(int(open("output.txt", 'r').read().strip())).decode())
