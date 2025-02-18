from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode as be

# generate RSA keypair
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# first pad encrypted text with OAEP then base64 encode it
def encrypt(public_key, message):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message.encode())
    ciphertext = be(ciphertext)
    return ciphertext

# Generate key
private_key, public_key = generate_rsa_keys()

# Read flag
message = open('flag.txt','r').read().strip()

# Encrypt flag
ciphertext = encrypt(public_key, message)

# Write keys and ciphertext to files
f=open("../private_key.pem", "wb")
f.write(private_key)
f.close()

f=open("../public_key.pem", "wb")
f.write(public_key)
f.close()

f=open("../ciphertext.txt", "wb")
f.write(ciphertext)
f.close()
    
