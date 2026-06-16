# ============================================================
# BIT4138: Advanced Cryptography
# Week 6 - Practical Task 1: Simple SPN Implementation
# ============================================================

# S-Box (Substitution Box) - maps 4-bit input (0-15) to output
SBOX = {
    0:  14, 1:  4,  2:  13, 3:  1,
    4:  2,  5:  15, 6:  11, 7:  8,
    8:  3,  9:  10, 10: 6,  11: 12,
    12: 5,  13: 9,  14: 0,  15: 7
}

# Inverse S-Box (for decryption)
INV_SBOX = {v: k for k, v in SBOX.items()}

# Permutation table - defines how bit positions are rearranged
# Position i goes to PBOX[i]
PBOX = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def substitute(block):
    """Apply S-Box substitution to each 4-bit nibble in a 16-bit block."""
    result = 0
    for i in range(4):  # 4 nibbles in 16 bits
        nibble = (block >> (12 - 4 * i)) & 0xF
        substituted = SBOX[nibble]
        result = (result << 4) | substituted
    return result


def permute(block):
    """Rearrange bits according to PBOX permutation table."""
    result = 0
    for i in range(16):
        bit = (block >> (15 - i)) & 1
        result |= (bit << (15 - PBOX[i]))
    return result


def key_mix(block, round_key):
    """XOR block with round key."""
    return block ^ round_key


def generate_round_keys(master_key, num_rounds=3):
    """Generate simple round keys by rotating the master key."""
    keys = []
    key = master_key & 0xFFFF  # keep 16 bits
    for i in range(num_rounds + 1):
        keys.append(key)
        # Rotate left by 4 bits for next round key
        key = ((key << 4) | (key >> 12)) & 0xFFFF
    return keys


def spn_encrypt(plaintext, master_key, num_rounds=3):
    """
    Encrypt plaintext using SPN with given master key.
    """
    round_keys = generate_round_keys(master_key, num_rounds)
    block = plaintext

    print(f"\n  [Encryption Steps]")
    print(f"  Plaintext  : {block:016b} (binary) | {block:04X} (hex)")

    for round_num in range(1, num_rounds + 1):
        # Step 1: Key Mixing
        block = key_mix(block, round_keys[round_num - 1])
        print(f"\n  -- Round {round_num} --")
        print(f"  After Key Mix : {block:016b} | {block:04X}")

        # Step 2: Substitution
        block = substitute(block)
        print(f"  After S-Box   : {block:016b} | {block:04X}")

        # Step 3: Permutation (skip on last round)
        if round_num < num_rounds:
            block = permute(block)
            print(f"  After Permute : {block:016b} | {block:04X}")

    # Final key mixing
    block = key_mix(block, round_keys[num_rounds])
    print(f"\n  Final Key Mix : {block:016b} | {block:04X}")
    print(f"  Ciphertext    : {block:04X} (hex) | {block} (decimal)")
    return block


def spn_decrypt(ciphertext, master_key, num_rounds=3):
    """
    Decrypt ciphertext using inverse SPN operations.
    """
    round_keys = generate_round_keys(master_key, num_rounds)
    block = ciphertext

    print(f"\n  [Decryption Steps]")
    print(f"  Ciphertext : {block:016b} | {block:04X}")

    # Reverse final key mixing
    block = key_mix(block, round_keys[num_rounds])

    for round_num in range(num_rounds, 0, -1):
        print(f"\n  -- Round {round_num} (inverse) --")

        # Inverse permutation (skip on last decryption round)
        if round_num < num_rounds:
            inv_block = 0
            for i in range(16):
                bit = (block >> (15 - PBOX[i])) & 1
                inv_block |= (bit << (15 - i))
            block = inv_block
            print(f"  After Inv-Permute : {block:016b} | {block:04X}")

        # Inverse substitution
        inv_result = 0
        for i in range(4):
            nibble = (block >> (12 - 4 * i)) & 0xF
            inv_result = (inv_result << 4) | INV_SBOX[nibble]
        block = inv_result
        print(f"  After Inv-S-Box   : {block:016b} | {block:04X}")

        # Key mixing
        block = key_mix(block, round_keys[round_num - 1])
        print(f"  After Key Mix     : {block:016b} | {block:04X}")

    print(f"\n  Recovered Plaintext: {block:016b} | {block:04X} | {block} (decimal)")
    return block


def display_sbox():
    """Display the S-Box as a formatted table."""
    print("\n  S-Box Lookup Table:")
    print("  " + "-" * 42)
    print("  | Input  | " + " | ".join(f"{i:2}" for i in range(8)) + " |")
    print("  | Output | " + " | ".join(f"{SBOX[i]:2}" for i in range(8)) + " |")
    print("  " + "-" * 42)
    print("  | Input  | " + " | ".join(f"{i:2}" for i in range(8, 16)) + " |")
    print("  | Output | " + " | ".join(f"{SBOX[i]:2}" for i in range(8, 16)) + " |")
    print("  " + "-" * 42)


def main():
    print("=" * 60)
    print("  BIT4138 - Week 6: SPN Cipher Implementation")
    print("=" * 60)

    display_sbox()

    print("\n  Enter values in decimal (0-65535 for 16-bit block)")
    print("  Example: plaintext = 9, key = 5\n")

    while True:
        try:
            plaintext = int(input("  Enter plaintext (decimal): "))
            key = int(input("  Enter secret key (decimal): "))

            if not (0 <= plaintext <= 65535) or not (0 <= key <= 65535):
                print("  ⚠ Values must be between 0 and 65535. Try again.\n")
                continue

            print("\n" + "=" * 60)
            ciphertext = spn_encrypt(plaintext, key)

            print("\n" + "=" * 60)
            recovered = spn_decrypt(ciphertext, key)

            print("\n" + "=" * 60)
            print("  Summary")
            print("  " + "-" * 30)
            print(f"  Original Plaintext : {plaintext}")
            print(f"  Secret Key         : {key}")
            print(f"  Ciphertext         : {ciphertext}")
            print(f"  Decrypted          : {recovered}")
            print(f"  Match              : {'✓ YES' if plaintext == recovered else '✗ NO'}")
            print("=" * 60)

        except ValueError:
            print("  ⚠ Please enter valid integers.\n")
            continue

        again = input("\n  Encrypt another message? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Exiting SPN program. Goodbye!")
            break


if __name__ == "__main__":
    main()
