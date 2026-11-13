import glob, os, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

all_html = glob.glob('public/**/*.html', recursive=True)

broken_links = []
empty_links = []

for f in sorted(all_html):
    with open(f, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp.read(), 'html.parser')
    dir_name = os.path.dirname(f)
    
    for a in soup.find_all('a'):
        href = a.get('href', '').strip()
        if not href or href == '#':
            empty_links.append((f, a.get_text(strip=True)[:40], str(a)[:80]))
            continue
            
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
            continue
            
        # Parse internal link
        clean_href = href.split('#')[0].split('?')[0]
        if not clean_href:
            continue
            
        target_path = os.path.normpath(os.path.join(dir_name, clean_href))
        if not os.path.exists(target_path):
            broken_links.append((f, href, target_path))

print(f"Total HTML files crawled: {len(all_html)}")
print(f"Broken internal links: {len(broken_links)}")
for src, href, tgt in broken_links:
    print(f"  ❌ {src} -> '{href}' (Target does not exist: {tgt})")

print(f"\nEmpty href='#' links: {len(empty_links)}")
for src, txt, tag in empty_links:
    print(f"  ⚠️ {src}: text='{txt}' -> {tag}")
