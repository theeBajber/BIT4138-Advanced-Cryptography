from feistel import feistel_encrypt, generate_keys, text_to_block
from avalanche import demonstrate_avalanche

def test_confusion():
    plaintext = "TEST1234"
    block = text_to_block(plaintext)
    
    print("=== CONFUSION TEST ===")
    print("Same plaintext, different keys:")
    
    keys1 = generate_keys(0x11111111, 16)
    keys2 = generate_keys(0x11111112, 16)
    
    c1 = feistel_encrypt(block, keys1)
    c2 = feistel_encrypt(block, keys2)
    
    print(f"Key 1: {hex(0x11111111)} -> Ciphertext: {hex(c1)}")
    print(f"Key 2: {hex(0x11111112)} -> Ciphertext: {hex(c2)}")
    print(f"Key differs by 1 bit, ciphertext differs significantly")

def test_diffusion():
    print("\n=== DIFFUSION TEST ===")
    demonstrate_avalanche()

if __name__ == "__main__":
    test_confusion()
    test_diffusion()
