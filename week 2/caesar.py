def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

if __name__ == "__main__":
    plaintext = "SECURITY"
    shift = 4
    print(f"Plain: {plaintext}")
    print(f"Encrypted: {caesar_encrypt(plaintext, shift)}")
    print(f"Decrypted: {caesar_decrypt(caesar_encrypt(plaintext, shift), shift)}")
