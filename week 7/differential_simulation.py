# BIT4138 Week 7 - Practical Task 1

def simple_encrypt(plaintext, key):
    """Simple XOR encryption for demonstration"""
    return plaintext ^ key

def compute_difference(val1, val2):
    """XOR difference between two values"""
    return val1 ^ val2

def analyze_differential(p1, p2, key):
    """Simulate differential cryptanalysis"""
    # Encrypt both plaintexts
    c1 = simple_encrypt(p1, key)
    c2 = simple_encrypt(p2, key)

    # Compute differences
    input_diff = compute_difference(p1, p2)
    output_diff = compute_difference(c1, c2)

    print("=" * 40)
    print("  DIFFERENTIAL CRYPTANALYSIS DEMO")
    print("=" * 40)
    print(f"Plaintext 1:     {p1:4d}  ({bin(p1)})")
    print(f"Plaintext 2:     {p2:4d}  ({bin(p2)})")
    print(f"Input Diff XOR:  {input_diff:4d}  ({bin(input_diff)})")
    print()
    print(f"Ciphertext 1:    {c1:4d}  ({bin(c1)})")
    print(f"Ciphertext 2:    {c2:4d}  ({bin(c2)})")
    print(f"Output Diff XOR: {output_diff:4d}  ({bin(output_diff)})")
    print()
    if input_diff == output_diff:
        print("OBSERVATION: Input and output differences are EQUAL.")
        print("This reveals the cipher is weak — XOR alone offers no diffusion.")
    else:
        print("OBSERVATION: Differences changed through encryption.")

# Run the simulation
analyze_differential(p1=10, p2=11, key=7)
