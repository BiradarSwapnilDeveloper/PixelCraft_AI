import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

def run_audit():
    print("==================================================================")
    print("PIXELCRAFT AI — GSC INDEXING & TECHNICAL SEO DEEP AUDIT")
    print("==================================================================")
    
    # 1. Sitemap check
    sitemap_path = 'public/sitemap.xml'
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap_urls = [elem.text.strip() for elem in root.findall('.//s:loc', ns)]
    
    print(f"\n1. Sitemap URL Count: {len(sitemap_urls)}")
    
    # 2. Check all public HTML files
    all_html_files = []
    for root_dir, _, files in os.walk('public'):
        for f in files:
            if f.endswith('.html') and not f.endswith('.bak'):
                all_html_files.append(os.path.join(root_dir, f))
                
    print(f"2. Total Public HTML Files: {len(all_html_files)}")
    
    # Map files to canonical and robots
    file_data = {}
    canonical_to_files = {}
    
    for file_path in all_html_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        canon_match = re.search(r'<link[^>]+rel=[\'"]canonical[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', content, re.I)
        if not canon_match:
            canon_match = re.search(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]canonical[\'"]', content, re.I)
        canonical = canon_match.group(1).strip() if canon_match else None
        
        robots_match = re.search(r'<meta[^>]+name=[\'"]robots[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', content, re.I)
        robots = robots_match.group(1).strip() if robots_match else None
        
        googlebot_match = re.search(r'<meta[^>]+name=[\'"]googlebot[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', content, re.I)
        googlebot = googlebot_match.group(1).strip() if googlebot_match else None
        
        refresh_match = re.search(r'<meta[^>]+http-equiv=[\'"]refresh[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', content, re.I)
        meta_refresh = refresh_match.group(1).strip() if refresh_match else None
        
        # Word count & title
        title_match = re.search(r'<title>([^<]+)</title>', content, re.I)
        title = title_match.group(1).strip() if title_match else ''
        
        file_data[file_path] = {
            'canonical': canonical,
            'robots': robots,
            'googlebot': googlebot,
            'meta_refresh': meta_refresh,
            'title': title,
            'size': len(content)
        }
        
        if canonical:
            if canonical not in canonical_to_files:
                canonical_to_files[canonical] = []
            canonical_to_files[canonical].append(file_path)

    # 3. Mismatches between Sitemap and Canonicals
    print("\n--- Canonical vs Sitemap Analysis ---")
    sitemap_set = set(sitemap_urls)
    
    for s_url in sitemap_urls:
        rel = s_url.replace('https://pixelcraftaitools.com/', '')
        if rel == '' or rel == '/':
            fp = os.path.normpath('public/index.html')
        else:
            fp = os.path.normpath(os.path.join('public', rel))
            
        if fp not in file_data:
            print(f"  ❌ SITEMAP URL NOT FOUND ON DISK: {s_url} -> {fp}")
            continue
            
        data = file_data[fp]
        if data['canonical'] != s_url:
            print(f"  ⚠️ CANONICAL MISMATCH: Sitemap={s_url} vs Tag={data['canonical']} in {fp}")
            
    print(f"  Total Sitemap URLs verified against disk files.")

    # 4. Files not in Sitemap
    print("\n--- Files in public/ NOT in Sitemap ---")
    for fp, d in file_data.items():
        # Derive expected URL
        norm_fp = fp.replace(os.sep, '/')
        clean_path = norm_fp.replace('public/', '')
        if clean_path == 'index.html':
            expected_url = 'https://pixelcraftaitools.com/'
        else:
            expected_url = f'https://pixelcraftaitools.com/{clean_path}'
            
        if expected_url not in sitemap_set:
            print(f"  ℹ️ Not in sitemap: {norm_fp} (Canonical: {d['canonical']}, Robots: {d['robots']}, Refresh: {d['meta_refresh']})")

    # 5. Potential Duplicate / Conflicting Canonicals
    print("\n--- Canonicals with multiple source files ---")
    for canon, files in canonical_to_files.items():
        if len(files) > 1:
            print(f"  ⚠️ Multiple files claim canonical {canon}: {files}")

    # 6. Internal Linking to Non-Canonical variants (e.g. index.html vs /)
    print("\n--- Internal Linking Audit ---")
    index_html_links = {}
    slash_links = {}
    clean_url_links = {}
    
    link_pattern = re.compile(r'href=[\'"]([^\'"#?]+)[\'"]', re.I)
    
    for fp in all_html_files:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        links = link_pattern.findall(content)
        for l in links:
            if 'index.html' in l and not 'blog/index.html' in l:
                index_html_links[fp] = index_html_links.get(fp, 0) + 1
            if l.endswith('blog.html'):
                print(f"  Found link to blog.html in {fp}: {l}")

    print(f"  Total files linking to index.html (non-canonical variant of /): {len(index_html_links)}")
    print(f"  Total link occurrences pointing to index.html: {sum(index_html_links.values())}")

if __name__ == '__main__':
    run_audit()
