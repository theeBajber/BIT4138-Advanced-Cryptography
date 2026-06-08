import math

def frequency_test(bits):
    """Test if 0s and 1s are balanced"""
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    ratio = ones / n
    return {
        'total_bits': n,
        'ones': ones,
        'zeros': zeros,
        'ratio': ratio,
        'balanced': 0.45 <= ratio <= 0.55
    }

def runs_test(bits):
    """Count runs (consecutive identical bits)"""
    if not bits:
        return {'runs': 0}
    
    runs = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i-1]:
            runs += 1
    
    n = len(bits)
    expected_runs = (2 * n - 1) / 3
    return {
        'runs': runs,
        'expected': round(expected_runs, 2),
        'close': abs(runs - expected_runs) < n * 0.1
    }

def mean_test(bits):
    """Mean should be ~0.5 for random bits"""
    mean = sum(bits) / len(bits)
    return {
        'mean': round(mean, 4),
        'random_like': 0.4 <= mean <= 0.6
    }

def chi_square_test(bits):
    """Chi-square test for uniformity"""
    ones = sum(bits)
    zeros = len(bits) - ones
    expected = len(bits) / 2
    
    chi_sq = ((ones - expected) ** 2 / expected) + ((zeros - expected) ** 2 / expected)
    return {
        'chi_square': round(chi_sq, 4),
        'uniform': chi_sq < 3.841  # 95% confidence for df=1
    }

def test_sequence(bits):
    print(f"Sequence: {''.join(map(str, bits[:50]))}...")
    print(f"Length: {len(bits)}")
    print()
    
    freq = frequency_test(bits)
    print(f"Frequency Test: {freq}")
    
    runs = runs_test(bits)
    print(f"Runs Test: {runs}")
    
    mean = mean_test(bits)
    print(f"Mean Test: {mean}")
    
    chi = chi_square_test(bits)
    print(f"Chi-Square Test: {chi}")
    
    all_pass = freq['balanced'] and runs['close'] and mean['random_like'] and chi['uniform']
    print(f"\nOverall: {'PASS' if all_pass else 'FAIL'}")

# Test with LFSR output
from lfsr import LFSR

lfsr = LFSR(seed=0b10110101, taps=[0, 2])
bits = lfsr.generate(1000)
test_sequence(bits)

# Compare with Python's random
import random
random_bits = [random.randint(0, 1) for _ in range(1000)]
print("\n--- Python random module ---")
test_sequence(random_bits)
