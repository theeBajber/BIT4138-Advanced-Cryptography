def vigenere_encrypt(text, key):
    result = ""
    key_len = len(key)
    key_idx = 0
    
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % key_len].upper()) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_idx += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key_len = len(key)
    key_idx = 0
    
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % key_len].upper()) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_idx += 1
        else:
            result += char
    return result

if __name__ == "__main__":
    plaintext = "NETWORK"
    key = "KEY"
    encrypted = vigenere_encrypt(plaintext, key)
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"Plain: {plaintext}")
    print(f"Key: {key}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
