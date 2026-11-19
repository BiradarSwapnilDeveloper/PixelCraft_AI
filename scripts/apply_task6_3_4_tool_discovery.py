"""
PixelCraft AI - Update Tool Discovery & Cross-Tool Conversion (Task 6.3.4)
1. Injects data-tool-cta and destination metadata into index.html tool cards.
2. Injects cross-tool CTA tracking into all 15 tool pages.
3. Injects educational research guide discovery banners into all 15 tool pages.
"""

import os
import re

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
TOOLS_DIR = os.path.join(ROOT_DIR, 'public/tools')
INDEX_PATH = os.path.join(ROOT_DIR, 'public/index.html')

TOOL_GUIDE_MAP = {
    'image-compressor.html': {
        'title': 'Mastering Lossless Image Compression for the Web',
        'blog': 'mastering-lossless-image-compression-for-web.html',
        'badge': 'Research Guide'
    },
    'format-converter.html': {
        'title': 'Browser vs Server-Side Media Processing Guide',
        'blog': 'browser-side-vs-server-side-file-processing.html',
        'badge': 'Architecture Guide'
    },
    'qr-generator.html': {
        'title': 'QR Code Security & Quishing Defense Guide',
        'blog': 'qr-code-security-quishing-and-malicious-redirects.html',
        'badge': 'Security Guide'
    },
    'smart-resize.html': {
        'title': 'Official Passport & Exam Photo Resizing Guide',
        'blog': 'passport-and-exam-photo-resizing-guide.html',
        'badge': 'Dimension Guide'
    },
    'images-to-pdf.html': {
        'title': 'Compiling Scanned Images to Standardized PDFs',
        'blog': 'compiling-scanned-images-to-pdf-documents.html',
        'badge': 'Document Guide'
    },
    'exif-viewer.html': {
        'title': 'EXIF Metadata Privacy Risks & Removal Guide',
        'blog': 'exif-metadata-privacy-risks-and-removal.html',
        'badge': 'Privacy Guide'
    },
    'phishing-scanner.html': {
        'title': 'The Dangers of Phishing & IDN Homograph Attacks',
        'blog': 'the-dangers-of-phishing-and-homograph-attacks.html',
        'badge': 'Security Guide'
    },
    'ai-dubbing.html': {
        'title': 'AI Voice Dubbing & Speech Translation Guide',
        'blog': 'ai-voice-dubbing-and-speech-translation.html',
        'badge': 'Media AI Guide'
    },
    'pdf-to-link.html': {
        'title': 'Securing PDFs: Redaction, Sanitization & Encryption',
        'blog': 'securing-pdfs-redaction-metadata-stripping-and-encryption.html',
        'badge': 'Security Guide'
    },
    'audio-steganography.html': {
        'title': 'The Complete Guide to Steganography & Data Concealment',
        'blog': 'complete-guide-to-image-steganography.html',
        'badge': 'Cryptography Guide'
    },
    'watermark-adder.html': {
        'title': 'Image Watermarking & Intellectual Property Attribution',
        'blog': 'image-watermarking-and-copyright-protection.html',
        'badge': 'Protection Guide'
    },
    'color-palette.html': {
        'title': 'Color Palette Extraction & Design Systems Guide',
        'blog': 'color-palette-extraction-and-design-systems.html',
        'badge': 'Design Guide'
    },
    'digital-fingerprint-wiper.html': {
        'title': 'What is PRNU Sensor Fingerprinting? Guide',
        'blog': 'what-is-prnu-sensor-fingerprinting.html',
        'badge': 'Forensics Guide'
    },
    'forensic-sanitizer.html': {
        'title': 'Digital Photo Forensics & Deep Sanitization Guide',
        'blog': 'what-is-prnu-sensor-fingerprinting.html',
        'badge': 'Forensics Guide'
    },
    'advanced-decoy.html': {
        'title': 'Plausible Deniability & Dual-Password Steganography Guide',
        'blog': 'complete-guide-to-image-steganography.html',
        'badge': 'Cryptography Guide'
    }
}

def update_homepage_tool_cards():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for tool card anchors: <a href="tools/<name>.html" class="tool-card" ...
    def replacer(match):
        full = match.group(0)
        tool_name = match.group(1)
        if 'data-tool-cta' in full:
            return full
        # Insert data attributes before class
        replacement = f'<a href="tools/{tool_name}.html" data-tool-cta="true" data-dest-tool="{tool_name}.html" data-cta-location="homepage_grid" data-content-type="homepage" class="tool-card"'
        return replacement

    updated = re.sub(r'<a href="tools/([a-zA-Z0-9_-]+)\.html"\s+class="tool-card"', replacer, content)
    if updated != content:
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(updated)
        print("Updated homepage tool cards with data-tool-cta attributes.")
    else:
        print("Homepage tool cards already updated.")

def update_tool_pages():
    for tool_file, guide_info in TOOL_GUIDE_MAP.items():
        filepath = os.path.join(TOOLS_DIR, tool_file)
        if not os.path.exists(filepath):
            print(f"Skipping {tool_file} (not found)")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update existing related tool links with data-tool-cta
        # Look for <a href="<other-tool>.html" style="text-decoration: none; padding: 16px; ...
        def cta_replacer(match):
            href = match.group(1)
            rest = match.group(2)
            if 'data-tool-cta' in rest:
                return match.group(0)
            return f'<a href="{href}" data-tool-cta="true" data-dest-tool="{href}" data-cta-location="related_tools" data-content-type="cross_tool" {rest}'

        content = re.sub(r'<a href="([a-zA-Z0-9_-]+\.html)"\s+(style="text-decoration:\s*none;\s*padding:\s*16px;[^"]*")', cta_replacer, content)

        # 2. Insert educational guide discovery banner if not present
        if 'data-cta-location="tool_guide_banner"' not in content:
            guide_banner = f"""          <!-- EDUCATIONAL RESEARCH GUIDE CALLOUT (TASK 6.3.4) -->
          <div style="margin-bottom: 22px; padding: 14px 18px; background: var(--surface-card); border-radius: 12px; border: 1px solid var(--border-color); border-left: 4px solid var(--primary); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="font-size: 1.3rem; line-height: 1;">📚</span>
              <div>
                <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; color: var(--primary); display: block;">{guide_info['badge']}</span>
                <span style="font-size: 0.92rem; font-weight: 600; color: var(--text-heading);">{guide_info['title']}</span>
              </div>
            </div>
            <a href="../blog/{guide_info['blog']}" style="display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; background: var(--surface-subtle); border: 1px solid var(--border-color); border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--primary); text-decoration: none; transition: 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-color)'" data-tool-cta="true" data-dest-tool="{guide_info['blog']}" data-cta-location="tool_guide_banner" data-content-type="tool_page">
              <span>Read Guide &rarr;</span>
            </a>
          </div>\n"""

            # Insert above the grid inside RELATED TOOLS
            # Find: <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            grid_pos = content.find('style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));')
            if grid_pos != -1:
                # Find previous <div or <h2
                h2_end = content.rfind('</h2>', 0, grid_pos)
                if h2_end != -1:
                    insert_at = h2_end + len('</h2>\n')
                    content = content[:insert_at] + guide_banner + content[insert_at:]
                    print(f"Added research guide banner to {tool_file}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    update_homepage_tool_cards()
    update_tool_pages()
    print("\nTool discovery and CTA instrumentation complete.")
