import os
import json
import re
from bs4 import BeautifulSoup

tools = [
    'image-compressor.html', 'format-converter.html', 'qr-generator.html',
    'smart-resize.html', 'images-to-pdf.html', 'exif-viewer.html',
    'phishing-scanner.html', 'ai-dubbing.html', 'pdf-to-link.html',
    'audio-steganography.html', 'watermark-adder.html', 'color-palette.html',
    'digital-fingerprint-wiper.html', 'forensic-sanitizer.html', 'advanced-decoy.html'
]

all_passed = True

for t in tools:
    path = os.path.join('public', 'tools', t)
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    title = soup.title.string.strip() if soup.title else ''
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    desc = desc_tag['content'].strip() if desc_tag else ''
    h1s = soup.find_all('h1')
    
    # Check Title
    if not (50 <= len(title) <= 60):
        print(f"❌ {t}: Bad title len ({len(title)}): {title}")
        all_passed = False
    else:
        print(f"✅ {t:<30} | Title ({len(title):2d}c): {title}")
        
    # Check Desc
    if not (140 <= len(desc) <= 160):
        print(f"❌ {t}: Bad desc len ({len(desc)}): {desc}")
        all_passed = False
    else:
        print(f"   Desc ({len(desc):3d}c): {desc[:75]}...")
        
    # Check H1
    if len(h1s) != 1:
        print(f"❌ {t}: Found {len(h1s)} H1 tags!")
        all_passed = False
    else:
        print(f"   H1: {h1s[0].get_text(strip=True)}")
        
    # Check FAQ Schema vs Visible
    schema_faqs = []
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            d = json.loads(s.string)
            items = d.get('@graph', [d])
            for it in items:
                if it.get('@type') == 'FAQPage':
                    schema_faqs = [q.get('name').strip() for q in it.get('mainEntity', [])]
        except:
            pass
            
    visible_faqs = []
    for h4 in soup.find_all('h4'):
        text = h4.get_text(strip=True)
        if text.startswith('Q') and ':' in text:
            clean_q = text[text.find(':')+1:].strip()
            visible_faqs.append(clean_q)
            
    if len(schema_faqs) != len(visible_faqs):
        print(f"❌ {t}: FAQ count mismatch! Schema: {len(schema_faqs)}, Visible: {len(visible_faqs)}")
        all_passed = False
    else:
        # Check alignment
        for sq, vq in zip(schema_faqs, visible_faqs):
            if sq != vq:
                print(f"❌ {t}: Question text mismatch!\n  Schema:  \"{sq}\"\n  Visible: \"{vq}\"")
                all_passed = False
                break
        else:
            print(f"   FAQ Parity: {len(schema_faqs)}/{len(visible_faqs)} questions matched 100%")

print("\n" + "="*70)
if all_passed:
    print("🎉 ALL 15 TOOLS PASSED METADATA, H1, AND SCHEMA CHECKS FLAWLESSLY!")
else:
    print("❌ SOME CHECKS FAILED!")
    exit(1)
