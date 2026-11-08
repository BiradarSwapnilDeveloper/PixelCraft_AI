"""
AVR-SHIELD — Payload Encryption Manager
Implements AES-256-GCM Authenticated Encryption with Associated Data (AEAD),
Argon2id / PBKDF2-HMAC-SHA256 key derivation, dual-vault plausible deniability,
and strict cryptographic verification.
"""

import os
import struct
import hashlib
import json
from typing import Tuple, Dict, Any, Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    raise RuntimeError("cryptography package is required for AVR-SHIELD AES-256-GCM encryption.")

# Check for argon2-cffi
HAS_ARGON2 = False
try:
    import argon2
    from argon2.low_level import hash_secret_raw, Type
    HAS_ARGON2 = True
except ImportError:
    HAS_ARGON2 = False

MAGIC_HEADER = b"AVR1"
SALT_SIZE = 16
NONCE_SIZE = 12
TAG_SIZE = 16

class AuthenticationFailedError(Exception):
    """Raised when GCM authentication tag verification fails or envelope is tampered with."""
    pass

class PayloadEncryptionManager:
    """
    Cryptographic manager handling AES-256-GCM authenticated encryption and decryption.
    Guarantees that plaintext is never exposed unless the GCM authentication tag passes.
    """

    def __init__(self, pbkdf2_iterations: int = 200_000):
        self.pbkdf2_iterations = pbkdf2_iterations
        # Argon2id benchmarked parameters (Memory: 32MB, Time: 2 iterations, Parallelism: 1)
        self.argon2_time_cost = 2
        self.argon2_memory_cost = 32768  # 32 MB in KiB
        self.argon2_parallelism = 1

    def derive_key(self, password: str, salt: bytes) -> Tuple[bytes, str]:
        """
        Derives a 256-bit (32-byte) key from the given password and salt.
        Uses Argon2id if available, otherwise falls back to hardened PBKDF2-HMAC-SHA256.
        Returns: (key_bytes, kdf_algorithm_name)
        """
        pwd_bytes = password.encode('utf-8')
        if HAS_ARGON2:
            try:
                key = hash_secret_raw(
                    secret=pwd_bytes,
                    salt=salt,
                    time_cost=self.argon2_time_cost,
                    memory_cost=self.argon2_memory_cost,
                    parallelism=self.argon2_parallelism,
                    hash_len=32,
                    type=Type.ID
                )
                return key, "ARGON2ID"
            except Exception:
                pass # Fallback to PBKDF2

        key = hashlib.pbkdf2_hmac(
            'sha256',
            pwd_bytes,
            salt,
            self.pbkdf2_iterations,
            dklen=32
        )
        return key, "PBKDF2-SHA256"

    def derive_key_with_params(self, password: str, salt: bytes, kdf_name: str, kdf_param: int) -> bytes:
        """Derives key using the exact KDF parameters stored in envelope metadata."""
        pwd_bytes = password.encode('utf-8')
        if kdf_name == "ARGON2ID" and HAS_ARGON2:
            try:
                return hash_secret_raw(
                    secret=pwd_bytes,
                    salt=salt,
                    time_cost=self.argon2_time_cost,
                    memory_cost=self.argon2_memory_cost,
                    parallelism=self.argon2_parallelism,
                    hash_len=32,
                    type=Type.ID
                )
            except Exception:
                pass
        
        # PBKDF2 fallback
        iters = kdf_param if kdf_param > 0 else self.pbkdf2_iterations
        return hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt, iters, dklen=32)

    def encrypt_payload(
        self,
        secret_text: str,
        password: str,
        channel_id: str = "A",
        decoy_text: Optional[str] = None,
        decoy_password: Optional[str] = None
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Encrypts a secret message into an authenticated AVR-SHIELD binary envelope.
        If decoy parameters are supplied, creates a dual-vault plausible deniability payload.
        """
        salt = os.urandom(SALT_SIZE)
        nonce = os.urandom(NONCE_SIZE)
        key, kdf_algo = self.derive_key(password, salt)

        # Primary payload serialization
        payload_data = secret_text.encode('utf-8')
        
        # Authenticated Additional Data (AAD): Magic (4B) + Version (1B) + Channel (1B) + KDF_ID (1B) + Salt (16B) + Nonce (12B)
        kdf_code = 1 if kdf_algo == "ARGON2ID" else 2
        aad = struct.pack("!4sBBB", MAGIC_HEADER, 1, ord(channel_id[0].upper()), kdf_code) + salt + nonce

        aesgcm = AESGCM(key)
        ciphertext_with_tag = aesgcm.encrypt(nonce, payload_data, aad)

        # Handle Decoy Vault if requested
        has_decoy = bool(decoy_text and decoy_password)
        decoy_blob = b""
        if has_decoy:
            decoy_salt = os.urandom(SALT_SIZE)
            decoy_nonce = os.urandom(NONCE_SIZE)
            decoy_key, decoy_kdf = self.derive_key(decoy_password, decoy_salt)
            decoy_aad = struct.pack("!4sBBB", MAGIC_HEADER, 1, ord(b"D"), 1 if decoy_kdf == "ARGON2ID" else 2) + decoy_salt + decoy_nonce
            decoy_aesgcm = AESGCM(decoy_key)
            decoy_enc = decoy_aesgcm.encrypt(decoy_nonce, decoy_text.encode('utf-8'), decoy_aad)
            # Decoy section: 1B has_decoy + 16B salt + 12B nonce + 2B len + enc
            decoy_blob = struct.pack("!B16s12sH", 1, decoy_salt, decoy_nonce, len(decoy_enc)) + decoy_enc
        else:
            decoy_blob = struct.pack("!B", 0)

        # Envelope Structure:
        # [0:4]   Magic "AVR1"
        # [4:5]   Version (1)
        # [5:6]   Channel ('A' or 'V' or 'X')
        # [6:7]   KDF Code (1=Argon2id, 2=PBKDF2)
        # [7:23]  Salt (16B)
        # [23:35] Nonce (12B)
        # [35:39] Primary Ciphertext Length (4B uint32)
        # [39:39+C] Primary Ciphertext + Tag
        # [39+C:] Decoy Section
        primary_len = len(ciphertext_with_tag)
        envelope = (
            aad +
            struct.pack("!I", primary_len) +
            ciphertext_with_tag +
            decoy_blob
        )

        metadata = {
            "channel": channel_id,
            "kdf": kdf_algo,
            "has_decoy": has_decoy,
            "primary_bytes": len(payload_data),
            "envelope_size": len(envelope),
            "salt_hex": salt.hex(),
            "nonce_hex": nonce.hex()
        }

        return envelope, metadata

    def decrypt_payload(self, envelope_bytes: bytes, password: str) -> Tuple[str, Dict[str, Any]]:
        """
        Decrypts an AVR-SHIELD binary envelope.
        Tries the primary vault first; if primary authentication fails, checks for a decoy vault.
        Strictly raises AuthenticationFailedError if neither passes authentication.
        """
        if len(envelope_bytes) < 39:
            raise AuthenticationFailedError("Payload truncated or invalid header: envelope length < 39 bytes.")

        magic, version, channel_byte, kdf_code = struct.unpack("!4sBBB", envelope_bytes[:7])
        if magic != MAGIC_HEADER:
            raise AuthenticationFailedError(f"Invalid magic header: expected {MAGIC_HEADER.decode()}, got {magic}")

        salt = envelope_bytes[7:23]
        nonce = envelope_bytes[23:35]
        aad = envelope_bytes[:35]

        kdf_algo = "ARGON2ID" if kdf_code == 1 else "PBKDF2-SHA256"
        key = self.derive_key_with_params(password, salt, kdf_algo, self.pbkdf2_iterations)

        primary_len = struct.unpack("!I", envelope_bytes[35:39])[0]
        if len(envelope_bytes) < 39 + primary_len:
            raise AuthenticationFailedError(f"Envelope truncated: expected at least {39 + primary_len} bytes.")

        ciphertext_with_tag = envelope_bytes[39:39 + primary_len]

        # 1. Attempt Primary Vault Decryption
        aesgcm = AESGCM(key)
        try:
            plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_with_tag, aad)
            plaintext = plaintext_bytes.decode('utf-8', errors='replace')
            return plaintext, {
                "vault": "PRIMARY",
                "channel": chr(channel_byte),
                "kdf": kdf_algo,
                "authenticated": True
            }
        except Exception:
            # Primary authentication failed, check decoy vault
            pass

        # 2. Attempt Decoy Vault Decryption if present
        decoy_offset = 39 + primary_len
        if len(envelope_bytes) > decoy_offset:
            has_decoy = envelope_bytes[decoy_offset]
            if has_decoy == 1 and len(envelope_bytes) >= decoy_offset + 1 + 16 + 12 + 2:
                _, d_salt, d_nonce, d_len = struct.unpack("!B16s12sH", envelope_bytes[decoy_offset:decoy_offset + 31])
                d_cipher = envelope_bytes[decoy_offset + 31:decoy_offset + 31 + d_len]
                d_key, _ = self.derive_key(password, d_salt)
                d_aad = struct.pack("!4sBBB", MAGIC_HEADER, 1, ord(b"D"), 2) + d_salt + d_nonce
                try:
                    d_aesgcm = AESGCM(d_key)
                    d_plain = d_aesgcm.decrypt(d_nonce, d_cipher, d_aad)
                    return d_plain.decode('utf-8', errors='replace'), {
                        "vault": "DECOY",
                        "channel": "DECOY",
                        "kdf": "PBKDF2-SHA256",
                        "authenticated": True
                    }
                except Exception:
                    pass

        # Neither primary nor decoy authenticated
        raise AuthenticationFailedError("Cryptographic verification failed: Incorrect passphrase or payload corrupted.")
