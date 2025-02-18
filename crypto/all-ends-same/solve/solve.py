from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode as bd

def read_private_key(file_path):
    with open(file_path, "rb") as key_file:
        private_key_data = key_file.read()
        private_key = RSA.import_key(private_key_data)
    return private_key


def decrypt(key, ciphertext):
    cipher = PKCS1_OAEP.new(key) 
    rsa_encrypted_message = bd(ciphertext) 
    plaintext = cipher.decrypt(rsa_encrypted_message)
    return plaintext.decode()

ciphertext= open('../ciphertext.txt','r').read()
private_key = read_private_key("../private_key.pem")
print(decrypt(private_key, ciphertext))
