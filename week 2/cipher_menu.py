from caesar import caesar_encrypt, caesar_decrypt
from vigenere import vigenere_encrypt, vigenere_decrypt

def get_valid_input():
    while True:
        text = input("Enter text (letters only): ").strip()
        if text and all(c.isalpha() or c.isspace() for c in text):
            return text.upper()
        print("Invalid input. Use letters and spaces only.")

def get_valid_key():
    while True:
        key = input("Enter key (letters only): ").strip()
        if key and key.isalpha():
            return key.upper()
        print("Invalid key. Use letters only.")

def main():
    print("=== CLASSICAL CIPHER SYSTEM ===")
    print("1. Caesar Cipher")
    print("2. Vigenère Cipher")
    
    choice = input("Select (1/2): ").strip()
    
    if choice == "1":
        text = get_valid_input()
        while True:
            try:
                shift = int(input("Enter shift (0-25): "))
                if 0 <= shift <= 25:
                    break
                print("Shift must be 0-25")
            except ValueError:
                print("Enter a number")
        
        encrypted = caesar_encrypt(text, shift)
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {caesar_decrypt(encrypted, shift)}")
        
    elif choice == "2":
        text = get_valid_input()
        key = get_valid_key()
        encrypted = vigenere_encrypt(text, key)
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {vigenere_decrypt(encrypted, key)}")

if __name__ == "__main__":
    main()
