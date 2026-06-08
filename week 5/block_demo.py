from feistel import feistel_encrypt, generate_keys, text_to_block

keys = generate_keys(0xDEADBEEF, 16)

messages = [
    'SECRET!!',
    'MESSAGE!',
    'BIT4138!',
    'BLOCK!!1'
]

print('=== BLOCK ENCRYPTION DEMONSTRATION ===')
for msg in messages:
    block = text_to_block(msg)
    cipher = feistel_encrypt(block, keys)
    print(f'{msg:8} -> {hex(block):18} -> {hex(cipher)}')
