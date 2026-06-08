from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
message = b"Hello BIT4138"
encrypted = cipher.encrypt(message)
print(f"Encrypted: {encrypted}")

# Decrypt
decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted.decode()}")
