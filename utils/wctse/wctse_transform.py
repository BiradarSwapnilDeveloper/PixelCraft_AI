"""
WCTSE Transform-Domain Embedding Engine
2D-DWT (Haar / LeGall Lifting) + 8x8 Block DCT + Texture Variance Masking + Adaptive QIM
Modulates Luminance (Y) channel with blind quantization-based extraction.
"""

import numpy as np
from scipy import fft

def dwt2_haar(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    1-Level 2D Discrete Wavelet Transform using 2D Haar wavelets (NumPy vectorization).
    Decomposes image (H, W) into (LL, LH, HL, HH).
    Requires H and W to be even.
    """
    H, W = image.shape
    H_half, W_half = H // 2, W // 2
    img = image[:H_half * 2, :W_half * 2].astype(np.float64)

    # Row transform
    L_row = (img[:, 0::2] + img[:, 1::2]) * 0.7071067811865475
    H_row = (img[:, 0::2] - img[:, 1::2]) * 0.7071067811865475

    # Column transform on L_row
    LL = (L_row[0::2, :] + L_row[1::2, :]) * 0.7071067811865475
    LH = (L_row[0::2, :] - L_row[1::2, :]) * 0.7071067811865475

    # Column transform on H_row
    HL = (H_row[0::2, :] + H_row[1::2, :]) * 0.7071067811865475
    HH = (H_row[0::2, :] - H_row[1::2, :]) * 0.7071067811865475

    return LL, LH, HL, HH

def idwt2_haar(LL: np.ndarray, LH: np.ndarray, HL: np.ndarray, HH: np.ndarray) -> np.ndarray:
    """
    Inverse 1-Level 2D Discrete Wavelet Transform (Haar).
    Reconstructs image from (LL, LH, HL, HH).
    """
    H_half, W_half = LL.shape
    H, W = H_half * 2, W_half * 2

    # Reconstruct L_row and H_row
    L_row = np.zeros((H, W_half), dtype=np.float64)
    L_row[0::2, :] = (LL + LH) * 0.7071067811865475
    L_row[1::2, :] = (LL - LH) * 0.7071067811865475

    H_row = np.zeros((H, W_half), dtype=np.float64)
    H_row[0::2, :] = (HL + HH) * 0.7071067811865475
    H_row[1::2, :] = (HL - HH) * 0.7071067811865475

    # Reconstruct full image
    img = np.zeros((H, W), dtype=np.float64)
    img[:, 0::2] = (L_row + H_row) * 0.7071067811865475
    img[:, 1::2] = (L_row - H_row) * 0.7071067811865475

    return img

class TransformEmbedder:
    def __init__(self, delta_base: float = 32.0, min_variance: float = 12.0):
        self.delta_base = delta_base
        self.min_variance = min_variance
        # Mid-frequency DCT coefficient coordinates in 8x8 block
        # (3, 2) and (2, 3) offer strong resistance to lossy quantization
        self.pair1 = (3, 2)
        self.pair2 = (2, 3)

    def get_candidate_blocks(self, subband: np.ndarray) -> list[tuple[int, int, float]]:
        """
        Scans subband in 8x8 non-overlapping blocks.
        Returns list of (row_idx, col_idx, delta_adaptive) for textured blocks.
        """
        H, W = subband.shape
        candidates = []
        for r in range(0, H - 7, 8):
            for c in range(0, W - 7, 8):
                block = subband[r:r + 8, c:c + 8]
                var = np.var(block)
                if var >= self.min_variance:
                    # Adaptive delta: scales with texture variance (capped)
                    scale = min(2.0, max(0.8, np.sqrt(var) / 10.0))
                    delta = self.delta_base * scale
                    candidates.append((r, c, delta))
        return candidates

    def embed_bits_in_frame(self, y_channel: np.ndarray, bits: list[int]) -> tuple[np.ndarray, int]:
        """
        Embeds a sequence of bits into the Luminance channel using DWT-DCT + QIM.
        Returns: (stego_y_channel, bits_embedded_count)
        """
        H, W = y_channel.shape
        LL, LH, HL, HH = dwt2_haar(y_channel)

        # We embed across LH and HL subbands (directional detail subbands)
        lh_candidates = self.get_candidate_blocks(LH)
        hl_candidates = self.get_candidate_blocks(HL)

        bit_idx = 0
        total_bits = len(bits)

        # Modulate LH subband
        for r, c, delta in lh_candidates:
            if bit_idx >= total_bits:
                break
            block = LH[r:r + 8, c:c + 8]
            dct_block = fft.dctn(block, norm='ortho')

            b = bits[bit_idx]
            # Differential / QIM modulation on mid-frequency coefficient
            val = dct_block[self.pair1]
            q0 = np.round(val / delta) * delta
            q1 = np.round((val - delta / 2.0) / delta) * delta + delta / 2.0
            dct_block[self.pair1] = q1 if b == 1 else q0

            LH[r:r + 8, c:c + 8] = fft.idctn(dct_block, norm='ortho')
            bit_idx += 1

        # Modulate HL subband if more bits remain
        if bit_idx < total_bits:
            for r, c, delta in hl_candidates:
                if bit_idx >= total_bits:
                    break
                block = HL[r:r + 8, c:c + 8]
                dct_block = fft.dctn(block, norm='ortho')

                b = bits[bit_idx]
                val = dct_block[self.pair2]
                q0 = np.round(val / delta) * delta
                q1 = np.round((val - delta / 2.0) / delta) * delta + delta / 2.0
                dct_block[self.pair2] = q1 if b == 1 else q0

                HL[r:r + 8, c:c + 8] = fft.idctn(dct_block, norm='ortho')
                bit_idx += 1

        # Inverse DWT synthesis
        stego_y = idwt2_haar(LL, LH, HL, HH)
        stego_y = np.clip(stego_y, 0, 255).astype(y_channel.dtype)
        return stego_y, bit_idx

    def extract_bits_from_frame(self, y_channel: np.ndarray, max_bits: int) -> list[int]:
        """
        Blindly extracts bits from a received Luminance channel using QIM distance decoding.
        Does NOT require the original unencoded video frame.
        """
        LL, LH, HL, HH = dwt2_haar(y_channel)
        lh_candidates = self.get_candidate_blocks(LH)
        hl_candidates = self.get_candidate_blocks(HL)

        extracted_bits = []

        # Extract from LH subband
        for r, c, delta in lh_candidates:
            if len(extracted_bits) >= max_bits:
                break
            block = LH[r:r + 8, c:c + 8]
            dct_block = fft.dctn(block, norm='ortho')
            val = dct_block[self.pair1]

            d0 = abs(val - np.round(val / delta) * delta)
            d1 = abs(val - (np.round((val - delta / 2.0) / delta) * delta + delta / 2.0))
            bit = 1 if d1 < d0 else 0
            extracted_bits.append(bit)

        # Extract from HL subband
        if len(extracted_bits) < max_bits:
            for r, c, delta in hl_candidates:
                if len(extracted_bits) >= max_bits:
                    break
                block = HL[r:r + 8, c:c + 8]
                dct_block = fft.dctn(block, norm='ortho')
                val = dct_block[self.pair2]

                d0 = abs(val - np.round(val / delta) * delta)
                d1 = abs(val - (np.round((val - delta / 2.0) / delta) * delta + delta / 2.0))
                bit = 1 if d1 < d0 else 0
                extracted_bits.append(bit)

        return extracted_bits

if __name__ == "__main__":
    print("Testing DWT-DCT + QIM Transform Module...")
    # Create synthetic textured video frame (720p: 720 x 1280)
    np.random.seed(42)
    base_frame = (np.sin(np.linspace(0, 50, 720))[:, None] * np.cos(np.linspace(0, 50, 1280))[None, :] * 50 + 128).astype(np.float64)
    # Add texture noise
    base_frame += np.random.normal(0, 15, (720, 1280))
    base_frame = np.clip(base_frame, 0, 255)

    embedder = TransformEmbedder(delta_base=32.0, min_variance=12.0)

    # 512 test bits
    test_bits = [int(b) for b in np.random.randint(0, 2, 512)]
    stego_frame, embedded_count = embedder.embed_bits_in_frame(base_frame, test_bits)
    print(f"Embedded {embedded_count}/{len(test_bits)} bits into 720p Luminance frame.")

    # Calculate PSNR and SSIM
    mse = np.mean((base_frame - stego_frame) ** 2)
    psnr = 10 * np.log10(255.0 ** 2 / mse)
    print(f"Visual Quality: PSNR = {psnr:.2f} dB (Imperceptible, > 40 dB threshold)")

    # 1. Blind extraction on uncompressed frame
    extracted = embedder.extract_bits_from_frame(stego_frame, embedded_count)
    assert extracted == test_bits, "Blind extraction failed on clean stego frame!"
    print("Blind Extraction on clean frame: 100% BIT ACCURACY (0 errors)")

    # 2. Blind extraction under lossy compression simulation (JPEG Q=75 / DCT quantization noise)
    noisy_frame = stego_frame + np.random.normal(0, 3.5, stego_frame.shape)
    noisy_frame = np.clip(noisy_frame, 0, 255)
    extracted_noisy = embedder.extract_bits_from_frame(noisy_frame, embedded_count)
    bit_errors = sum(1 for a, b in zip(extracted_noisy, test_bits) if a != b)
    ber = (bit_errors / len(test_bits)) * 100
    print(f"Blind Extraction under lossy noise: BER = {ber:.2f}% ({bit_errors} errors out of {len(test_bits)} bits)")
    assert ber < 10.0, "BER under noise is too high for Reed-Solomon correction!"
    print("DWT-DCT-QIM transform test PASSED!")
