# PixelCraft AI — Privacy & Data Processing Inventory
**Document Version:** 1.0.0  
**Effective Date:** October 11, 2026  
**Classification:** Technical Source of Truth  
**Repository Branch:** `feature/advanced-cicd`

---

## 1. Scope & Verification Standards

This document establishes the technical source of truth for all data collection, browser versus server processing boundaries, storage mechanisms, retention schedules, and external third-party data transfers across the PixelCraft AI platform.

### Evidence Classification Legend
Every statement and behavior in this inventory is categorized into one of the following evidence tiers:
* **`[VERIFIED IN CODE]`**: Inspected directly in the local application source code with exact file and line references.
* **`[VERIFIED BY TEST]`**: Validated through programmatic unit/integration tests running against the actual codebase.
* **`[VERIFIED IN PRODUCTION]`**: Validated in a deployed production environment (e.g., live cloud database indexes, DNS, SSL termination).
* **`[PARTIALLY VERIFIED]`**: Partially supported by code, but subject to operational latency, schedule intervals, or external factors.
* **`[EXTERNAL PROVIDER PRACTICE]`**: Data handling governed by a third party's external privacy policy and terms.
* **`[UNVERIFIED]`**: Behavior depends on runtime environment variables or external infrastructure that cannot be inspected locally.

---

## 2. Tool-by-Tool Technical Inventory

### 2.1 Core Client-Side Utilities (Zero Server Upload)

The following tools execute **100% within the client browser's local sandbox**. No file bytes, image pixel arrays, or decrypted text payloads are transmitted across the network to PixelCraft AI servers or any third-party infrastructure.

| Tool Name | Source File | Technologies Used | Network Transmissions | Storage Medium | Retention & Cleanup | Evidence Tier |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Image Compressor** | `public/tools/image-compressor.html` | HTML5 Canvas, `canvas.toBlob()`, FileReader | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Image Filters** | `public/tools/image-filters.html` | Canvas 2D Context, CSS image-rendering | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Watermark Adder** | `public/tools/watermark-adder.html` | Canvas 2D Context, Font API | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Format Converter** | `public/tools/format-converter.html` | Canvas image encoders (JPEG, PNG, WebP) | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Smart Resize** | `public/tools/smart-resize.html` | Canvas dynamic aspect-ratio scaling | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **EXIF Viewer** | `public/tools/exif-viewer.html` | `exif-js` client-side binary parser | Optional link to Google Maps if user clicks coords | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Digital Fingerprint Wiper** | `public/tools/digital-fingerprint-wiper.html` | Canvas re-rasterization, `piexif.js`, QIM algorithm | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Audio Steganography** | `public/tools/audio-steganography.html` | Web Audio API, AudioBuffer LSB, CryptoJS AES-256 | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Decoy Steganography** | `public/tools/advanced-decoy.html` | Canvas ImageData LSB, CryptoJS AES-256 | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |
| **Images to PDF** | `public/tools/images-to-pdf.html` | `jspdf` browser bundle | None (0 requests) | Browser volatile RAM | Discarded on tab close/reload | `[VERIFIED IN CODE]` |

---

### 2.2 Server-Assisted & Network-Active Tools

The following tools transmit data to the PixelCraft AI backend server or third-party cloud APIs to perform operations that cannot be completed within browser JavaScript alone.

#### Tool: PDF to Link (`public/tools/pdf-to-link.html`)
* **Endpoint:** `POST /api/upload-pdf` (`server.js:L1345-1353`) `[VERIFIED IN CODE]`
* **Data Collected:** User-uploaded PDF document (max 50MB).
* **Storage Location:** Persistent server disk storage at `public/uploads/pdf/<shortId>.pdf`. `[VERIFIED IN CODE]`
* **Public Access:** File is accessible to anyone possessing the short link (`/p/:id`). `[VERIFIED IN CODE]`
* **Retention Mechanism:** Evaluated by `cleanupExpiredPdfs(maxAgeMs = 24 * 60 * 60 * 1000)` (`server.js:L1356-1385`). Files with `now - stats.mtimeMs > 24 hours` are unlinked with `fs.promises.unlink()`. `[VERIFIED IN CODE]`
* **Cleanup Schedule:** Runs once on server startup, and once every 60 minutes thereafter via `setInterval(..., 60 * 60 * 1000)`. `[VERIFIED IN CODE]`
* **Deletion Limitations & Exceptions:** `[PARTIALLY VERIFIED]`
  1. Because sweeps run hourly, an expired file may remain on disk for up to 24 hours and 59 minutes before the next scheduled pass.
  2. If the hosting container goes to sleep (e.g. Render inactivity spin-down), scheduled ticks pause until the server restarts.
  3. Operating system file locks (`EBUSY`) defer deletion to subsequent sweeps.
* **Third-Party Transfers:** None. `[VERIFIED IN CODE]`
* **Authentication Required:** No. `[VERIFIED IN CODE]`

#### Tool: AI Audio & Video Dubbing (`public/tools/ai-dubbing.html`)
* **Endpoint:** `POST /api/dub-media` (`server.js:L799-960`) `[VERIFIED IN CODE]`
* **Data Collected:** Audio or video file (max 20MB) + target language string.
* **Storage Location:**
  * In-memory buffer via `multer.memoryStorage()`. `[VERIFIED IN CODE]`
  * Ephemeral temp files in `os.tmpdir()` (`tempVideoPath`, `tempAudioPath`, `outputVideoPath`) for FFmpeg extraction and remuxing. `[VERIFIED IN CODE]`
* **Retention Mechanism:** Temporary files are **unlinked immediately** in `finally` blocks (`fs.unlinkSync()`) as soon as the response is returned. **Files are not stored for 24 hours.** `[VERIFIED IN CODE]`
* **Third-Party Recipients:**
  1. **Groq Inc. (USA):** Receives audio binary buffer for Whisper speech-to-text (`whisper-large-v3`) and transcript text for translation (`qwen/qwen3.8-27b`). `[VERIFIED IN CODE]`
  2. **Google TTS:** Receives translated text string chunks to generate synthesized speech base64 data. `[VERIFIED IN CODE]`
* **Deletion Limitations & Exceptions:** Unhandled container termination or power failures during FFmpeg processing could leave temp files in `os.tmpdir()` until OS boot cleanup. `[PARTIALLY VERIFIED]`
* **Authentication Required:** No. `[VERIFIED IN CODE]`

#### Tool: Forensic Image Sanitizer (`public/tools/forensic-sanitizer.html`)
* **Endpoints:** `POST /api/tools/forensic-sanitize` and `POST /api/tools/verify-seal` (`server.js:L1762-1887`) `[VERIFIED IN CODE]`
* **Data Collected:** Raw user image file uploaded via multipart `FormData`.
* **Storage Location:** Server volatile memory (`multer.memoryStorage()`). Processed via `Sharp` and `ExifReader`. `[VERIFIED IN CODE]`
* **Retention Mechanism:** In-memory request lifecycle only. Sanitized output returned as base64 JPEG/PNG. Never written to server disk. `[VERIFIED IN CODE]`
* **Third-Party Transfers:** None. `[VERIFIED IN CODE]`
* **Deletion Limitations & Exceptions:** Memory buffer dereferenced by Node.js garbage collection upon response completion. `[VERIFIED IN CODE]`
* **Authentication Required:** No. `[VERIFIED IN CODE]`

#### Tool: Phishing & Threat Link Scanner (`public/tools/phishing-scanner.html`)
* **Endpoint:** `POST /api/scan-link` (`server.js:L1210-1275`) `[VERIFIED IN CODE]`
* **Data Collected:** Target URL string submitted by user.
* **Storage Location:** In-memory processing buffer. Not written to database or persistent disk. `[VERIFIED IN CODE]`
* **Processing Workflow:** Backend runs regex heuristics for homograph punycode, typosquatting, raw IP routing, and TLD reputation. URL shorteners are unmasked via `fetch(target, { method: 'HEAD' })`. `[VERIFIED IN CODE]`
* **Third-Party Recipients:** If `process.env.HF_API_KEY` is present, the URL and heuristic score are sent to **Hugging Face Inference API** for contextual threat analysis. `[VERIFIED IN CODE]`
* **Retention Mechanism:** Ephemeral; discarded upon response delivery. `[VERIFIED IN CODE]`
* **Authentication Required:** No. `[VERIFIED IN CODE]`

#### Tool: Advanced QR Generator — 3D AI Feature (`public/tools/qr-generator.html`)
* **Standard QR Mode:** 100% Client-side browser execution via `qr-code-styling.js`. Zero network traffic. `[VERIFIED IN CODE]`
* **3D AI Feature Mode:** When user clicks "Generate 3D AI Background", text prompt is posted to `POST /api/generate-image` (`server.js:L986-1021`). `[VERIFIED IN CODE]`
* **Third-Party Recipients:** Prompt is transmitted to **Hugging Face Inference API** (`models/stabilityai/stable-diffusion-xl-base-1.0`). `[VERIFIED IN CODE]`
* **Storage Location:** Server memory during proxying. Response delivered as base64 image data URL. `[VERIFIED IN CODE]`
* **Retention Mechanism:** Ephemeral on PixelCraft server. Discarded immediately. `[VERIFIED IN CODE]`
* **Authentication Required:** No. `[VERIFIED IN CODE]`

---

## 3. User Accounts, Sessions & Security Logging

### 3.1 User Authentication (`models/User.js` & `server.js`)
* **Provider:** Google OAuth 2.0 via Passport.js (`server.js:L319-350`). `[VERIFIED IN CODE]`
* **Persisted Fields:**
  * `googleId`: Unique Google identifier string.
  * `name`: Profile display name.
  * `email`: Primary account email address.
  * `avatar`: Public Google profile photo URL.
  * `toolsUsedCount`: Integer counter.
  * `loginCount`: Integer counter.
  * `createdAt`, `lastLogin`: Timestamps.
  * `isBanned`, `banUntil`, `banReason`: Security controls.
  * `toolUsageHistory`: Array of `{ toolName, usedAt, durationSeconds }`.
* **Fields NEVER Persisted:** Passwords, Google OAuth `accessToken`, Google OAuth `refreshToken`. `[VERIFIED IN CODE]`
* **Session Cookie:** `connect.sid`. Configured with `maxAge: 30 * 24 * 60 * 60 * 1000` (**30 Days rolling persistent cookie**) in `server.js:L36` and backed by MongoDB `connect-mongo`. `[VERIFIED IN CODE]`
* **Logout Destruction:** `GET /logout` and `GET /auth/switch-account` call `req.logout()`, `req.session.destroy()`, and `res.clearCookie('connect.sid')`. `[VERIFIED IN CODE]`
* **Account Deletion:** Administrative endpoint `POST /api/admin/delete-user` calls `User.findByIdAndDelete(userId)`. Self-service deletion is handled via contact form request within 30 days. `[VERIFIED IN CODE]`

### 3.2 Security Honeypots & Active Defense Logs (`models/TrapLog.js`)
* **Trigger:** Traps requests containing canary API keys or decoy credentials via `middlewares/honeytokenTrap.js`. `[VERIFIED IN CODE]`
* **Persisted Fields:** `tokenId`, `ipAddress`, `location`, `isp`, `userAgent`, `method`, `endpoint`, `payloadSent`, `timestamp`, `expiresAt`, `legalHold`, `legalHoldReason`. `[VERIFIED IN CODE]`
* **Data Sanitization:** Keys matching `/password|pass|secret|token|key|auth|cookie|session|credential|admin/i` are redacted to `[REDACTED]`. Strings exceeding 500 characters are truncated. `[VERIFIED IN CODE]`
* **Third-Party Transmissions:**
  * Attacker IP is queried against `http://ip-api.com/json/{ip}` over HTTP for OSINT location/ISP. `[VERIFIED IN CODE]`
  * Notification with masked IP (`.xxx.xxx`) is sent to administrator via Telegram Bot API. `[VERIFIED IN CODE]`
* **Retention Schedule:** **180 Days** default rolling window per Indian CERT-In Direction 2(iv). Enforced by MongoDB TTL index on `expiresAt`. `[VERIFIED IN CODE]` & `[VERIFIED BY TEST]`
* **Legal Hold Exception:** When `legalHold: true`, `expiresAt` is set to `null`, suspending TTL auto-deletion during active investigations. `[VERIFIED IN CODE]` & `[VERIFIED BY TEST]`

---

## 4. Cookies & Consent Management (`public/js/cookie-consent.js`)

* **Essential Cookies:**
  * `connect.sid`: HTTP-only session cookie for authenticated Google login. Duration: **30 Days (Rolling)**. `[VERIFIED IN CODE]`
  * `localStorage.cookieConsent`: Stores `'accepted'` or `'rejected'`. Duration: Persistent in browser local storage. `[VERIFIED IN CODE]`
  * `localStorage.pc_consent_v1`: Stores `'true'` or `'false'`. Duration: Persistent in browser local storage. `[VERIFIED IN CODE]`
* **Analytics Cookies (Optional):**
  * `_ga`, `_gid`, `_ga_*`: Google Analytics (ID: `G-V78ZLHJLR8`). Blocked until user clicks "Accept All". `[VERIFIED IN CODE]`
* **Advertising Cookies (Optional):**
  * `__gads`, `__gpi`: Google AdSense (Client: `ca-pub-3788374704176398`). Blocked until user clicks "Accept All". `[VERIFIED IN CODE]`

---

## 5. Third-Party Provider Data Matrix

| Provider | Purpose | Data Transmitted | Legal Basis / Policy Reference |
| :--- | :--- | :--- | :--- |
| **Groq Inc. (USA)** | Whisper Audio Transcription & LLM Translation | Raw audio media stream and transcript text strings | User consent upon initiating AI Dubbing `[EXTERNAL PROVIDER PRACTICE]` |
| **Google LLC (USA)** | Text-to-Speech (Google TTS API) | Translated text strings | User consent upon initiating AI Dubbing `[EXTERNAL PROVIDER PRACTICE]` |
| **Hugging Face Inc. (USA)** | Stable Diffusion XL (3D QR) & AudioLDM2 (SFX) | Prompt text strings and target scan URLs | User consent upon initiating AI Generation `[EXTERNAL PROVIDER PRACTICE]` |
| **Google LLC (USA)** | reCAPTCHA v2 / v3 spam prevention | Client interaction token and server verification secret | Legitimate security interest on Contact form `[EXTERNAL PROVIDER PRACTICE]` |
| **Google LLC (USA)** | Google Analytics (GA4) | Aggregated site interaction metrics, anonymized IP | User consent via Cookie Consent Banner `[EXTERNAL PROVIDER PRACTICE]` |
| **Google LLC (USA)** | Google AdSense | Advertising personalization cookies and device metadata | User consent via Cookie Consent Banner `[EXTERNAL PROVIDER PRACTICE]` |
| **Telegram FZ-LLC** | Admin incident alerts & registration notifications | Admin notification text with masked IP (`.xxx.xxx`) and user email | Legitimate security and operational monitoring `[EXTERNAL PROVIDER PRACTICE]` |
| **IP-API.com** | Geolocation enrichment for honeypot intrusions | Attacker IP address | Legitimate security interest under CERT-In forensics `[EXTERNAL PROVIDER PRACTICE]` |

---

## 6. Prohibited Terminology & Marketing Boundaries

To prevent misleading claims, the following terms are **prohibited across all PixelCraft AI documentation and marketing**:
1. ❌ **"Zero-Knowledge"** when describing standard client-side browser execution. (Use: *"Client-Side Browser-Sandboxed Architecture"*).
2. ❌ **"100% Anonymous"** or **"Guaranteed Anonymity"**. (Use: *"Metadata Removal with Statistical Disruption"*).
3. ❌ **"Files never leave your device"** on network-assisted tools (Forensic Sanitizer, Dubbing, PDF-to-Link, Phishing Scanner).
4. ❌ **"Guaranteed Immediate Deletion"** when referring to cron jobs or TTL monitors. (Use: *"Scheduled 24-Hour Purge Window"* or *"Automated TTL Monitor"*).
5. ❌ **"Immune to Law Enforcement"** or absolute cryptographic guarantees.
