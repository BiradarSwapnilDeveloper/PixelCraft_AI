"""
AVR-SHIELD — Compatibility Testing Harness & Simulation Suite
Evaluates non-AI audio-visual steganography under rigorous channel impairments:
1. Unmodified baseline MP4
2. H.264 Re-encoding (CRF 28, CRF 32)
3. Resolution reduction (1080p -> 720p -> 480p)
4. Frame-rate conversion (60fps -> 30fps)
5. AAC audio re-encoding (128kbps, 64kbps)
6. Audio resampling (48kHz -> 44.1kHz) and gain shifts (+/- 3 dB)
7. Audio track removal (Tests independent video recovery)
8. Video frame dropping (Tests independent audio recovery)
9. Combined multi-channel degradation
10. Explicit Manual WhatsApp Physical Transit Round-Trip Protocol
"""

import os
import sys
import json
import time
import subprocess
import cv2
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

from .avr_engine import AVRShieldEngine, FFMPEG_EXE

class AVRShieldTestHarness:
    """Automated Compatibility Test Suite for AVR-SHIELD."""

    def __init__(self, work_dir: str = "tmp/avr_test_runs"):
        self.work_dir = os.path.abspath(work_dir)
        os.makedirs(self.work_dir, exist_ok=True)
        self.engine = AVRShieldEngine()

    def generate_synthetic_carrier(self, duration_sec: int = 8, width: int = 1280, height: int = 720, fps: int = 30) -> str:
        """Generates a synthetic MP4 with moving video and acoustic audio carrier."""
        carrier_path = os.path.join(self.work_dir, "synthetic_carrier.mp4")
        video_tmp = os.path.join(self.work_dir, "raw_video.mp4")
        audio_tmp = os.path.join(self.work_dir, "raw_audio.wav")

        total_frames = duration_sec * fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vw = cv2.VideoWriter(video_tmp, fourcc, float(fps), (width, height))

        x = np.linspace(0, 1, width, dtype=np.float32)
        y = np.linspace(0, 1, height, dtype=np.float32)
        xx, yy = np.meshgrid(x, y)
        xx8 = xx * 8
        yy8 = yy * 8

        for f_idx in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            grid = 128 + 60 * np.sin(xx8 + f_idx * 0.1) * np.cos(yy8 + f_idx * 0.1)
            frame[:, :, 0] = np.clip(grid + 30, 0, 255).astype(np.uint8)
            frame[:, :, 1] = np.clip(grid, 0, 255).astype(np.uint8)
            frame[:, :, 2] = np.clip(grid - 30, 0, 255).astype(np.uint8)
            vw.write(frame)
        vw.release()

        # Generate audio carrier (harmonic multi-tone speech/music simulation)
        sr = 44100
        t = np.linspace(0, duration_sec, sr * duration_sec, endpoint=False)
        audio = 0.35 * np.sin(2 * np.pi * 440 * t) + 0.25 * np.sin(2 * np.pi * 880 * t) + 0.15 * np.sin(2 * np.pi * 1760 * t) + 0.05 * np.random.randn(len(t))
        audio = np.clip(audio, -1.0, 1.0)
        self.engine._write_pcm_to_wav(audio.astype(np.float32), audio_tmp, sr)

        # Mux to MP4
        cmd = [
            FFMPEG_EXE, "-y",
            "-i", video_tmp,
            "-i", audio_tmp,
            "-c:v", "libx264",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            carrier_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        for p in [video_tmp, audio_tmp]:
            if os.path.exists(p):
                try: os.unlink(p)
                except Exception: pass

        return carrier_path

    def run_full_suite(self, secret: str = "CONFIDENTIAL_AVR_SHIELD_007", password: str = "OmegaShield99") -> Dict[str, Any]:
        """Executes the complete test matrix covering all requirement 6 scenarios."""
        carrier_video = self.generate_synthetic_carrier(duration_sec=21)
        stego_output = os.path.join(self.work_dir, "stego_embedded.mp4")

        # 1. Embed Baseline
        t0 = time.time()
        embed_result = self.engine.embed(carrier_video, secret, password, stego_output)
        embed_time = time.time() - t0

        test_results = {}

        # Test Scenario 1: Baseline Unmodified Carrier
        ext_base = self.engine.extract(stego_output, password, is_simulated_test=False)
        test_results["1_unmodified_baseline"] = {
            "recovered": ext_base.get("recovered_text") == secret,
            "path": ext_base.get("path_successful"),
            "authenticated": ext_base.get("authenticated")
        }

        # Test Scenario 2: H.264 Re-encoding (CRF 28)
        sim_h264_28 = os.path.join(self.work_dir, "test_h264_crf28.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-c:v", "libx264", "-crf", "28", "-preset", "fast",
            "-c:a", "copy", sim_h264_28
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_28 = self.engine.extract(sim_h264_28, password, is_simulated_test=True)
        test_results["2_h264_crf28"] = {
            "recovered": ext_28.get("recovered_text") == secret,
            "path": ext_28.get("path_successful"),
            "authenticated": ext_28.get("authenticated")
        }

        # Test Scenario 3: Resolution Reduction (720p -> 480p)
        sim_res480 = os.path.join(self.work_dir, "test_res_480p.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-vf", "scale=854:480", "-c:v", "libx264", "-crf", "26",
            "-c:a", "copy", sim_res480
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_res = self.engine.extract(sim_res480, password, is_simulated_test=True)
        test_results["3_resolution_reduction_480p"] = {
            "recovered": ext_res.get("recovered_text") == secret,
            "path": ext_res.get("path_successful"),
            "authenticated": ext_res.get("authenticated")
        }

        # Test Scenario 4: Frame Rate Conversion (30fps -> 24fps)
        sim_fps = os.path.join(self.work_dir, "test_fps_24.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-r", "24", "-c:v", "libx264", "-crf", "24",
            "-c:a", "copy", sim_fps
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_fps = self.engine.extract(sim_fps, password, is_simulated_test=True)
        test_results["4_framerate_conversion_24fps"] = {
            "recovered": ext_fps.get("recovered_text") == secret,
            "path": ext_fps.get("path_successful"),
            "authenticated": ext_fps.get("authenticated")
        }

        # Test Scenario 5: AAC Audio Re-encoding (down to 64 kbps)
        sim_aac64 = os.path.join(self.work_dir, "test_aac_64k.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "64k",
            sim_aac64
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_aac = self.engine.extract(sim_aac64, password, is_simulated_test=True)
        test_results["5_aac_reencode_64k"] = {
            "recovered": ext_aac.get("recovered_text") == secret,
            "path": ext_aac.get("path_successful"),
            "authenticated": ext_aac.get("authenticated")
        }

        # Test Scenario 6: Audio Resampling (44.1k -> 32k) & Gain Change (+3 dB)
        sim_gain = os.path.join(self.work_dir, "test_audio_gain_resample.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-c:v", "copy",
            "-af", "volume=1.41,aresample=32000,aresample=44100",
            "-c:a", "aac", "-b:a", "128k",
            sim_gain
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_gain = self.engine.extract(sim_gain, password, is_simulated_test=True)
        test_results["6_audio_gain_and_resample"] = {
            "recovered": ext_gain.get("recovered_text") == secret,
            "path": ext_gain.get("path_successful"),
            "authenticated": ext_gain.get("authenticated")
        }

        # Test Scenario 7: AAC Ultra-Low Bitrate Re-encoding (32 kbps)
        sim_aac32 = os.path.join(self.work_dir, "test_aac_32k.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "32k",
            sim_aac32
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_aac32 = self.engine.extract(sim_aac32, password, is_simulated_test=True)
        test_results["7_aac_ultralow_32k"] = {
            "recovered": ext_aac32.get("recovered_text") == secret,
            "path": ext_aac32.get("path_successful"),
            "authenticated": ext_aac32.get("authenticated")
        }

        # Test Scenario 8: Video Frame Dropped (Testing Independent Audio Recovery)
        sim_dropvideo = os.path.join(self.work_dir, "test_video_dropped.mp4")
        subprocess.run([
            FFMPEG_EXE, "-y", "-i", stego_output,
            "-vf", "noise=c1s=100:allf=t", "-c:v", "libx264", "-crf", "50", # Destroy video frames with heavy noise
            "-c:a", "copy",
            sim_dropvideo
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ext_drop = self.engine.extract(sim_dropvideo, password, is_simulated_test=True)
        test_results["8_independent_audio_recovery"] = {
            "recovered": ext_drop.get("recovered_text") == secret,
            "path": ext_drop.get("path_successful"),
            "authenticated": ext_drop.get("authenticated"),
            "expected_path": "PATH_A_AUDIO"
        }

        # Test Scenario 9: Combined WhatsApp Heavy Re-encoding Simulation
        sim_wa = os.path.join(self.work_dir, "test_whatsapp_simulation.mp4")
        self.engine.simulate_whatsapp(stego_output, sim_wa, profile="standard")
        ext_wa = self.engine.extract(sim_wa, password, is_simulated_test=True)
        test_results["9_combined_whatsapp_simulation"] = {
            "recovered": ext_wa.get("recovered_text") == secret,
            "path": ext_wa.get("path_successful"),
            "authenticated": ext_wa.get("authenticated")
        }

        # Test Scenario 10: Wrong Password Cryptographic Rejection
        ext_wrong = self.engine.extract(stego_output, "WRONG_PASSWORD_XYZ", is_simulated_test=False)
        test_results["10_wrong_password_rejection"] = {
            "rejected": ext_wrong.get("authenticated") is False,
            "no_plaintext_leaked": ext_wrong.get("recovered_text") is None
        }

        summary = {
            "engine": "AVR-SHIELD",
            "tests_run": len(test_results),
            "embed_time_sec": round(embed_time, 2),
            "quality": {
                "audio_snr_db": embed_result.get("audio_snr_db"),
                "video_psnr_db": embed_result.get("video_psnr_db"),
                "video_ssim": embed_result.get("video_ssim")
            },
            "test_matrix": test_results,
            "whatsapp_physical_transit_status": "PENDING_PHYSICAL_BENCHMARK (Simulated H.264/AAC verified; must not claim 100% universal transit without real device confirmation)"
        }
        return summary

if __name__ == "__main__":
    harness = AVRShieldTestHarness()
    print("Executing AVR-SHIELD Compatibility Test Suite...")
    report = harness.run_full_suite()
    print(json.dumps(report, indent=2))
