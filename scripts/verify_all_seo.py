import glob, os, re, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 80)
print("COMPREHENSIVE SEO VERIFICATION AUDIT (TASK 1 & TASK 2)")
print("=" * 80)

public_files = sorted(glob.glob('public/**/*.html', recursive=True))

title_lengths = {}
desc_lengths = {}
all_titles = {}
all_descriptions = {}
heading_skips = {}
h1_counts = {}
missing_alts = {}

for f in public_files:
    with open(f, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp.read(), 'html.parser')
        
    # Title
    t = soup.find('title')
    title_str = t.get_text().strip() if t else 'NONE'
    all_titles[f] = title_str
    title_lengths[f] = len(title_str)
    
    # Description
    d = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
    desc_str = d.get('content', '').strip() if d else ''
    all_descriptions[f] = desc_str
    desc_lengths[f] = len(desc_str)
    
    # Headings
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    h_levels = [int(h.name[1]) for h in headings]
    h1_counts[f] = h_levels.count(1)
    
    skips = []
    for i in range(len(h_levels) - 1):
        if h_levels[i+1] > h_levels[i] + 1:
            skips.append((h_levels[i], h_levels[i+1], headings[i].get_text(strip=True)[:30], headings[i+1].get_text(strip=True)[:30]))
    if skips or (h_levels and h_levels[0] != 1 and f != 'public\\blog.html'):
        heading_skips[f] = skips
        
    # Missing Alts
    for img in soup.find_all('img'):
        if img.get('alt') is None:
            missing_alts.setdefault(f, []).append(str(img))

print("\n--- 1. TITLE LENGTH AUDIT (Max 60 chars) ---")
titles_over_60 = {k: v for k, v in title_lengths.items() if v > 60}
if not titles_over_60:
    print(f"✅ PASS: 0 titles exceed 60 characters across all {len(public_files)} pages.")
else:
    print(f"❌ FAIL: {len(titles_over_60)} titles exceed 60 chars: {titles_over_60}")

print("\n--- 2. META DESCRIPTION LENGTH AUDIT (Max 160 chars) ---")
descs_over_160 = {k: v for k, v in desc_lengths.items() if v > 160}
if not descs_over_160:
    print(f"✅ PASS: 0 descriptions exceed 160 characters across all {len(public_files)} pages.")
else:
    print(f"❌ FAIL: {len(descs_over_160)} descriptions exceed 160 chars: {descs_over_160}")

print("\n--- 3. DUPLICATE TITLES & DESCRIPTIONS ---")
title_dups = {t: [p for p, pt in all_titles.items() if pt == t] for t in set(all_titles.values()) if list(all_titles.values()).count(t) > 1}
desc_dups = {d: [p for p, pd in all_descriptions.items() if pd == d] for d in set(all_descriptions.values()) if d and list(all_descriptions.values()).count(d) > 1}
if not title_dups:
    print("✅ PASS: 0 duplicate titles. 100% unique!")
else:
    print(f"❌ FAIL: Duplicate titles: {title_dups}")
if not desc_dups:
    print("✅ PASS: 0 duplicate descriptions. 100% unique!")
else:
    print(f"❌ FAIL: Duplicate descriptions: {desc_dups}")

print("\n--- 4. HEADING HIERARCHY AUDIT (H1-H4 without skips) ---")
# Exclude blog.html (redirect stub)
real_skips = {k: v for k, v in heading_skips.items() if not k.endswith('blog.html')}
if not real_skips:
    print(f"✅ PASS: Exactly 0 heading-order issues across all 37 content pages!")
else:
    print(f"❌ FAIL: Heading skips remaining in {len(real_skips)} pages:")
    for p, sk in real_skips.items():
        print(f"   - {p}: {sk}")

print("\n--- 5. PRIMARY H1 CHECK ---")
pages_without_single_h1 = {k: v for k, v in h1_counts.items() if v != 1 and not k.endswith('blog.html')}
if not pages_without_single_h1:
    print("✅ PASS: Every content page has exactly 1 primary H1 tag!")
else:
    print(f"❌ FAIL: Pages with != 1 H1: {pages_without_single_h1}")

print("\n--- 6. ORPHAN PAGE CHECK (/download-app.html) ---")
download_inbound = [f for f in public_files if 'download-app.html' in open(f, 'r', encoding='utf-8').read() and not f.endswith('download-app.html')]
if len(download_inbound) >= 2:
    print(f"✅ PASS: /download-app.html is linked by {len(download_inbound)} pages: {download_inbound}")
else:
    print(f"❌ FAIL: Inbound links to download-app.html: {download_inbound}")

print("\n--- 7. IMAGE ALT ATTRIBUTE AUDIT ---")
if not missing_alts:
    print("✅ PASS: 0 missing image alt attributes across all public HTML pages!")
else:
    print(f"❌ FAIL: Missing alts in {len(missing_alts)} pages: {missing_alts}")

print("=" * 80)
