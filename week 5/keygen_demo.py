from feistel import generate_keys

print('=== KEY GENERATION PROCESS ===')
master = 0x12345678
print(f'Master key: {hex(master)}')

keys = generate_keys(master, 16)
print('Round keys (first 5 shown):')
for i, k in enumerate(keys[:5]):
    print(f'  K{i+1:2d}: {hex(k)}')

print('...')
print('Key derivation: K_i = (master XOR (0x6ED9EBA1 * (i+1))) & 0xFFFFFFFF')
print('Purpose: Ensure round keys are different and unpredictable')
