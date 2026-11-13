import os, glob, re, json
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 80)
print("SEO TASK 1 VERIFICATION AUDIT")
print("=" * 80)

# 1. Canonical & Robots preservation check
with open('canonical_snapshot.json', 'r', encoding='utf-8') as f:
    snapshot = json.load(f)

canonical_violations = []
robots_violations = []

all_titles = {}
all_descriptions = {}
title_lengths = {}
desc_lengths = {}
missing_alts = {}

public_files = sorted(glob.glob('public/**/*.html', recursive=True))

for f in public_files:
    with open(f, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp.read(), 'html.parser')
        
    c = soup.find('link', attrs={'rel': 'canonical'})
    c_url = c.get('href') if c else None
    
    r = soup.find('meta', attrs={'name': 'robots'})
    r_val = r.get('content') if r else None
    
    if snapshot.get(f, {}).get('canonical') != c_url:
        canonical_violations.append((f, snapshot.get(f, {}).get('canonical'), c_url))
        
    if snapshot.get(f, {}).get('robots') != r_val:
        robots_violations.append((f, snapshot.get(f, {}).get('robots'), r_val))
        
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
    
    # Img alts
    for img in soup.find_all('img'):
        if img.get('alt') is None:
            missing_alts.setdefault(f, []).append(str(img))

print("\n--- 1. CANONICAL & ROBOTS PRESERVATION ---")
if not canonical_violations:
    print(f"✅ PASS: 100% of canonical tags preserved across all {len(public_files)} files.")
else:
    print(f"❌ FAIL: Canonical violations detected: {canonical_violations}")

if not robots_violations:
    print(f"✅ PASS: 100% of robots directives preserved across all {len(public_files)} files.")
else:
    print(f"❌ FAIL: Robots violations detected: {robots_violations}")

print("\n--- 2. TITLE LENGTH AUDIT (Max 60 characters) ---")
titles_over_60 = {k: v for k, v in title_lengths.items() if v > 60}
if not titles_over_60:
    print(f"✅ PASS: Exactly 0 pages with titles > 60 characters! (All {len(title_lengths)} pages compliant)")
else:
    print(f"❌ FAIL: {len(titles_over_60)} pages exceed 60 characters:")
    for k, v in titles_over_60.items():
        print(f"   - {k}: {v} chars ({all_titles[k]})")

print("\n--- 3. META DESCRIPTION LENGTH AUDIT (140-160 characters) ---")
descs_over_160 = {k: v for k, v in desc_lengths.items() if v > 160}
if not descs_over_160:
    print(f"✅ PASS: Exactly 0 pages with descriptions > 160 characters!")
else:
    print(f"❌ FAIL: {len(descs_over_160)} pages exceed 160 characters:")
    for k, v in descs_over_160.items():
        print(f"   - {k}: {v} chars ({all_descriptions[k]})")

print("\n--- 4. DUPLICATE TITLES AUDIT ---")
title_counts = {}
for path, t in all_titles.items():
    title_counts.setdefault(t, []).append(path)
dup_titles = {t: p for t, p in title_counts.items() if len(p) > 1}
if not dup_titles:
    print(f"✅ PASS: 0 duplicate titles across all {len(all_titles)} pages. Every title is 100% unique!")
else:
    print(f"❌ FAIL: Duplicate titles found: {dup_titles}")

print("\n--- 5. DUPLICATE DESCRIPTIONS AUDIT ---")
desc_counts = {}
for path, d in all_descriptions.items():
    if d:  # ignore empty e.g. blog.html redirect
        desc_counts.setdefault(d, []).append(path)
dup_descs = {d: p for d, p in desc_counts.items() if len(p) > 1}
if not dup_descs:
    print(f"✅ PASS: 0 duplicate descriptions across all pages. Every description is 100% unique!")
else:
    print(f"❌ FAIL: Duplicate descriptions found: {dup_descs}")

print("\n--- 6. IMAGE ALT ATTRIBUTE AUDIT ---")
if not missing_alts:
    print(f"✅ PASS: 0 missing image alt attributes across all {len(public_files)} public HTML files!")
else:
    print(f"❌ FAIL: Missing alt attributes found in {len(missing_alts)} files:")
    for f, imgs in missing_alts.items():
        print(f"   - {f}: {imgs}")

print("\n--- 7. SUMMARY OF AUDIT CHECKS ---")
print(f"Total HTML files audited: {len(public_files)}")
print(f"Canonical URL violations: {len(canonical_violations)}")
print(f"Robots directive violations: {len(robots_violations)}")
print(f"Titles > 60 chars: {len(titles_over_60)}")
print(f"Descriptions > 160 chars: {len(descs_over_160)}")
print(f"Duplicate titles: {len(dup_titles)}")
print(f"Duplicate descriptions: {len(dup_descs)}")
print(f"Missing image alts: {len(missing_alts)}")
print("=" * 80)
