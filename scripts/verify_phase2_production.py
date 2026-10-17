import sys, os, glob, json, re
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
TOOLS_DIR = os.path.join(PUBLIC_DIR, 'tools')

tools = [
  'advanced-decoy.html', 'ai-dubbing.html', 'audio-steganography.html',
  'color-palette.html', 'digital-fingerprint-wiper.html', 'exif-viewer.html',
  'forensic-sanitizer.html', 'format-converter.html', 'image-compressor.html',
  'images-to-pdf.html', 'pdf-to-link.html', 'phishing-scanner.html',
  'qr-generator.html', 'smart-resize.html', 'watermark-adder.html'
]

non_tools = [
  'about-us.html', 'contact-us.html', 'cookies-policy.html', 'data-practices.html',
  'disclaimer.html', 'download-app.html', 'login.html', 'privacy-policy.html',
  'terms-conditions.html'
]

def verify_tool(tool_file):
    filepath = os.path.join(TOOLS_DIR, tool_file)
    content = open(filepath, encoding='utf-8').read()
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Title
    title = soup.title.string.strip() if soup.title and soup.title.string else 'MISSING'
    
    # 2. Desc
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    desc = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else 'MISSING'
    
    # 3. Canonical
    canon_tag = soup.find('link', attrs={'rel': 'canonical'})
    canon = canon_tag['href'].strip() if canon_tag and canon_tag.get('href') else 'MISSING'
    
    # 4. H1
    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text(strip=True) if h1_tag else 'MISSING'
    
    # 5. Quick Steps
    has_steps = soup.find(id='quick-start-guide') is not None
    
    # 6. JSON-LD
    json_valid = False
    has_app_schema = False
    has_faq_schema = False
    faq_count = 0
    app_category = None
    script = soup.find('script', attrs={'type': 'application/ld+json'})
    if script:
        try:
            data = json.loads(script.string)
            json_valid = True
            for item in data.get('@graph', []):
                t = item.get('@type')
                if t == 'SoftwareApplication':
                    has_app_schema = True
                    app_category = item.get('applicationCategory')
                elif t == 'FAQPage':
                    has_faq_schema = True
                    faq_count = len(item.get('mainEntity', []))
        except Exception as e:
            json_valid = False
            
    # 7. Check visible FAQs
    m_faq = re.search(r'Frequently Asked Questions', content)
    sub = content[m_faq.start():] if m_faq else ""
    # count visible Q cards
    vis_q_count = len(re.findall(r'Q\d+:', sub))
    
    # 8. Check checklist or table section
    has_section6 = bool(re.search(r'<h3[^>]*>\s*6\.', sub)) or bool(re.search(r'<h3[^>]*>\s*7\.', content))
    
    # 9. Related tools
    has_related = 'Explore More' in content
    
    return {
        'title': title,
        'title_len': len(title),
        'desc_len': len(desc),
        'canonical': canon,
        'h1': h1,
        'has_steps': has_steps,
        'json_valid': json_valid,
        'has_app_schema': has_app_schema,
        'app_category': app_category,
        'has_faq_schema': has_faq_schema,
        'faq_count': faq_count,
        'vis_q_count': vis_q_count,
        'has_section6': has_section6,
        'has_related': has_related
    }

def verify_non_tool(nt_file):
    filepath = os.path.join(PUBLIC_DIR, nt_file)
    content = open(filepath, encoding='utf-8').read()
    soup = BeautifulSoup(content, 'html.parser')
    
    title = soup.title.string.strip() if soup.title and soup.title.string else 'MISSING'
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    desc = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else 'MISSING'
    canon_tag = soup.find('link', attrs={'rel': 'canonical'})
    canon = canon_tag['href'].strip() if canon_tag and canon_tag.get('href') else 'MISSING'
    rob_tag = soup.find('meta', attrs={'name': 'robots'})
    robots = rob_tag['content'].strip() if rob_tag and rob_tag.get('content') else 'MISSING'
    
    return {
        'title': title,
        'title_len': len(title),
        'desc_len': len(desc),
        'canonical': canon,
        'robots': robots
    }

if __name__ == '__main__':
    print("=" * 80)
    print("PIXELCRAFT AI — PHASE 2 PRODUCTION AUDIT REPORT")
    print("=" * 80)
    
    all_tools_pass = True
    print("\n--- ACTIVE 15 TOOLS AUDIT ---")
    for t in tools:
        r = verify_tool(t)
        status = "PASS" if (r['json_valid'] and r['has_app_schema'] and r['has_faq_schema'] and r['has_steps'] and r['has_related']) else "FAIL"
        if status == "FAIL":
            all_tools_pass = False
        print(f"[{status}] {t:30} | Title ({r['title_len']}c) | Desc ({r['desc_len']}c) | FAQs: {r['faq_count']} | Quick Steps: {r['has_steps']}")
        
    print(f"\nAll 15 Tools Verified: {'YES' if all_tools_pass else 'NO'}")
    
    print("\n--- KEY NON-TOOL PAGES AUDIT ---")
    for nt in non_tools:
        r = verify_non_tool(nt)
        print(f"[OK] {nt:25} | Title ({r['title_len']}c) | Desc ({r['desc_len']}c) | Robots: {r['robots'][:20]}")
