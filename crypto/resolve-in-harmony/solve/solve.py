#!/usr/bin/env python3
from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes

HOST="localhost"
PORT=1337

r=remote(HOST, PORT)
r.recvuntil(b'key: ')
public_key=r.recvuntil(b'END PUBLIC KEY-----')
r.recvuntil(b'ciphertext:')
cipher=int(r.recvuntil(b'\n').decode().strip(),16)
r.recv()

public_key_pair=RSA.import_key(public_key)
n, e = public_key_pair.n , public_key_pair.e
to_send=pow(3,e,n)*cipher%n
r.sendline(hex(to_send)[2:].encode())
response=int(r.recvuntil(b'public')[:-6].decode(),16)
print((long_to_bytes(response*pow(3,-1,n)%n)).decode())
