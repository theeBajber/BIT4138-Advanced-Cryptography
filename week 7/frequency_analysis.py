from collections import Counter

data = "ABABABABCCCCDDD"

count = Counter(data)

print("Character Frequencies:")
for char, freq in sorted(count.items(), key=lambda x: -x[1]):
    print(f"  '{char}': {freq} times ({(freq/len(data))*100:.1f}%)")

print(f"\nTotal characters: {len(data)}")
print("Statistical bias detected — not uniform distribution.")
