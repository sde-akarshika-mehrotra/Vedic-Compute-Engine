class VedicMathEngine:
    """
    Core Arithmetic Logic Unit using Nikhilam Sutra.
    """
    def __init__(self):
        self.SCALE = 100000  # Scaling factor for decimal precision

    def _get_base(self, n):
        """Finds closest power of 10."""
        s = str(n)
        length = len(s)
        # Dynamic base selection logic
        return 10 ** (length - 1) if n < 10**length - 5 * 10**(length-2) else 10 ** length

    def nikhilam_multiply(self, a, b):
        """
        Vedic Multiplication: (Base + Dev A) * (Base + Dev B)
        """
        base = self._get_base(max(a, b))
        dev_a = a - base
        dev_b = b - base
        
        lhs = a + dev_b
        rhs = dev_a * dev_b
        
        return (lhs * base) + rhs

    def vedic_power_scaled(self, base_val, power):
        """
        Calculates (base_val ^ power) using Recursive Vedic Squaring.
        Input 'base_val' is assumed to be scaled (integer).
        """
        result = self.SCALE
        current_base = base_val
        
        while power > 0:
            if power % 2 == 1:
                # Vedic Multiply: Result * CurrentBase
                result = self.nikhilam_multiply(result, current_base) // self.SCALE
            
            # Vedic Square: CurrentBase * CurrentBase
            current_base = self.nikhilam_multiply(current_base, current_base) // self.SCALE
            power = power // 2
            
        return result

    def calculate_emi(self, principal, rate_annual, tenure_years):
        try:
            r_monthly = rate_annual / (12 * 100)
            n_months = int(tenure_years * 12)
            
            # 1. Scale decimal to integer for Vedic Engine
            # e.g., 1.0083 -> 100830
            scaled_base = int((1 + r_monthly) * self.SCALE)
            
            # 2. Execute Vedic Exponentiation
            scaled_pow = self.vedic_power_scaled(scaled_base, n_months)
            
            # 3. Descale
            factor = scaled_pow / self.SCALE
            
            # 4. Final EMI Formula
            if factor == 1: return 0 # Avoid division by zero
            
            numerator = principal * r_monthly * factor
            denominator = factor - 1
            
            return round(numerator / denominator, 2)
        except Exception as e:
            return {"error": str(e)}