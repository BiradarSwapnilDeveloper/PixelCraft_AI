import os
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def deep_audit():
    tree = ET.parse('public/sitemap.xml')
    root = tree.getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap_urls = [elem.text.strip() for elem in root.findall('.//s:loc', ns)]
    
    results = []
    
    for url in sitemap_urls:
        rel = url.replace('https://pixelcraftaitools.com/', '')
        if rel == '' or rel == '/':
            fp = 'public/index.html'
        else:
            fp = os.path.join('public', rel.replace('/', os.sep))
            
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Title
        title = soup.title.string.strip() if soup.title and soup.title.string else ''
        
        # Meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        desc = desc_tag['content'].strip() if desc_tag and desc_tag.get('content') else ''
        
        # Canonical
        canon_tag = soup.find('link', attrs={'rel': 'canonical'})
        canon = canon_tag['href'].strip() if canon_tag and canon_tag.get('href') else ''
        
        # Robots
        robots_tag = soup.find('meta', attrs={'name': 'robots'})
        robots = robots_tag['content'].strip() if robots_tag and robots_tag.get('content') else 'DEFAULT (index, follow)'
        
        # H1 tags
        h1s = [h.get_text(strip=True) for h in soup.find_all('h1')]
        
        # JSON-LD Schema (Extract BEFORE decomposing script tags)
        schemas = soup.find_all('script', attrs={'type': 'application/ld+json'})
        schema_types = []
        for s in schemas:
            if s.string:
                for match in re.findall(r'"@type":\s*"([^"]+)"', s.string):
                    schema_types.append(match)
                    
        # Word count (excluding scripts, styles)
        for s in soup(['script', 'style', 'noscript', 'svg']):
            s.decompose()
        text = soup.get_text(separator=' ')
        words = len(re.findall(r'\b\w+\b', text))
        
        results.append({
            'url': url,
            'file': fp,
            'title_len': len(title),
            'desc_len': len(desc),
            'canon_matches': canon == url,
            'canon': canon,
            'robots': robots,
            'word_count': words,
            'h1_count': len(h1s),
            'schema_types': schema_types
        })
        
    print(f"{'URL':<55} | Words | H1 | Canon | Schema Types")
    print("-" * 105)
    for r in results:
        short_url = r['url'].replace('https://pixelcraftaitools.com', '') or '/'
        canon_str = 'OK' if r['canon_matches'] else f"ERR({r['canon']})"
        schemas_str = ', '.join(r['schema_types'][:3]) if r['schema_types'] else 'NONE'
        print(f"{short_url:<55} | {r['word_count']:<5} | {r['h1_count']:<2} | {canon_str:<5} | {schemas_str}")

if __name__ == '__main__':
    deep_audit()
