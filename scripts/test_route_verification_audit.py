import requests
import json
import sys

tools = [
    'image-compressor', 'format-converter', 'qr-generator', 'smart-resize',
    'images-to-pdf', 'exif-viewer', 'phishing-scanner', 'ai-dubbing',
    'pdf-to-link', 'audio-steganography', 'watermark-adder', 'color-palette',
    'digital-fingerprint-wiper', 'forensic-sanitizer', 'advanced-decoy'
]

blogs = [
    'ai-voice-dubbing-and-speech-translation',
    'browser-side-vs-server-side-file-processing',
    'color-palette-extraction-and-design-systems',
    'compiling-scanned-images-to-pdf-documents',
    'complete-guide-to-image-steganography',
    'exif-metadata-privacy-risks-and-removal',
    'how-honeypots-and-canary-tokens-detect-breaches',
    'image-watermarking-and-copyright-protection',
    'mastering-lossless-image-compression-for-web',
    'passport-and-exam-photo-resizing-guide',
    'qr-code-security-quishing-and-malicious-redirects',
    'securing-pdfs-redaction-metadata-stripping-and-encryption',
    'the-dangers-of-phishing-and-homograph-attacks',
    'understanding-ai-prompt-injection-attacks',
    'what-is-prnu-sensor-fingerprinting'
]

key_routes = [
    ('/', 'Root'),
    ('/tools', 'Tools Section Redirect'),
    ('/tools/', 'Tools Slash Redirect'),
    ('/index.html', 'Index HTML Redirect'),
    ('/blog', 'Blog Directory Redirect'),
    ('/blog.html', 'Blog HTML Redirect'),
    ('/blog/index.html', 'Blog Hub')
]

def check(url):
    try:
        r = requests.get(url, allow_redirects=False, timeout=5)
        return r.status_code, r.headers.get('Location', '-')
    except Exception as e:
        return 'ERR', str(e)

print("=== LOCAL SERVER ROUTE AUDIT (PORT 8085) ===")
local_base = 'http://localhost:8085'
for route, desc in key_routes:
    status, loc = check(f"{local_base}{route}")
    print(f"Route: {route:<20} | Status: {status:<4} | Location: {loc:<25} | ({desc})")

print("\n--- 15 Tools Extensionless Canonical Redirect on Local ---")
all_tools_ok = True
for t in tools:
    st_clean, loc_clean = check(f"{local_base}/tools/{t}")
    st_html, _ = check(f"{local_base}/tools/{t}.html")
    if st_clean != 301 or st_html != 200:
        all_tools_ok = False
    print(f"Tool: {t:<26} | clean -> {st_clean} ({loc_clean}) | html -> {st_html}")

print(f"All 15 Tools Canonical Structure Local: {'PASS' if all_tools_ok else 'FAIL'}")

print("\n--- 15 Blog Articles on Local ---")
all_blogs_ok = True
for b in blogs:
    st_html, _ = check(f"{local_base}/blog/{b}.html")
    st_clean, loc_clean = check(f"{local_base}/blog/{b}")
    if st_clean != 301 or st_html != 200:
        all_blogs_ok = False
    print(f"Blog: {b[:30]:<30} | html -> {st_html} | clean -> {st_clean} ({loc_clean})")

print(f"All 15 Blogs Canonical Structure Local: {'PASS' if all_blogs_ok else 'FAIL'}")
