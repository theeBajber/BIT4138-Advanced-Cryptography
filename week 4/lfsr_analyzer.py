from lfsr import LFSR
from berlekamp_massey import berlekamp_massey

def analyze_lfsr_security(seed, taps, bits_to_generate=100):
    lfsr = LFSR(seed, taps)
    bits = lfsr.generate(bits_to_generate)
    
    print(f"=== LFSR Security Analysis ===")
    print(f"Seed: {bin(seed)}")
    print(f"Taps: {taps}")
    print(f"Generated {bits_to_generate} bits")
    
    period, start = lfsr.detect_period(max_steps=10000)
    print(f"\n1. PERIOD ANALYSIS")
    print(f"   Period: {period}")
    print(f"   Starts repeating at: {start}")
    if period and period < 1000:
        print(f"   ⚠️ WEAK: Short period makes it predictable!")
    else:
        print(f"   ✓ Period is sufficiently long")
    
    sample = bits[:50]
    L, recovered_taps, _ = berlekamp_massey(sample)
    print(f"\n2. LINEAR COMPLEXITY")
    print(f"   Linear complexity: {L}")
    print(f"   Recovered taps from 50 bits: {recovered_taps}")
    if L < 20:
        print(f"   ⚠️ WEAK: Low linear complexity - easily broken!")
    else:
        print(f"   ✓ Linear complexity is adequate")
    
    print(f"\n3. PREDICTION TEST")
    predicted = []
    test_lfsr = LFSR(seed, recovered_taps if recovered_taps else taps)
    test_lfsr.generate(50)
    for _ in range(10):
        predicted.append(test_lfsr.step())
    
    actual_next = bits[50:60]
    print(f"   Predicted next 10 bits: {predicted}")
    print(f"   Actual next 10 bits:  {actual_next}")
    match = predicted == actual_next
    print(f"   Match: {'✓ YES - LFSR is fully predictable!' if match else '✗ NO'}")
    
    return {
        'period': period,
        'linear_complexity': L,
        'predictable': match
    }

if __name__ == "__main__":
    print("Testing WEAK LFSR (8-bit):")
    result = analyze_lfsr_security(seed=0b10110101, taps=[0, 2], bits_to_generate=200)
    print(f"\nOverall security: {'WEAK' if result['predictable'] or result['period'] < 1000 else 'MODERATE'}")
