class LFSR:
    def __init__(self, seed, taps):
        """
        seed: initial state (integer)
        taps: list of bit positions to XOR (e.g., [0, 2] for S_n = S_{n-1} XOR S_{n-3})
        """
        self.state = seed
        self.taps = taps
        self.period = 0
        self.initial_state = seed
    
    def step(self):
        # XOR the tap bits
        new_bit = 0
        for tap in self.taps:
            new_bit ^= (self.state >> tap) & 1
        
        # Shift left, add new bit at LSB
        self.state = (self.state << 1) | new_bit
        self.state &= 0xFF  # Keep 8 bits for demo
        self.period += 1
        
        return new_bit
    
    def generate(self, n_bits):
        return [self.step() for _ in range(n_bits)]
    
    def detect_period(self, max_steps=1000):
        seen = {}
        self.state = self.initial_state
        self.period = 0
        
        for i in range(max_steps):
            state_key = self.state
            if state_key in seen:
                return i - seen[state_key], seen[state_key]
            seen[state_key] = i
            self.step()
        
        return None, None

# Example: LFSR with taps at positions 0 and 2 (equivalent to S_n = S_{n-1} XOR S_{n-3})
lfsr = LFSR(seed=0b10110101, taps=[0, 2])
bits = lfsr.generate(50)
print(f"Generated bits: {bits}")
print(f"Bit string: {''.join(map(str, bits))}")

period, start = lfsr.detect_period()
print(f"Period detected: {period} (starts repeating at step {start})")
