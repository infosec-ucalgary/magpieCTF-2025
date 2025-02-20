from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long

# generate RSA keypair
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt(public_key, message):
    key = RSA.import_key(public_key)
    message=bytes_to_long(message)
    n, e = key.n, key.e
    ciphertext = pow(message,e,n)
    return hex(ciphertext)[2:]

# Generate key
private_key, public_key = generate_rsa_keys()

# Read flag
message = open('flag.txt','r').read().strip().encode()

# Encrypt flag
ciphertext = encrypt(public_key, message)

# Write keys and ciphertext to files
f=open("private_key.pem", "wb")
f.write(private_key)
f.close()

f=open("public_key.pem", "wb")
f.write(public_key)
f.close()

f=open("ciphertext.txt", "w")
f.write(ciphertext)
f.close()
    
