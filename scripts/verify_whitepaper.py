# -*- coding: utf-8 -*-
with open('public/security-whitepaper.html', encoding='utf-8') as f:
    content = f.read()

print('Characters:', len(content))

tools = [
  'tool-advanced-decoy',
  'tool-forensic-sanitizer',
  'tool-audio-steganography',
  'tool-digital-fingerprint-wiper',
  'tool-phishing-scanner',
  'tool-exif-viewer',
  'tool-ai-dubbing',
  'tool-pdf-to-link',
  'tool-images-to-pdf',
  'tool-watermark-adder',
  'tool-qr-generator',
  'tool-image-compressor',
  'tool-format-converter',
  'tool-smart-resize',
  'tool-color-palette'
]

missing = []
for t in tools:
    card_marker = f'data-tool-id="{t}"'
    article_marker = f'id="{t}"'
    if card_marker not in content:
        missing.append((t, 'card'))
    if article_marker not in content:
        missing.append((t, 'article'))

if missing:
    print('FAILED! Missing markers:', missing)
else:
    print(f'SUCCESS! All {len(tools)} tools present in cards and articles.')
