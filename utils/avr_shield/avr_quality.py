"""
AVR-SHIELD — Perceptual Quality and Bit Error Rate (BER) Evaluator
Calculates:
- Audio Signal-to-Noise Ratio (SNR) and Audio PSNR
- Video Peak Signal-to-Noise Ratio (PSNR)
- Video Structural Similarity Index (SSIM)
- Pre-FEC and Post-FEC Bit Error Rate (BER)
"""

import math
import numpy as np
import cv2
from typing import Dict, Any, List

def compute_audio_snr(original: np.ndarray, watermarked: np.ndarray) -> float:
    """Computes the Signal-to-Noise Ratio (SNR) in dB between original and watermarked audio."""
    orig = original.flatten().astype(np.float64)
    wm = watermarked.flatten().astype(np.float64)
    min_len = min(len(orig), len(wm))
    orig = orig[:min_len]
    wm = wm[:min_len]

    signal_power = np.sum(orig ** 2)
    noise_power = np.sum((orig - wm) ** 2)
    if noise_power == 0:
        return 100.0  # Mathematically infinite SNR
    if signal_power == 0:
        return 0.0

    snr_db = 10.0 * math.log10(signal_power / noise_power)
    return round(float(snr_db), 2)

def compute_video_psnr(orig_frame: np.ndarray, wm_frame: np.ndarray) -> float:
    """Computes the Peak Signal-to-Noise Ratio (PSNR) in dB between two video frames."""
    mse = np.mean((orig_frame.astype(np.float64) - wm_frame.astype(np.float64)) ** 2)
    if mse == 0:
        return 100.0
    psnr = 20.0 * math.log10(255.0 / math.sqrt(mse))
    return round(float(psnr), 2)

def compute_video_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """Computes Structural Similarity Index (SSIM) on the luminance (Y) channel."""
    if img1.ndim == 3:
        y1 = cv2.cvtColor(img1, cv2.COLOR_BGR2YUV)[:, :, 0].astype(np.float64)
        y2 = cv2.cvtColor(img2, cv2.COLOR_BGR2YUV)[:, :, 0].astype(np.float64)
    else:
        y1 = img1.astype(np.float64)
        y2 = img2.astype(np.float64)

    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(y1, -1, window)[5:-5, 5:-5]
    mu2 = cv2.filter2D(y2, -1, window)[5:-5, 5:-5]

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = cv2.filter2D(y1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(y2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(y1 * y2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return round(float(np.mean(ssim_map)), 4)

def compute_ber(original_bits: List[int], recovered_bits: List[int]) -> float:
    """Computes the Bit Error Rate (BER) as a percentage [0.0%, 100.0%]."""
    if not original_bits or not recovered_bits:
        return 100.0
    min_len = min(len(original_bits), len(recovered_bits))
    errors = sum(1 for i in range(min_len) if original_bits[i] != recovered_bits[i])
    errors += abs(len(original_bits) - len(recovered_bits))
    max_len = max(len(original_bits), len(recovered_bits))
    ber = (errors / max_len) * 100.0
    return round(float(ber), 2)
