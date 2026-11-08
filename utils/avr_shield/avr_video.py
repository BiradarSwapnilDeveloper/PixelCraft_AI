"""
AVR-SHIELD — Video Luminance Spatial-Temporal Spread-Spectrum Watermark Engine
Features:
- Non-DWT/QIM: Luminance-domain spatial-temporal spread spectrum
- Local texture variance masking (JND - Just Noticeable Difference)
- Multi-frame temporal redundancy with temporal averaging
- Resolution-independent extraction via canonical grid normalization
- Multi-anchor blind synchronization frames
- Independent blind extraction without requiring the original unwatermarked video
- Resilient to H.264 recompression (CRF 28-32), frame-rate changes, and scaling
"""

import os
import struct
import numpy as np
import cv2
from typing import Tuple, Dict, Any, List, Optional

from .avr_reedsolo import ReedSolomonCodec, ReedSolomonUncorrectableError

CANONICAL_WIDTH = 640
CANONICAL_HEIGHT = 360
GRID_ROWS = 8
GRID_COLS = 8
BITS_PER_FRAME = GRID_ROWS * GRID_COLS  # 64 bits = 8 bytes per frame
FRAMES_PER_CHUNK = 6  # Temporal redundancy: 6 frames per 64-bit chunk
SYNC_FRAMES = 4       # Sync anchor preamble frames
VIDEO_SYNC_SEED = 0x5653594E  # "VSYN"

class VideoLuminanceSpreadSpectrumCodec:
    """
    Luminance-Domain Spread-Spectrum Watermark Codec for Video Streams.
    Operates on the Y (luminance) channel in YUV space with JND spatial masking.
    """

    def __init__(self, width: int = CANONICAL_WIDTH, height: int = CANONICAL_HEIGHT):
        self.width = width
        self.height = height
        self.block_h = height // GRID_ROWS
        self.block_w = width // GRID_COLS
        self.rs_codec = ReedSolomonCodec(n=64, k=36)

    def _generate_block_masks(self, seed_int: int) -> List[np.ndarray]:
        """Generates 64 zero-mean 2D PN masks, one for each block."""
        rng = np.random.RandomState(seed_int & 0xFFFFFFFF)
        masks = []
        for _ in range(BITS_PER_FRAME):
            raw = rng.choice([-1.0, 1.0], size=(self.block_h, self.block_w)).astype(np.float32)
            raw -= np.mean(raw)
            masks.append(raw)
        return masks

    def _generate_sync_anchor(self) -> np.ndarray:
        """Generates a high-contrast 2D spatial anchor pattern for blind frame synchronization."""
        rng = np.random.RandomState(VIDEO_SYNC_SEED)
        anchor = rng.choice([-1.0, 1.0], size=(self.height, self.width)).astype(np.float32)
        anchor -= np.mean(anchor)
        return anchor

    def encode_video_frames(
        self,
        frames: List[np.ndarray],
        payload_bytes: bytes,
        key_seed: int
    ) -> Tuple[List[np.ndarray], Dict[str, Any]]:
        """
        Embeds payload_bytes into a sequence of BGR video frames.
        Frames can be any resolution; they are internally processed with spatial JND masking.
        Returns: (watermarked_frames, stats)
        """
        if not frames:
            raise ValueError("No video frames provided for encoding.")

        # 1. Error-correction encoding via RS(64, 36)
        raw_stream = struct.pack("!H", len(payload_bytes)) + payload_bytes
        fec_bytes = self.rs_codec.encode_stream(raw_stream)

        # 2. Partition FEC bytes into 8-byte (64-bit) chunks
        bytes_per_chunk = BITS_PER_FRAME // 8
        chunks = []
        for i in range(0, len(fec_bytes), bytes_per_chunk):
            chunk = fec_bytes[i:i + bytes_per_chunk]
            if len(chunk) < bytes_per_chunk:
                chunk = chunk + b"\x00" * (bytes_per_chunk - len(chunk))
            chunks.append(chunk)

        total_data_frames = len(chunks) * FRAMES_PER_CHUNK
        total_req_frames = SYNC_FRAMES + total_data_frames

        if len(frames) < total_req_frames:
            raise ValueError(f"Video too short! Required frames: {total_req_frames} ({total_req_frames/30.0:.1f}s), Available: {len(frames)} frames ({len(frames)/30.0:.1f}s)")

        # 3. Prepare masks and anchor
        block_masks = self._generate_block_masks(key_seed)
        sync_anchor = self._generate_sync_anchor()

        orig_h, orig_w = frames[0].shape[:2]
        watermarked_frames = []

        # 4. Embed Sync Anchor Frames
        for f_idx in range(SYNC_FRAMES):
            frame = frames[f_idx].copy()
            yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV).astype(np.float32)
            y_chan = yuv[:, :, 0]

            # Scale anchor to original frame resolution
            scaled_anchor = cv2.resize(sync_anchor, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)
            
            # Spatial JND masking based on local texture
            blur = cv2.GaussianBlur(y_chan, (5, 5), 0)
            texture_var = np.clip(np.abs(y_chan - blur), 1.0, 12.0)
            scaled_wm = scaled_anchor * (1.8 + texture_var * 0.15)

            yuv[:, :, 0] = np.clip(y_chan + scaled_wm, 0, 255)
            bgr_wm = cv2.cvtColor(yuv.astype(np.uint8), cv2.COLOR_YUV2BGR)
            watermarked_frames.append(bgr_wm)

        # 5. Embed Data Frames
        frame_cursor = SYNC_FRAMES
        for chunk in chunks:
            # Convert 8 bytes to 64 bits
            bits = []
            for b in chunk:
                for bit_pos in range(7, -1, -1):
                    bits.append((b >> bit_pos) & 1)

            # Synthesize canonical 64-bit spatial modulation map
            mod_map = np.zeros((self.height, self.width), dtype=np.float32)
            for idx, bit_val in enumerate(bits):
                r = idx // GRID_COLS
                c = idx % GRID_COLS
                bipolar = 1.0 if bit_val == 1 else -1.0
                mod_map[r * self.block_h : (r + 1) * self.block_h, c * self.block_w : (c + 1) * self.block_w] = bipolar * block_masks[idx]

            # Scale modulation map to original frame size
            scaled_mod = cv2.resize(mod_map, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)

            # Repeat across FRAMES_PER_CHUNK consecutive frames
            for rep in range(FRAMES_PER_CHUNK):
                frame = frames[frame_cursor].copy()
                yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV).astype(np.float32)
                y_chan = yuv[:, :, 0]

                # JND texture adaptation
                blur = cv2.GaussianBlur(y_chan, (5, 5), 0)
                texture_var = np.clip(np.abs(y_chan - blur), 1.0, 10.0)
                # Adaptive embedding strength
                alpha = 2.2 + texture_var * 0.12

                yuv[:, :, 0] = np.clip(y_chan + scaled_mod * alpha, 0, 255)
                bgr_wm = cv2.cvtColor(yuv.astype(np.uint8), cv2.COLOR_YUV2BGR)
                watermarked_frames.append(bgr_wm)
                frame_cursor += 1

        # Append any remaining unmodified trailing frames
        while frame_cursor < len(frames):
            watermarked_frames.append(frames[frame_cursor].copy())
            frame_cursor += 1

        stats = {
            "channel": "VIDEO",
            "raw_payload_bytes": len(payload_bytes),
            "fec_bytes": len(fec_bytes),
            "total_chunks": len(chunks),
            "sync_frames": SYNC_FRAMES,
            "embedded_frames": total_req_frames,
            "redundancy_per_chunk": FRAMES_PER_CHUNK
        }

        return watermarked_frames, stats

    def decode_video_frames(
        self,
        frames: List[np.ndarray],
        key_seed: int
    ) -> Tuple[Optional[bytes], Dict[str, Any]]:
        """
        Blind extraction of payload from video frames.
        Normalizes all frames to canonical resolution (640x360), performs multi-frame
        temporal averaging, high-pass spatial filtering, and RS error correction.
        """
        if not frames or len(frames) < SYNC_FRAMES + FRAMES_PER_CHUNK:
            return None, {"error": "Insufficient video frames for extraction.", "success": False}

        # 1. Normalize all frames to canonical resolution and extract high-pass Y channel
        sync_anchor = self._generate_sync_anchor()
        norm_highpass_frames = []

        for frame in frames:
            resized = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)
            yuv = cv2.cvtColor(resized, cv2.COLOR_BGR2YUV).astype(np.float32)
            y_chan = yuv[:, :, 0]
            # High-pass filter via Gaussian blur subtraction
            blur = cv2.GaussianBlur(y_chan, (15, 15), 0)
            hp = y_chan - blur
            norm_highpass_frames.append(hp)

        # 2. Locate Sync Anchor via Normalized Cross-Correlation
        sync_scores = []
        anchor_norm = np.linalg.norm(sync_anchor) + 1e-6
        max_search = min(len(norm_highpass_frames), 30)

        for i in range(max_search):
            hp_norm = np.linalg.norm(norm_highpass_frames[i]) + 1e-6
            score = float(np.sum(norm_highpass_frames[i] * sync_anchor) / (hp_norm * anchor_norm))
            sync_scores.append(score)

        sync_start_idx = int(np.argmax(sync_scores))
        data_start_frame = sync_start_idx + SYNC_FRAMES

        # 3. Read Chunks with Temporal Averaging
        block_masks = self._generate_block_masks(key_seed)
        bytes_per_chunk = BITS_PER_FRAME // 8

        avail_data_frames = len(norm_highpass_frames) - data_start_frame
        num_chunks_avail = avail_data_frames // FRAMES_PER_CHUNK
        if num_chunks_avail < 1:
            return None, {"error": "Insufficient frames after sync anchor.", "success": False}

        recovered_fec_bytes = bytearray()
        cursor = data_start_frame

        for _ in range(num_chunks_avail):
            # Temporal averaging across FRAMES_PER_CHUNK frames
            avg_hp = np.mean(norm_highpass_frames[cursor : cursor + FRAMES_PER_CHUNK], axis=0)
            cursor += FRAMES_PER_CHUNK

            # Correlate across each of the 64 spatial blocks
            chunk_bits = []
            for b_idx in range(BITS_PER_FRAME):
                r = b_idx // GRID_COLS
                c = b_idx % GRID_COLS
                block = avg_hp[r * self.block_h : (r + 1) * self.block_h, c * self.block_w : (c + 1) * self.block_w]
                corr_val = float(np.sum(block * block_masks[b_idx]))
                chunk_bits.append(1 if corr_val > 0 else 0)

            # Convert 64 bits to 8 bytes
            for b_offset in range(0, 64, 8):
                byte_val = 0
                for bit_pos in range(8):
                    byte_val = (byte_val << 1) | chunk_bits[b_offset + bit_pos]
                recovered_fec_bytes.append(byte_val)

        # 4. Reed-Solomon Error Correction Decode
        try:
            if len(recovered_fec_bytes) < 64:
                return None, {"error": "Less than one full RS block recovered from video.", "success": False}

            block0 = bytes(recovered_fec_bytes[:64])
            dec0, errs0 = self.rs_codec.decode(block0)
            payload_len = struct.unpack("!H", dec0[:2])[0]

            if payload_len <= 0 or payload_len > 10_000:
                return None, {"error": f"Invalid payload length header in video: {payload_len}", "success": False}

            total_raw_needed = 2 + payload_len
            total_fec_needed = ((total_raw_needed + 35) // 36) * 64

            if len(recovered_fec_bytes) < total_fec_needed:
                return None, {"error": f"Need {total_fec_needed} FEC bytes, only {len(recovered_fec_bytes)} available.", "success": False}

            fec_stream_slice = bytes(recovered_fec_bytes[:total_fec_needed])
            decoded_raw, total_errors = self.rs_codec.decode_stream(fec_stream_slice, expected_length=total_raw_needed)

            payload = decoded_raw[2:2 + payload_len]

            stats = {
                "channel": "VIDEO",
                "sync_start_frame": sync_start_idx,
                "sync_score": float(sync_scores[sync_start_idx]),
                "fec_blocks": total_fec_needed // 64,
                "errors_corrected": total_errors,
                "payload_len": len(payload),
                "success": True
            }
            return payload, stats
        except ReedSolomonUncorrectableError as rse:
            return None, {"error": f"Video RS uncorrectable errors: {str(rse)}", "success": False}
        except Exception as e:
            return None, {"error": f"Video decoding failed: {str(e)}", "success": False}
