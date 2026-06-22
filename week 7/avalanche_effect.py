import hashlib

text1 = "HELLO"
text2 = "HELLo"

hash1 = hashlib.sha256(text1.encode()).hexdigest()
hash2 = hashlib.sha256(text2.encode()).hexdigest()

print("Text 1:", text1)
print("Hash 1:", hash1)
print()
print("Text 2:", text2)
print("Hash 2:", hash2)

# Count differing characters
diffs = sum(1 for a, b in zip(hash1, hash2) if a != b)
print(f"\nDiffering hex characters: {diffs}/{len(hash1)}")
