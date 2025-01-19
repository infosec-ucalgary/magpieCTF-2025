#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long
f=open('../output.txt','w')
f.write(str(bytes_to_long(open('flag.txt', 'r').read().strip().encode())))
f.close()
