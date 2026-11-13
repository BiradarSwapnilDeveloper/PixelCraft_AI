import os, re, json

title_updates = {
    'public/index.html': 'Free AI Tools & Private Image Utilities | PixelCraft AI',
    'public/cookies-policy.html': 'Cookies Policy | PixelCraft AI Privacy & Tracking Standards',
    'public/data-practices.html': 'Data Retention & Ephemeral Privacy Practices | PixelCraft AI',
    'public/download-app.html': 'Install PixelCraft AI App - Offline PWA Privacy Utilities',
    'public/privacy-policy.html': 'Privacy Policy | PixelCraft AI Client-Side Data Protection',
    'public/security-whitepaper.html': 'Security Whitepaper: Zero-Knowledge Systems | PixelCraft AI',
    'public/tools/advanced-decoy.html': 'Decoy Steganography Tool - Dual Encryption | PixelCraft AI',
    'public/tools/ai-dubbing.html': 'AI Voice & Video Dubbing - Free Audio Tool | PixelCraft AI',
    'public/tools/audio-steganography.html': 'Audio & Video Steganography - Hide Payloads | PixelCraft AI',
    'public/tools/color-palette.html': 'Color Palette Extractor - Extract HEX Codes | PixelCraft AI',
    'public/tools/digital-fingerprint-wiper.html': 'Digital Fingerprint Wiper - Wipe PRNU Noise | PixelCraft AI',
    'public/tools/exif-viewer.html': 'EXIF Data Viewer & Metadata Remover Online | PixelCraft AI',
    'public/tools/forensic-sanitizer.html': 'Forensic Sanitizer - Wipe Image Traces Free | PixelCraft AI',
    'public/tools/format-converter.html': 'Image Format Converter - PNG, JPG & WebP | PixelCraft AI',
    'public/tools/image-compressor.html': 'Image Compressor - Reduce Image Size in KB | PixelCraft AI',
    'public/tools/images-to-pdf.html': 'Images to PDF Converter - Free Photo to PDF | PixelCraft AI',
    'public/tools/pdf-to-link.html': 'PDF to Link Converter - Share PDF via Link | PixelCraft AI',
    'public/tools/phishing-scanner.html': 'Phishing Link Scanner - Check Malicious URLs | PixelCraft AI',
    'public/tools/qr-generator.html': 'Free QR Code Generator - Custom Logo & UPI | PixelCraft AI',
    'public/tools/smart-resize.html': 'Photo Resizer - Resize Images in Pixels & KB | PixelCraft AI',
    'public/tools/watermark-adder.html': 'Add Watermark to Photos Online - Text & Logo | PixelCraft AI',
    'public/blog/browser-side-vs-server-side-file-processing.html': 'Client vs Server File Processing Privacy | PixelCraft AI',
    'public/blog/complete-guide-to-image-steganography.html': 'Image & Audio Steganography Complete Guide | PixelCraft AI',
    'public/blog/exif-metadata-privacy-risks-and-removal.html': 'EXIF Metadata Privacy Risks & Removal Guide | PixelCraft AI',
    'public/blog/how-honeypots-and-canary-tokens-detect-breaches.html': 'Honeypots & Canary Tokens Breach Detection | PixelCraft AI',
    'public/blog/mastering-lossless-image-compression-for-web.html': 'Lossless Image Compression Guide for the Web | PixelCraft AI',
    'public/blog/qr-code-security-quishing-and-malicious-redirects.html': 'QR Code Security: Quishing & Malicious Links | PixelCraft AI',
    'public/blog/securing-pdfs-redaction-metadata-stripping-and-encryption.html': 'PDF Security Guide: Redaction & Encryption | PixelCraft AI',
    'public/blog/the-dangers-of-phishing-and-homograph-attacks.html': 'Phishing & IDN Homograph Attacks Explained | PixelCraft AI',
    'public/blog/understanding-ai-prompt-injection-attacks.html': 'AI Prompt Injection Attacks & Defenses Guide | PixelCraft AI',
    'public/blog/what-is-prnu-sensor-fingerprinting.html': 'What is PRNU? Camera Sensor Fingerprinting | PixelCraft AI'
}

desc_updates = {
    'public/index.html': 'Free private AI tools and image utilities. Compress images, generate QR codes, convert to PDF, and inspect metadata securely in your browser with zero uploads.',
    'public/about-us.html': 'Discover PixelCraft AI and our mission to deliver fast, client-side image tools, steganography, and cybersecurity utilities without storing any personal data.',
    'public/security-whitepaper.html': 'Explore PixelCraft AI\'s security whitepaper detailing zero-knowledge client pipelines, ephemeral RAM buffers, Encrypt-then-MAC, and PRNU sensor noise removal.',
    'public/tools/audio-steganography.html': 'Hide encrypted secret text and files inside audio tracks and videos online. Zero quality loss, client-side ISO-BMFF multiplexing, and 100% private in browser.'
}

def process_file(rel_path):
    full_path = os.path.normpath(rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return False
        
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content

    # 1. Title update
    if rel_path in title_updates:
        new_title = title_updates[rel_path]
        # Replace <title>...</title>
        new_content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', new_content, count=1, flags=re.DOTALL)
        # Replace og:title
        new_content = re.sub(r'(<meta\s+property=["\']og:title["\']\s+content=)["\'].*?["\'](\s*/?>)',
                             rf'\g<1>"{new_title}"\g<2>', new_content, count=1)
        # Replace twitter:title
        new_content = re.sub(r'(<meta\s+name=["\']twitter:title["\']\s+content=)["\'].*?["\'](\s*/?>)',
                             rf'\g<1>"{new_title}"\g<2>', new_content, count=1)

    # 2. Desc update
    if rel_path in desc_updates:
        new_desc = desc_updates[rel_path]
        # Replace meta name="description"
        new_content = re.sub(r'(<meta\s+name=["\']description["\']\s+content=)["\'].*?["\'](\s*/?>)',
                             rf'\g<1>"{new_desc}"\g<2>', new_content, count=1)
        # Replace og:description
        new_content = re.sub(r'(<meta\s+property=["\']og:description["\']\s+content=)["\'].*?["\'](\s*/?>)',
                             rf'\g<1>"{new_desc}"\g<2>', new_content, count=1)
        # Replace twitter:description
        new_content = re.sub(r'(<meta\s+name=["\']twitter:description["\']\s+content=)["\'].*?["\'](\s*/?>)',
                             rf'\g<1>"{new_desc}"\g<2>', new_content, count=1)

    # 3. Image Alt updates
    if rel_path == 'public/tools/color-palette.html':
        target = '<img id="preview-img" style="width:100%;border-radius:12px;border:1.5px solid var(--border);object-fit:contain;max-height:300px;"/>'
        replacement = '<img id="preview-img" alt="Uploaded photo preview for color palette extraction" style="width:100%;border-radius:12px;border:1.5px solid var(--border);object-fit:contain;max-height:300px;"/>'
        if target in new_content:
            new_content = new_content.replace(target, replacement, 1)
        else:
            print(f'Warning: preview-img target not matched in {rel_path}')

    if rel_path == 'public/tools/exif-viewer.html':
        target = '<img id="preview-img" style="width:100%;border-radius:12px;border:1.5px solid var(--border);object-fit:contain;max-height:280px;"/>'
        replacement = '<img id="preview-img" alt="Uploaded image preview for EXIF metadata inspection" style="width:100%;border-radius:12px;border:1.5px solid var(--border);object-fit:contain;max-height:280px;"/>'
        if target in new_content:
            new_content = new_content.replace(target, replacement, 1)
        else:
            print(f'Warning: preview-img target not matched in {rel_path}')

    if new_content != content:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {rel_path}")
        return True
    else:
        print(f"No changes: {rel_path}")
        return False

all_targets = set(list(title_updates.keys()) + list(desc_updates.keys()) + ['public/tools/color-palette.html', 'public/tools/exif-viewer.html'])
print(f"Total target files to update: {len(all_targets)}")

updated_count = 0
for p in sorted(all_targets):
    if process_file(p):
        updated_count += 1

print(f"Total files successfully updated: {updated_count}")
