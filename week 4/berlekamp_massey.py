def berlekamp_massey(sequence):
    n = len(sequence)
    C = [1] + [0] * n
    B = [1] + [0] * n
    L = 0
    m = 1
    
    for i in range(n):
        d = sequence[i]
        for j in range(1, L + 1):
            d ^= C[j] & sequence[i - j]
        
        if d == 1:
            T = C[:]
            for j in range(n - m + 1):
                if j + m <= n:
                    C[j + m] ^= B[j]
            
            if 2 * L <= i:
                L = i + 1 - L
                B = T
                m = 1
            else:
                m += 1
        else:
            m += 1
    
    taps = [i for i in range(1, len(C)) if C[i] == 1]
    return L, taps, C[:L+1]

if __name__ == "__main__":
    from lfsr import LFSR
    
    lfsr = LFSR(seed=0b10110101, taps=[0, 2])
    known_bits = lfsr.generate(20)
    print(f"Known bits: {known_bits}")
    print(f"Known taps: [0, 2]")
    
    L, taps, poly = berlekamp_massey(known_bits)
    print(f"\nRecovered length: {L}")
    print(f"Recovered taps: {taps}")
    print(f"Connection polynomial: {poly}")
