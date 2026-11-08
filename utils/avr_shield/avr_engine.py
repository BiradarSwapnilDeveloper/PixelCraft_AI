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
        self.video_codec = VideoLuminanceSpreadSpectrumCodec()
        self.coordinator = RecoveryCoordinator(self.crypto_mgr)

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
        Embeds secret_text across both Audio and Video Luminance channels with AES-256-GCM.
        Generates production-ready resilient MP4 carrier.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # 1. Derive key seed for PN spreading sequences
        key_seed = zlib.crc32(password.encode('utf-8'))

        # 2. Encrypt payload via AES-256-GCM
        envelope, enc_meta = self.crypto_mgr.encrypt_payload(
            secret_text=secret_text,
            password=password,
            channel_id="X",
            decoy_text=decoy_text,
            decoy_password=decoy_password
        )

        # 3. Frame payload into audio and video packet blocks
        audio_pkts, video_pkts = self.coordinator.frame_envelope(envelope, max_packet_size=128)
        audio_payload_bytes = audio_pkts[0] if audio_pkts else envelope
        video_payload_bytes = video_pkts[0] if video_pkts else envelope

        # 4. Process Audio Track (Primary)
        audio_pcm, has_audio = self._extract_audio_pcm(video_path, 44100)
        audio_stats = {}
        snr_val = 0.0

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf_audio:
            wm_audio_tmp = tf_audio.name

        try:
            if has_audio and len(audio_pcm) > 44100:
                wm_audio, audio_stats = self.audio_codec.encode_audio_stream(audio_pcm, audio_payload_bytes, key_seed)
                snr_val = compute_audio_snr(audio_pcm, wm_audio)
                self._write_pcm_to_wav(wm_audio, wm_audio_tmp, 44100)
            else:
                # Generate synthetic silent audio carrier if video has no audio
                dummy_pcm = np.random.randn(44100 * 8).astype(np.float32) * 0.01
                wm_audio, audio_stats = self.audio_codec.encode_audio_stream(dummy_pcm, audio_payload_bytes, key_seed)
                self._write_pcm_to_wav(wm_audio, wm_audio_tmp, 44100)
                has_audio = True

            # 5. Process Video Track (Secondary / Backup)
            cap = cv2.VideoCapture(video_path)
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            cap.release()

            if not frames:
                raise ValueError("Could not read any frames from input video.")

            wm_frames, video_stats = self.video_codec.encode_video_frames(frames, video_payload_bytes, key_seed)
            psnr_val = compute_video_psnr(frames[0], wm_frames[0])
            ssim_val = compute_video_ssim(frames[0], wm_frames[0])

            # Write watermarked frames to temp video
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tf_vid:
                raw_vid_tmp = tf_vid.name

            orig_h, orig_w = frames[0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_vid = cv2.VideoWriter(raw_vid_tmp, fourcc, 30.0, (orig_w, orig_h))
            for f in wm_frames:
                out_vid.write(f)
            out_vid.release()

            # 6. Re-mux Video and Audio with FFmpeg
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            remux_cmd = [
                FFMPEG_EXE, "-y",
                "-i", raw_vid_tmp,
                "-i", wm_audio_tmp,
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "libx264",
                "-crf", "18",
                "-preset", "faster",
                "-pix_fmt", "yuv420p",
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
            if 'raw_vid_tmp' in locals() and os.path.exists(raw_vid_tmp):
                try: os.unlink(raw_vid_tmp)
                except Exception: pass

        return {
            "success": True,
            "engine": "AVR-SHIELD",
            "output_path": output_path,
            "audio_snr_db": snr_val,
            "video_psnr_db": psnr_val,
            "video_ssim": ssim_val,
            "encryption": enc_meta,
            "audio_stats": audio_stats,
            "video_stats": video_stats
        }

    def extract(self, video_path: str, password: str, is_simulated_test: bool = False) -> Dict[str, Any]:
        """
        Blind extraction of payload from video_path.
        Extracts audio and video independently and triggers 3-path Recovery Coordinator.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Media file not found: {video_path}")

        key_seed = zlib.crc32(password.encode('utf-8'))

        # 1. Extract and decode Audio Stream
        audio_pcm, has_audio = self._extract_audio_pcm(video_path, 44100)
        audio_payload = None
        audio_stats = {"extracted": False}
        if has_audio and len(audio_pcm) > 44100:
            audio_payload, audio_stats = self.audio_codec.decode_audio_stream(audio_pcm, key_seed)

        # 2. Extract and decode Video Frames
        cap = cv2.VideoCapture(video_path)
        frames = []
        max_extract_frames = 900
        while len(frames) < max_extract_frames:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()

        video_payload = None
        video_stats = {"extracted": False}
        if frames:
            video_payload, video_stats = self.video_codec.decode_video_frames(frames, key_seed)

        # 3. Recovery Coordinator across Path A, Path B, and Path C
        secret, report = self.coordinator.recover_message(
            audio_raw_payload=audio_payload,
            video_raw_payload=video_payload,
            password=password,
            audio_stats=audio_stats,
            video_stats=video_stats
        )

        report["is_simulated_test"] = is_simulated_test
        report["engine"] = "AVR-SHIELD"
        report["success"] = report["authenticated"]
        return report

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
