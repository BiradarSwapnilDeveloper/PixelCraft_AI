"""
WCTSE Temporal Packetization, Multi-Anchor Synchronization & Interleaving Engine
Implements packet framing with CRC32, Reed-Solomon RS(n, k), symbol interleaving,
and multi-anchor blind synchronization across video frames.
"""

import zlib
import struct
import numpy as np
try:
    from .wctse_reedsolo import ReedSolomonCodec, ReedSolomonUncorrectableError
except (ImportError, ValueError):
    from wctse_reedsolo import ReedSolomonCodec, ReedSolomonUncorrectableError

# 4-Byte Barker/Gold Sync Pilot Preamble
SYNC_PREAMBLE = b"\xFA\x85\x39\xC6"
BARKER_13 = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]

class TemporalPacketizer:
    def __init__(self, n: int = 64, k: int = 36):
        self.n = n
        self.k = k
        self.rs = ReedSolomonCodec(n, k)
        # 4 bytes for Seq (2B) + Total (2B) in header
        self.chunk_size = k - 4

    def packetize(self, envelope_bytes: bytes) -> list[bytes]:
        """
        Splits envelope bytes into RS-protected, CRC32-checked packets.
        Packet structure:
          [PREAMBLE (4B)]
          [RS Codeword (n bytes):
             Header: [Seq (2B)] [Total (2B)]
             Payload: [Chunk (k-4 bytes)]
             Parity: [2t bytes]
          ]
          [CRC32 (4B)]
        """
        chunks = []
        for i in range(0, len(envelope_bytes), self.chunk_size):
            chunks.append(envelope_bytes[i:i + self.chunk_size])

        total_pkts = len(chunks)
        packets = []

        for seq, chunk in enumerate(chunks):
            # Header: Seq (uint16) + Total (uint16)
            header = struct.pack(">HH", seq, total_pkts)
            # Pad chunk to exact chunk_size if last chunk
            padded_chunk = chunk + b"\x00" * (self.chunk_size - len(chunk))
            data_to_encode = header + padded_chunk
            assert len(data_to_encode) == self.k

            # Reed-Solomon encode
            codeword = self.rs.encode(data_to_encode)
            assert len(codeword) == self.n

            # CRC32 of codeword
            crc = zlib.crc32(codeword) & 0xFFFFFFFF
            crc_bytes = struct.pack(">I", crc)

            packet = SYNC_PREAMBLE + codeword + crc_bytes
            packets.append(packet)

        return packets

    def depacketize(self, raw_packets: list[bytes]) -> tuple[bytes, dict]:
        """
        De-packetizes received packets, performs CRC32 checks,
        applies Reed-Solomon error correction, and reassembles payload.
        Returns: (reconstructed_envelope, telemetry_dict)
        """
        total_packets_expected = None
        recovered_chunks = {}
        total_errors_corrected = 0
        packets_clean = 0
        packets_corrected = 0
        packets_failed = 0
        total_bits_evaluated = 0
        total_bit_errors = 0

        for raw_pkt in raw_packets:
            if len(raw_pkt) < 4 + self.n + 4:
                continue

            # Verify preamble
            preamble = raw_pkt[:4]
            if preamble != SYNC_PREAMBLE:
                continue

            codeword = raw_pkt[4:4 + self.n]
            crc_received = struct.unpack(">I", raw_pkt[4 + self.n:4 + self.n + 4])[0]
            crc_calc = zlib.crc32(codeword) & 0xFFFFFFFF

            total_bits_evaluated += self.n * 8

            if crc_received == crc_calc:
                # Completely clean codeword
                packets_clean += 1
                header_data = codeword[:self.k]
                seq, total = struct.unpack(">HH", header_data[:4])
                chunk = header_data[4:self.k]
                total_packets_expected = total
                recovered_chunks[seq] = chunk
            else:
                # Codeword has errors - attempt Reed-Solomon algebraic decoding
                try:
                    corrected_data, err_count = self.rs.decode(codeword)
                    seq, total = struct.unpack(">HH", corrected_data[:4])
                    chunk = corrected_data[4:self.k]
                    total_packets_expected = total
                    recovered_chunks[seq] = chunk
                    total_errors_corrected += err_count
                    packets_corrected += 1
                    total_bit_errors += err_count * 4 # Estimated bit error count
                except ReedSolomonUncorrectableError:
                    packets_failed += 1
                    total_bit_errors += self.n * 4 # Assume half bits corrupted

        if total_packets_expected is None or len(recovered_chunks) == 0:
            raise ValueError("No valid packets could be synchronized or recovered.")

        # Reassemble payload chunks in sequence
        reassembled = bytearray()
        missing_count = 0
        for seq in range(total_packets_expected):
            if seq in recovered_chunks:
                reassembled.extend(recovered_chunks[seq])
            else:
                missing_count += 1

        pre_fec_ber = (total_bit_errors / max(1, total_bits_evaluated)) * 100.0

        telemetry = {
            "total_packets_expected": total_packets_expected,
            "packets_recovered": len(recovered_chunks),
            "packets_clean": packets_clean,
            "packets_corrected": packets_corrected,
            "packets_failed": packets_failed,
            "missing_packets": missing_count,
            "total_symbols_corrected": total_errors_corrected,
            "pre_fec_ber_percent": round(pre_fec_ber, 2),
            "recovery_ratio_percent": round((len(recovered_chunks) / max(1, total_packets_expected)) * 100, 1)
        }

        if missing_count > 0:
            raise ValueError(f"Packet reassembly incomplete: missing {missing_count} out of {total_packets_expected} packets.")

        return bytes(reassembled), telemetry

class Interleaver:
    """
    Symbol/Bit Interleaver across temporal frame groups.
    Disperses contiguous packet bytes across M frames to prevent burst errors.
    """
    @staticmethod
    def interleave(bit_streams: list[list[int]]) -> list[list[int]]:
        """
        Matrix interleaving: rows are packets, columns are transmitted frames.
        """
        if not bit_streams:
            return []
        max_len = max(len(s) for s in bit_streams)
        padded = [s + [0] * (max_len - len(s)) for s in bit_streams]
        arr = np.array(padded, dtype=np.uint8)
        # Transpose so that each transmitted frame receives 1 bit from each packet
        return arr.T.tolist()

    @staticmethod
    def deinterleave(frame_bit_streams: list[list[int]], original_packet_count: int) -> list[list[int]]:
        """
        Reverses matrix interleaving.
        """
        if not frame_bit_streams:
            return []
        arr = np.array(frame_bit_streams, dtype=np.uint8)
        transposed = arr.T.tolist()
        return transposed[:original_packet_count]

if __name__ == "__main__":
    print("Testing Temporal Packetization & Interleaving Module...")
    packetizer = TemporalPacketizer(n=64, k=36)
    test_envelope = b"WCT1\x01" + b"A" * 120 + b"WCTSE-AUTHENTICATED-ENVELOPE-TEST-DATA-XYZ"
    
    packets = packetizer.packetize(test_envelope)
    print(f"Generated {len(packets)} RS(64, 36) packets for {len(test_envelope)} bytes envelope.")

    # Corrupt 10 bytes in packet 0 (within 14 error correction capability of RS)
    corrupted_packets = [bytearray(p) for p in packets]
    for i in range(10):
        corrupted_packets[0][4 + i * 4] ^= 0x55

    recovered_env, stats = packetizer.depacketize([bytes(p) for p in corrupted_packets])
    assert recovered_env.startswith(test_envelope), "Envelope reconstruction failed!"
    print("Depacketize with error correction SUCCESS!")
    print("Telemetry:", stats)
