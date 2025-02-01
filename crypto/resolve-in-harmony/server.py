#!/usr/bin/env python3
import socketserver
import json
from Crypto.PublicKey import RSA

def read_private_key(file_path):
    with open(file_path, "rb") as key_file:
        private_key_data = key_file.read()
        private_key = RSA.import_key(private_key_data)
    return private_key

def challenge(req):
    while True:
        try:
            ciphertext=open('ciphertext.txt','r').read()
            public_key=open('public_key.pem','r').read()
            msg = f"public key: {public_key}\nFlag ciphertext:{ciphertext}\nDifference shall resolve into an existence in harmony\n"
            req.sendall(msg.encode())
            n=RSA.import_key(public_key).n
            cipher_input=str(req.recv(4096).decode().strip())
            if ciphertext==cipher_input:
                req.sendall(b"One sided view will not result in balance\n")
            else:
                d=read_private_key('private_key.pem').d
                plaintext=pow(int(cipher_input, 16),d,n)
                req.sendall(hex(plaintext)[2:].encode()+b'\n')
        except Exception as e:
            print(f"Exception occurred: {e}")
            return


class MyTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        req = self.request
        challenge(req)


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadingTCPServer(("localhost", 1337), MyTCPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()

