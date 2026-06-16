# ============================================================
# BIT4138: Advanced Cryptography
# Week 6 - Practical Task 2: Non-Linearity Investigation
# (Run this to see demonstrations supporting the report)
# ============================================================

def linear_transform(x):
    """A simple LINEAR transformation: output = 2x + 3."""
    return 2 * x + 3


def sbox_transform(x):
    """A NON-LINEAR S-Box transformation."""
    sbox = {
        0: 14, 1: 4,  2: 13, 3:  1,
        4:  2, 5: 15, 6: 11, 7:  8,
        8:  3, 9: 10, 10: 6, 11: 12,
        12: 5, 13: 9, 14: 0, 15:  7
    }
    return sbox.get(x % 16, 0)


def check_linearity(transform_fn, name, sample_range=8):
    """
    Test if f(a XOR b) == f(a) XOR f(b).
    If this holds for all inputs, the function is LINEAR.
    A non-linear function will FAIL this test.
    """
    print(f"\n  Testing: {name}")
    print("  " + "-" * 55)
    print(f"  {'a':>4} {'b':>4} {'a XOR b':>8} {'f(a XOR b)':>12} {'f(a) XOR f(b)':>14} {'Linear?':>8}")
    print("  " + "-" * 55)

    linear_count = 0
    total = 0

    for a in range(sample_range):
        for b in range(a + 1, sample_range):
            fa = transform_fn(a)
            fb = transform_fn(b)
            axorb = a ^ b
            faxorb = transform_fn(axorb)
            faxorfb = fa ^ fb
            is_linear = (faxorb == faxorfb)
            if is_linear:
                linear_count += 1
            total += 1
            marker = "✓" if is_linear else "✗"
            print(f"  {a:>4} {b:>4} {axorb:>8} {faxorb:>12} {faxorfb:>14} {marker:>8}")

    print("  " + "-" * 55)
    score = (linear_count / total) * 100
    verdict = "LINEAR" if linear_count == total else "NON-LINEAR"
    print(f"  Linear pairs: {linear_count}/{total} ({score:.1f}%) → Function is {verdict}")
    return linear_count == total


def demonstrate_avalanche(transform_fn, name, inputs):
    """Show that small input changes produce large output changes (avalanche)."""
    print(f"\n  Avalanche Effect — {name}")
    print("  " + "-" * 40)
    for i in range(len(inputs) - 1):
        a, b = inputs[i], inputs[i + 1]
        out_a = transform_fn(a)
        out_b = transform_fn(b)
        input_diff = a ^ b
        output_diff = out_a ^ out_b
        print(f"  Input  : {a:04b} → {b:04b}  (differ by {bin(input_diff).count('1')} bit(s))")
        print(f"  Output : {out_a:04b} → {out_b:04b}  (differ by {bin(output_diff).count('1')} bit(s))")
        print()


def show_sbox_uniqueness():
    """Show that a good S-Box has unique, non-repeating outputs."""
    sbox = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    outputs = list(sbox)
    unique = len(set(outputs)) == len(outputs)

    print("\n  S-Box Output Uniqueness Check")
    print("  " + "-" * 40)
    print(f"  Outputs : {outputs}")
    print(f"  Unique  : {'✓ YES — all outputs are distinct (bijective)' if unique else '✗ NO — repeated outputs detected'}")


def main():
    print("=" * 60)
    print("  BIT4138 - Week 6: Non-Linearity Investigation")
    print("=" * 60)

    print("\n  PART 1: Linearity Testing")
    print("  Checking if f(a XOR b) = f(a) XOR f(b)")

    check_linearity(linear_transform, "Linear Function: f(x) = 2x + 3")
    check_linearity(sbox_transform,   "S-Box (Non-linear transformation)")

    print("\n\n  PART 2: Avalanche Effect")
    demonstrate_avalanche(
        sbox_transform,
        "S-Box",
        [0, 1, 2, 3, 4]
    )

    print("\n  PART 3: S-Box Quality Check")
    show_sbox_uniqueness()

    print("\n" + "=" * 60)
    print("  CONCLUSION")
    print("  " + "-" * 58)
    print("  Linear functions expose predictable patterns.")
    print("  S-Boxes introduce non-linearity, breaking those patterns.")
    print("  Non-linearity is essential for resisting:")
    print("    - Linear cryptanalysis")
    print("    - Algebraic attacks")
    print("    - Differential cryptanalysis")
    print("=" * 60)


if __name__ == "__main__":
    main()
