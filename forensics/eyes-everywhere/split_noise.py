import base64
import random
import string

def encode_and_split(input_string, num_pieces=3, noise_chars=10):
    # Step 1: Base64 encode
    encoded = base64.b64encode(input_string.encode()).decode()
    print(f"Base64 encoded: {encoded}")
    
    # Step 2: Add random noise
    noise_chars_list = [random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(noise_chars)]
    positions = random.sample(range(len(encoded) + 1), noise_chars)
    positions.sort()
    
    noisy_string = list(encoded)
    for pos, char in zip(positions, noise_chars_list):
        noisy_string.insert(pos, f"${char}$")  # Wrap noise in $$ to identify it later
    noisy_string = ''.join(noisy_string)
    print(f"With noise added: {noisy_string}")
    
    # Step 3: Split into pieces
    chunk_size = len(noisy_string) // num_pieces
    pieces = [noisy_string[i:i + chunk_size] for i in range(0, len(noisy_string), chunk_size)]
    print(f"Split into pieces: {pieces}")
    
    return pieces

def decode_from_pieces(pieces):
    # Step 1: Join pieces
    joined = ''.join(pieces)
    print(f"Joined pieces: {joined}")
    
    # Step 2: Remove noise (characters between $)
    cleaned = ''
    i = 0
    while i < len(joined):
        if joined[i] == '$':
            # Skip until next $
            i = joined.index('$', i + 1) + 1
        else:
            cleaned += joined[i]
            i += 1
    print(f"Cleaned string: {cleaned}")
    
    # Step 3: Base64 decode
    decoded = base64.b64decode(cleaned).decode()
    print(f"Decoded result: {decoded}")
    
    return decoded

# Test the functions
original = "magpieCTF{B1INDnES5_!s_4_PRIV47e_Ma7t3R_83twE3n_A_PER$on_aND_tHE_3YE5_Wi7H_wHIcH_tHey_w3rE_BorN}"

# Encode, add noise, and split
print("=== Encoding Process ===")
pieces = encode_and_split(original, num_pieces=5, noise_chars=15)

# Decode from pieces
print("\n=== Decoding Process ===")
result = decode_from_pieces(pieces)

# Verify
print("\n=== Verification ===")
print(f"Original string matches decoded string: {original == result}")