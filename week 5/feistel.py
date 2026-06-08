def feistel_round(left, right, round_key):
    """One round of Feistel network"""
    # F function: simple XOR with key, then some mixing
    f_output = ((right ^ round_key) * 0x5A827999) & 0xFFFFFFFF
    new_left = right
    new_right = left ^ f_output
    return new_left, new_right

def feistel_encrypt(block, keys, rounds=16):
    """
    Encrypt a 64-bit block using Feistel structure
    block: 64-bit integer
    keys: list of round keys
    """
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    
    for i in range(rounds):
        left, right = feistel_round(left, right, keys[i])
    
    # Final swap (not needed but standard)
    return ((right << 32) | left) & 0xFFFFFFFFFFFFFFFF

def feistel_decrypt(block, keys, rounds=16):
    """Decrypt by reversing the key order"""
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    
    for i in range(rounds - 1, -1, -1):
        left, right = feistel_round(left, right, keys[i])
    
    return ((right << 32) | left) & 0xFFFFFFFFFFFFFFFF

def generate_keys(master_key, rounds=16):
    """Generate round keys from master key"""
    keys = []
    for i in range(rounds):
        keys.append((master_key ^ (0x6ED9EBA1 * (i + 1))) & 0xFFFFFFFF)
    return keys

def text_to_block(text):
    """Convert 8-char string to 64-bit block"""
    block = 0
    for i, char in enumerate(text[:8]):
        block |= (ord(char) << (8 * (7 - i)))
    return block

def block_to_text(block):
    """Convert 64-bit block to string"""
    text = ""
    for i in range(8):
        text += chr((block >> (8 * (7 - i))) & 0xFF)
    return text

# Test
master_key = 0x12345678
keys = generate_keys(master_key, rounds=16)

plaintext = "BIT4138!"
block = text_to_block(plaintext)
print(f"Plaintext: {plaintext}")
print(f"Block: {hex(block)}")

encrypted = feistel_encrypt(block, keys)
print(f"Encrypted: {hex(encrypted)}")

decrypted = feistel_decrypt(encrypted, keys)
decrypted_text = block_to_text(decrypted)
print(f"Decrypted: {decrypted_text}")
