"""
WCTSE Video Quality Assessment & Perceptual Quality Gate
Computes frame-level PSNR, SSIM, and temporal quality variation.
Enforces automated quality gate to prevent perceptible stego artifacts.
"""

import numpy as np

def compute_psnr(orig: np.ndarray, stego: np.ndarray) -> float:
    """Computes Peak Signal-to-Noise Ratio (PSNR) in decibels (dB)."""
    mse = np.mean((orig.astype(np.float64) - stego.astype(np.float64)) ** 2)
    if mse == 0:
        return 100.0 # Effectively perfect
    return float(10.0 * np.log10((255.0 ** 2) / mse))

def compute_ssim_single_channel(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Computes Structural Similarity Index (SSIM) on 2D single channel array.
    Using standard Wang et al. constants C1 = (0.01*255)^2, C2 = (0.03*255)^2.
    """
    C1 = (0.01 * 255.0) ** 2
    C2 = (0.03 * 255.0) ** 2

    x = img1.astype(np.float64)
    y = img2.astype(np.float64)

    mu_x = np.mean(x)
    mu_y = np.mean(y)

    sigma_x_sq = np.var(x)
    sigma_y_sq = np.var(y)
    sigma_xy = np.mean((x - mu_x) * (y - mu_y))

    numerator = (2.0 * mu_x * mu_y + C1) * (2.0 * sigma_xy + C2)
    denominator = (mu_x ** 2 + mu_y ** 2 + C1) * (sigma_x_sq + sigma_y_sq + C2)

    if denominator == 0:
        return 1.0
    return float(numerator / denominator)

class QualityGate:
    def __init__(self, min_psnr: float = 38.0, min_ssim: float = 0.960):
        self.min_psnr = min_psnr
        self.min_ssim = min_ssim

    def evaluate_video(self, orig_frames: list[np.ndarray], stego_frames: list[np.ndarray]) -> dict:
        """
        Evaluates a sequence of frames for visual transparency.
        Returns metrics dict and pass/fail gate decision.
        """
        if len(orig_frames) == 0 or len(stego_frames) == 0:
            return {"passed": False, "reason": "No frames provided"}

        psnr_vals = []
        ssim_vals = []

        count = min(len(orig_frames), len(stego_frames))
        for i in range(count):
            p = compute_psnr(orig_frames[i], stego_frames[i])
            s = compute_ssim_single_channel(orig_frames[i], stego_frames[i])
            psnr_vals.append(p)
            ssim_vals.append(s)

        avg_psnr = float(np.mean(psnr_vals))
        avg_ssim = float(np.mean(ssim_vals))
        min_p = float(np.min(psnr_vals))
        min_s = float(np.min(ssim_vals))

        # Temporal flicker variance: standard deviation of PSNR across time
        temporal_var = float(np.std(psnr_vals))

        passed = (avg_psnr >= self.min_psnr) and (avg_ssim >= self.min_ssim)

        return {
            "passed": passed,
            "avg_psnr_db": round(avg_psnr, 2),
            "min_psnr_db": round(min_p, 2),
            "avg_ssim": round(avg_ssim, 4),
            "min_ssim": round(min_s, 4),
            "temporal_flicker_std_db": round(temporal_var, 3),
            "gate_thresholds": {
                "min_psnr_db": self.min_psnr,
                "min_ssim": self.min_ssim
            }
        }
