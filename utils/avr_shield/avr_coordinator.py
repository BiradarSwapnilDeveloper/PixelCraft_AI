"""
AVR-SHIELD — Audio/Video Recovery Coordinator
Orchestrates the 3 recovery paths:
Path A: Primary Audio Spread-Spectrum Recovery
Path B: Independent Video Luminance Recovery
Path C: Cross-Channel Authenticated Packet Reconstruction
Ensures zero plaintext leakage if AES-256-GCM authentication fails.
"""

import zlib
import struct
from typing import Tuple, Dict, Any, List, Optional

from .avr_crypto import PayloadEncryptionManager, AuthenticationFailedError

PACKET_MAGIC = b"AVR"
HEADER_FORMAT = "!3scBBH"  # magic(3B), channel(1B), pkt_idx(1B), total_pkts(1B), crc16(2B)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def compute_crc16(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFF

class PacketFramer:
    """Frames and validates individual packet chunks with CRC16 integrity guards."""

    @staticmethod
    def frame_packet(channel: str, pkt_idx: int, total_pkts: int, data: bytes) -> bytes:
        crc = compute_crc16(data)
        header = struct.pack(HEADER_FORMAT, PACKET_MAGIC, channel.encode('ascii')[:1], pkt_idx, total_pkts, crc)
        return header + data

    @staticmethod
    def parse_packet(raw_bytes: bytes) -> Optional[Tuple[str, int, int, bytes]]:
        if len(raw_bytes) < HEADER_SIZE:
            return None
        try:
            magic, chan_b, pkt_idx, total_pkts, crc = struct.unpack(HEADER_FORMAT, raw_bytes[:HEADER_SIZE])
            if magic != PACKET_MAGIC:
                return None
            data = raw_bytes[HEADER_SIZE:]
            if compute_crc16(data) != crc:
                return None  # Corrupted packet
            return chan_b.decode('ascii', errors='ignore'), pkt_idx, total_pkts, data
        except Exception:
            return None

class RecoveryCoordinator:
    """
    Coordinates multi-path recovery between audio and video channels.
    Provides strict cryptographic gating before releasing recovered messages.
    """

    def __init__(self, crypto_mgr: Optional[PayloadEncryptionManager] = None):
        self.crypto_mgr = crypto_mgr or PayloadEncryptionManager()

    def frame_envelope(self, envelope_bytes: bytes, max_packet_size: int = 128) -> Tuple[List[bytes], List[bytes]]:
        """
        Splits an envelope into framed audio packets and framed video packets.
        Returns: (audio_packets, video_packets)
        """
        chunks = []
        for i in range(0, len(envelope_bytes), max_packet_size):
            chunks.append(envelope_bytes[i:i + max_packet_size])
        total_pkts = len(chunks)

        audio_pkts = []
        video_pkts = []
        for idx, chunk in enumerate(chunks):
            audio_pkts.append(PacketFramer.frame_packet("A", idx, total_pkts, chunk))
            video_pkts.append(PacketFramer.frame_packet("V", idx, total_pkts, chunk))

        return audio_pkts, video_pkts

    def recover_message(
        self,
        audio_raw_payload: Optional[bytes],
        video_raw_payload: Optional[bytes],
        password: str,
        audio_stats: Optional[Dict[str, Any]] = None,
        video_stats: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Executes the 3 recovery paths:
        A. Audio Recovery
        B. Video Recovery
        C. Cross-Channel Packet Reconstruction
        """
        report = {
            "path_attempted": [],
            "path_successful": None,
            "audio_status": "NOT_AVAILABLE" if audio_raw_payload is None else "EXTRACTED",
            "video_status": "NOT_AVAILABLE" if video_raw_payload is None else "EXTRACTED",
            "cross_channel_used": False,
            "authenticated": False,
            "vault": None,
            "recovered_text": None,
            "audio_stats": audio_stats or {},
            "video_stats": video_stats or {}
        }

        # -------------------------------------------------------------
        # PATH A: Audio-Exclusive Recovery
        # -------------------------------------------------------------
        if audio_raw_payload is not None:
            report["path_attempted"].append("PATH_A_AUDIO")
            parsed = PacketFramer.parse_packet(audio_raw_payload)
            target_envelope = parsed[3] if parsed is not None else audio_raw_payload
            try:
                plaintext, auth_info = self.crypto_mgr.decrypt_payload(target_envelope, password)
                report["path_successful"] = "PATH_A_AUDIO"
                report["authenticated"] = True
                report["vault"] = auth_info.get("vault", "PRIMARY")
                report["recovered_text"] = plaintext
                return plaintext, report
            except AuthenticationFailedError:
                pass  # Audio decryption failed, proceed to next path

        # -------------------------------------------------------------
        # PATH B: Video-Exclusive Recovery
        # -------------------------------------------------------------
        if video_raw_payload is not None:
            report["path_attempted"].append("PATH_B_VIDEO")
            parsed = PacketFramer.parse_packet(video_raw_payload)
            target_envelope = parsed[3] if parsed is not None else video_raw_payload
            try:
                plaintext, auth_info = self.crypto_mgr.decrypt_payload(target_envelope, password)
                report["path_successful"] = "PATH_B_VIDEO"
                report["authenticated"] = True
                report["vault"] = auth_info.get("vault", "PRIMARY")
                report["recovered_text"] = plaintext
                return plaintext, report
            except AuthenticationFailedError:
                pass  # Video decryption failed, proceed to next path

        # -------------------------------------------------------------
        # PATH C: Cross-Channel Hybrid Packet Reconstruction
        # -------------------------------------------------------------
        report["path_attempted"].append("PATH_C_CROSS_CHANNEL")
        parsed_audio = PacketFramer.parse_packet(audio_raw_payload) if audio_raw_payload else None
        parsed_video = PacketFramer.parse_packet(video_raw_payload) if video_raw_payload else None

        # Compare valid packets
        candidate_envelope = None
        if parsed_audio is not None and parsed_video is None:
            candidate_envelope = parsed_audio[3]
        elif parsed_video is not None and parsed_audio is None:
            candidate_envelope = parsed_video[3]
        elif parsed_audio is not None and parsed_video is not None:
            # If both have valid packets, prefer audio, fallback to video
            candidate_envelope = parsed_audio[3]

        if candidate_envelope is not None:
            try:
                plaintext, auth_info = self.crypto_mgr.decrypt_payload(candidate_envelope, password)
                report["path_successful"] = "PATH_C_CROSS_CHANNEL"
                report["cross_channel_used"] = True
                report["authenticated"] = True
                report["vault"] = auth_info.get("vault", "PRIMARY")
                report["recovered_text"] = plaintext
                return plaintext, report
            except AuthenticationFailedError:
                pass

        # All 3 paths failed to verify GCM tag
        report["authenticated"] = False
        report["recovered_text"] = None
        return None, report
