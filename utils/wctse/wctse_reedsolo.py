"""
WCTSE Reed-Solomon Error Correction Codec
Field: GF(2^8), Primitive Polynomial: x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
Zero external dependencies (pure Python / NumPy).
Systematic RS(n, k) encoder and Berlekamp-Massey / Forney decoder.
"""

import sys
import random

class ReedSolomonError(Exception):
    """Base exception for Reed-Solomon decoding failures."""
    pass

class ReedSolomonUncorrectableError(ReedSolomonError):
    """Raised when errors exceed the correction capability of the code."""
    pass

class GaloisField256:
    def __init__(self, prim=0x11D):
        self.prim = prim
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(255):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:
                x ^= self.prim
        for i in range(255, 512):
            self.exp[i] = self.exp[i - 255]

    def mul(self, x, y):
        if x == 0 or y == 0:
            return 0
        return self.exp[self.log[x] + self.log[y]]

    def div(self, x, y):
        if y == 0:
            raise ZeroDivisionError("Division by zero in GF(256)")
        if x == 0:
            return 0
        return self.exp[(self.log[x] - self.log[y]) % 255]

    def poly_mul(self, p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                r[i + j] ^= self.mul(a, b)
        return r

    def poly_div(self, dividend, divisor):
        msg_out = list(dividend)
        for i in range(len(dividend) - len(divisor) + 1):
            coef = msg_out[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    msg_out[i + j] ^= self.mul(divisor[j], coef)
        sep = -(len(divisor) - 1)
        return msg_out[:sep], msg_out[sep:]

    def poly_eval_high(self, poly, x):
        """Evaluates highest-degree-first polynomial: poly[0]*x^(d) + ... + poly[d]"""
        y = poly[0]
        for i in range(1, len(poly)):
            y = self.mul(y, x) ^ poly[i]
        return y

    def poly_eval_low(self, poly, x):
        """Evaluates lowest-degree-first polynomial: poly[0] + poly[1]*x + ..."""
        res = 0
        p = 1
        for c in poly:
            res ^= self.mul(c, p)
            p = self.mul(p, x)
        return res

    def generator_poly(self, nsym):
        g = [1]
        for i in range(nsym):
            g = self.poly_mul(g, [1, self.exp[i]])
        return g

_gf = GaloisField256()

class ReedSolomonCodec:
    def __init__(self, n, k):
        if n > 255 or k >= n or k <= 0:
            raise ValueError(f"Invalid RS parameters: n={n}, k={k}. Must have 0 < k < n <= 255.")
        self.n = n
        self.k = k
        self.nsym = n - k
        self.t = self.nsym // 2
        self.gf = _gf
        self.gen = self.gf.generator_poly(self.nsym)

    def encode(self, data_bytes):
        """
        Systematic encode: data_bytes (len <= k) -> bytes of length n.
        Appends nsym parity bytes.
        """
        if len(data_bytes) > self.k:
            raise ValueError(f"Data length {len(data_bytes)} exceeds capacity {self.k}")
        
        # Pad data with zeros if shorter than k
        pad_len = self.k - len(data_bytes)
        padded = list(data_bytes) + [0] * pad_len
        
        # Multiply by x^(nsym)
        msg_poly = padded + [0] * self.nsym
        _, remainder = self.gf.poly_div(msg_poly, self.gen)
        
        codeword = padded + remainder
        return bytes(codeword)

    def decode(self, codeword_bytes):
        """
        Decodes a received codeword of length n.
        Returns: (data_bytes, errors_corrected_count)
        Raises: ReedSolomonUncorrectableError if uncorrectable.
        """
        if len(codeword_bytes) != self.n:
            raise ValueError(f"Codeword length {len(codeword_bytes)} does not match n={self.n}")

        r = list(codeword_bytes)
        nsym = self.nsym
        gf = self.gf

        # 1. Compute syndromes: S_i = r(alpha^i)
        syndromes = [gf.poly_eval_high(r, gf.exp[i]) for i in range(nsym)]
        if max(syndromes) == 0:
            # Clean codeword, zero errors
            return bytes(r[:self.k]), 0

        # 2. Berlekamp-Massey algorithm for error locator polynomial C(x) (lowest degree first)
        C = [1]
        B = [1]
        L = 0
        m = 1
        b = 1

        for N in range(nsym):
            d = syndromes[N]
            for i in range(1, L + 1):
                if i < len(C):
                    d ^= gf.mul(C[i], syndromes[N - i])

            if d == 0:
                m += 1
            elif 2 * L <= N:
                T = list(C)
                scale = gf.div(d, b)
                shifted_B = [0] * m + [gf.mul(scale, x) for x in B]
                max_len = max(len(C), len(shifted_B))
                C = [(C[i] if i < len(C) else 0) ^ (shifted_B[i] if i < len(shifted_B) else 0) for i in range(max_len)]
                L = N + 1 - L
                B = T
                b = d
                m = 1
            else:
                scale = gf.div(d, b)
                shifted_B = [0] * m + [gf.mul(scale, x) for x in B]
                max_len = max(len(C), len(shifted_B))
                C = [(C[i] if i < len(C) else 0) ^ (shifted_B[i] if i < len(shifted_B) else 0) for i in range(max_len)]
                m += 1

        num_errors = len(C) - 1
        if num_errors * 2 > nsym:
            raise ReedSolomonUncorrectableError(f"Too many errors ({num_errors}) for nsym={nsym}")

        # 3. Chien search for error positions
        roots = []
        for i in range(self.n):
            X = gf.exp[self.n - 1 - i]
            X_inv = gf.div(1, X)
            if gf.poly_eval_low(C, X_inv) == 0:
                roots.append((i, X, X_inv))

        if len(roots) != num_errors:
            raise ReedSolomonUncorrectableError(f"Chien search found {len(roots)} roots, expected {num_errors}")

        # 4. Error evaluator polynomial Omega(x) = (S(x) * C(x)) mod x^(nsym)
        omega = [0] * nsym
        for i in range(nsym):
            for j in range(len(C)):
                if i + j < nsym:
                    omega[i + j] ^= gf.mul(syndromes[i], C[j])

        # Formal derivative C'(x)
        C_prime = [C[i] for i in range(1, len(C), 2)]

        corrected = list(r)
        for pos, X, X_inv in roots:
            omega_val = gf.poly_eval_low(omega, X_inv)
            prime_val = gf.poly_eval_low(C_prime, gf.mul(X_inv, X_inv))
            if prime_val == 0:
                raise ReedSolomonUncorrectableError("Zero derivative in Forney algorithm")
            err_val = gf.mul(X, gf.div(omega_val, prime_val))
            corrected[pos] ^= err_val

        # Verify corrected codeword
        new_syndromes = [gf.poly_eval_high(corrected, gf.exp[i]) for i in range(nsym)]
        if max(new_syndromes) != 0:
            raise ReedSolomonUncorrectableError("Correction verification failed; uncorrectable corruption pattern")

        return bytes(corrected[:self.k]), len(roots)

# Self-test when executed directly
if __name__ == "__main__":
    print("Testing Reed-Solomon Codec...")
    # Test RS(64, 36) - 28 parity symbols, can correct 14 errors
    rs64 = ReedSolomonCodec(64, 36)
    msg = b"PixelCraft-AI-WCTSE-Payload-Chunk-01"
    assert len(msg) == 36
    codeword = bytearray(rs64.encode(msg))
    assert len(codeword) == 64

    # Inject 14 random errors
    corrupted = bytearray(codeword)
    error_indices = random.sample(range(64), 14)
    for idx in error_indices:
        corrupted[idx] ^= random.randint(1, 255)

    recovered, err_count = rs64.decode(corrupted)
    assert recovered == msg, "RS(64, 36) failed to recover original message!"
    assert err_count == 14, f"Expected 14 errors corrected, got {err_count}"
    print(f"RS(64, 36) PASSED: Successfully corrected {err_count}/14 injected byte errors!")

    # Test RS(48, 20) - 28 parity symbols, can correct 14 errors
    rs48 = ReedSolomonCodec(48, 20)
    msg20 = b"WCTSE-Profile-B-Test"
    assert len(msg20) == 20
    cw48 = bytearray(rs48.encode(msg20))
    error_indices2 = random.sample(range(48), 14)
    for idx in error_indices2:
        cw48[idx] ^= random.randint(1, 255)
    rec20, err2 = rs48.decode(cw48)
    assert rec20 == msg20, "RS(48, 20) failed to recover original message!"
    assert err2 == 14
    print(f"RS(48, 20) PASSED: Successfully corrected {err2}/14 injected byte errors!")
