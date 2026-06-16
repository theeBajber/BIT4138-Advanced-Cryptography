# ============================================================
# BIT4138: Advanced Cryptography
# Week 6 - Practical Task 3: SPN vs Feistel Security Evaluation
# ============================================================

import time


# ── Simple Feistel Cipher ──────────────────────────────────

def feistel_round_function(half_block, key):
    """Feistel F-function: XOR with key, then simple scramble."""
    return (half_block ^ key) & 0xFF


def feistel_encrypt(plaintext, key, num_rounds=4):
    """Encrypt using a basic Feistel network (16-bit block, two 8-bit halves)."""
    L = (plaintext >> 8) & 0xFF   # Left half
    R = plaintext & 0xFF           # Right half

    round_keys = [(key + i * 13) & 0xFF for i in range(num_rounds)]

    for i in range(num_rounds):
        new_L = R
        new_R = L ^ feistel_round_function(R, round_keys[i])
        L, R = new_L, new_R

    return (L << 8) | R


def feistel_decrypt(ciphertext, key, num_rounds=4):
    """Decrypt Feistel — same process, keys applied in reverse."""
    L = (ciphertext >> 8) & 0xFF
    R = ciphertext & 0xFF

    round_keys = [(key + i * 13) & 0xFF for i in range(num_rounds)]

    for i in reversed(range(num_rounds)):
        new_R = L
        new_L = R ^ feistel_round_function(L, round_keys[i])
        L, R = new_L, new_R

    return (L << 8) | R


# ── Simple SPN Cipher ─────────────────────────────────────

SBOX = {
    0: 14, 1: 4,  2: 13, 3:  1,
    4:  2, 5: 15, 6: 11, 7:  8,
    8:  3, 9: 10, 10: 6, 11: 12,
    12: 5, 13: 9, 14: 0, 15:  7
}
INV_SBOX = {v: k for k, v in SBOX.items()}
PBOX = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def spn_encrypt(plaintext, key, num_rounds=3):
    block = plaintext
    rk = key
    for _ in range(num_rounds):
        block ^= rk & 0xFFFF
        sub = 0
        for i in range(4):
            nibble = (block >> (12 - 4 * i)) & 0xF
            sub = (sub << 4) | SBOX[nibble]
        block = sub
        perm = 0
        for i in range(16):
            bit = (block >> (15 - i)) & 1
            perm |= (bit << (15 - PBOX[i]))
        block = perm
        rk = ((rk << 4) | (rk >> 12)) & 0xFFFF
    block ^= rk & 0xFFFF
    return block & 0xFFFF


# ── Tests ──────────────────────────────────────────────────

def test_avalanche(encrypt_fn, name, plaintext=0b1010101010101010, key=0b1100110011001100, num_bits=16):
    """Flip each input bit and measure how many output bits change."""
    base_cipher = encrypt_fn(plaintext, key)
    total_changes = 0
    print(f"\n  Avalanche Test — {name}")
    print(f"  {'Bit Flipped':>12} | {'Output Diff (bin)':>20} | {'Bits Changed':>12}")
    print("  " + "-" * 50)
    for bit in range(num_bits):
        flipped = plaintext ^ (1 << bit)
        new_cipher = encrypt_fn(flipped, key)
        diff = base_cipher ^ new_cipher
        bits_changed = bin(diff).count('1')
        total_changes += bits_changed
        print(f"  Bit {bit:>2} flipped | {diff:>016b}     | {bits_changed:>6} / {num_bits}")
    avg = total_changes / num_bits
    print(f"  Average bits changed: {avg:.2f} / {num_bits} ({avg/num_bits*100:.1f}%)")
    print(f"  (Ideal avalanche = 50% = {num_bits//2} bits changed per flip)")
    return avg


def test_speed(encrypt_fn, name, key=12345, iterations=10000):
    """Benchmark encryption speed."""
    start = time.time()
    for i in range(iterations):
        encrypt_fn(i % 65536, key)
    elapsed = time.time() - start
    print(f"  {name}: {iterations} encryptions in {elapsed:.4f}s ({iterations/elapsed:.0f} ops/sec)")


def comparison_table():
    """Print a formatted comparison of Feistel vs SPN."""
    rows = [
        ("Structure",       "Splits block into two halves",     "Operates on entire block"),
        ("Operations",      "Round function (F) + XOR",         "S-Box + Permutation + XOR"),
        ("Decryption",      "Same circuit, reverse key order",   "Requires inverse S-Box & perm"),
        ("Diffusion speed", "Slower (half-block at a time)",     "Faster (full-block permutation)"),
        ("Non-linearity",   "From round function design",        "From S-Box design"),
        ("Famous example",  "DES (56-bit key, 16 rounds)",       "AES (128/256-bit key, 10-14 rds)"),
        ("Security status", "DES broken (1999); 3DES deprecated","AES — no practical break known"),
        ("Implementation",  "Easier (encryption = decryption)",  "Slightly more complex inverse"),
    ]

    col_w = [22, 34, 34]
    header = f"  {'Property':<{col_w[0]}} | {'Feistel Network':<{col_w[1]}} | {'SPN':<{col_w[2]}}"
    divider = "  " + "-" * (sum(col_w) + 6)

    print(f"\n  {'Feistel vs SPN — Comparison Table':^{sum(col_w)+6}}")
    print(divider)
    print(header)
    print(divider)
    for prop, feistel, spn in rows:
        print(f"  {prop:<{col_w[0]}} | {feistel:<{col_w[1]}} | {spn:<{col_w[2]}}")
    print(divider)


def main():
    print("=" * 60)
    print("  BIT4138 - Week 6: SPN vs Feistel Security Evaluation")
    print("=" * 60)

    # Verify both ciphers work correctly
    print("\n  Correctness Check")
    print("  " + "-" * 40)
    pt, key = 0xABCD, 0x1234
    fc = feistel_encrypt(pt, key)
    fd = feistel_decrypt(fc, key)
    sc = spn_encrypt(pt, key)
    print(f"  Feistel: {pt:#06x} → encrypt → {fc:#06x} → decrypt → {fd:#06x}  {'✓' if fd==pt else '✗'}")
    print(f"  SPN    : {pt:#06x} → encrypt → {sc:#06x}")

    # Avalanche comparison
    print("\n" + "=" * 60)
    print("  AVALANCHE EFFECT COMPARISON")
    print("=" * 60)
    avg_f = test_avalanche(feistel_encrypt, "Feistel", num_bits=16)
    avg_s = test_avalanche(spn_encrypt,     "SPN",     num_bits=16)

    print(f"\n  Feistel avg bits changed: {avg_f:.2f}")
    print(f"  SPN     avg bits changed: {avg_s:.2f}")
    winner = "SPN" if avg_s > avg_f else "Feistel"
    print(f"  Better avalanche: {winner}")

    # Speed comparison
    print("\n" + "=" * 60)
    print("  PERFORMANCE COMPARISON")
    print("=" * 60)
    test_speed(feistel_encrypt, "Feistel")
    test_speed(spn_encrypt,     "SPN")

    # Comparison table
    print("\n" + "=" * 60)
    print("  STRUCTURAL COMPARISON")
    print("=" * 60)
    comparison_table()

    print("\n" + "=" * 60)
    print("  CONCLUSION")
    print("  Both are secure when properly implemented.")
    print("  SPN (AES): preferred for modern standards due to stronger")
    print("  diffusion and better resistance to known attacks.")
    print("  Feistel (DES/3DES): largely legacy, now deprecated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
