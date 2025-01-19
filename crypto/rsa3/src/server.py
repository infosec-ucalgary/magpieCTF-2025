#!/usr/bin/env python3
import socketserver
import json
import decrypt

def challenge(req):
    while True:
        try:
            ciphertext=open('ciphertext.txt','r').read()
            public_key=open('public_key.pem','r').read()
            msg = f"public key: {public_key}\nI can decrypt anything but the flag ciphertext for you\nGive me a base64 encoded ciphertext\n"
            req.sendall(msg.encode())

            cipher_input=str(req.recv(4096).decode().strip())
            if ciphertext==cipher_input:
                raise Exception("Don't try to trick me")
            private_key=decrypt.read_private_key("private_key.pem")
            plaintext=decrypt.decrypt(private_key, cipher_input)
            req.sendall(plaintext.encode())
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

