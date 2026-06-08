import random

def generate_keystream(length, seed):
    """Generate pseudorandom keystream"""
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]

def xor_encrypt(plaintext, keystream):
    """Encrypt/decrypt using XOR"""
    return bytes([p ^ k for p, k in zip(plaintext, keystream)])

def main():
    message = b"Hello, this is a secret message for BIT4138!"
    seed = 12345
    
    # Generate keystream
    keystream = generate_keystream(len(message), seed)
    
    # Encrypt
    ciphertext = xor_encrypt(message, keystream)
    print(f"Plaintext: {message}")
    print(f"Keystream: {keystream[:10]}... (length: {len(keystream)})")
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    print(f"Ciphertext (raw): {ciphertext}")
    
    # Decrypt (same operation)
    decrypted = xor_encrypt(ciphertext, keystream)
    print(f"Decrypted: {decrypted.decode()}")

if __name__ == "__main__":
    main()
