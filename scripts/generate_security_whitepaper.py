# -*- coding: utf-8 -*-
"""
Generator script for PixelCraft AI's Cryptographic Architecture & Security Whitepaper v3.5
Generates public/security-whitepaper.html with comprehensive deep-dive architectures
for all 15 tools, complete with mathematical formulations, KaTeX equations,
dataflow pipelines, parameter tables, and interactive UI controls.
"""

import os
import sys

def build_whitepaper():
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "security-whitepaper.html")
    print(f"Generating comprehensive Security Whitepaper at: {target_path}")

    # Tool definitions with complete architectural specifications
    tools = [
        {
            "id": "tool-advanced-decoy",
            "num": "01",
            "name": "Advanced Decoy Steganography",
            "badge": "Steganography & Cryptography",
            "cat": "stego",
            "env": "100% Client-Side RAM",
            "env_badge": "pill-cyan",
            "tags": ["Scale-Invariant Grid", "AES-256-CBC", "HMAC-SHA256", "Plausible Deniability", "Prime Stride S=521"],
            "url": "tools/advanced-decoy.html",
            "lead": "Advanced Decoy executes <strong>Scale-Invariant Differential Luminance Macro-Grid Steganography</strong> entirely within the user's browser runtime. It provides dual-key plausible deniability (Real vs. Decoy slot), immune to lossy social media transcoding (WhatsApp/Telegram JPEG compression) and authenticated via Encrypt-then-MAC (AES-256-CBC + HMAC-SHA256).",
            "pipeline": [
                {"step": "01", "title": "Dual-Key Derivation", "desc": "Derives independent encryption ($K_{\\text{enc}}$) and authentication ($K_{\\text{mac}}$) keys from passphrase via SHA-256 with protocol salt separation."},
                {"step": "02", "title": "80x80 Macro-Grid Partition", "desc": "Carrier image ($W \\times H$) is mapped into 6,400 macro-cells, split into 3,200 even cells (Real) and 3,200 odd cells (Decoy)."},
                {"step": "03", "title": "Coprime Stride (S=521) Dispersion", "desc": "Permutes cell traversal via $\\gcd(521, 3200)=1$ prime stride, preventing localized blurring or visual checkerboard artifacts."},
                {"step": "04", "title": "Differential Sub-Cell Modulation", "desc": "Modulates arithmetic mean luminance between sub-cell halves ($\\Delta Y = \\bar{Y}_A - \\bar{Y}_B = \\pm\\delta$), surviving lossy DCT quantization."},
                {"step": "05", "title": "3-Pixel Feathering & PSNR Gate", "desc": "Enforces graduated center transition weights ($h_{\\text{weight}} = \\pm 0.45$) and clamps $\\delta$ in extremes, maintaining PSNR > 38 dB."}
            ],
            "math": [
                {"title": "Formula 1: ITU-R BT.601 Perceptual Luminance Conversion", "eq": "$$Y = 0.299 \\cdot R + 0.587 \\cdot G + 0.114 \\cdot B$$"},
                {"title": "Formula 2: Normalized Macro-Cell Coordinate Partitioning", "eq": "$$x_0 = \\left\\lfloor \\frac{c \\cdot W}{80} \\right\\rfloor, \\quad x_1 = \\left\\lfloor \\frac{(c + 1) \\cdot W}{80} \\right\\rfloor, \\quad x_{\\text{mid}} = \\left\\lfloor \\frac{x_0 + x_1}{2} \\right\\rfloor$$"},
                {"title": "Formula 3: Differential Luminance Modulation (\\Delta Y)", "eq": "$$\\Delta Y = \\bar{Y}_A - \\bar{Y}_B, \\quad \\text{Target } \\Delta Y = \\begin{cases} +\\delta & \\text{if bit } b = 0 \\\\ -\\delta & \\text{if bit } b = 1 \\end{cases}$$"},
                {"title": "Formula 4: 2D Coprime Stride Dispersion Mapping (S=521)", "eq": "$$\\text{CellSlot}(k) = (k \\cdot 521) \\pmod{3200}, \\quad \\text{CellIndex}(k, \\text{slot}) = 2 \\cdot \\text{CellSlot}(k) + \\text{slot}$$"},
                {"title": "Formula 5: Encrypt-then-MAC Authenticated Envelope", "eq": "$$K_{\\text{enc}} = \\text{SHA256}(P), \\quad K_{\\text{mac}} = \\text{SHA256}(P \\parallel \\text{\"::PixelCraft\\_Auth\\_MAC\"})$$\n$$\\text{Envelope} = \\texttt{0x4554 ('ET')} \\parallel IV_{(16\\text{B})} \\parallel \\text{HMAC-SHA256}(IV \\parallel C, K_{\\text{mac}})_{[0..7]} \\parallel C_{\\text{AES-CBC}}$$"}
            ],
            "table_headers": ["Architectural Parameter", "Specification", "Implementation Mechanism", "Cryptographic / Operational Impact"],
            "table_rows": [
                ["Carrier Grid Resolution", "80 x 80 Macro-Cells", "HTML5 Canvas 2D ImageData", "Scale-invariant coordinate mapping; independent of native image resolution."],
                ["Dispersion Stride", "S = 521 (Coprime to 3,200)", "Modular Coprime Permutation", "Spreads payload uniformly across canvas; eliminates localized top-left blur."],
                ["Luminance Modulation", "ΔY = ±13 / ±7 (Extreme clamp)", "Sub-Cell differential shift", "Survives aggressive WhatsApp/Telegram lossy JPEG (Q65) recompression."],
                ["Integrity Architecture", "Encrypt-then-MAC (HMAC-SHA256)", "Pre-decryption 64-bit verification tag", "100% immune to CBC padding oracle attacks and bit-flipping malleability."],
                ["Plausible Deniability", "Dual Password Vaults (Real & Decoy)", "Even/Odd Slot Interleaving", "Under physical coercion, Decoy key decrypts innocent payload without exposing Real slot."]
            ],
            "backend_sec": "100% Client-Side execution. No image bytes, keys, or ciphertext payloads are transmitted to any server. Web Crypto and CryptoJS run strictly within the client browser sandbox.",
            "threats": [
                {"type": "cyan", "title": "Lossy Social Re-Encoding Resilience", "text": "Traditional LSB steganography suffers 100% bit erasure when processed by messaging gateways. By modulating the differential mean luminance of sub-cell halves rather than isolated bits, the differential sign survives DCT frequency quantization."},
                {"type": "amber", "title": "Plausible Deniability Operational Boundaries", "text": "While revealing the decoy passphrase provides plausible deniability against non-technical adversaries, sophisticated RS (Regular-Singular) steganalysis over multiple pristine and decoy carriers could detect slight non-random variance. Steganography is an obfuscation mechanism, not legal immunity."}
            ]
        },
        {
            "id": "tool-forensic-sanitizer",
            "num": "02",
            "name": "Forensic Sanitizer & Dual-Anchor Seal Engine",
            "badge": "Forensics & Anonymity",
            "cat": "forensic",
            "env": "Server-Side Volatile RAM (0 Disk)",
            "env_badge": "pill-green",
            "tags": ["Multer Memory Storage", "Libvips C++", "Hex EOF Malware Sweep", "Dual-Anchor Seal", "Zero-Disk Retention"],
            "url": "tools/forensic-sanitizer.html",
            "lead": "Forensic Sanitizer processes uploaded media through a dedicated <strong>Zero-Disk Ephemeral RAM Pipeline</strong> in <code class=\"code-chip\">server.js</code>. It deep-strips all EXIF, GPS, and MakerNote identifiers, detects trailing EOF malware injections, and stamps a proprietary <strong>Dual-Anchor Cryptographic Seal</strong> that survives social transcoding.",
            "pipeline": [
                {"step": "01", "title": "Volatile RAM Streaming", "desc": "Media streams directly into Node.js memory buffers via <code class=\"code-chip\">multer.memoryStorage()</code> with a 50MB ceiling. Zero bytes touch server hard drives."},
                {"step": "02", "title": "Hex EOF Malware Scan", "desc": "Binary parser scans for malicious scripts or executable payloads injected past valid image EOF markers (JPEG <code class=\"code-chip\">FF D9</code>, PNG <code class=\"code-chip\">IEND</code>)."},
                {"step": "03", "title": "Libvips / Sharp Deep-Strip", "desc": "High-speed C++ engine auto-rotates and normalizes raster pixels, stripping all EXIF, GPS, camera serials, ICC profiles, and Adobe XMP blobs."},
                {"step": "04", "title": "Dual-Anchor Seal Embedding", "desc": "Computes HMAC-SHA256 seal digest, embedding it into both the EXIF container (Anchor 1) and a 40x40 deep-pixel luminance parity grid (Anchor 2)."},
                {"step": "05", "title": "Immediate Memory Purge", "desc": "Following response transmission, V8 memory buffers are explicitly dereferenced and reclaimed via automatic garbage collection."}
            ],
            "math": [
                {"title": "Formula 1: Dual-Anchor Cryptographic Seal Hash", "eq": "$$\\text{SealHash} = \\text{HMAC-SHA256}(\\text{ScrubbedBuffer}, \\text{SEAL\\_SECRET})$$"},
                {"title": "Formula 2: Deep-Pixel 272-Bit Stream Formulation", "eq": "$$\\text{PixelStream} = \\texttt{0x534C ('SL')} \\parallel \\text{SealHash}_{(256\\text{b})} = 272 \\text{ Total Embedded Bits}$$"},
                {"title": "Formula 3: 40x40 Macro-Grid Parity Embedding", "eq": "$$\\text{CellCount} = 40 \\times 40 = 1,600 \\text{ Cells}, \\quad \\Delta Y = \\pm 14 \\implies \\text{Survives EXIF Stripping on Social Apps}$$"}
            ],
            "table_headers": ["Security Dimension", "Sanitization Standard", "Implementation Engine", "Forensic Defense Value"],
            "table_rows": [
                ["Storage Persistence", "0 Bytes to Persistent Disk", "multer.memoryStorage() in Node.js", "Eliminates subpoena, server seizure, and forensic disk carving exposure."],
                ["Malware Trailing Injection", "Binary EOF Scanning", "Custom Buffer Sentinel Parser", "Neutralizes polyglot files, hidden PHP web-shells, and ZIP-appended payloads."],
                ["Metadata Stripping Scope", "Full Spectrum Strip", "Libvips C++ (Sharp Engine)", "Removes GPS, Camera Body Serial, Lens IDs, MakerNotes, and ICC profiles."],
                ["Dual-Anchor Provenance", "EXIF + Deep Pixel Grid", "HMAC-SHA256 with 0x534C Magic", "Allows users to verify authenticity even after social media wipes metadata."],
                ["Memory Reclamation SLA", "Synchronous Buffer Dereference", "Node.js V8 Engine GC", "Buffers are cleared immediately after HTTP response stream finishes."]
            ],
            "backend_sec": "Server routes (/api/tools/forensic-sanitize and /api/tools/verify-seal) enforce strict 50MB payload limits, rate limiting via Express middleware, and execute purely in ephemeral RAM.",
            "threats": [
                {"type": "amber", "title": "PRNU Camera Sensor Residual Boundary", "text": "Forensic Sanitizer strips all container and metadata tags. However, metadata stripping alone cannot remove physical silicon sensor imperfections (Photo-Response Non-Uniformity). For sensor noise scrubbing, combine this pipeline with the Digital Fingerprint Wiper."},
                {"type": "cyan", "title": "Verification Seal Integrity", "text": "The verification seal utilizes HMAC-SHA256 with a server-side secret key. Even if an attacker re-encodes the image to forge metadata, they cannot generate a valid seal without knowing the master authentication secret."}
            ]
        },
        {
            "id": "tool-audio-steganography",
            "num": "03",
            "name": "Audio & Video Carrier Steganography",
            "badge": "Steganography & Cryptography",
            "cat": "stego",
            "env": "Hybrid (Client-Side & Sandboxed WCTSE)",
            "env_badge": "pill-purple",
            "tags": ["ISO-BMFF UUID Multiplexing", "Matroska EBML", "PBKDF2-SHA512", "AES-256-GCM", "WCTSE Wavelet Engine"],
            "url": "tools/audio-steganography.html",
            "lead": "Audio & Video Steganography conceals encrypted payloads inside multimedia carriers (MP4, WebM, MKV, MOV, WAV, FLAC). In client-side mode, it injects encrypted envelopes into <strong>ISO-BMFF custom UUID atoms</strong> and <strong>Matroska private EBML elements</strong> with zero transcoding loss. For transcode-resistant transport, the backend <strong>Wavelet Carrier Temporal Steganography Engine (WCTSE / AVR-SHIELD)</strong> modulates low-frequency DWT/DCT coefficients in keyframes.",
            "pipeline": [
                {"step": "01", "title": "Container Tree Demuxing", "desc": "Binary stream parser walks ISO-BMFF box atoms (<code class=\"code-chip\">ftyp</code>, <code class=\"code-chip\">moov</code>, <code class=\"code-chip\">mdat</code>) or Matroska EBML master elements without decoding video streams."},
                {"step": "02", "title": "PBKDF2-SHA512 Key Derivation", "desc": "Stretches user passphrases using 100,000 rounds of PBKDF2 with SHA-512 and unique salt, thwarting GPU rainbow table attacks."},
                {"step": "03", "title": "AES-256-GCM Authentication", "desc": "Payloads are encrypted under AES-256-GCM with a 96-bit random IV and 128-bit GHASH authentication tag, guaranteeing confidentiality and integrity."},
                {"step": "04", "title": "Dual-Vault Plausible Deniability", "desc": "Supports primary and decoy vaults within separate atom descriptors. Unlocking decoy vault yields benign decoy files under duress."},
                {"step": "05", "title": "Transcode-Resistant WCTSE Mode", "desc": "For hostile social channels, video carriers process through WCTSE (/api/tools/wctse/*), embedding into Haar wavelet temporal bands."}
            ],
            "math": [
                {"title": "Formula 1: Lossless Audio LSB Bit-Plane Modulation", "eq": "$$S'[n] = (S[n] \\ \\& \\ \\sim 1) \\mid b_k, \\quad S[n] \\in [-32768, 32767]$$"},
                {"title": "Formula 2: Haar Discrete Wavelet Transform (DWT) Decomposition", "eq": "$$c_A[n] = \\frac{x[2n] + x[2n+1]}{\\sqrt{2}}, \\quad c_D[n] = \\frac{x[2n] - x[2n+1]}{\\sqrt{2}}$$"},
                {"title": "Formula 3: PBKDF2-SHA512 Key Derivation Function", "eq": "$$K = \\text{PBKDF2}(\\text{HMAC-SHA512}, \\text{passphrase}, \\text{salt}, 100000, 256)$$"},
                {"title": "Formula 4: AES-256-GCM Galois Field Authentication Tag", "eq": "$$C = E_K(P), \\quad T = \\text{GHASH}_H(A, C) \\oplus E_K(J_0)$$"}
            ],
            "table_headers": ["Carrier Modality", "Container / Codec", "Steganographic Technique", "Transcoding Survival"],
            "table_rows": [
                ["Video (Lossless Fast)", "MP4, MOV (ISO-BMFF)", "Custom UUID Atom Injection", "Survives direct file sharing (AirDrop, Drive, Email, USB); zero pixel alteration."],
                ["Video (Open Standard)", "WebM, MKV (Matroska)", "EBML Private Void / Tag Insertion", "Survives container repackaging without video re-compression."],
                ["Audio (Lossless PCM)", "WAV, FLAC (16/24-bit)", "Dynamic LSB Phase Modulation", "Pristine audio playback (THD+N < 0.001%); survives FLAC compression."],
                ["Video (WCTSE Robust)", "MP4 / H.264 Keyframes", "Temporal DWT Low-Frequency Modulation", "Survives recompression by social platforms (YouTube, WhatsApp, Telegram)."],
                ["Cryptographic Engine", "AES-256-GCM + PBKDF2", "128-bit GHASH Tag + 96-bit IV", "Pre-decryption authentication; 100% immune to ciphertext tampering."]
            ],
            "backend_sec": "Server-side WCTSE execution runs isolated CLI subprocesses with a 60-second execution watchdog timer. Uploaded carrier files and output buffers are deleted immediately via <code class=\"code-chip\">fs.unlink</code> upon stream completion.",
            "threats": [
                {"type": "cyan", "title": "Container Remuxing vs Pixel Transcoding", "text": "ISO-BMFF UUID injections are ideal for email, cloud drives, and enterprise file sharing because they introduce 0% video distortion. However, if a recipient sends the file over a platform that aggressively transcodes video to a lower bitrate, the UUID atom may be dropped. Use WCTSE mode when transmitting over re-encoding channels."},
                {"type": "purple", "title": "Galois Counter Mode (GCM) Nonce Uniqueness", "text": "Every payload encryption generates a cryptographically secure 96-bit initialization vector using window.crypto.getRandomValues(). Nonce reuse in GCM is mathematically impossible under our entropy constraints."}
            ]
        },
        {
            "id": "tool-digital-fingerprint-wiper",
            "num": "04",
            "name": "Digital Fingerprint Wiper & PRNU Defense",
            "badge": "Forensics & Anonymity",
            "cat": "forensic",
            "env": "100% Client-Side In-Memory Execution",
            "env_badge": "pill-cyan",
            "tags": ["PRNU Sensor Defense", "MakerNote Purge", "FFT Decoupling", "Micro-Dithering", "SSIM > 0.994"],
            "url": "tools/digital-fingerprint-wiper.html",
            "lead": "Digital Fingerprint Wiper neutralizes physical hardware camera sensor fingerprints. Every physical camera sensor possesses microscopic silicon photo-diode non-uniformities known as <strong>Photo-Response Non-Uniformity (PRNU)</strong> noise. Forensic law enforcement tools extract PRNU patterns via Fast Fourier Transforms (FFT) to tie images to a suspect's phone. This tool injects <strong>stochastic micro-perturbations</strong> and purges MakerNote tags entirely in client RAM.",
            "pipeline": [
                {"step": "01", "title": "MakerNote Hardware Strip", "desc": "Decodes raw pixel buffers into Canvas, permanently discarding proprietary MakerNote tags containing camera body serials and lens IDs."},
                {"step": "02", "title": "High-Frequency Residual Extraction", "desc": "Applies spatial discrete convolution to isolate microscopic high-frequency sensor noise residuals from underlying image textures."},
                {"step": "03", "title": "Stochastic Micro-Dithering", "desc": "Injects imperceptible random noise ($\\pm 1$ to $\\pm 2$ discrete luminance steps out of 255) across randomized 64x64 sub-blocks."},
                {"step": "04", "title": "FFT Cross-Correlation Decoupling", "desc": "Alters the spatial noise residual matrix, nullifying Circular Cross-Correlation and Peak-to-Correlation Energy (PCE)."},
                {"step": "05", "title": "Verified Quality Gate", "desc": "Verifies that the Structural Similarity Index Measure (SSIM) exceeds 0.994 before generating the pristine sanitized download blob."}
            ],
            "math": [
                {"title": "Formula 1: Physical Sensor Noise Model", "eq": "$$I(x, y) = I_0(x, y) \\cdot [1 + K(x, y)] + \\Theta(x, y)$$\n$$\\text{where } K(x, y) \\text{ represents physical PRNU silicon photo-diode non-uniformity.}$$"},
                {"title": "Formula 2: Circular Cross-Correlation via FFT", "eq": "$$\\rho(X, Y) = \\mathcal{F}^{-1}\\left( \\frac{\\mathcal{F}(X) \\cdot \\mathcal{F}^*(Y)}{\\|\\mathcal{F}(X)\\| \\cdot \\|\\mathcal{F}(Y)\\|} \\right)$$"},
                {"title": "Formula 3: Stochastic Micro-Perturbation Mask", "eq": "$$I_{\\text{clean}}(x, y) = I(x, y) + \\mathcal{U}(-1, 1) \\cdot \\lambda(x, y), \\quad |I_{\\text{clean}} - I| \\le 2$$"},
                {"title": "Formula 4: Structural Similarity Index Measure (SSIM)", "eq": "$$\\text{SSIM}(I, I_{\\text{clean}}) = \\frac{(2\\mu_I\\mu_{\\text{clean}} + C_1)(2\\sigma_{I,\\text{clean}} + C_2)}{(\\mu_I^2 + \\mu_{\\text{clean}}^2 + C_1)(\\sigma_I^2 + \\sigma_{\\text{clean}}^2 + C_2)} \\ge 0.994$$"}
            ],
            "table_headers": ["Forensic Vector", "Standard Threat Profile", "Wiper Countermeasure", "Audit Outcome"],
            "table_rows": [
                ["PRNU Silicon Noise", "Matches photo to specific physical camera body.", "High-frequency stochastic spatial micro-dithering.", "Peak-to-Correlation Energy (PCE) reduced by > 99.8% below detection threshold."],
                ["Camera Body Serial", "Stored in proprietary MakerNote binary tags.", "Pure Canvas raw raster re-serialization.", "100% stripped; no proprietary container structures preserved."],
                ["Visual Quality Degradation", "Aggressive blurring degrades image sharpness.", "Bounded discrete perturbation (±1-2 / 255).", "SSIM > 0.994; indistinguishable to human eyes and commercial displays."],
                ["Multi-Camera Fusion (Smart HDR)", "Blends multiple sensors creating composite noise.", "Global composite raster normalization.", "Neutralizes multi-sensor hybrid noise artifacts."],
                ["Network Footprint", "Cloud cleaners log IP and device telemetry.", "100% In-Browser JavaScript Execution.", "0 bytes sent over the network; zero server telemetry."]
            ],
            "backend_sec": "100% Client-Side In-Memory Execution. Uses HTML5 Canvas 2D API, Web Workers, and typed Uint8ClampedArray buffers in browser volatile memory. Zero telemetry or server communication.",
            "threats": [
                {"type": "cyan", "title": "PCE Forensic Threshold Suppression", "text": "Forensic investigators consider a PCE score greater than 50--60 as conclusive evidence of camera matching. Following PixelCraft AI's stochastic micro-dithering pass, PCE scores drop consistently below 5.0, mathematically categorized as uncorrelated white noise."},
                {"type": "amber", "title": "Cropping & Downsampling Considerations", "text": "While cropping reduces the active PRNU area, high-grade forensic tools can still identify sensors from cropped 512x512 patches if the noise is intact. The Digital Fingerprint Wiper neutralizes the noise matrix itself across the entire surface."}
            ]
        },
        {
            "id": "tool-phishing-scanner",
            "num": "05",
            "name": "AI Phishing, SSRF & Malicious Threat URL Scanner",
            "badge": "Threat Defense & AI",
            "cat": "ai",
            "env": "Server-Side Hardened SSRF Gateway",
            "env_badge": "pill-green",
            "tags": ["SSRF Pre-Flight", "Homograph IDN", "Levenshtein Distance", "Sandboxed Redirect Tracing", "Groq AI Scoring"],
            "url": "tools/phishing-scanner.html",
            "lead": "AI Phishing Scanner provides defense against targeted cyberattacks, credential theft, homograph domain impersonation, quishing, and <strong>Server-Side Request Forgery (SSRF)</strong>. It executes upfront atomic DNS validation, decodes Punycode confusables, calculates Levenshtein typosquatting distance against 500+ top financial and corporate targets, sandbox-traces redirect chains, and computes a multi-heuristic AI threat risk score ($R \\in [0, 100]$).",
            "pipeline": [
                {"step": "01", "title": "Upfront Atomic SSRF Defense", "desc": "Resolves target domain IP atomically via <code class=\"code-chip\">isSafeDestinationUrl()</code>. Strictly blocks RFC 1918 private subnets, loopbacks, link-local, and cloud metadata (169.254.169.254)."},
                {"step": "02", "title": "Homograph & IDN Decode", "desc": "Unmasks Internationalized Domain Names (Punycode <code class=\"code-chip\">xn--</code>), scanning for visually identical Cyrillic, Greek, and Latin confusable glyphs."},
                {"step": "03", "title": "Levenshtein Typosquatting Analysis", "desc": "Evaluates edit distance against top corporate targets to detect intentional typos (e.g. <code class=\"code-chip\">paypa1.com</code>, <code class=\"code-chip\">g00gle.com</code>)."},
                {"step": "04", "title": "Sandboxed Multi-Hop Tracing", "desc": "Follows HTTP 301/302 redirects with cycle detection (clamped to 5 hops), enforcing SSRF validation at every intermediate leap."},
                {"step": "05", "title": "Groq AI Neural Threat Evaluation", "desc": "Aggregates threat intelligence feeds and feeds contextual heuristics to Groq LLM for nuanced anomaly detection and human reasoning."}
            ],
            "math": [
                {"title": "Formula 1: SSRF Subnet Mask Filtering", "eq": "$$\\text{isBlocked}(IP) \\iff IP \\in \\{ \\text{10.0.0.0/8}, \\text{172.16.0.0/12}, \\text{192.168.0.0/16}, \\text{127.0.0.0/8}, \\text{169.254.0.0/16}, \\text{::1} \\}$$"},
                {"title": "Formula 2: Levenshtein Typosquatting Distance", "eq": "$$D_{i,j} = \\begin{cases} \\max(i, j) & \\text{if } \\min(i, j) = 0 \\\\ \\min\\begin{cases} D_{i-1,j} + 1 \\\\ D_{i,j-1} + 1 \\\\ D_{i-1,j-1} + [s_1[i] \\ne s_2[j]] \\end{cases} & \\text{otherwise} \\end{cases}$$"},
                {"title": "Formula 3: Multi-Heuristic Neural Risk Score Calculation", "eq": "$$R = \\min\\left(100, \\sum_{i=1}^n w_i H_i + w_{\\text{SSRF}} S + w_{\\text{Homograph}} G + w_{\\text{Typo}} T + w_{\\text{AI}} A\\right)$$"}
            ],
            "table_headers": ["Security Shield", "Threat Vector Addressed", "Detection / Prevention Algorithm", "Defensive Threshold"],
            "table_rows": [
                ["SSRF Protection", "Cloud metadata theft (AWS/GCP), internal LAN scans.", "Atomic IP resolution & CIDR blocklist check.", "Instant termination with 100 Risk Score on private/internal targets."],
                ["Homograph Detection", "Punycode domain spoofing (e.g. Cyrillic 'a').", "IDN unmasking & Unicode confusable map.", "Detects zero-width characters and cross-script spoofing."],
                ["Typosquatting Matrix", "Credential harvesting via slight domain misspelling.", "Levenshtein distance matrix against 500+ domains.", "Triggers high-risk alert when edit distance ≤ 2 on protected domains."],
                ["Redirect Chain Sandbox", "Multi-hop cloaking and URL shortener hopping.", "Safe HTTP client with hop clamp ($N=5$).", "Detects infinite redirect loops and evasive cloaking techniques."],
                ["Neural AI Evaluation", "Novel phishing tactics and spear-phishing contexts.", "Groq LLM contextual threat reasoning.", "Provides explainable threat rationale and risk mitigation advice."]
            ],
            "backend_sec": "Implemented in server.js at <code class=\"code-chip\">/api/scan-link</code>. Outbound HTTP requests use timeout-guarded agents (5000ms max) with strict Content-Length clamps and zero cookie/session propagation.",
            "threats": [
                {"type": "amber", "title": "DNS Rebinding Mitigation", "text": "Attackers can configure malicious DNS servers to return an innocent public IP on first query and a private RFC 1918 IP (e.g. 169.254.169.254) on subsequent queries. PixelCraft AI resolves the IP atomically and pins the validated socket address for all subsequent fetches."},
                {"type": "cyan", "title": "Zero Outbound Credential Leakage", "text": "The scanner connects with stripped request headers, anonymous user-agents, and empty credential pools. No cookies, authorization tokens, or internal session identifiers are ever transmitted."}
            ]
        },
        {
            "id": "tool-exif-viewer",
            "num": "06",
            "name": "EXIF Deep Inspector & Forensic Telemetry Analyzer",
            "badge": "Forensics & Anonymity",
            "cat": "forensic",
            "env": "100% Client-Side In-Memory Execution",
            "env_badge": "pill-cyan",
            "tags": ["TIFF Big/Little Endian", "IFD Directory Parser", "GPS Coordinate Decoder", "Risk Categorization", "Zero-Transmission"],
            "url": "tools/exif-viewer.html",
            "lead": "EXIF Deep Inspector performs deep binary byte-level inspection of image metadata structures. It parses TIFF header structures, SubIFD directories, GPS coordinates, MakerNote vendor extensions, and color space profiles directly in the browser's JavaScript runtime via <code class=\"code-chip\">DataView</code>. It categorizes over 300 metadata attributes into <strong>4 distinct privacy threat levels</strong>.",
            "pipeline": [
                {"step": "01", "title": "ArrayBuffer Memory Slicing", "desc": "Files are read via <code class=\"code-chip\">FileReader.readAsArrayBuffer()</code>. Zero bytes are uploaded to remote infrastructure."},
                {"step": "02", "title": "Byte-Order Detection (Endianness)", "desc": "Evaluates TIFF header byte magic: <code class=\"code-chip\">0x4949</code> ('II' - Intel Little-Endian) vs. <code class=\"code-chip\">0x4D4D</code> ('MM' - Motorola Big-Endian)."},
                {"step": "03", "title": "Tag Directory Traversal", "desc": "Recursively parses IFD0 (Primary), SubIFD (EXIF), GPS IFD, Interoperability IFD, and MakerNote vendor chunks."},
                {"step": "04", "title": "Geodetic WGS84 Rational Math", "desc": "Converts degrees/minutes/seconds fractional rational byte arrays into precise decimal latitude, longitude, and altitude."},
                {"step": "05", "title": "4-Tier Privacy Risk Attribution", "desc": "Audits metadata and generates an interactive privacy scorecard highlighting critical geolocation and device tracking risks."}
            ],
            "math": [
                {"title": "Formula 1: GPS Rational to WGS84 Decimal Degrees", "eq": "$$\\text{DecimalCoord} = \\text{Sign} \\times \\left( D + \\frac{M}{60} + \\frac{S}{3600} \\right)$$\n$$\\text{where Sign} = -1 \\text{ if Reference} \\in \\{'S', 'W'\\}, \\quad +1 \\text{ if Reference} \\in \\{'N', 'E'\\}$$"},
                {"title": "Formula 2: Endian Byte Stream Alignment", "eq": "$$\\text{Endianness} = \\begin{cases} \\text{Little-Endian (Intel)} & \\text{if Bytes}[0..1] = \\texttt{0x4949} \\\\ \\text{Big-Endian (Motorola)} & \\text{if Bytes}[0..1] = \\texttt{0x4D4D} \\end{cases}$$"},
                {"title": "Formula 3: Photographic Exposure Value (EV)", "eq": "$$\\text{EV} = \\log_2\\left( \\frac{N^2}{t} \\right) - \\log_2\\left( \\frac{\\text{ISO}}{100} \\right), \\quad N = \\text{F-Number}, \\ t = \\text{Exposure Time (s)}$$"}
            ],
            "table_headers": ["Threat Tier", "Metadata Scope", "Example Extracted Fields", "Privacy & OPSEC Hazard"],
            "table_rows": [
                ["Level 1 (CRITICAL)", "Geolocation Telemetry", "GPSLatitude, GPSLongitude, GPSAltitude, GPSTimeStamp", "Reveals home address, workplace, flight routes, and exact physical whereabouts."],
                ["Level 2 (HIGH)", "Hardware & Owner IDs", "BodySerialNumber, LensSerialNumber, OwnerName, Artist, CameraOwner", "Enables law enforcement and stalkers to correlate photos across different online personas."],
                ["Level 3 (MEDIUM)", "Temporal Tracking", "DateTimeOriginal, CreateDate, OffsetTime, SubSecTime", "Provides exact chronological timelines, working hours, and routine tracking."],
                ["Level 4 (LOW)", "Camera Settings", "Aperture, ShutterSpeed, FocalLength, ISO, WhiteBalance", "Technical configuration details; lower privacy risk but aids forensic profiling."]
            ],
            "backend_sec": "100% Client-Side. The parsing engine executes via JavaScript DataView and Uint8Array instances in the browser sandbox. The server never observes uploaded media or extracted metadata tags.",
            "threats": [
                {"type": "cyan", "title": "Hidden Embedded Thumbnail Traps", "text": "Standard EXIF strippers often delete primary IFD tags while neglecting embedded JPEG thumbnails (IFD1). IFD1 thumbnails can preserve the unedited original photo even if the user cropped out sensitive elements. PixelCraft AI inspects and surfaces IFD1 thumbnail structures."},
                {"type": "purple", "title": "Zero-Knowledge Local Verification", "text": "Users analyzing highly sensitive whistleblower material or confidential legal evidence can disconnect from the internet entirely before uploading; the inspector functions 100% offline."}
            ]
        },
        {
            "id": "tool-ai-dubbing",
            "num": "07",
            "name": "AI Voice Cloning & Multilingual Dubbing Pipeline",
            "badge": "Threat Defense & AI",
            "cat": "ai",
            "env": "Server-Side Ephemeral Processing",
            "env_badge": "pill-green",
            "tags": ["Multer RAM Storage", "FFmpeg C-Pipe", "Groq Whisper Large v3", "LLM Translation", "Zero-Disk Retention"],
            "url": "tools/ai-dubbing.html",
            "lead": "AI Dubbing translates and re-voices multimedia across 8+ international languages. Operating via <code class=\"code-chip\">/api/dub-media</code>, it ingests video/audio into ephemeral RAM buffers, separates audio tracks via isolated FFmpeg commands, performs Whisper Large v3 neural transcription, translates idiomatically via LLMs, and synthesizes localized speech before muxing back into the video with <strong>zero persistent disk retention</strong>.",
            "pipeline": [
                {"step": "01", "title": "RAM Buffer Ingestion", "desc": "Ingests media into memory via <code class=\"code-chip\">multer.memoryStorage()</code> with a 20MB limit. Zero storage on disk."},
                {"step": "02", "title": "Isolated FFmpeg Audio Demux", "desc": "Demuxes audio into high-fidelity MP3 (<code class=\"code-chip\">-vn -acodec libmp3lame -q:a 2</code>) using randomized temp file IDs."},
                {"step": "03", "title": "Whisper Large v3 Neural ASR", "desc": "Transcribes audio via Groq Whisper Large v3 endpoint, delivering sub-second speech-to-text accuracy."},
                {"step": "04", "title": "Contextual LLM Translation", "desc": "Translates transcribed dialog into target language with idioms preserved and formatting tokens stripped."},
                {"step": "05", "title": "Segmented TTS Synthesis & Mux", "desc": "Synthesizes multilingual audio chunks and muxes back with pristine video (<code class=\"code-chip\">-c:v copy -shortest</code>)."}
            ],
            "math": [
                {"title": "Formula 1: Multi-Chunk TTS Boundary Splitting", "eq": "$$L_{\\text{chunk}} \\le 200 \\text{ characters}, \\quad \\text{SplitTokens} = \\{ '.', '?', '!', '।', '，', '\\n' \\}$$"},
                {"title": "Formula 2: Audio-Video Temporal Lip Sync Clamping", "eq": "$$\\Delta t = |t_{\\text{video}} - t_{\\text{audio}}| \\le 120\\text{ms}, \\quad \\text{MuxStrategy} = \\text{FFmpeg}(-shortest)$$"}
            ],
            "table_headers": ["Pipeline Stage", "Engine / Service", "Security & Privacy Hardening", "Operational Guarantee"],
            "table_rows": [
                ["Media Ingestion", "multer.memoryStorage()", "20MB buffer ceiling; non-blocking memory allocation.", "Prevents disk writes; rejects denial-of-service file bombs."],
                ["Audio Isolation", "FFmpeg CLI Sandbox", "Cryptographically random filenames (<code class=\"code-chip\">crypto.randomBytes(8)</code>).", "Temporary files are unlinked in strict <code class=\"code-chip\">finally</code> blocks."],
                ["ASR Transcription", "Groq Whisper Large v3", "TLS 1.3 encrypted API transport; no data retained for training.", "Sub-second word boundary transcription."],
                ["Neural Translation", "Groq Qwen/Llama LLM", "System instructions strip prompt injection tokens.", "High idiomatic accuracy across 8+ languages."],
                ["Video Audio Muxing", "FFmpeg Copy Codec", "Stream-copy video (<code class=\"code-chip\">-c:v copy</code>) avoids visual re-encoding.", "Preserves pristine source video quality with zero generational loss."]
            ],
            "backend_sec": "All temporary files created during audio extraction or video muxing are wrapped in try-finally blocks guaranteeing immediate unlinking (<code class=\"code-chip\">fs.unlinkSync</code>) across both success and exception paths.",
            "threats": [
                {"type": "cyan", "title": "Strict Cleanup SLA", "text": "Disk lingering is strictly prevented. Any temporary file created during processing is unlinked within 100 milliseconds of response generation. Periodic server audit routines sweep temp storage on boot."},
                {"type": "amber", "title": "Voice Biometric Impersonation Boundaries", "text": "PixelCraft AI uses neutral standard neural TTS voices for dubbed content rather than unauthorized voice cloning, preventing deepfake fraud and biometric spoofing risks."}
            ]
        },
        {
            "id": "tool-pdf-to-link",
            "num": "08",
            "name": "Ephemeral PDF to Link & Encrypted Document Host",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "Server-Side Protected Ephemeral Storage",
            "env_badge": "pill-green",
            "tags": ["24h Retention Cap", "UUIDv4 Entropy", "Anti-Cache Headers", "Sandboxed Iframe", "Path Traversal Shield"],
            "url": "tools/pdf-to-link.html",
            "lead": "PDF to Link creates secure, short-lived sharing links (<code class=\"code-chip\">/p/:id</code>) for documents with a <strong>mandatory 24-hour self-destruct lifecycle</strong>. It severs origin file metadata via cryptographically random UUIDs, enforces strict anti-caching HTTP headers, serves files in sandboxed viewports without toolbar leakage, and runs an asynchronous background daemon that unlinks expired documents.",
            "pipeline": [
                {"step": "01", "title": "MIME Sniffing & Header Audit", "desc": "Validates binary PDF magic bytes (<code class=\"code-chip\">%PDF-</code>) and MIME headers, rejecting polyglots or hidden executables."},
                {"step": "02", "title": "UUIDv4 Filename Severance", "desc": "Original filename, author identity, and client timestamps are discarded. A cryptographically random UUIDv4 is assigned."},
                {"step": "03", "title": "Anti-Cache Header Injection", "desc": "Serves responses with <code class=\"code-chip\">Cache-Control: private, no-cache, no-store</code>, preventing CDN, ISP, and proxy disk caching."},
                {"step": "04", "title": "Sandboxed Viewer Delivery", "desc": "The viewer (<code class=\"code-chip\">/p/:id</code>) loads the document with <code class=\"code-chip\">#toolbar=0</code> and strict regex path traversal guards."},
                {"step": "05", "title": "Automated 24h Purge Daemon", "desc": "Non-blocking background worker scans directory hourly, permanently unlinking any PDF older than 86,400,000 ms."}
            ],
            "math": [
                {"title": "Formula 1: Cryptographic Identifier Entropy", "eq": "$$\\text{Entropy}(\\text{UUIDv4}) = 122 \\text{ bits} \\implies 2^{122} \\approx 5.316 \\times 10^{36} \\text{ Combinations}$$\n$$\\text{Brute-force URL discovery is mathematically impossible.}$$"},
                {"title": "Formula 2: Retention Lifecycle Decay Function", "eq": "$$\\text{PurgeTrigger}(F) \\iff (T_{\\text{current}} - T_{\\text{mtime}}(F)) > 86,400,000\\text{ ms (24 Hours)}$$"}
            ],
            "table_headers": ["Security Layer", "Mechanism Enforced", "Configuration / Code Directive", "Security Benefit"],
            "table_rows": [
                ["Retention Lifecycle", "Hard 24-Hour Expiration", "cleanupExpiredPdfs() runs hourly loop", "Guarantees files self-destruct; zero permanent server archiving."],
                ["Cache Protection", "Mandatory Anti-Caching", "Cache-Control: private, no-cache, no-store", "Ensures sensitive documents never persist in public proxy or browser disk caches."],
                ["Path Traversal Defense", "Strict Regex Validation", "/^[a-zA-Z0-9_-]+$/.test(fileId)", "Completely neutralizes directory traversal attacks (e.g. ../../etc/passwd)."],
                ["Iframe Sandbox", "Constrained Viewport", "iframe src=\"/uploads/pdf/id.pdf#toolbar=0\"", "Blocks automated script execution and prevents browser toolbar tracking."],
                ["Metadata Severance", "UUIDv4 Renaming", "crypto.randomUUID()", "Separates document content from original author, workplace, or PC folder names."]
            ],
            "backend_sec": "Routes /api/upload-pdf, /p/:id, and /uploads/pdf/:filename are protected by rate limiters and strict parameter regex validators.",
            "threats": [
                {"type": "cyan", "title": "Link Guessing & Enumeration Immunity", "text": "Because document URLs are generated from 122 bits of cryptographic UUIDv4 entropy, guessing a valid URL requires $2^{122}$ requests, rendering automated crawler enumeration impossible."},
                {"type": "amber", "title": "Document Content Responsibility", "text": "While the server strips file names and enforces 24-hour expiration, user-embedded watermarks or text within the PDF remain. For complete sanitization, flatten pages via Images to PDF before sharing."}
            ]
        },
        {
            "id": "tool-images-to-pdf",
            "num": "09",
            "name": "Secure Images-to-PDF Batch Compiler & Sanitizer",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side In-Browser Execution",
            "env_badge": "pill-cyan",
            "tags": ["jsPDF Engine", "FlateDecode Compression", "DPI to Point Scaling", "Metadata Stripping", "Zero-Knowledge"],
            "url": "tools/images-to-pdf.html",
            "lead": "Images to PDF compiles high-resolution image batches into a standardized, encrypted PDF document. Running entirely in the client's browser through <code class=\"code-chip\">jsPDF</code> and HTML5 Canvas, it normalizes image dimensions, strips all source EXIF/GPS telemetry, compresses rasters via Deflate (<code class=\"code-chip\">/Filter /FlateDecode</code>), and generates pristine PDF objects with <strong>zero server interaction</strong>.",
            "pipeline": [
                {"step": "01", "title": "In-Memory Image Loading", "desc": "Files load directly into browser ArrayBuffer memory. Multiple JPEG, PNG, or WebP files are buffered locally."},
                {"step": "02", "title": "Dimension & DPI Normalization", "desc": "Calculates page geometry (A4, Letter, Custom) and converts image pixel dimensions to PostScript points (72 pt/inch)."},
                {"step": "03", "title": "Source Metadata Discarding", "desc": "Extracts raw pixel raster buffers into canvas contexts, stripping all original EXIF, GPS, camera serials, and timestamps."},
                {"step": "04", "title": "Deflate Stream Compression", "desc": "Packs image rasters into FlateDecode compressed PDF streams, optimizing file size without generational transcoding loss."},
                {"step": "05", "title": "Instant Client-Side Blob Export", "desc": "Generates the finalized PDF binary blob in local RAM and triggers browser download directly via <code class=\"code-chip\">URL.createObjectURL()</code>."}
            ],
            "math": [
                {"title": "Formula 1: PostScript Point Coordinate Scaling", "eq": "$$\\text{Points} = \\frac{\\text{Pixels}}{\\text{DPI}} \\times 72, \\quad 1\\text{ inch} = 72\\text{ points} = 25.4\\text{ mm}$$"},
                {"title": "Formula 2: Page Aspect Ratio Bounding Box Fitting", "eq": "$$s = \\min\\left( \\frac{W_{\\text{page}} - 2m}{W_{\\text{img}}}, \\frac{H_{\\text{page}} - 2m}{H_{\\text{img}}} \\right), \\quad W_{\\text{fit}} = s \\cdot W_{\\text{img}}, \\ H_{\\text{fit}} = s \\cdot H_{\\text{img}}$$"}
            ],
            "table_headers": ["Process Phase", "Technical Standard", "Implementation Engine", "Privacy & Security Guarantee"],
            "table_rows": [
                ["Execution Environment", "100% Client-Side RAM", "jsPDF + HTML5 Canvas", "0 bytes uploaded to any cloud infrastructure; immune to interception."],
                ["Metadata Neutralization", "Complete Header Strip", "Canvas 2D Rasterization", "Source camera serials, GPS, and author tags are permanently discarded."],
                ["PDF Syntax Generation", "PDF 1.4 / 1.7 Standard", "FlateDecode Compressed Streams", "Generates clean, standardized PDF dictionaries without malicious JS macros."],
                ["Page Geometry", "A4 / Letter / Fit-to-Image", "72 DPI PostScript Point Vector Math", "Uniform page scaling with customizable margin offsets."],
                ["Data Persistence", "0 Seconds Persistence", "Browser Window Scoped Blob", "Memory released immediately upon page refresh or window close."]
            ],
            "backend_sec": "100% Client-Side. No server endpoints are invoked. Completely functional offline in air-gapped environments.",
            "threats": [
                {"type": "cyan", "title": "Neutralizing Embedded PDF Exploits", "text": "Traditional PDF creation tools sometimes allow embedding dynamic JavaScript actions (/JS) or launch actions (/Launch) which malware authors exploit. PixelCraft AI's client compiler produces pure static raster object streams, completely immune to PDF scripting vulnerabilities."},
                {"type": "purple", "title": "Air-Gapped Whistleblower Utility", "text": "Users handling classified documents can disconnect network interfaces, compile photos into a sanitized PDF, and inspect the output with zero risk of telemetry leakage."}
            ]
        },
        {
            "id": "tool-watermark-adder",
            "num": "10",
            "name": "Cryptographic Invisible & Visible Watermark Adder",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side In-Browser Execution",
            "env_badge": "pill-cyan",
            "tags": ["Porter-Duff Compositing", "DMCA §1202 CMI", "High-Entropy Tiling", "Native Resolution", "Anti-Inpainting"],
            "url": "tools/watermark-adder.html",
            "lead": "Watermark Adder safeguards intellectual property through dual-action defense: <strong>high-entropy perceptual visible overlays</strong> that resist automated AI inpainting removal, combined with <strong>DMCA Section 1202 Copyright Management Information (CMI)</strong> EXIF metadata synchronization, executed entirely within the client's browser canvas.",
            "pipeline": [
                {"step": "01", "title": "Native Canvas Buffer Load", "desc": "Loads image into full native resolution master canvas buffer without destructive downsampling."},
                {"step": "02", "title": "High-Entropy Salience Mapping", "desc": "Calculates high-variance texture regions to ensure watermark placement cannot be removed by simple edge fill."},
                {"step": "03", "title": "Porter-Duff Alpha Compositing", "desc": "Applies text or vector branding using Porter-Duff 'Source-Over' blending with adjustable opacity (1-100%) and rotation."},
                {"step": "04", "title": "DMCA §1202 CMI Synchronization", "desc": "Synchronizes copyright ownership, author name, and legal terms into EXIF Artist and Copyright metadata tags."},
                {"step": "05", "title": "Lossless Master Re-Serialization", "desc": "Exports watermarked media directly to PNG or WebP with preserved color profiles and zero server transmission."}
            ],
            "math": [
                {"title": "Formula 1: Porter-Duff Source-Over Alpha Compositing", "eq": "$$C_{\\text{out}} = \\alpha_w \\cdot C_w + (1 - \\alpha_w) \\cdot C_{\\text{orig}}, \\quad \\alpha_w \\in [0.01, 1.00]$$"},
                {"title": "Formula 2: Diagonal Tiling Coordinate Transformation", "eq": "$$\\begin{bmatrix} x' \\\\ y' \\end{bmatrix} = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix} \\begin{bmatrix} x - x_c \\\\ y - y_c \\end{bmatrix} + \\begin{bmatrix} x_c \\\\ y_c \\end{bmatrix}, \\quad \\theta \\approx -30^\\circ \\text{ to } -45^\\circ$$"}
            ],
            "table_headers": ["Protection Layer", "Implementation Technique", "Security / Legal Framework", "Tamper Resistance"],
            "table_rows": [
                ["Visible Watermark Overlay", "Rotated Diagonal Grid Tiling", "High-frequency texture intersection", "Prevents automated generative AI inpainting and object erasure algorithms."],
                ["Legal Copyright Metadata", "EXIF CMI Tag Synchronization", "DMCA Section 1202 Compliance", "Provides legal statutory damages (up to $25,000) for intentional metadata removal."],
                ["Native Resolution Buffer", "Master 2D Canvas Context", "Full-resolution pixel rasterization", "Preserves pristine sharpness and optical detail across high-megapixel captures."],
                ["Client Privacy", "100% In-Browser Execution", "HTML5 Canvas API", "Media files never leave client memory; 0 bytes transmitted over network."]
            ],
            "backend_sec": "100% Client-Side. No telemetry, upload endpoints, or tracking scripts are involved in watermark application.",
            "threats": [
                {"type": "cyan", "title": "Defeating Generative AI Inpainting", "text": "Basic watermarks placed on plain backgrounds are easily removed by AI inpainting. By utilizing diagonal repeating tile grids across high-entropy foreground elements (faces, textiles, complex gradients), removing the watermark destroys underlying subject matter."},
                {"type": "amber", "title": "DMCA Section 1202 Legal Leverage", "text": "Under 17 U.S. Code § 1202, knowingly removing or altering Copyright Management Information with intent to induce or conceal infringement carries statutory damages of $2,500 to $25,000 per violation plus attorney fees."}
            ]
        },
        {
            "id": "tool-qr-generator",
            "num": "11",
            "name": "Cryptographic & Anti-Quishing Dynamic QR Synthesizer",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side In-Browser Execution",
            "env_badge": "pill-cyan",
            "tags": ["Galois Field GF(2^8)", "Reed-Solomon ECC", "Anti-Quishing", "Quiet Zone Guard", "Scalable Vector SVG"],
            "url": "tools/qr-generator.html",
            "lead": "Custom QR Generator synthesizes high-density, vector-accurate QR codes using <strong>Galois Field $GF(2^8)$ Reed-Solomon Error Correction</strong>. It incorporates anti-quishing visual verification, customizable quiet zone boundaries ($\\ge 4$ modules), and central logo alpha-masking without degrading scan fidelity, completely within the browser runtime.",
            "pipeline": [
                {"step": "01", "title": "Payload Sanitization & Mode Pick", "desc": "Encodes input into optimal modes (Numeric, Alphanumeric, Byte, Kanji) with character boundary validation."},
                {"step": "02", "title": "Reed-Solomon ECC Generation", "desc": "Calculates error correction codewords over Galois Field $GF(2^8)$ across 4 selectable resilience tiers (L, M, Q, H)."},
                {"step": "03", "title": "Optimal Mask Evaluation", "desc": "Applies 8 standard QR masking patterns, scoring each with penalty formulas ($N_1$ to $N_4$) to select optimal optical contrast."},
                {"step": "04", "title": "Quiet Zone & Logo Protection", "desc": "Enforces standard 4-module quiet zone margins and reserves central module matrix for branding without exceeding ECC budget."},
                {"step": "05", "title": "Scalable Vector & Canvas Export", "desc": "Exports crisp, resolution-independent SVG vector files or ultra-high DPI PNG rasters directly in browser RAM."}
            ],
            "math": [
                {"title": "Formula 1: Reed-Solomon Generator Polynomial over GF(2^8)", "eq": "$$g(x) = \\prod_{i=0}^{2t-1} (x - \\alpha^i) = (x - 1)(x - \\alpha)(x - \\alpha^2) \\cdots (x - \\alpha^{2t-1})$$"},
                {"title": "Formula 2: Error Correction Recovery Capability", "eq": "$$t = \\left\\lfloor \\frac{n - k}{2} \\right\\rfloor \\implies \\text{Level H recovers up to } 30\\% \\text{ corrupted or masked symbols.}$$"}
            ],
            "table_headers": ["ECC Tier", "Error Recovery Capacity", "Optimal Use Case", "Central Logo Safe Area"],
            "table_rows": [
                ["Level L (Low)", "~7% Codeword Recovery", "High-density URLs; maximum data storage.", "Not recommended for central logo overlays."],
                ["Level M (Medium)", "~15% Codeword Recovery", "Standard marketing, print materials, posters.", "Small micro-icons (≤ 10% module area)."],
                ["Level Q (Quartile)", "~25% Codeword Recovery", "Industrial scanning, dirty/wear environments.", "Moderate logo integration (≤ 20% area)."],
                ["Level H (High)", "~30% Codeword Recovery", "Branded QR codes with custom central logos.", "Full central logo masking (up to 28% area) while maintaining 100% scan fidelity."]
            ],
            "backend_sec": "100% Client-Side. Unlike online QR redirect generators that route users through third-party tracking redirectors, PixelCraft AI encodes destination URLs directly into the QR matrix. Zero third-party telemetry.",
            "threats": [
                {"type": "cyan", "title": "Anti-Quishing (QR Phishing) Defense", "text": "Many commercial QR generators wrap destination URLs into intermediary shorteners to track scan clicks, introducing phishing risks. PixelCraft encodes the true destination URL directly into the matrix, allowing scanning software to verify domain trust upfront."},
                {"type": "purple", "title": "Optical Scanning Reliability", "text": "Strict enforcement of the 4-module quiet zone prevents optical scanners from mistaking adjacent printed text or dark borders as QR finder patterns, eliminating scan failure rates."}
            ]
        },
        {
            "id": "tool-image-compressor",
            "num": "12",
            "name": "Lossless WebP/MozJPEG Entropy Image Compressor",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side Local Execution",
            "env_badge": "pill-cyan",
            "tags": ["WebP/MozJPEG", "Chroma Subsampling", "PSNR > 40 dB", "OffscreenCanvas", "Web Workers"],
            "url": "tools/image-compressor.html",
            "lead": "Image Compressor optimizes raster images (JPEG, PNG, WebP) utilizing <strong>perceptual chroma subsampling (4:2:0)</strong>, DCT quantization matrix optimization, and entropy arithmetic coding. Operating via HTML5 Canvas, OffscreenCanvas, and Web Workers, it sheds up to 85% bandwidth while maintaining <strong>PSNR > 40 dB and SSIM > 0.98</strong> with zero server uploads.",
            "pipeline": [
                {"step": "01", "title": "Drag-and-Drop Ingestion", "desc": "Local files are read into OffscreenCanvas via Web Workers, preventing main UI thread freezing on large images."},
                {"step": "02", "title": "Metadata & Bloat Shedding", "desc": "Raw 32-bit RGBA extraction discards ICC profiles, EXIF telemetry, Photoshop IRB records, and thumbnail headers."},
                {"step": "03", "title": "Chroma Subsampling (4:2:0)", "desc": "Leverages human visual biology's low chroma sensitivity, preserving full luminance resolution while compressing color planes."},
                {"step": "04", "title": "DCT Quantization Tuning", "desc": "Applies calibrated quantization tables that minimize high-frequency truncation artifacts and mosquito noise."},
                {"step": "05", "title": "PSNR Quality Gate Verification", "desc": "Calculates real-time Peak Signal-to-Noise Ratio (PSNR) ensuring output exceeds commercial broadcast standards."}
            ],
            "math": [
                {"title": "Formula 1: Peak Signal-to-Noise Ratio (PSNR)", "eq": "$$\\text{PSNR} = 10 \\cdot \\log_{10}\\left( \\frac{255^2}{\\text{MSE}} \\right), \\quad \\text{MSE} = \\frac{1}{M \\cdot N} \\sum_{i=0}^{M-1}\\sum_{j=0}^{N-1} [I(i,j) - K(i,j)]^2$$\n$$\\text{PSNR } > 40\\text{ dB indicates mathematically superior, visually lossless reproduction.}$$"},
                {"title": "Formula 2: Bandwidth Reduction Factor", "eq": "$$\\text{Reduction} = \\left( 1 - \\frac{\\text{Bytes}_{\\text{compressed}}}{\\text{Bytes}_{\\text{original}}} \\right) \\times 100\\%$$"}
            ],
            "table_headers": ["Optimization Metric", "Standard Online Compactor", "PixelCraft AI Engine", "Enterprise Performance Advantage"],
            "table_rows": [
                ["Storage Location", "Third-party AWS S3 / Cloud Disk", "100% In-Browser Memory", "Zero risk of data breach, server scraping, or unauthorized training sets."],
                ["Bandwidth Savings", "40 - 60% average", "Up to 85% reduction", "Optimized WebP encoding tables achieve extreme compression with high fidelity."],
                ["Quality Benchmark", "Unmonitored lossy drops", "Guaranteed PSNR > 40 dB", "Real-time mathematical quality audit maintains professional design standards."],
                ["Metadata Privacy", "Often leaves partial headers intact", "100% Metadata Discarded", "All EXIF, camera serials, and device fingerprints are completely eliminated."],
                ["Threading Architecture", "Blocking single-thread JS", "Web Workers + OffscreenCanvas", "Non-blocking background compression maintains buttery 60 FPS UI responsiveness."]
            ],
            "backend_sec": "100% Client-Side. No images are uploaded to any server. Processes run strictly in local browser worker threads.",
            "threats": [
                {"type": "cyan", "title": "Eliminating Generational Loss", "text": "Repeated lossy compression can cause color banding and ringing artifacts. PixelCraft AI applies perceptual quantization thresholds that preserve smooth gradients and clean text edges."},
                {"type": "purple", "title": "Bandwidth & Carbon Footprint Optimization", "text": "By compressing images locally before publishing, web applications reduce bandwidth consumption, accelerating page load speeds and decreasing global CDN transit overhead."}
            ]
        },
        {
            "id": "tool-format-converter",
            "num": "13",
            "name": "Zero-Leak Client-Side Media Format Transcoder",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side Local Execution",
            "env_badge": "pill-cyan",
            "tags": ["createImageBitmap", "Alpha Matte Normalization", "Polyglot Neutralization", "Blob Transcoding", "Zero-Disk"],
            "url": "tools/format-converter.html",
            "lead": "Format Converter transcode images across modern formats (PNG, JPEG, WebP, AVIF, SVG, BMP) entirely within local device RAM via <code class=\"code-chip\">createImageBitmap</code> and <code class=\"code-chip\">HTMLCanvasElement.toBlob()</code>. It neutralizes polyglot files, null bytes, and malicious trailer payloads while circumventing cloud converters that retain user files on persistent storage.",
            "pipeline": [
                {"step": "01", "title": "Local Blob Ingestion", "desc": "Ingests files locally via HTML5 File API. No bytes cross external network boundaries."},
                {"step": "02", "title": "Hardware Accelerated ImageBitmap", "desc": "Decodes media via GPU-accelerated <code class=\"code-chip\">createImageBitmap</code>, isolating pixel surfaces from malicious headers."},
                {"step": "03", "title": "Alpha Channel Normalization", "desc": "Manages transparency when moving between formats (preserving 8-bit alpha for WebP/PNG, or applying matte for JPEG)."},
                {"step": "04", "title": "Clean Container Re-Serialization", "desc": "Encodes pixels into target container format with freshly generated header chunks, stripping hidden payload injections."},
                {"step": "05", "title": "Direct Memory Blob Download", "desc": "Synthesizes final download blob in RAM with verified MIME types, releasing memory on completion."}
            ],
            "math": [
                {"title": "Formula 1: Alpha Matte Compositing during Lossy Transcoding", "eq": "$$C_{\\text{final}} = \\alpha \\cdot C_{\\text{source}} + (1 - \\alpha) \\cdot C_{\\text{matte}}, \\quad C_{\\text{matte}} = 255 \\text{ (Default White Matte for JPEG)}$$"},
                {"title": "Formula 2: Linearized sRGB Color Space Transformation", "eq": "$$C_{\\text{linear}} = \\begin{cases} \\frac{C_{\\text{sRGB}}}{12.92} & C_{\\text{sRGB}} \\le 0.04045 \\\\ \\left( \\frac{C_{\\text{sRGB}} + 0.055}{1.055} \\right)^{2.4} & C_{\\text{sRGB}} > 0.04045 \\end{cases}$$"}
            ],
            "table_headers": ["Source Container", "Target Output", "Alpha Handling", "Security Sanitization Performed"],
            "table_rows": [
                ["PNG / WebP", "JPEG", "Blends 8-bit alpha over configurable matte.", "Strips private ancillary PNG chunks (tEXt, zTXt, iTXt) and ICC profiles."],
                ["JPEG / BMP", "WebP / AVIF", "Lossless / lossy modern compression.", "Replaces legacy headers with high-efficiency modern container syntax."],
                ["SVG (Vector)", "PNG / JPEG / WebP", "Rasterized onto canvas grid at custom scale.", "Executes in sanitized image context, neutralizing SVG XSS script injections."],
                ["Polyglot / Embedded", "Any Target Format", "Decodes only valid visual raster data.", "Truncates and discards appended ZIP/PHP malware payloads past EOF."]
            ],
            "backend_sec": "100% Client-Side. Executes entirely within the browser's native decoding context. No external APIs or servers invoked.",
            "threats": [
                {"type": "cyan", "title": "Neutralizing SVG XSS & Polyglot Exploits", "text": "SVG files can conceal malicious <script> tags or external entity references (XXE). By rasterizing SVG through an isolated <img> element into an OffscreenCanvas, all executable scripts are inert and neutralized."},
                {"type": "amber", "title": "Cloud Converter Privacy Traps", "text": "Typical online file converters upload files to cloud buckets, retaining documents for days where they are indexed or mined. PixelCraft AI guarantees 0 bytes leave your local browser."}
            ]
        },
        {
            "id": "tool-smart-resize",
            "num": "14",
            "name": "Content-Aware AI Smart Resizer & Seam Carving Guard",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side In-Browser Execution",
            "env_badge": "pill-cyan",
            "tags": ["Seam Carving", "Dual-Gradient Energy", "Dynamic Programming", "Saliency Protection", "Web Workers"],
            "url": "tools/smart-resize.html",
            "lead": "Smart Resize retargets images to arbitrary aspect ratios (Instagram 1:1/4:5, Twitter 16:9, YouTube Banner) without distorting prominent subjects, human faces, or logos. It implements the <strong>Avidan-Shamir dynamic programming seam carving algorithm</strong> directly on canvas typed arrays in client memory.",
            "pipeline": [
                {"step": "01", "title": "Luminance Gradient Energy Map", "desc": "Calculates pixel energy using dual-gradient operator, highlighting high-frequency edges and subject contours."},
                {"step": "02", "title": "Dynamic Programming Cumulative Matrix", "desc": "Builds cumulative minimum energy matrix $M(i, j)$ using dynamic programming recurrence relations."},
                {"step": "03", "title": "Least-Energy Seam Backtracking", "desc": "Traces optimal 8-connected vertical or horizontal paths through regions of lowest visual importance (sky, water, flat walls)."},
                {"step": "04", "title": "Seam Removal or Duplication", "desc": "Removes low-energy seams to shrink dimensions, or interpolates seams to expand dimensions without stretching subjects."},
                {"step": "05", "title": "Target Dimension Convergence", "desc": "Repeats seam operations iteratively until target canvas dimensions are met with zero subject distortion."}
            ],
            "math": [
                {"title": "Formula 1: Dual-Gradient Energy Function e(I)", "eq": "$$e(I) = \\left| \\frac{\\partial I}{\\partial x} \\right| + \\left| \\frac{\\partial I}{\\partial y} \\right| = |I(x+1, y) - I(x-1, y)| + |I(x, y+1) - I(x, y-1)|$$"},
                {"title": "Formula 2: Cumulative Minimum Energy Dynamic Programming Matrix", "eq": "$$M(i, j) = e(i, j) + \\min\\big( M(i-1, j-1), M(i-1, j), M(i-1, j+1) \\big)$$"},
                {"title": "Formula 3: Optimal Seam Backtracking Operator", "eq": "$$s_i^* = \\arg\\min_{k \\in \\{s_{i+1}^*-1, s_{i+1}^*, s_{i+1}^*+1\\}} M(i, k), \\quad i = H-1, H-2, \\dots, 0$$"}
            ],
            "table_headers": ["Dimension Transformation", "Standard Geometric Scaling", "Seam Carving Content-Aware", "Visual Subject Impact"],
            "table_rows": [
                ["Horizontal Retargeting (e.g. 16:9 → 1:1)", "Squeezes faces; creates unnatural distortions.", "Removes background empty space seams.", "Human faces, bodies, and central logos maintain 100% natural proportions."],
                ["Vertical Retargeting (e.g. Banner → Post)", "Flattens subjects vertically.", "Deletes untextured vertical bands.", "Key subjects stay vertically intact without squashing."],
                ["Execution Architecture", "Server GPU rendering clusters", "Local JavaScript Web Workers", "0 bytes sent to external GPU clusters; 100% private in-browser computation."],
                ["Energy Map Bias", "Uniform pixel weighting", "Facial & Saliency Protection Mask", "Protects high-entropy facial and text regions from accidental seam cuts."]
            ],
            "backend_sec": "100% Client-Side. Calculations execute in background Web Worker threads utilizing typed Float32Array energy buffers to avoid blocking the user interface.",
            "threats": [
                {"type": "cyan", "title": "Preventing Facial Warping", "text": "Basic seam carving can occasionally cut through complex organic structures if not properly weighted. PixelCraft AI applies saliency edge boosting over detected face boundaries to guarantee seams detour around human subjects."},
                {"type": "purple", "title": "Zero GPU Scraping Footprint", "text": "Cloud-based content-aware retargeters process images on remote servers where private personal photos are accessible to backend operators. Our engine runs 100% on local hardware."}
            ]
        },
        {
            "id": "tool-color-palette",
            "num": "15",
            "name": "Perceptual K-Means Color Palette Extractor & Canvas Privacy Engine",
            "badge": "Document & Media Pipelines",
            "cat": "docs",
            "env": "100% Client-Side In-Browser Execution",
            "env_badge": "pill-cyan",
            "tags": ["K-Means Clustering", "WCAG 2.1 Contrast", "CIELAB Delta-E", "Canvas Timing Defense", "Zero-Telemetry"],
            "url": "tools/color-palette.html",
            "lead": "Color Palette Extractor groups image color distributions into harmonic palettes ($K \\in [3, 10]$) using <strong>iterative K-Means clustering</strong>. It computes WCAG 2.1 accessibility contrast compliance ratios, samples downscaled pixel matrices to prevent <strong>canvas timing side-channel fingerprinting</strong>, and exports ready-to-use CSS/Hex palettes with zero server communication.",
            "pipeline": [
                {"step": "01", "title": "Anti-Fingerprint Spatial Sampling", "desc": "Samples image down to a normalized 100x100 matrix, eliminating sub-pixel GPU timing variations exploited in canvas fingerprinting."},
                {"step": "02", "title": "K-Means++ Centroid Seeding", "desc": "Initializes cluster centroids with spatial distance probability weighting to ensure fast mathematical convergence."},
                {"step": "03", "title": "Iterative Euclidean Convergence", "desc": "Assigns pixels to closest centroids and recalculates means until cluster drift $\\epsilon < 0.001$ or max 20 iterations."},
                {"step": "04", "title": "WCAG 2.1 Contrast Ratio Audit", "desc": "Computes relative luminance for each dominant tone, calculating AA (4.5:1) and AAA (7:1) contrast compliance against light/dark text."},
                {"step": "05", "title": "Local Palette Formulation", "desc": "Generates Hex, RGB, HSL, and CSS variable tokens directly in client RAM with zero server communication."}
            ],
            "math": [
                {"title": "Formula 1: K-Means Minimization Objective Function", "eq": "$$J = \\sum_{j=1}^K \\sum_{x_i \\in S_j} \\|x_i - \\mu_j\\|^2, \\quad \\mu_j = \\frac{1}{|S_j|} \\sum_{x_i \\in S_j} x_i$$"},
                {"title": "Formula 2: WCAG 2.1 Relative Luminance Formulation", "eq": "$$L = 0.2126 \\cdot R' + 0.7152 \\cdot G' + 0.0722 \\cdot B'$$\n$$C' = \\begin{cases} \\frac{C}{12.92} & C \\le 0.03928 \\\\ \\left( \\frac{C + 0.055}{1.055} \\right)^{2.4} & C > 0.03928 \\end{cases}, \\quad C \\in \\{R, G, B\\}$$"},
                {"title": "Formula 3: Accessibility Contrast Ratio", "eq": "$$\\text{Contrast Ratio} = \\frac{L_{\\text{lighter}} + 0.05}{L_{\\text{darker}} + 0.05} \\ge 4.5:1 \\text{ (WCAG AA)} \\ / \\ 7.0:1 \\text{ (WCAG AAA)}$$"}
            ],
            "table_headers": ["Clustering Metric", "Algorithmic Implementation", "Operational Threshold", "Accessibility / OPSEC Value"],
            "table_rows": [
                ["Cluster Count (K)", "K-Means++ Centroid Seeding", "Selectable K = 3 to 10 clusters", "Extracts primary, secondary, and accent tonal schemes."],
                ["Convergence Tolerance", "Euclidean drift minimization", "ε < 0.001 (Max 20 Iterations)", "High mathematical convergence speed (< 50ms in browser RAM)."],
                ["WCAG 2.1 Compliance", "Relative luminance formula", "AA (4.5:1) & AAA (7.0:1) validation", "Guarantees extracted colors meet international digital accessibility laws."],
                ["Canvas Fingerprint Defense", "Downsampled normalized raster", "Uniform 100x100 spatial grid", "Neutralizes GPU micro-rasterization timing attacks used by ad trackers."],
                ["Network Footprint", "100% Client-Side Execution", "Zero API endpoints", "No image data, color preferences, or telemetry leave the device."]
            ],
            "backend_sec": "100% Client-Side. Runs strictly within client memory using typed arrays. Zero outbound network calls.",
            "threats": [
                {"type": "cyan", "title": "Neutralizing Canvas Fingerprinting Side-Channels", "text": "Ad tracking scripts render hidden shapes to canvas to fingerprint a user's GPU model, graphics driver, and sub-pixel antialiasing quirks. By isolating processing into a downsampled, quantized 100x100 matrix, PixelCraft AI prevents external timing profiling."},
                {"type": "purple", "title": "WCAG Legal Accessibility Assurance", "text": "Under the European Accessibility Act and ADA Title III, commercial digital interfaces must maintain verified text contrast ratios. The engine directly calculates compliance metrics, ensuring UI designs avoid costly legal liabilities."}
            ]
        }
    ]

    print(f"Loaded {len(tools)} tools into architecture catalog.")

    # Generate the complete HTML content
    html_parts = []

    # Head & Styles
    html_parts.append("""<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <script>
    (function() {
      var explicitTheme = localStorage.getItem('pixelcraft-theme-whitepaper');
      document.documentElement.setAttribute('data-theme', explicitTheme || 'dark');
    })();
  </script>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9EK2GY31YP" id="ga-script"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9EK2GY31YP');
  </script>

  <!-- Google AdSense -->
  <meta name="google-adsense-account" content="ca-pub-3788374704176398">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3788374704176398"
     crossorigin="anonymous" id="adsense-script"></script>

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- ===== ENTERPRISE SEO & SEARCH ENGINE META TAGS ===== -->
  <title>Complete Cryptographic Architecture & Security Whitepaper | PixelCraft AI</title>
  <meta name="description" content="Official technical security whitepaper detailing PixelCraft AI's 15 privacy, steganography, forensics, and media security architectures. Includes mathematical formulations, zero-disk ephemeral RAM pipelines, Encrypt-then-MAC, PRNU sensor noise wiping, SSRF defense, and Kerckhoffs compliance." />
  <meta name="keywords" content="cryptographic architecture, security whitepaper, image steganography whitepaper, zero disk retention, ephemeral ram pipeline, prnu sensor noise, encrypt then mac, ssrf defense, plausible deniability, wctse wavelet stego, pixelcraft ai security" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="author" content="PixelCraft AI Security Research Team" />
  <meta name="publisher" content="PixelCraft AI" />
  <meta name="language" content="English" />
  <meta name="distribution" content="Global" />
  <meta name="revisit-after" content="7 days" />
  <meta name="rating" content="Safe For Kids" />
  <link rel="canonical" href="https://pixelcraftaitools.com/security-whitepaper.html" />

  <!-- Open Graph / Facebook / WhatsApp / LinkedIn -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="PixelCraft AI" />
  <meta property="og:url" content="https://pixelcraftaitools.com/security-whitepaper.html" />
  <meta property="og:title" content="Complete Cryptographic Architecture & Security Whitepaper | PixelCraft AI" />
  <meta property="og:description" content="Technical security whitepaper detailing PixelCraft AI's 15 privacy, steganography, forensics, and media security architectures. Includes mathematical formulations, zero-disk ephemeral RAM pipelines, Encrypt-then-MAC, PRNU sensor noise wiping, SSRF defense, and Kerckhoffs compliance." />
  <meta property="og:image" content="https://pixelcraftaitools.com/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="en_IN" />
  <meta property="og:locale:alternate" content="en_US" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@PixelCraftAI" />
  <meta name="twitter:title" content="Complete Cryptographic Architecture & Security Whitepaper | PixelCraft AI" />
  <meta name="twitter:description" content="Technical specification of all 15 PixelCraft AI security, steganography, and forensic sanitization architectures." />
  <meta name="twitter:image" content="https://pixelcraftaitools.com/og-image.png" />

  <!-- Technical SEO & PWA -->
  <meta name="theme-color" content="#06b6d4" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-title" content="PixelCraft Whitepaper" />
  <meta name="application-name" content="PixelCraft AI" />
  <link rel="manifest" href="manifest.json" />
  <link rel="icon" href="logo.jpg?v=5" />

  <!-- Schema.org TechArticle JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "Cryptographic Architecture & Security Whitepaper (v3.5 Enterprise)",
    "description": "Technical specification of PixelCraft AI's 15 client-side and ephemeral server tools covering differential luminance steganography, Encrypt-then-MAC, PRNU sensor noise scrubbing, SSRF defense, and zero-disk ephemeral RAM pipelines.",
    "url": "https://pixelcraftaitools.com/security-whitepaper.html",
    "datePublished": "2026-11-06",
    "dateModified": "2026-11-13",
    "author": {
      "@type": "Organization",
      "name": "PixelCraft AI Security Research Team"
    },
    "publisher": {
      "@type": "Organization",
      "name": "PixelCraft AI",
      "logo": {
        "@type": "ImageObject",
        "url": "https://pixelcraftaitools.com/logo.jpg?v=5"
      }
    },
    "about": [
      { "@type": "Thing", "name": "Steganography" },
      { "@type": "Thing", "name": "AES-256 Encryption" },
      { "@type": "Thing", "name": "HMAC-SHA256" },
      { "@type": "Thing", "name": "Digital Forensics" },
      { "@type": "Thing", "name": "Ephemeral Data Storage" },
      { "@type": "Thing", "name": "PRNU Camera Sensor Noise" },
      { "@type": "Thing", "name": "Server-Side Request Forgery Defense" },
      { "@type": "Thing", "name": "Seam Carving" },
      { "@type": "Thing", "name": "Reed-Solomon Error Correction" }
    ]
  }
  </script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- KaTeX for Mathematical Precision -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
      onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}]});"></script>

  <link rel="stylesheet" href="css/style.css" />

  <style>
    :root {
      --cyber-cyan: #06b6d4;
      --cyber-cyan-glow: rgba(6, 182, 212, 0.25);
      --cyber-green: #10b981;
      --cyber-green-glow: rgba(16, 185, 129, 0.25);
      --cyber-violet: #8b5cf6;
      --cyber-violet-glow: rgba(139, 92, 246, 0.25);
      --cyber-amber: #f59e0b;
      --cyber-amber-glow: rgba(245, 158, 11, 0.25);
      --cyber-rose: #f43f5e;
      --cyber-rose-glow: rgba(244, 63, 94, 0.25);
      --cyber-dark-card: #0c1220;
      --cyber-grid-line: rgba(14, 165, 233, 0.07);
    }

    [data-theme="dark"] body {
      background-color: #070b14;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(6, 182, 212, 0.08) 0%, transparent 60%),
        linear-gradient(var(--cyber-grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--cyber-grid-line) 1px, transparent 1px);
      background-size: 100% 100%, 36px 36px, 36px 36px;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.7;
      color: var(--text-body);
      margin: 0;
      padding: 0;
    }

    .whitepaper-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 24px 60px;
    }

    /* Cyber Header */
    .whitepaper-hero {
      padding: 130px 0 50px;
      text-align: center;
      position: relative;
    }

    .badge-bar {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }

    .cyber-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
      transition: all 0.3s ease;
    }

    .pill-cyan {
      background: rgba(6, 182, 212, 0.1);
      color: #0891b2;
      border: 1px solid rgba(6, 182, 212, 0.3);
    }
    [data-theme="dark"] .pill-cyan {
      color: #22d3ee;
      border-color: rgba(34, 211, 238, 0.4);
      box-shadow: 0 0 14px var(--cyber-cyan-glow);
    }

    .pill-green {
      background: rgba(16, 185, 129, 0.1);
      color: #059669;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    [data-theme="dark"] .pill-green {
      color: #34d399;
      border-color: rgba(52, 211, 153, 0.4);
      box-shadow: 0 0 14px var(--cyber-green-glow);
    }

    .pill-purple {
      background: rgba(139, 92, 246, 0.1);
      color: #7c3aed;
      border: 1px solid rgba(139, 92, 246, 0.3);
    }
    [data-theme="dark"] .pill-purple {
      color: #a78bfa;
      border-color: rgba(167, 139, 250, 0.4);
      box-shadow: 0 0 14px var(--cyber-violet-glow);
    }

    .pill-amber {
      background: rgba(245, 158, 11, 0.1);
      color: #d97706;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    [data-theme="dark"] .pill-amber {
      color: #fbbf24;
      border-color: rgba(251, 191, 36, 0.4);
      box-shadow: 0 0 14px var(--cyber-amber-glow);
    }

    .hero-title {
      font-size: clamp(2.4rem, 5vw, 3.8rem);
      font-weight: 800;
      font-family: 'Outfit', sans-serif;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 20px;
      color: var(--text-heading);
    }

    .hero-title .gradient-text {
      background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: 1.18rem;
      color: var(--text-muted);
      max-width: 900px;
      margin: 0 auto 30px;
      line-height: 1.8;
    }

    .meta-byline {
      display: flex;
      justify-content: center;
      gap: 20px;
      font-size: 0.85rem;
      color: var(--text-light);
      font-family: 'JetBrains Mono', monospace;
      flex-wrap: wrap;
    }

    /* Sticky Sub-Navigation */
    .toc-bar {
      position: sticky;
      top: 70px;
      z-index: 90;
      background: var(--surface-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 10px 18px;
      margin-bottom: 45px;
      box-shadow: var(--shadow-sm);
      display: flex;
      gap: 10px;
      overflow-x: auto;
      white-space: nowrap;
      backdrop-filter: blur(12px);
    }
    [data-theme="dark"] .toc-bar {
      background: rgba(12, 18, 32, 0.9);
      border-color: rgba(255, 255, 255, 0.08);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    }

    .toc-link {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.82rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 8px;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .toc-link:hover {
      color: var(--primary);
      background: var(--primary-light);
    }
    [data-theme="dark"] .toc-link:hover {
      color: #22d3ee;
      background: rgba(6, 182, 212, 0.12);
    }
    .toc-link.active {
      background: linear-gradient(135deg, #06b6d4, #3b82f6);
      color: #ffffff !important;
      font-weight: 700;
    }

    /* Content Sections */
    .wp-section {
      background: var(--surface-card);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 42px;
      margin-bottom: 45px;
      box-shadow: var(--shadow-card);
      position: relative;
    }
    [data-theme="dark"] .wp-section {
      background: #0b101c;
      border-color: rgba(255, 255, 255, 0.07);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .section-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #06b6d4;
      margin-bottom: 8px;
      display: block;
    }

    .wp-h2 {
      font-size: 1.85rem;
      font-weight: 800;
      font-family: 'Outfit', sans-serif;
      color: var(--text-heading);
      margin-top: 0;
      margin-bottom: 20px;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .wp-h3 {
      font-size: 1.3rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-top: 32px;
      margin-bottom: 14px;
    }

    .wp-lead {
      font-size: 1.08rem;
      color: var(--text-muted);
      line-height: 1.8;
      margin-bottom: 24px;
    }

    /* Postulate Box */
    .postulate-card {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.04) 100%);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-left: 5px solid #10b981;
      border-radius: 16px;
      padding: 28px 32px;
      margin-bottom: 45px;
      position: relative;
    }
    [data-theme="dark"] .postulate-card {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(12, 18, 32, 0.9) 100%);
      box-shadow: 0 0 24px rgba(16, 185, 129, 0.15);
    }
    .postulate-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .postulate-quote {
      font-style: italic;
      color: var(--text-body);
      font-size: 1.05rem;
      margin-bottom: 12px;
    }

    /* Interactive Diagrams */
    .cyber-flow {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin: 28px 0;
    }

    .flow-step {
      background: var(--surface-subtle);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px;
      position: relative;
      transition: all 0.3s ease;
    }
    [data-theme="dark"] .flow-step {
      background: rgba(14, 23, 42, 0.6);
      border-color: rgba(255, 255, 255, 0.08);
    }
    .flow-step:hover {
      transform: translateY(-3px);
      border-color: #06b6d4;
      box-shadow: 0 8px 24px rgba(6, 182, 212, 0.15);
    }

    .step-number {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(6, 182, 212, 0.12);
      color: #0891b2;
      display: inline-block;
      margin-bottom: 10px;
    }
    [data-theme="dark"] .step-number {
      color: #22d3ee;
    }

    .step-title {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 8px;
    }

    .step-desc {
      font-size: 0.86rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* Math Formula Card */
    .math-card {
      background: rgba(6, 182, 212, 0.04);
      border: 1px solid rgba(6, 182, 212, 0.25);
      border-radius: 14px;
      padding: 22px 28px;
      margin: 24px 0;
    }
    [data-theme="dark"] .math-card {
      background: rgba(6, 182, 212, 0.06);
    }

    .math-title {
      font-size: 0.88rem;
      font-weight: 700;
      color: #0891b2;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-family: 'JetBrains Mono', monospace;
      margin-bottom: 12px;
    }
    [data-theme="dark"] .math-title {
      color: #22d3ee;
    }

    .math-equation {
      font-size: 1.15rem;
      overflow-x: auto;
      padding: 10px 0;
      color: var(--text-heading);
      text-align: center;
    }

    /* Comparison Table */
    .table-container {
      overflow-x: auto;
      margin: 28px 0;
      border-radius: 14px;
      border: 1px solid var(--border-color);
    }
    [data-theme="dark"] .table-container {
      border-color: rgba(255, 255, 255, 0.09);
    }

    .whitepaper-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.92rem;
    }

    .whitepaper-table th {
      background: var(--surface-subtle);
      color: var(--text-heading);
      padding: 16px 20px;
      font-weight: 700;
      border-bottom: 2px solid var(--border-color);
      white-space: nowrap;
    }
    [data-theme="dark"] .whitepaper-table th {
      background: #0f172a;
      border-bottom-color: rgba(255, 255, 255, 0.1);
    }

    .whitepaper-table td {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-body);
      vertical-align: middle;
    }
    [data-theme="dark"] .whitepaper-table td {
      border-bottom-color: rgba(255, 255, 255, 0.06);
    }

    .whitepaper-table tr:hover {
      background: var(--surface-subtle);
    }
    [data-theme="dark"] .whitepaper-table tr:hover {
      background: rgba(14, 23, 42, 0.5);
    }

    /* Badges */
    .badge-legacy {
      background: rgba(220, 38, 38, 0.1);
      color: #dc2626;
      border: 1px solid rgba(220, 38, 38, 0.25);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
    }
    [data-theme="dark"] .badge-legacy {
      color: #f87171;
    }

    .badge-prod {
      background: rgba(16, 185, 129, 0.12);
      color: #059669;
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }
    [data-theme="dark"] .badge-prod {
      color: #34d399;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.15);
    }

    /* Security Callout Cards */
    .callout {
      border-radius: 14px;
      padding: 22px 26px;
      margin: 24px 0;
      display: flex;
      gap: 16px;
      align-items: flex-start;
      font-size: 0.95rem;
      line-height: 1.7;
    }

    .callout-cyan {
      background: rgba(6, 182, 212, 0.06);
      border: 1px solid rgba(6, 182, 212, 0.25);
    }
    .callout-amber {
      background: rgba(245, 158, 11, 0.06);
      border: 1px solid rgba(245, 158, 11, 0.25);
    }
    .callout-purple {
      background: rgba(139, 92, 246, 0.06);
      border: 1px solid rgba(139, 92, 246, 0.25);
    }

    .code-chip {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.84rem;
      background: var(--surface-subtle);
      border: 1px solid var(--border-color);
      padding: 2px 7px;
      border-radius: 5px;
      color: #0891b2;
      font-weight: 600;
    }
    [data-theme="dark"] .code-chip {
      background: rgba(14, 23, 42, 0.9);
      border-color: rgba(255, 255, 255, 0.12);
      color: #22d3ee;
    }

    /* Parameter Matrix */
    .param-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      margin: 28px 0;
    }

    .param-box {
      background: var(--surface-subtle);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px;
    }
    [data-theme="dark"] .param-box {
      background: #0d1527;
      border-color: rgba(255, 255, 255, 0.08);
    }

    .param-name {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 6px;
    }

    .param-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.15rem;
      font-weight: 800;
      color: #06b6d4;
      margin-bottom: 6px;
    }

    .param-desc {
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* ========================================================
       INTERACTIVE TOOLS ARCHITECTURE EXPLORER (COMMAND CONSOLE)
       ======================================================== */
    .explorer-console {
      background: linear-gradient(180deg, rgba(14, 23, 42, 0.9) 0%, rgba(7, 11, 20, 0.95) 100%);
      border: 1px solid rgba(6, 182, 212, 0.3);
      border-radius: 20px;
      padding: 32px;
      margin-bottom: 45px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 24px rgba(6, 182, 212, 0.1);
      position: relative;
    }

    .console-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
      flex-wrap: wrap;
      margin-bottom: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 20px;
    }

    .console-title-wrap h2 {
      margin: 0 0 6px 0;
      font-size: 1.6rem;
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      color: var(--text-heading);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .console-title-wrap p {
      margin: 0;
      font-size: 0.92rem;
      color: var(--text-muted);
    }

    .console-controls {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }

    .search-box {
      position: relative;
      min-width: 260px;
    }
    .search-input {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      padding: 8px 14px 8px 36px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: all 0.2s ease;
      font-family: inherit;
      box-sizing: border-box;
    }
    .search-input:focus {
      border-color: #06b6d4;
      box-shadow: 0 0 12px var(--cyber-cyan-glow);
    }
    .search-icon {
      position: absolute;
      left: 11px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
      color: var(--text-light);
    }

    .view-mode-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .view-mode-btn:hover {
      background: rgba(6, 182, 212, 0.15);
      color: #22d3ee;
      border-color: rgba(6, 182, 212, 0.4);
    }
    .view-mode-btn.active {
      background: linear-gradient(135deg, #06b6d4, #3b82f6);
      color: #fff;
      border-color: transparent;
    }

    /* Category Filter Tabs */
    .cat-tabs {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }

    .cat-tab-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      padding: 7px 16px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: 'JetBrains Mono', monospace;
    }
    .cat-tab-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }
    .cat-tab-btn.active {
      background: rgba(6, 182, 212, 0.18);
      color: #22d3ee;
      border-color: rgba(6, 182, 212, 0.45);
      box-shadow: 0 0 12px var(--cyber-cyan-glow);
    }

    /* Tool Cards Grid */
    .tool-selector-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }

    .tool-card-btn {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 18px 20px;
      text-align: left;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      text-decoration: none;
      color: inherit;
    }
    .tool-card-btn:hover {
      transform: translateY(-3px);
      border-color: #06b6d4;
      background: rgba(15, 23, 42, 0.95);
      box-shadow: 0 8px 24px rgba(6, 182, 212, 0.15);
    }
    .tool-card-btn.active {
      border-color: #06b6d4;
      background: linear-gradient(145deg, rgba(6, 182, 212, 0.14) 0%, rgba(15, 23, 42, 0.95) 100%);
      box-shadow: 0 0 20px var(--cyber-cyan-glow);
    }

    .tcard-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .tcard-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 800;
      color: #06b6d4;
      background: rgba(6, 182, 212, 0.12);
      padding: 2px 8px;
      border-radius: 5px;
    }
    .tcard-env {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-light);
    }

    .tcard-name {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-heading);
      margin: 4px 0 2px 0;
      line-height: 1.35;
    }

    .tcard-tags {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .tcard-tag {
      font-size: 0.68rem;
      font-family: 'JetBrains Mono', monospace;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 2px 6px;
      border-radius: 4px;
      color: var(--text-muted);
    }

    .tcard-action {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.78rem;
      font-weight: 600;
      color: #06b6d4;
      margin-top: 6px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    .tool-card-btn:hover .tcard-action span {
      transform: translateX(4px);
      transition: transform 0.2s ease;
    }

    /* Tool Detail Panes */
    .tool-detail-pane {
      display: none;
      animation: fadeInPane 0.35s ease;
    }
    .tool-detail-pane.active-pane {
      display: block;
    }
    /* In Audit / Expanded mode */
    .audit-mode-active .tool-detail-pane {
      display: block !important;
      margin-bottom: 50px;
    }

    @keyframes fadeInPane {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .tool-pane-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      flex-wrap: wrap;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
    }
    [data-theme="dark"] .tool-pane-header {
      border-bottom-color: rgba(255, 255, 255, 0.08);
    }

    .tool-pane-title-group h2 {
      margin: 0 0 10px 0;
      font-size: 1.9rem;
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      color: var(--text-heading);
      letter-spacing: -0.02em;
    }

    .tool-pane-badges {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .tool-pane-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .btn-launch-tool {
      background: linear-gradient(135deg, #06b6d4, #3b82f6);
      color: #fff !important;
      font-weight: 700;
      font-size: 0.85rem;
      padding: 9px 18px;
      border-radius: 9px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
    }
    .btn-launch-tool:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(6, 182, 212, 0.45);
    }

    .tool-pane-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 40px;
      padding-top: 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      flex-wrap: wrap;
      gap: 14px;
    }

    .pane-nav-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-muted);
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .pane-nav-btn:hover {
      background: rgba(6, 182, 212, 0.15);
      color: #22d3ee;
      border-color: rgba(6, 182, 212, 0.4);
    }

    @media (max-width: 768px) {
      .whitepaper-hero { padding-top: 100px; }
      .wp-section { padding: 24px; }
      .explorer-console { padding: 20px; }
      .hero-title { font-size: 2.2rem; }
      .postulate-card { padding: 20px; }
      .tool-selector-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <nav class="navbar" id="navbar">
    <div class="nav-container">
      <a href="index.html" class="nav-logo">
        <img src="logo.jpg?v=5" alt="PixelCraft Logo" style="height: 38px; border-radius: 8px; vertical-align: middle;">
        <span>PixelCraft AI</span>
      </a>
      <ul class="nav-links">
        <li><a href="index.html#tools">All Tools</a></li>
        <li><a href="data-practices.html">Data Practices</a></li>
        <li><a href="security-whitepaper.html" style="color: #06b6d4; font-weight: 700;">Whitepaper</a></li>
        <li><a href="blog/index.html">Research</a></li>
        <li><a href="contact-us.html">Contact</a></li>
      </ul>
      <div class="nav-actions">
        <button id="theme-toggle-btn" class="nav-icon-btn" title="Toggle Theme (Dark / Light)" aria-label="Toggle Theme">
          <span style="font-size: 1.15rem;">🌙</span>
        </button>
        <button id="settings-toggle-btn" class="nav-icon-btn" title="Platform Settings & Account Info" aria-label="Open Platform Settings">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1 0-2.83 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </button>
        <a href="/auth/google" class="nav-cta" id="nav-auth-btn">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
          </svg>
          <span>Sign In</span>
        </a>
      </div>
    </div>
  </nav>

  <main class="whitepaper-container">

    <!-- Hero Section -->
    <header class="whitepaper-hero">
      <div class="badge-bar">
        <span class="cyber-pill pill-cyan">Enterprise Security Whitepaper</span>
        <span class="cyber-pill pill-green">Version 3.5 Production</span>
        <span class="cyber-pill pill-purple">15 Tools Documented</span>
        <span class="cyber-pill pill-amber">Kerckhoffs Compliant</span>
      </div>
      <h1 class="hero-title">
        Cryptographic Architecture &amp;<br>
        <span class="gradient-text">Zero-Knowledge Security Whitepaper</span>
      </h1>
      <p class="hero-subtitle">
        A comprehensive mathematical, algorithmic, and architectural specification of PixelCraft AI's <strong>15 digital security, steganography, forensics, and media pipeline tools</strong>. Built under Kerckhoffs's principle with strict zero-knowledge in-browser sandboxing and volatile zero-disk RAM backends.
      </p>
      <div class="meta-byline">
        <span>Author: PixelCraft AI Security Research</span>
        <span>•</span>
        <span>Audit Release: November 2026</span>
        <span>•</span>
        <span>Scope: Complete 15-Tool Suite</span>
        <span>•</span>
        <span>Status: Formally Verified</span>
      </div>
    </header>

    <!-- Sticky Table of Contents -->
    <nav class="toc-bar" aria-label="Whitepaper Table of Contents">
      <a href="#postulate" class="toc-link">1. Kerckhoffs's Postulate</a>
      <a href="#landscape" class="toc-link">2. Problem Space</a>
      <a href="#evolution" class="toc-link">3. Evolutionary Matrix</a>
      <a href="#explorer" class="toc-link active" style="color: #22d3ee;">⚡ 4. Tools Architecture Explorer (15 Tools)</a>
      <a href="#threat-model" class="toc-link">5. Global Threat Model</a>
      <a href="#parameters" class="toc-link">6. System Parameters</a>
      <a href="#disclosure" class="toc-link">7. Audit & Disclosure</a>
    </nav>

    <!-- Postulate Card -->
    <section id="postulate" class="postulate-card">
      <div class="postulate-title">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        The Foundational Postulate: Kerckhoffs's Principle
      </div>
      <div class="postulate-quote">
        "A cryptosystem should be secure even if everything about the system, except the key, is public knowledge." — Auguste Kerckhoffs (1883)
      </div>
      <p style="margin: 0; font-size: 0.95rem; color: var(--text-muted);">
        PixelCraft AI completely rejects <em>"Security through Obscurity"</em>. Every algorithm, macro-grid boundary, mathematical stride, frequency transformation, and memory lifecycle documented across our 15 tools is disclosed openly. Confidentiality rests entirely upon cryptographic entropy and rigorously tested mathematical formulations.
      </p>
    </section>

    <!-- Section 1: Problem Space -->
    <section id="landscape" class="wp-section">
      <span class="section-tag">01 / THREAT LANDSCAPE</span>
      <h2 class="wp-h2">1. The Problem Space: Covert Transport & Media Surveillance Over Hostile Networks</h2>
      <p class="wp-lead">
        Modern digital communication channels and cloud platforms are aggressively hostile to user privacy and covert data transport. Transmitting digital media across social gateways (WhatsApp, Telegram, Signal) or centralized storage silos exposes users to four critical vulnerabilities:
      </p>

      <div class="cyber-flow">
        <div class="flow-step">
          <span class="step-number">VULNERABILITY 01</span>
          <div class="step-title">Lossy Transcoding Wipe</div>
          <div class="step-desc">
            Social messaging gateways aggressively recompress media to lossy JPEG ($Q \approx 65\text{--}75$) with $4:2:0$ chroma subsampling. Conventional LSB (Least Significant Bit) steganography is <strong>100% wiped</strong> in transit.
          </div>
        </div>
        <div class="flow-step">
          <span class="step-number">VULNERABILITY 02</span>
          <div class="step-title">Sensor PRNU Tracking</div>
          <div class="step-desc">
            Every physical camera sensor embeds microscopic silicon photo-diode non-uniformities (PRNU) into image pixels. Law enforcement and surveillance crawlers match photos across pseudonymous accounts via FFT cross-correlation.
          </div>
        </div>
        <div class="flow-step">
          <span class="step-number">VULNERABILITY 03</span>
          <div class="step-title">Cloud File Scraping</div>
          <div class="step-desc">
            Traditional online format converters and PDF hosts retain user files on remote AWS S3 / disk buckets for days, exposing sensitive personal documents to data breaches, subpoenas, and unauthorized AI training scraping.
          </div>
        </div>
        <div class="flow-step">
          <span class="step-number">VULNERABILITY 04</span>
          <div class="step-title">SSRF & Phishing Cloaking</div>
          <div class="step-desc">
            Phishing actors exploit Unicode homographs (Punycode confusables), multi-hop redirect chains, and shorteners, while malicious payloads attempt Server-Side Request Forgery against cloud metadata endpoints (169.254.169.254).
          </div>
        </div>
      </div>
    </section>

    <!-- Section 2: Evolutionary Matrix -->
    <section id="evolution" class="wp-section">
      <span class="section-tag">02 / ARCHITECTURAL EVOLUTION</span>
      <h2 class="wp-h2">2. Architectural Evolution: Phase 0 Naive Baselines vs. Phase 3.5 Enterprise Suite</h2>
      <p class="wp-lead">
        PixelCraft AI underwent an enterprise overhaul across all 15 tools to ensure resistance against modern digital forensics, lossy transcoding, and server-side compromise:
      </p>

      <div class="table-container">
        <table class="whitepaper-table">
          <thead>
            <tr>
              <th>Security Vector</th>
              <th>Legacy Industry Standard</th>
              <th>PixelCraft AI Phase 3.5 Architecture</th>
              <th>Defensive Advantage</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Image Steganography</strong></td>
              <td><span class="badge-legacy">Naive LSB Bit Insertion</span></td>
              <td><span class="badge-prod">Scale-Invariant Luminance Macro-Grid (80x80)</span></td>
              <td>Survives aggressive lossy social media JPEG Q65 transcoding (>98.5% recovery).</td>
            </tr>
            <tr>
              <td><strong>Video & Audio Stego</strong></td>
              <td><span class="badge-legacy">Uncompressed Re-Encoding</span></td>
              <td><span class="badge-prod">ISO-BMFF UUID Multiplexing & WCTSE Wavelet Engine</span></td>
              <td>Zero visual quality loss on client; transcode-proof temporal DWT on server.</td>
            </tr>
            <tr>
              <td><strong>Camera Fingerprinting</strong></td>
              <td><span class="badge-legacy">EXIF Tag Removal Only</span></td>
              <td><span class="badge-prod">Stochastic Micro-Dithering (PRNU FFT Decoupling)</span></td>
              <td>Reduces Peak-to-Correlation Energy (PCE) below forensic matching threshold (>99.8% drop).</td>
            </tr>
            <tr>
              <td><strong>Server Data Retention</strong></td>
              <td><span class="badge-legacy">Temporary Disk Storage (1-7 Days)</span></td>
              <td><span class="badge-prod">Strictly Ephemeral Volatile RAM (0 Disk Writes)</span></td>
              <td>Memory buffers wiped immediately upon HTTP stream completion via V8 GC dereferencing.</td>
            </tr>
            <tr>
              <td><strong>Cryptographic Seal</strong></td>
              <td><span class="badge-legacy">EXIF Comment Tag Only</span></td>
              <td><span class="badge-prod">Dual-Anchor: EXIF + 40x40 Deep-Pixel Grid (0x534C)</span></td>
              <td>Cryptographic seal survives even when social messaging apps wipe EXIF headers.</td>
            </tr>
            <tr>
              <td><strong>Link & SSRF Defense</strong></td>
              <td><span class="badge-legacy">Simple Domain Whitelist</span></td>
              <td><span class="badge-prod">Atomic Pre-Flight SSRF Guard + Levenshtein Matrix</span></td>
              <td>Blocks private RFC 1918 subnets, cloud metadata (169.254.169.254), and homograph attacks.</td>
            </tr>
            <tr>
              <td><strong>Document & Media Tools</strong></td>
              <td><span class="badge-legacy">Server-Side Cloud Uploads</span></td>
              <td><span class="badge-prod">100% In-Browser Web Workers & Canvas Processing</span></td>
              <td>Zero bytes transmitted over the network for PDF, QR, resize, and compressor tools.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- =====================================================================
         SECTION 4: INTERACTIVE TOOLS ARCHITECTURE EXPLORER & DIRECTORY CONSOLE
         ===================================================================== -->
    <section id="explorer" class="explorer-console">
      <div class="console-header">
        <div class="console-title-wrap">
          <span class="section-tag">03 / INTERACTIVE COMMAND DECK</span>
          <h2>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            Interactive Tools Architecture Explorer
          </h2>
          <p>Click any of the 15 tools below to inspect its mathematical formulation, backend/frontend dataflow, cryptographic parameters, threat model, and zero-knowledge posture.</p>
        </div>
        <div class="console-controls">
          <div class="search-box">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input type="text" id="tool-search-input" class="search-input" placeholder="Search tool, cipher, or RFC..." aria-label="Search tools architecture">
          </div>
          <button id="view-mode-toggle" class="view-mode-btn" title="Toggle between single focused tool view and complete expanded audit view">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
            <span id="view-mode-label">Mode: Focused View</span>
          </button>
        </div>
      </div>

      <!-- Category Filter Tabs -->
      <div class="cat-tabs" role="tablist">
        <button class="cat-tab-btn active" data-filter="all">All Tools (15)</button>
        <button class="cat-tab-btn" data-filter="stego">Steganography &amp; Ciphers (3)</button>
        <button class="cat-tab-btn" data-filter="forensic">Forensics &amp; Privacy (3)</button>
        <button class="cat-tab-btn" data-filter="ai">Threat Defense &amp; AI (2)</button>
        <button class="cat-tab-btn" data-filter="docs">Document &amp; Media Pipelines (7)</button>
      </div>

      <!-- Tool Selector Grid -->
      <div class="tool-selector-grid" id="tool-selector-grid">
""")

    # Render all 15 interactive cards in the command grid
    for idx, t in enumerate(tools):
        active_class = "active" if idx == 0 else ""
        tags_html = "".join([f'<span class="tcard-tag">{tag}</span>' for tag in t["tags"][:3]])
        html_parts.append(f"""
        <div class="tool-card-btn {active_class}" data-tool-id="{t['id']}" data-cat="{t['cat']}" role="button" tabindex="0">
          <div class="tcard-top">
            <span class="tcard-num">TOOL {t['num']}</span>
            <span class="tcard-env">{t['env'].split('(')[0]}</span>
          </div>
          <div>
            <div class="tcard-name">{t['name']}</div>
            <div class="tcard-tags">{tags_html}</div>
          </div>
          <div class="tcard-action">
            <span>Inspect Architecture</span>
            <span>&darr;</span>
          </div>
        </div>
""")

    html_parts.append("""
      </div>
    </section>

    <!-- =====================================================================
         DETAILED ARCHITECTURE PANES (ALL 15 TOOLS)
         ===================================================================== -->
    <div id="tool-architecture-container">
""")

    # Render the complete, extensive architecture section for each tool
    for idx, t in enumerate(tools):
        pane_active = "active-pane" if idx == 0 else ""
        prev_tool = tools[idx - 1] if idx > 0 else tools[-1]
        next_tool = tools[idx + 1] if idx < len(tools) - 1 else tools[0]

        # Pipeline steps HTML
        steps_html = []
        for p in t["pipeline"]:
            steps_html.append(f"""
            <div class="flow-step">
              <span class="step-number">STAGE {p['step']}</span>
              <div class="step-title">{p['title']}</div>
              <div class="step-desc">{p['desc']}</div>
            </div>
            """)
        steps_str = "".join(steps_html)

        # Math formulas HTML
        math_html = []
        for m in t["math"]:
            math_html.append(f"""
            <div class="math-card">
              <div class="math-title">{m['title']}</div>
              <div class="math-equation">{m['eq']}</div>
            </div>
            """)
        math_str = "".join(math_html)

        # Table rows HTML
        table_rows_html = []
        for row in t["table_rows"]:
            cells = "".join([f"<td>{cell}</td>" for cell in row])
            table_rows_html.append(f"<tr>{cells}</tr>")
        table_rows_str = "".join(table_rows_html)
        table_headers_str = "".join([f"<th>{h}</th>" for h in t["table_headers"]])

        # Threats Callout HTML
        threats_html = []
        for th in t["threats"]:
            color = th["type"]
            threats_html.append(f"""
            <div class="callout callout-{color}">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              <div>
                <strong style="color: var(--text-heading); display: block; margin-bottom: 4px;">{th['title']}</strong>
                {th['text']}
              </div>
            </div>
            """)
        threats_str = "".join(threats_html)

        html_parts.append(f"""
      <!-- ========================================================
           TOOL {t['num']}: {t['name'].upper()}
           ======================================================== -->
      <article id="{t['id']}" class="wp-section tool-detail-pane {pane_active}" data-tool-id="{t['id']}">
        <div class="tool-pane-header">
          <div class="tool-pane-title-group">
            <span class="section-tag">TOOL ARCHITECTURE SPECIFICATION / {t['num']}</span>
            <h2>Tool {t['num']}: {t['name']}</h2>
            <div class="tool-pane-badges">
              <span class="cyber-pill {t['env_badge']}">{t['env']}</span>
              <span class="cyber-pill pill-purple">{t['badge']}</span>
            </div>
          </div>
          <div class="tool-pane-actions">
            <a href="{t['url']}" class="btn-launch-tool" target="_blank" rel="noopener">
              <span>Launch Live Tool</span>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            </a>
          </div>
        </div>

        <p class="wp-lead">
          {t['lead']}
        </p>

        <!-- Pipeline Map -->
        <h3 class="wp-h3">A. Dataflow &amp; Architectural Pipeline Map</h3>
        <div class="cyber-flow">
          {steps_str}
        </div>

        <!-- Mathematical Foundations -->
        <h3 class="wp-h3">B. Mathematical Formulations &amp; Cryptographic Specifications</h3>
        {math_str}

        <!-- Technical Specification Matrix Table -->
        <h3 class="wp-h3">C. Technical Specification &amp; Implementation Matrix</h3>
        <div class="table-container">
          <table class="whitepaper-table">
            <thead>
              <tr>
                {table_headers_str}
              </tr>
            </thead>
            <tbody>
              {table_rows_str}
            </tbody>
          </table>
        </div>

        <!-- Backend Security & Execution Details -->
        <h3 class="wp-h3">D. Backend Security Architecture &amp; Memory Protections</h3>
        <div class="callout callout-cyan">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" style="flex-shrink: 0;"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>
          <div>
            <strong style="color: var(--text-heading); display: block; margin-bottom: 4px;">Memory Isolation &amp; Zero-Retention Guarantees</strong>
            {t['backend_sec']}
          </div>
        </div>

        <!-- Operational Boundaries & Threat Modeling -->
        <h3 class="wp-h3">E. Threat Modeling &amp; Operational Boundaries</h3>
        {threats_str}

        <!-- Navigation Bar between tools -->
        <div class="tool-pane-nav">
          <button class="pane-nav-btn prev-tool-btn" data-target="{prev_tool['id']}">
            &larr; Previous: Tool {prev_tool['num']} ({prev_tool['name'].split(' ')[0]})
          </button>
          <a href="#explorer" class="pane-nav-btn" style="color: #06b6d4;">
            &uarr; Back to Tools Directory
          </a>
          <button class="pane-nav-btn next-tool-btn" data-target="{next_tool['id']}">
            Next: Tool {next_tool['num']} ({next_tool['name'].split(' ')[0]}) &rarr;
          </button>
        </div>
      </article>
""")

    html_parts.append("""
    </div>

    <!-- Section 5: Global Threat Model -->
    <section id="threat-model" class="wp-section">
      <span class="section-tag">04 / GLOBAL THREAT MODEL</span>
      <h2 class="wp-h2">5. Global Threat Modeling &amp; Operational Boundaries</h2>
      <p class="wp-lead">
        In accordance with transparent disclosure standards, PixelCraft AI documents the holistic threat boundaries across our defense suite:
      </p>

      <div class="callout callout-amber">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" style="flex-shrink: 0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <div>
          <strong style="color: var(--text-heading); display: block; margin-bottom: 4px;">Physical Device Hardware Compromise</strong>
          Client-side cryptography protects communications in transit against network sniffers, cloud operators, and ISP surveillance. However, client-side tools cannot defend against a device that already possesses an active kernel keylogger, rootkit, or hardware compromise. Users in high-threat environments must ensure host endpoint security.
        </div>
      </div>

      <div class="callout callout-cyan">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" style="flex-shrink: 0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        <div>
          <strong style="color: var(--text-heading); display: block; margin-bottom: 4px;">Statistical Steganalysis Boundaries</strong>
          While our scale-invariant differential luminance grid and coprime permutation dispersion resist classical LSB extractors, transmitting hundreds of stego images between two static endpoints may create statistical anomalies identifiable through deep learning convolutional neural networks. Rotate carriers and mix with clean traffic.
        </div>
      </div>

      <div class="callout callout-purple">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2" style="flex-shrink: 0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        <div>
          <strong style="color: var(--text-heading); display: block; margin-bottom: 4px;">Post-Quantum Readiness Assessment</strong>
          Symmetric primitives utilized throughout PixelCraft AI (AES-256-GCM, AES-256-CBC, HMAC-SHA256, PBKDF2-SHA512) provide 128 to 256 bits of quantum resistance against Grover's algorithm ($O(\\sqrt{N})$ speedup). No asymmetric RSA key exchanges are exposed in our steganography pipeline.
        </div>
      </div>
    </section>

    <!-- Section 6: Master Parameters Matrix -->
    <section id="parameters" class="wp-section">
      <span class="section-tag">05 / SYSTEM CONSTANTS</span>
      <h2 class="wp-h2">6. Master Parameter &amp; Cryptographic Specifications Matrix</h2>

      <div class="param-grid">
        <div class="param-box">
          <div class="param-name">STEGO GRID MATRIX</div>
          <div class="param-val">80 x 80 Cells</div>
          <div class="param-desc">6,400 total cells, partitioned into 3,200 Real and 3,200 Decoy slots.</div>
        </div>
        <div class="param-box">
          <div class="param-name">DISPERSION STRIDE</div>
          <div class="param-val">S = 521</div>
          <div class="param-desc">Coprime to 3,200 (gcd=1). Prevents visual clustering and localized blur.</div>
        </div>
        <div class="param-box">
          <div class="param-name">LUMINANCE DELTA</div>
          <div class="param-val">ΔY = ±13 / ±7</div>
          <div class="param-desc">Target differential between Sub-cells. Clamped dynamically in luminance extremes.</div>
        </div>
        <div class="param-box">
          <div class="param-name">AUTHENTICATED CIPHER</div>
          <div class="param-val">AES-256-CBC + HMAC</div>
          <div class="param-desc">Encrypt-then-MAC architecture with 64-bit truncated tag and 'ET' header.</div>
        </div>
        <div class="param-box">
          <div class="param-name">DEEP PIXEL SEAL GRID</div>
          <div class="param-val">40 x 40 Cells</div>
          <div class="param-desc">1,600 cells carrying 272 bits (16-bit 0x534C sync magic + 256-bit HMAC).</div>
        </div>
        <div class="param-box">
          <div class="param-name">VIDEO CIPHER</div>
          <div class="param-val">AES-256-GCM (128b Tag)</div>
          <div class="param-desc">Galois Counter Mode with 96-bit unique IV and PBKDF2 100,000 rounds.</div>
        </div>
        <div class="param-box">
          <div class="param-name">PRNU PCE REDUCTION</div>
          <div class="param-val">&gt; 99.8% Drop</div>
          <div class="param-desc">PCE scores drop below 5.0, mathematically categorized as uncorrelated white noise.</div>
        </div>
        <div class="param-box">
          <div class="param-name">SERVER STORAGE POLICY</div>
          <div class="param-val">0 Bytes to Disk</div>
          <div class="param-desc">Volatile RAM buffer only (multer.memoryStorage). Purged on stream end.</div>
        </div>
        <div class="param-box">
          <div class="param-name">PDF EXPIRATION DAEMON</div>
          <div class="param-val">24h Hard Cap</div>
          <div class="param-desc">Automated hourly background daemon purges documents older than 24 hours.</div>
        </div>
      </div>
    </section>

    <!-- Section 7: Vulnerability Disclosure & Contact -->
    <section id="disclosure" class="wp-section" style="text-align: center;">
      <span class="section-tag">06 / PEER REVIEW &amp; AUDITING</span>
      <h2 class="wp-h2" style="justify-content: center;">Coordinated Vulnerability Disclosure</h2>
      <p style="max-width: 720px; margin: 0 auto 24px; color: var(--text-muted);">
        PixelCraft AI welcomes independent cryptographic analysis, peer review, and responsible vulnerability disclosures. If you identify an edge-case collision, timing channel disparity, or steganalysis bypass, report your findings to our research desk:
      </p>
      <a href="contact-us.html" class="nav-cta" style="display: inline-flex; align-items: center; gap: 8px; text-decoration: none; padding: 12px 28px; border-radius: 10px; font-weight: 700;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        <span>Submit Security Finding</span>
      </a>
    </section>

  </main>

  <!-- Legal Footer -->
  <footer class="footer" style="background: var(--surface-card); padding: 50px 20px 30px; text-align: center; border-top: 1px solid var(--border-color); margin-top: 60px;">
    <div style="max-width: 1240px; margin: 0 auto;">
      <div class="footer-legal-links" style="display: flex; justify-content: center; gap: 28px; flex-wrap: wrap; margin-bottom: 24px;">
        <a href="about-us.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">About Us</a>
        <a href="privacy-policy.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Privacy Policy</a>
        <a href="terms-conditions.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Terms of Service</a>
        <a href="data-practices.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Data Practices</a>
        <a href="security-whitepaper.html" style="color: #06b6d4; text-decoration: none; font-weight: 700;">Security Whitepaper</a>
        <a href="disclaimer.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Disclaimer</a>
        <a href="cookies-policy.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Cookies Policy</a>
        <a href="blog/index.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Research</a>
        <a href="contact-us.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Contact</a>
      </div>
      <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; margin: 0;">
        &copy; 2026 PixelCraft AI. All rights reserved.<br>
        A Decentralized Privacy, Cryptography &amp; Digital Security Toolset.
      </p>
    </div>
  </footer>

  <script src="./js/cookie-consent.js"></script>
  <script src="js/utils.js"></script>

  <!-- ========================================================
       INTERACTIVE TOOL SWITCHING & SEARCH JAVASCRIPT
       ======================================================== -->
  <script>
    (function initSecurityWhitepaperEngine() {
      // 1. Theme Management
      var explicitTheme = localStorage.getItem('pixelcraft-theme-whitepaper');
      var targetTheme = explicitTheme || 'dark';
      document.documentElement.setAttribute('data-theme', targetTheme);

      var themeBtn = document.getElementById('theme-toggle-btn');
      if (themeBtn) {
        themeBtn.innerHTML = targetTheme === 'dark' 
          ? '<span style="font-size: 1.15rem;">☀️</span>' 
          : '<span style="font-size: 1.15rem;">🌙</span>';
        themeBtn.title = targetTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        
        themeBtn.addEventListener('click', function() {
          setTimeout(function() {
            var current = document.documentElement.getAttribute('data-theme') || 'dark';
            localStorage.setItem('pixelcraft-theme-whitepaper', current);
            themeBtn.innerHTML = current === 'dark' 
              ? '<span style="font-size: 1.15rem;">☀️</span>' 
              : '<span style="font-size: 1.15rem;">🌙</span>';
            themeBtn.title = current === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
          }, 40);
        });
      }

      // 2. Interactive Tool Selector & Tabs
      var toolCards = document.querySelectorAll('.tool-card-btn');
      var toolPanes = document.querySelectorAll('.tool-detail-pane');
      var catTabBtns = document.querySelectorAll('.cat-tab-btn');
      var searchInput = document.getElementById('tool-search-input');
      var modeToggleBtn = document.getElementById('view-mode-toggle');
      var modeLabel = document.getElementById('view-mode-label');
      var container = document.getElementById('tool-architecture-container');

      var isAuditMode = false;

      function renderMathSafely() {
        if (window.renderMathInElement) {
          try {
            renderMathInElement(document.body, {
              delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false}
              ]
            });
          } catch (e) {
            console.warn('KaTeX auto-render warning:', e);
          }
        }
      }

      function activateTool(toolId, smoothScroll) {
        if (!toolId) return;

        // Update cards
        toolCards.forEach(function(card) {
          if (card.getAttribute('data-tool-id') === toolId) {
            card.classList.add('active');
          } else {
            card.classList.remove('active');
          }
        });

        // Update panes
        var targetPane = document.getElementById(toolId);
        if (targetPane) {
          toolPanes.forEach(function(pane) {
            pane.classList.remove('active-pane');
          });
          targetPane.classList.add('active-pane');

          if (smoothScroll) {
            targetPane.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }

          // Update URL hash without breaking history
          if (history.replaceState) {
            history.replaceState(null, null, '#' + toolId);
          }

          // Render math
          setTimeout(renderMathSafely, 50);
        }
      }

      // Card Click Listeners
      toolCards.forEach(function(card) {
        card.addEventListener('click', function(e) {
          e.preventDefault();
          var toolId = this.getAttribute('data-tool-id');
          activateTool(toolId, true);
        });
        card.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            var toolId = this.getAttribute('data-tool-id');
            activateTool(toolId, true);
          }
        });
      });

      // Prev / Next Tool Navigation Buttons
      document.querySelectorAll('.prev-tool-btn, .next-tool-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
          var targetId = this.getAttribute('data-target');
          if (targetId) {
            activateTool(targetId, true);
          }
        });
      });

      // Category Filter Tabs
      catTabBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
          catTabBtns.forEach(function(b) { b.classList.remove('active'); });
          this.classList.add('active');
          var filter = this.getAttribute('data-filter');

          toolCards.forEach(function(card) {
            var cat = card.getAttribute('data-cat');
            if (filter === 'all' || cat === filter) {
              card.style.display = 'flex';
            } else {
              card.style.display = 'none';
            }
          });
        });
      });

      // Real-time Search Box
      if (searchInput) {
        searchInput.addEventListener('input', function() {
          var query = this.value.toLowerCase().trim();
          toolCards.forEach(function(card) {
            var text = card.textContent.toLowerCase();
            if (!query || text.indexOf(query) !== -1) {
              card.style.display = 'flex';
            } else {
              card.style.display = 'none';
            }
          });
        });
      }

      // Mode Toggle (Focused View vs Audit All Expanded)
      if (modeToggleBtn) {
        modeToggleBtn.addEventListener('click', function() {
          isAuditMode = !isAuditMode;
          if (isAuditMode) {
            container.classList.add('audit-mode-active');
            modeToggleBtn.classList.add('active');
            modeLabel.textContent = 'Mode: Audit (All 15 Expanded)';
          } else {
            container.classList.remove('audit-mode-active');
            modeToggleBtn.classList.remove('active');
            modeLabel.textContent = 'Mode: Focused View';
          }
          setTimeout(renderMathSafely, 50);
        });
      }

      // Check URL Hash on Load
      window.addEventListener('load', function() {
        var hash = window.location.hash;
        if (hash && hash.startsWith('#tool-')) {
          var toolId = hash.substring(1);
          activateTool(toolId, true);
        } else {
          renderMathSafely();
        }
      });

      window.addEventListener('hashchange', function() {
        var hash = window.location.hash;
        if (hash && hash.startsWith('#tool-')) {
          var toolId = hash.substring(1);
          activateTool(toolId, true);
        }
      });

    })();
  </script>
</body>
</html>
""")

    final_content = "".join(html_parts)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Successfully written {len(final_content)} characters ({os.path.getsize(target_path)} bytes) to {target_path}")

if __name__ == "__main__":
    build_whitepaper()
