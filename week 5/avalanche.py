from feistel import feistel_encrypt, generate_keys, text_to_block

def bit_difference(a, b):
    xor = a ^ b
    count = 0
    while xor:
        count += xor & 1
        xor >>= 1
    return count

def demonstrate_avalanche():
    master_key = 0x12345678
    keys = generate_keys(master_key, rounds=16)
    
    text1 = "BIT4138A"
    block1 = text_to_block(text1)
    
    text2 = "BIT4138B"
    block2 = text_to_block(text2)
    
    print(f"=== AVALANCHE EFFECT DEMONSTRATION ===")
    print(f"Plaintext 1: {text1} -> {hex(block1)}")
    print(f"Plaintext 2: {text2} -> {hex(block2)}")
    print(f"Input bit difference: {bit_difference(block1, block2)}")
    
    cipher1 = feistel_encrypt(block1, keys)
    cipher2 = feistel_encrypt(block2, keys)
    
    print(f"\nCiphertext 1: {hex(cipher1)}")
    print(f"Ciphertext 2: {hex(cipher2)}")
    
    diff = bit_difference(cipher1, cipher2)
    total_bits = 64
    percentage = (diff / total_bits) * 100
    
    print(f"\nOutput bit difference: {diff} out of {total_bits}")
    print(f"Avalanche percentage: {percentage:.1f}%")
    
    if percentage > 50:
        print("✓ Strong avalanche effect - good diffusion!")
    else:
        print("⚠️ Weak avalanche effect - cipher needs improvement")

if __name__ == "__main__":
    demonstrate_avalanche()
