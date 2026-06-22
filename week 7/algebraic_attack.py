plaintext = 12
key = 5

ciphertext = plaintext ^ key
recovered = ciphertext ^ plaintext

print("Plaintext:", plaintext)
print("Key:", key)
print("Ciphertext:", ciphertext)
print("Recovered Key:", recovered)
