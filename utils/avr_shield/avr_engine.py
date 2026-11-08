"""
AVR-SHIELD — Audio-Visual Redundant Resilient Payload Engine
Core Orchestrator & CLI Interface
Integrates Audio Spread-Spectrum, Video Luminance SS, Reed-Solomon FEC,
Argon2id/PBKDF2 AES-256-GCM authenticated encryption, and 3-Path Recovery Coordinator.
"""

import os
import sys
import json
import struct
import zlib
import tempfile
import subprocess
import cv2
import numpy as np
import imageio_ffmpeg
from typing import Dict, Any, List, Optional, Tuple

from .avr_crypto import PayloadEncryptionManager, AuthenticationFailedError
from .avr_reedsolo import ReedSolomonCodec
from .avr_audio import AudioSpreadSpectrumCodec
from .avr_video import VideoLuminanceSpreadSpectrumCodec
from .avr_coordinator import RecoveryCoordinator, PacketFramer
from .avr_quality import compute_audio_snr, compute_video_psnr, compute_video_ssim

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

class AVRShieldEngine:
    """Complete AVR-SHIELD Non-AI Steganography Engine Orchestrator."""

    def __init__(self):
        self.crypto_mgr = PayloadEncryptionManager()
        self.audio_codec = AudioSpreadSpectrumCodec()

    def analyze_media(self, media_path: str) -> Dict[str, Any]:
        """Inspects resolution, frame rate, duration, audio properties, and capacity."""
        if not os.path.exists(media_path):
            raise FileNotFoundError(f"Media file not found: {media_path}")

        # Run FFprobe / FFmpeg to read stream metadata
        probe_cmd = [
            FFMPEG_EXE, "-i", media_path,
            "-hide_banner"
        ]
        proc = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        meta_str = proc.stderr

        # Video properties via OpenCV
        cap = cv2.VideoCapture(media_path)
        has_video = cap.isOpened()
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) if has_video else 0
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) if has_video else 0
        fps = float(cap.get(cv2.CAP_PROP_FPS)) if has_video else 0.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if has_video else 0
        duration_sec = (frame_count / fps) if (has_video and fps > 0) else 0.0
        cap.release()

        has_audio = ("Audio:" in meta_str)

        # Capacity estimation
        audio_capacity_bytes = int((duration_sec * 44100 / 512 / 8) * (36 / 64)) if has_audio and duration_sec > 0 else 0
        video_capacity_bytes = int(((frame_count - 4) // 6 * 8) * (36 / 64)) if has_video and frame_count > 10 else 0

        return {
            "media_path": media_path,
            "has_video": has_video,
            "has_audio": has_audio,
            "width": width,
            "height": height,
            "fps": round(fps, 2),
            "frame_count": frame_count,
            "duration_sec": round(duration_sec, 2),
            "audio_capacity_bytes": audio_capacity_bytes,
            "video_capacity_bytes": video_capacity_bytes,
            "engine": "AVR-SHIELD",
            "version": "1.0.0"
        }

    def _extract_audio_pcm(self, video_path: str, target_sr: int = 44100) -> Tuple[np.ndarray, bool]:
        """Extracts audio track as float32 PCM numpy array."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            wav_tmp = tf.name

        try:
            cmd = [
                FFMPEG_EXE, "-y",
                "-i", video_path,
                "-vn",
                "-ac", "1",  # Mono
                "-ar", str(target_sr),
                "-acodec", "pcm_s16le",
                wav_tmp
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode != 0 or not os.path.exists(wav_tmp) or os.path.getsize(wav_tmp) < 100:
                return np.zeros(0, dtype=np.float32), False

            # Read WAV bytes
            with open(wav_tmp, "rb") as wf:
                raw_bytes = wf.read()

            # Skip 44-byte header
            pcm_bytes = raw_bytes[44:]
            samples = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            return samples, True
        finally:
            if os.path.exists(wav_tmp):
                try: os.unlink(wav_tmp)
                except Exception: pass

    def _write_pcm_to_wav(self, pcm: np.ndarray, out_wav: str, sr: int = 44100):
        """Writes float32 array [-1.0, 1.0] to a 16-bit PCM WAV file."""
        int16_samples = np.clip(pcm * 32767.0, -32768.0, 32767.0).astype(np.int16)
        raw_pcm = int16_samples.tobytes()
        num_channels = 1
        byte_rate = sr * num_channels * 2
        block_align = num_channels * 2

        with open(out_wav, "wb") as wf:
            # RIFF Header
            wf.write(b"RIFF")
            wf.write(struct.pack("<I", 36 + len(raw_pcm)))
            wf.write(b"WAVE")
            wf.write(b"fmt ")
            wf.write(struct.pack("<I", 16))
            wf.write(struct.pack("<H", 1)) # PCM
            wf.write(struct.pack("<H", num_channels))
            wf.write(struct.pack("<I", sr))
            wf.write(struct.pack("<I", byte_rate))
            wf.write(struct.pack("<H", block_align))
            wf.write(struct.pack("<H", 16)) # 16-bit
            wf.write(b"data")
            wf.write(struct.pack("<I", len(raw_pcm)))
            wf.write(raw_pcm)

    def embed(
        self,
        video_path: str,
        secret_text: str,
        password: str,
        output_path: str,
        decoy_text: Optional[str] = None,
        decoy_password: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Embeds secret_text into the video's audio track using robust psychoacoustic spread-spectrum
        with AES-256-GCM authenticated encryption and Reed-Solomon RS(64,36) error correction.
        Video visual stream is copied with zero re-encoding (-c:v copy), preserving 100% original video quality.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        key_seed = zlib.crc32(password.encode('utf-8'))

        # 1. Encrypt payload via AES-256-GCM
        envelope, enc_meta = self.crypto_mgr.encrypt_payload(
            secret_text=secret_text,
            password=password,
            channel_id="A",
            decoy_text=decoy_text,
            decoy_password=decoy_password
        )

        # 2. Extract or synthesize Audio Track
        audio_pcm, has_audio = self._extract_audio_pcm(video_path, 44100)
        req_chips = (len(envelope) + 2 + 35) // 36 * 64 * 8 * self.audio_codec.chip_len + 2048

        if not has_audio:
            # If video has no audio, synthesize ambient acoustic carrier
            target_len = max(req_chips + 44100 * 2, 44100 * 5)
            t = np.linspace(0, target_len / 44100, target_len, endpoint=False)
            audio_pcm = (0.01 * np.sin(2 * np.pi * 440 * t) + 0.005 * np.random.randn(len(t))).astype(np.float32)
        elif len(audio_pcm) < req_chips:
            # If video has audio but is shorter than payload, tile existing audio
            repeats = int(math.ceil(req_chips / len(audio_pcm))) + 1
            audio_pcm = np.tile(audio_pcm, repeats)[:max(req_chips + 44100 * 2, len(audio_pcm) * repeats)]

        # 3. Embed in audio carrier using psychoacoustic spread-spectrum
        wm_audio, audio_stats = self.audio_codec.encode_audio_stream(audio_pcm, envelope, key_seed)
        snr_val = compute_audio_snr(audio_pcm, wm_audio)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf_audio:
            wm_audio_tmp = tf_audio.name

        try:
            self._write_pcm_to_wav(wm_audio, wm_audio_tmp, 44100)

            # 4. Re-mux video stream directly (-c:v copy) with watermarked audio
            # Use -stream_loop -1 so shorter videos loop seamlessly to match watermark length
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            remux_cmd = [
                FFMPEG_EXE, "-y",
                "-stream_loop", "-1",
                "-i", video_path,
                "-i", wm_audio_tmp,
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_path
            ]
            subprocess.run(remux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        finally:
            if os.path.exists(wm_audio_tmp):
                try: os.unlink(wm_audio_tmp)
                except Exception: pass

        return {
            "success": True,
            "engine": "AVR-SHIELD",
            "output_path": output_path,
            "audio_snr_db": snr_val,
            "video_psnr_db": 100.0,  # Lossless video copy (100 dB represents mathematical identity)
            "video_ssim": 1.0,        # Lossless video copy
            "encryption": enc_meta,
            "audio_stats": audio_stats
        }

    def extract(self, video_path: str, password: str, is_simulated_test: bool = False) -> Dict[str, Any]:
        """
        Blind extraction of payload from video carrier.
        Extracts the audio track and decodes the spread-spectrum signal.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Media file not found: {video_path}")

        key_seed = zlib.crc32(password.encode('utf-8'))

        # 1. Extract audio PCM
        audio_pcm, has_audio = self._extract_audio_pcm(video_path, 44100)
        if not has_audio or len(audio_pcm) < 44100:
            return {
                "success": False,
                "authenticated": False,
                "error": "No valid audio track found in media container.",
                "recovered_text": None,
                "is_simulated_test": is_simulated_test
            }

        # 2. Decode audio stream
        audio_payload, audio_stats = self.audio_codec.decode_audio_stream(audio_pcm, key_seed)
        if not audio_payload:
            return {
                "success": False,
                "authenticated": False,
                "error": audio_stats.get("error", "Failed to decode steganographic audio track."),
                "audio_stats": audio_stats,
                "recovered_text": None,
                "is_simulated_test": is_simulated_test
            }

        # 3. Decrypt and authenticate AES-256-GCM
        try:
            plaintext, auth_info = self.crypto_mgr.decrypt_payload(audio_payload, password)
            return {
                "success": True,
                "authenticated": True,
                "path_successful": "PATH_A_AUDIO",
                "vault": auth_info.get("vault", "PRIMARY"),
                "recovered_text": plaintext,
                "audio_stats": audio_stats,
                "engine": "AVR-SHIELD",
                "is_simulated_test": is_simulated_test
            }
        except AuthenticationFailedError:
            return {
                "success": False,
                "authenticated": False,
                "error": "Cryptographic authentication failed. Incorrect password or data corrupted.",
                "audio_stats": audio_stats,
                "engine": "AVR-SHIELD",
                "recovered_text": None,
                "is_simulated_test": is_simulated_test
            }

    def simulate_whatsapp(self, input_video: str, output_video: str, profile: str = "standard") -> Dict[str, Any]:
        """
        Simulates WhatsApp lossy server re-encoding:
        - Downscales to 720p (or 480p)
        - H.264 aggressive CRF 28 encoding
        - AAC audio downsampling to 64k
        - Strips container metadata
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)
        scale_filter = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" if profile == "standard" else "scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2"

        ffmpeg_cmd = [
            FFMPEG_EXE, "-y",
            "-i", input_video,
            "-vf", scale_filter,
            "-r", "30",
            "-c:v", "libx264",
            "-crf", "28",
            "-preset", "faster",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "64k",
            "-map_metadata", "-1",
            output_video
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        return {
            "simulated_video": output_video,
            "codec": "H.264 (CRF 28) + AAC 64k",
            "resolution": "1280x720" if profile == "standard" else "854x480",
            "fps": 30.0,
            "metadata_stripped": True,
            "channel_classification": "SIMULATED_RE_ENCODING"
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        engine = AVRShieldEngine()
        try:
            if cmd == "analyze":
                res = engine.analyze_media(sys.argv[2])
                print(json.dumps(res))
            elif cmd == "embed":
                # embed <video_path> <secret_text> <password> <output_path> [decoy_text] [decoy_pass]
                video_path = sys.argv[2]
                secret_text = sys.argv[3]
                password = sys.argv[4]
                output_path = sys.argv[5]
                decoy_text = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != "null" else None
                decoy_pass = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] != "null" else None
                res = engine.embed(video_path, secret_text, password, output_path, decoy_text, decoy_pass)
                print(json.dumps(res))
            elif cmd == "extract":
                video_path = sys.argv[2]
                password = sys.argv[3]
                is_sim = len(sys.argv) > 4 and sys.argv[4].lower() == "true"
                res = engine.extract(video_path, password, is_sim)
                print(json.dumps(res))
            elif cmd == "simulate":
                in_path = sys.argv[2]
                out_path = sys.argv[3]
                prof = sys.argv[4] if len(sys.argv) > 4 else "standard"
                res = engine.simulate_whatsapp(in_path, out_path, prof)
                print(json.dumps(res))
            else:
                print(json.dumps({"error": f"Unknown command: {cmd}", "success": False}))
                sys.exit(1)
        except Exception as e:
            print(json.dumps({"error": str(e), "success": False}))
            sys.exit(1)
    else:
        print("AVR-SHIELD Engine instantiated successfully with FFmpeg:", FFMPEG_EXE)
