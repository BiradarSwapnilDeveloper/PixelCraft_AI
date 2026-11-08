"""
AVR-SHIELD — Reed-Solomon Forward Error Correction (FEC)
Field: GF(2^8), Primitive Polynomial: x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
Provides systematic RS(n, k) block encoding/decoding and multi-block stream framing.
"""

from typing import List, Tuple, Optional

class ReedSolomonError(Exception):
    pass

class ReedSolomonUncorrectableError(ReedSolomonError):
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

    def mul(self, x: int, y: int) -> int:
        if x == 0 or y == 0:
            return 0
        return self.exp[self.log[x] + self.log[y]]

    def div(self, x: int, y: int) -> int:
        if y == 0:
            raise ZeroDivisionError("Division by zero in GF(256)")
        if x == 0:
            return 0
        return self.exp[(self.log[x] - self.log[y]) % 255]

    def poly_mul(self, p: List[int], q: List[int]) -> List[int]:
        r = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                r[i + j] ^= self.mul(a, b)
        return r

    def poly_div(self, dividend: List[int], divisor: List[int]) -> Tuple[List[int], List[int]]:
        msg_out = list(dividend)
        for i in range(len(dividend) - len(divisor) + 1):
            coef = msg_out[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    msg_out[i + j] ^= self.mul(divisor[j], coef)
        sep = -(len(divisor) - 1)
        return msg_out[:sep], msg_out[sep:]

    def poly_eval_high(self, poly: List[int], x: int) -> int:
        """Evaluates highest-degree-first polynomial: poly[0]*x^d + ... + poly[d]"""
        y = poly[0]
        for i in range(1, len(poly)):
            y = self.mul(y, x) ^ poly[i]
        return y

    def poly_eval_low(self, poly: List[int], x: int) -> int:
        """Evaluates lowest-degree-first polynomial: poly[0] + poly[1]*x + ..."""
        res = 0
        p = 1
        for c in poly:
            res ^= self.mul(c, p)
            p = self.mul(p, x)
        return res

    def generator_poly(self, nsym: int) -> List[int]:
        g = [1]
        for i in range(nsym):
            g = self.poly_mul(g, [1, self.exp[i]])
        return g

_gf = GaloisField256()

class ReedSolomonCodec:
    """
    Reed-Solomon Systematic (n, k) Codec for AVR-SHIELD.
    Default parameters: n=64, k=36 (28 parity bytes, can correct up to 14 byte errors per block).
    """

    def __init__(self, n: int = 64, k: int = 36):
        if n > 255 or k >= n or k <= 0:
            raise ValueError(f"Invalid RS parameters: n={n}, k={k}. Must satisfy 0 < k < n <= 255.")
        self.n = n
        self.k = k
        self.nsym = n - k
        self.t = self.nsym // 2
        self.gf = _gf
        self.gen = self.gf.generator_poly(self.nsym)

    def encode(self, data_bytes: bytes) -> bytes:
        """Systematic RS(n, k) encoding of a block with length <= k."""
        if len(data_bytes) > self.k:
            raise ValueError(f"Data length {len(data_bytes)} exceeds capacity {self.k}")
        
        pad_len = self.k - len(data_bytes)
        padded = list(data_bytes) + [0] * pad_len
        msg_poly = padded + [0] * self.nsym
        _, remainder = self.gf.poly_div(msg_poly, self.gen)
        codeword = padded + remainder
        return bytes(codeword)

    def decode(self, codeword_bytes: bytes) -> Tuple[bytes, int]:
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
            return bytes(r[:self.k]), 0

        # 2. Berlekamp-Massey algorithm for error locator polynomial C(x)
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

    def encode_stream(self, data: bytes) -> bytes:
        """Splits an arbitrary length byte stream into k-byte blocks and encodes each to n bytes."""
        out = bytearray()
        for i in range(0, len(data), self.k):
            chunk = data[i:i + self.k]
            out.extend(self.encode(chunk))
        return bytes(out)

    def decode_stream(self, encoded_data: bytes, expected_length: Optional[int] = None) -> Tuple[bytes, int]:
        """Decodes an n-byte aligned stream of RS blocks."""
        out = bytearray()
        total_errors = 0
        if len(encoded_data) % self.n != 0:
            raise ReedSolomonError(f"Stream length ({len(encoded_data)}) must be a multiple of n={self.n}")

        for i in range(0, len(encoded_data), self.n):
            block = encoded_data[i:i + self.n]
            dec_chunk, errs = self.decode(block)
            out.extend(dec_chunk)
            total_errors += errs

        res = bytes(out)
        if expected_length is not None and expected_length <= len(res):
            res = res[:expected_length]
        return res, total_errors
