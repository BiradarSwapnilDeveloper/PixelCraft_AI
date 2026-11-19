"""
PixelCraft AI - Apply Task 6.3.4 Blog-to-Tool CTAs and Internal Discovery Grids
Upgrades the remaining 10 blog posts with contextual mid-article CTA cards and
responsive end-of-article tool discovery grids with full GA4 tracking hooks.
"""

import os
import re

BLOG_DIR = os.path.join(os.path.dirname(__file__), '../public/blog')

ARTICLES_DATA = {
    'mastering-lossless-image-compression-for-web.html': {
        'icon': '🗜️',
        'title': 'Compress Your Web Images In-Browser Now',
        'desc': 'Reduce photo and graphic payloads up to 85% losslessly with real-time target KB controls and instant side-by-side visual preview. 100% private.',
        'primary_btn': '🚀 Open Smart Image Compressor',
        'primary_tool': 'image-compressor.html',
        'sec_text': 'Convert to next-gen WebP/AVIF? Launch Format Converter &rarr;',
        'sec_tool': 'format-converter.html',
        'related_title': 'Recommended Image Optimization Tools',
        'related_cards': [
            ('image-compressor.html', '🗜️', 'Smart Image Compressor', 'Reduce photo weight to exact 20KB, 50KB, or 100KB limits with instant preview.'),
            ('format-converter.html', '🔄', 'Format Converter', 'Batch transcode images between WebP, AVIF, PNG, and JPG in local browser memory.'),
            ('smart-resize.html', '📐', 'Smart Social & Exam Resize', 'Crop and scale portraits for social media platforms and official government portals.')
        ]
    },
    'browser-side-vs-server-side-file-processing.html': {
        'icon': '🔒',
        'title': 'Experience 100% Client-Side Private Processing',
        'desc': 'Compress, convert, and format photos directly inside your browser sandbox using HTML5 Canvas and WebAssembly. Zero bytes sent to cloud servers.',
        'primary_btn': '🚀 Open Smart Image Compressor',
        'primary_tool': 'image-compressor.html',
        'sec_text': 'Batch convert image formats locally? Format Converter &rarr;',
        'sec_tool': 'format-converter.html',
        'related_title': 'Recommended Client-Side Media Tools',
        'related_cards': [
            ('image-compressor.html', '🗜️', 'Image Compressor', 'Fast in-memory compression with visual diff slider and target file size presets.'),
            ('format-converter.html', '🔄', 'Format Converter', 'Client-side batch format transcoding supporting WebP, AVIF, PNG, and JPEG.'),
            ('exif-viewer.html', '🔍', 'EXIF Data Viewer', 'Inspect camera metadata and scrub sensitive GPS coordinates before sharing.')
        ]
    },
    'complete-guide-to-image-steganography.html': {
        'icon': '🎭',
        'title': 'Try Plausible Deniability Steganography',
        'desc': 'Conceal dual encrypted payloads with AES-256-GCM under coercive duress scenarios. Zero server storage, zero metadata traces.',
        'primary_btn': '🚀 Open Advanced Decoy Steganography',
        'primary_tool': 'advanced-decoy.html',
        'sec_text': 'Embed secrets in audio/video containers? Audio Steganography &rarr;',
        'sec_tool': 'audio-steganography.html',
        'related_title': 'Recommended Cryptography & Privacy Tools',
        'related_cards': [
            ('advanced-decoy.html', '🎭', 'Advanced Decoy Steganography', 'Plausible deniability with decoy and vault passphrases using AES-256-GCM.'),
            ('audio-steganography.html', '🎬', 'Audio & Video Steganography', 'Multiplex encrypted text payloads inside WAV audio and WebM/MKV video containers.'),
            ('forensic-sanitizer.html', '🧹', 'Forensic Sanitizer', 'Strip hidden ICC color profiles, thumbnails, and forensic traces from carrier images.')
        ]
    },
    'exif-metadata-privacy-risks-and-removal.html': {
        'icon': '🔍',
        'title': 'Inspect & Strip EXIF GPS Coordinates Now',
        'desc': 'Analyze camera serials, lens specs, and geolocation tags, then scrub metadata in local browser memory before uploading publicly.',
        'primary_btn': '🚀 Open EXIF Data Viewer',
        'primary_tool': 'exif-viewer.html',
        'sec_text': 'Perform deep pixel sanitization? Forensic Sanitizer &rarr;',
        'sec_tool': 'forensic-sanitizer.html',
        'related_title': 'Recommended Privacy & Forensics Utilities',
        'related_cards': [
            ('exif-viewer.html', '🔍', 'EXIF Data Viewer', 'Extract full EXIF/IPTC/XMP headers and scrub geolocation data locally in browser.'),
            ('digital-fingerprint-wiper.html', '🛡️', 'Digital Fingerprint Wiper', 'Disrupt camera PRNU sensor noise and anonymize photographic hardware fingerprints.'),
            ('forensic-sanitizer.html', '🧹', 'Forensic Metadata Sanitizer', 'Deep canvas redraw and ICC profile stripping for total forensic sanitization.')
        ]
    },
    'qr-code-security-quishing-and-malicious-redirects.html': {
        'icon': '📱',
        'title': 'Generate Safe Vector QR Codes Locally',
        'desc': 'Create vector SVG/PNG QR codes with Reed-Solomon error correction and custom styling. Zero tracking or telemetry redirects.',
        'primary_btn': '🚀 Open QR Code Generator',
        'primary_tool': 'qr-generator.html',
        'sec_text': 'Verify a suspicious destination URL? Scan for Phishing &rarr;',
        'sec_tool': 'phishing-scanner.html',
        'related_title': 'Recommended Security & Utility Tools',
        'related_cards': [
            ('qr-generator.html', '📱', 'Custom QR Generator', 'Generate clean static URL and payment QR codes with customizable colors and SVG export.'),
            ('phishing-scanner.html', '🛡️', 'Phishing & Malware Scanner', 'Inspect URLs for punycode homoglyphs, high entropy, and malicious redirect chains.'),
            ('pdf-to-link.html', '🔗', 'Secure PDF to Link', 'Share PDF documents via temporary web links with automatic 24-hour purge.')
        ]
    },
    'the-dangers-of-phishing-and-homograph-attacks.html': {
        'icon': '🛡️',
        'title': 'Analyze Suspicious Links for IDN Homoglyphs',
        'desc': 'Evaluate URLs using Shannon entropy, punycode spoof detection, and credential harvester heuristics in isolated memory.',
        'primary_btn': '🚀 Open Phishing Link Scanner',
        'primary_tool': 'phishing-scanner.html',
        'sec_text': 'Generate secure, direct QR links? QR Generator &rarr;',
        'sec_tool': 'qr-generator.html',
        'related_title': 'Recommended Security & Verification Tools',
        'related_cards': [
            ('phishing-scanner.html', '🛡️', 'Phishing & Malware Scanner', 'Detect IDN homograph impersonations, tracking tokens, and malicious URL redirects.'),
            ('qr-generator.html', '📱', 'Custom QR Generator', 'Generate clean, transparent QR codes with zero intermediate tracking redirects.'),
            ('exif-viewer.html', '🔍', 'EXIF Data Viewer', 'Verify image origin and metadata headers to detect forged or tampered visual assets.')
        ]
    },
    'what-is-prnu-sensor-fingerprinting.html': {
        'icon': '🔬',
        'title': 'Neutralize Camera Sensor Noise (PRNU) Locally',
        'desc': 'Perturb microscopic sensor pattern noise and anonymize photographic hardware fingerprints via client-side dithering.',
        'primary_btn': '🚀 Open Digital Fingerprint Wiper',
        'primary_tool': 'digital-fingerprint-wiper.html',
        'sec_text': 'Strip color profile & deep forensic tags? Forensic Sanitizer &rarr;',
        'sec_tool': 'forensic-sanitizer.html',
        'related_title': 'Recommended Privacy & Anti-Forensics Utilities',
        'related_cards': [
            ('digital-fingerprint-wiper.html', '🛡️', 'Digital Fingerprint Wiper', 'Neutralize Photo-Response Non-Uniformity (PRNU) noise patterns locally.'),
            ('forensic-sanitizer.html', '🧹', 'Forensic Metadata Sanitizer', 'Deep pixel re-rasterization and total metadata scrubbing for sensitive images.'),
            ('exif-viewer.html', '🔍', 'EXIF Data Viewer', 'Inspect embedded camera serial numbers and GPS coordinates before publication.')
        ]
    },
    'securing-pdfs-redaction-metadata-stripping-and-encryption.html': {
        'icon': '🔗',
        'title': 'Share Sensitive PDFs with 24-Hour Ephemeral Purge',
        'desc': 'Host encrypted documents with automatic 24-hour expiration and instant QR access. Zero permanent cloud retention.',
        'primary_btn': '🚀 Open Secure PDF to Link',
        'primary_tool': 'pdf-to-link.html',
        'sec_text': 'Compile clean multi-page PDFs client-side? Images to PDF &rarr;',
        'sec_tool': 'images-to-pdf.html',
        'related_title': 'Recommended Document & Privacy Utilities',
        'related_cards': [
            ('pdf-to-link.html', '🔗', 'Secure PDF to Link', 'Zero-knowledge temporary document sharing with automatic 24-hour expiration purge.'),
            ('images-to-pdf.html', '📄', 'Images to PDF Converter', 'Merge photos, receipts, and multi-page scans into clean, standardized PDF documents.'),
            ('image-compressor.html', '🗜️', 'Image Compressor', 'Compress scanned high-res pages before document assembly to minimize file size.')
        ]
    },
    'how-honeypots-and-canary-tokens-detect-breaches.html': {
        'icon': '🛡️',
        'title': 'Audit Links & Traps with Threat Intelligence',
        'desc': 'Scan suspect links for tracking tokens, malicious redirects, and credential harvesting infrastructure in sandboxed memory.',
        'primary_btn': '🚀 Open Phishing Link Scanner',
        'primary_tool': 'phishing-scanner.html',
        'sec_text': 'Deploy plausible deniability payloads? Advanced Decoy &rarr;',
        'sec_tool': 'advanced-decoy.html',
        'related_title': 'Recommended Security & Defensive Utilities',
        'related_cards': [
            ('phishing-scanner.html', '🛡️', 'Phishing & Malware Scanner', 'Scan incoming links and attachments for credential harvesters and tracking beacons.'),
            ('advanced-decoy.html', '🎭', 'Advanced Decoy Steganography', 'Conceal sensitive operational keys in encrypted decoy carriers for plausible deniability.'),
            ('exif-viewer.html', '🔍', 'EXIF Data Viewer', 'Check embedded author and device metadata on shared security documentation.')
        ]
    },
    'understanding-ai-prompt-injection-attacks.html': {
        'icon': '🛡️',
        'title': 'Scan Input Payloads for Adversarial Exploits',
        'desc': 'Evaluate URLs, payloads, and redirect chains for obfuscated injection vectors and homograph traps in isolated memory.',
        'primary_btn': '🚀 Open Phishing Link Scanner',
        'primary_tool': 'phishing-scanner.html',
        'sec_text': 'Analyze encoded steganographic media? Audio Steganography &rarr;',
        'sec_tool': 'audio-steganography.html',
        'related_title': 'Recommended AI & Cybersecurity Utilities',
        'related_cards': [
            ('phishing-scanner.html', '🛡️', 'Phishing & Malware Scanner', 'Analyze suspicious endpoints and malicious redirect chains in sandboxed memory.'),
            ('ai-dubbing.html', '🎙️', 'AI Voice & Video Dubbing', 'Translate speech and synthesize voiceovers across 30+ languages in browser.'),
            ('audio-steganography.html', '🎬', 'Audio Steganography', 'Conceal encrypted cryptographic payloads inside WAV and WebM/MKV media.')
        ]
    }
}

def generate_mid_cta_html(data):
    return f"""
      <!-- CONTEXTUAL BLOG-TO-TOOL CTA (MID-ARTICLE) -->
      <div class="blog-tool-cta-card">
        <div class="blog-tool-cta-header">
          <span class="blog-tool-cta-icon">{data['icon']}</span>
          <h3 class="blog-tool-cta-title">{data['title']}</h3>
        </div>
        <p class="blog-tool-cta-desc">
          {data['desc']}
        </p>
        <div class="blog-tool-cta-actions">
          <a href="../tools/{data['primary_tool']}" class="tool-cta-btn" data-tool-cta="true" data-dest-tool="{data['primary_tool']}" data-cta-location="blog_mid" data-content-type="blog_article">
            <span>{data['primary_btn']}</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
          <a href="../tools/{data['sec_tool']}" class="tool-cta-secondary-link" data-tool-cta="true" data-dest-tool="{data['sec_tool']}" data-cta-location="blog_mid_secondary" data-content-type="blog_article">
            <span>{data['sec_text']}</span>
          </a>
        </div>
      </div>
"""

def generate_related_grid_html(data):
    cards_html = ""
    for tool_file, icon, name, desc in data['related_cards']:
        cards_html += f"""          <a href="../tools/{tool_file}" class="blog-related-card" data-tool-cta="true" data-dest-tool="{tool_file}" data-cta-location="blog_end" data-content-type="blog_article">
            <div>
              <div style="font-size: 1.5rem; margin-bottom: 6px;">{icon}</div>
              <strong style="color: var(--text-heading); display: block; margin-bottom: 4px;">{name}</strong>
              <span style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.4; display: block;">{desc}</span>
            </div>
            <span style="font-size: 0.85rem; font-weight: 600; color: var(--primary); margin-top: 10px; display: inline-flex; align-items: center; gap: 4px;">Launch Tool &rarr;</span>
          </a>\n"""

    return f"""      <div class="related-tools">
        <h3>{data['related_title']}</h3>
        <p>Enhance your productivity with PixelCraft AI's client-side, zero-knowledge utilities:</p>
        <div class="blog-related-grid">
{cards_html}        </div>
      </div>"""

def upgrade_article(filename, data):
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert Mid-Article CTA before FAQ section if not already present
    if 'class="blog-tool-cta-card"' not in content:
        # Match FAQ h2 heading
        faq_match = re.search(r'(<h2[^>]*>\s*(?:\d+\.\s*)?Frequently Asked Questions\s*</h2>)', content, re.IGNORECASE)
        if faq_match:
            mid_cta = generate_mid_cta_html(data)
            content = content[:faq_match.start()] + mid_cta + '\n' + content[faq_match.start():]
            print(f"Added mid-article CTA to {filename}")
        else:
            print(f"WARNING: FAQ heading not found in {filename}")

    # 2. Upgrade .related-tools block
    rel_match = re.search(r'<div class="related-tools">[\s\S]*?</div>', content)
    if rel_match:
        new_related = generate_related_grid_html(data)
        content = content[:rel_match.start()] + new_related + content[rel_match.end():]
        print(f"Upgraded related-tools in {filename}")
    else:
        print(f"WARNING: related-tools block not found in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for filename, data in ARTICLES_DATA.items():
        upgrade_article(filename, data)
    print("\nAll 10 remaining blog articles upgraded successfully.")
