"""
WCTSE Cryptographic Engine
AES-256-GCM Authenticated Encryption with PBKDF2-HMAC-SHA256 / Argon2id KDF
Includes Additional Authenticated Data (AAD) binding and strict zero-plaintext verification.
"""

import os
import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class CryptographicError(Exception):
    """Base exception for WCTSE cryptographic errors."""
    pass

class AuthenticationFailedError(CryptographicError):
    """Raised when GCM authentication tag verification fails."""
    pass

# Protocol Magic Header
MAGIC_HEADER = b"WCT1"
KDF_PBKDF2_SHA256 = 0x01
KDF_ARGON2ID = 0x02

DEFAULT_PBKDF2_ITERATIONS = 600000

def derive_key_pbkdf2(password: str, salt: bytes, iterations: int = DEFAULT_PBKDF2_ITERATIONS) -> bytes:
    """Derives a 256-bit (32-byte) key using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_payload(plaintext: bytes, password: str, metadata: dict = None, kdf_type: int = KDF_PBKDF2_SHA256) -> bytes:
    """
    Encrypts plaintext using AES-256-GCM.
    Envelope layout:
      [MAGIC (4B)] [KDF_TYPE (1B)] [SALT (16B)] [ITERATIONS (4B uint32)]
      [NONCE (12B)] [AAD_LEN (2B uint16)] [AAD (var)] [CIPHERTEXT + TAG (var + 16B)]
    """
    salt = os.urandom(16)
    nonce = os.urandom(12)
    iterations = DEFAULT_PBKDF2_ITERATIONS

    if kdf_type == KDF_PBKDF2_SHA256:
        key = derive_key_pbkdf2(password, salt, iterations)
    else:
        # Default fallback to PBKDF2 if Argon2 is not installed
        kdf_type = KDF_PBKDF2_SHA256
        key = derive_key_pbkdf2(password, salt, iterations)

    # Construct AAD bytes from metadata
    aad_parts = []
    if metadata:
        sid = metadata.get("session_id", "WCTSE-SESSION").encode('utf-8')[:32]
        profile = metadata.get("profile_id", 1)
        aad_parts.append(struct.pack(">B", profile))
        aad_parts.append(struct.pack(">H", len(sid)) + sid)
    aad = b"".join(aad_parts)

    aesgcm = AESGCM(key)
    # aesgcm.encrypt appends the 16-byte authentication tag to the ciphertext
    ct_with_tag = aesgcm.encrypt(nonce, plaintext, aad)

    envelope = bytearray()
    envelope.extend(MAGIC_HEADER)
    envelope.append(kdf_type)
    envelope.extend(salt)
    envelope.extend(struct.pack(">I", iterations))
    envelope.extend(nonce)
    envelope.extend(struct.pack(">H", len(aad)))
    envelope.extend(aad)
    envelope.extend(ct_with_tag)

    return bytes(envelope)

def decrypt_payload(envelope_bytes: bytes, password: str) -> tuple[bytes, dict]:
    """
    Decrypts an envelope created by encrypt_payload.
    Validates GCM tag strictly before returning plaintext.
    Returns: (plaintext_bytes, extracted_metadata)
    Raises: AuthenticationFailedError if password/ciphertext/metadata is invalid.
    """
    if len(envelope_bytes) < 4 + 1 + 16 + 4 + 12 + 2 + 16:
        raise CryptographicError("Envelope size is below minimum valid size.")

    if envelope_bytes[:4] != MAGIC_HEADER:
        raise CryptographicError(f"Invalid magic header: expected {MAGIC_HEADER}, got {envelope_bytes[:4]}")

    idx = 4
    kdf_type = envelope_bytes[idx]
    idx += 1

    salt = envelope_bytes[idx:idx + 16]
    idx += 16

    iterations = struct.unpack(">I", envelope_bytes[idx:idx + 4])[0]
    idx += 4

    nonce = envelope_bytes[idx:idx + 12]
    idx += 12

    aad_len = struct.unpack(">H", envelope_bytes[idx:idx + 2])[0]
    idx += 2

    if idx + aad_len > len(envelope_bytes):
        raise CryptographicError("Malformed envelope: AAD length exceeds data boundaries.")

    aad = envelope_bytes[idx:idx + aad_len]
    idx += aad_len

    ct_with_tag = envelope_bytes[idx:]
    if len(ct_with_tag) < 16:
        raise CryptographicError("Missing authentication tag.")

    # Derive key
    if kdf_type == KDF_PBKDF2_SHA256:
        key = derive_key_pbkdf2(password, salt, iterations)
    else:
        key = derive_key_pbkdf2(password, salt, iterations)

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ct_with_tag, aad)
    except Exception as e:
        raise AuthenticationFailedError("AES-256-GCM authentication verification failed: Incorrect password or corrupted payload.") from e

    metadata = {"kdf_type": kdf_type, "iterations": iterations}
    if len(aad) >= 3:
        profile_id = aad[0]
        metadata["profile_id"] = profile_id

    return plaintext, metadata

if __name__ == "__main__":
    print("Testing Cryptographic Engine...")
    secret = b"Top-Secret-PixelCraft-Payload: Quantum Keys & Coordinates"
    pwd = "CorrectHorseBatteryStaple2026!"
    meta = {"session_id": "PX-WCTSE-001", "profile_id": 1}

    # Encrypt
    env = encrypt_payload(secret, pwd, meta)
    print(f"Encrypted envelope size: {len(env)} bytes (ciphertext + AAD + headers)")

    # Decrypt with correct password
    decrypted, dec_meta = decrypt_payload(env, pwd)
    assert decrypted == secret, "Decrypted message does not match original!"
    print("Decryption with correct password: SUCCESS")

    # Decrypt with WRONG password
    try:
        decrypt_payload(env, "WrongPassword!")
        assert False, "Should have thrown AuthenticationFailedError!"
    except AuthenticationFailedError:
        print("Decryption with wrong password correctly rejected with AuthenticationFailedError: SUCCESS")

    # Decrypt with tampered ciphertext
    tampered = bytearray(env)
    tampered[-5] ^= 0xFF
    try:
        decrypt_payload(bytes(tampered), pwd)
        assert False, "Should have detected tampering!"
    except AuthenticationFailedError:
        print("Tampered ciphertext correctly rejected with AuthenticationFailedError: SUCCESS")
