import os, json, re
from bs4 import BeautifulSoup

NEW_BLOGS = [
    {
        'file': 'public/blog/passport-and-exam-photo-resizing-guide.html',
        'tool_link': '../tools/smart-resize.html',
        'canonical': 'https://pixelcraftaitools.com/blog/passport-and-exam-photo-resizing-guide.html',
        'title': 'Passport & Exam Photo Resizing Guide | PixelCraft AI'
    },
    {
        'file': 'public/blog/image-watermarking-and-copyright-protection.html',
        'tool_link': '../tools/watermark-adder.html',
        'canonical': 'https://pixelcraftaitools.com/blog/image-watermarking-and-copyright-protection.html',
        'title': 'Image Watermarking & Copyright Guide | PixelCraft AI'
    },
    {
        'file': 'public/blog/color-palette-extraction-and-design-systems.html',
        'tool_link': '../tools/color-palette.html',
        'canonical': 'https://pixelcraftaitools.com/blog/color-palette-extraction-and-design-systems.html',
        'title': 'Color Palette Extraction & Design Guide | PixelCraft AI'
    },
    {
        'file': 'public/blog/ai-voice-dubbing-and-speech-translation.html',
        'tool_link': '../tools/ai-dubbing.html',
        'canonical': 'https://pixelcraftaitools.com/blog/ai-voice-dubbing-and-speech-translation.html',
        'title': 'AI Voice Dubbing & Speech Translation | PixelCraft AI'
    },
    {
        'file': 'public/blog/compiling-scanned-images-to-pdf-documents.html',
        'tool_link': '../tools/images-to-pdf.html',
        'canonical': 'https://pixelcraftaitools.com/blog/compiling-scanned-images-to-pdf-documents.html',
        'title': 'Compiling Scanned Images to PDF Guide | PixelCraft AI'
    }
]

def test_new_blogs():
    with open('public/sitemap.xml', 'r', encoding='utf-8') as f:
        sitemap_content = f.read()
        
    with open('public/blog/index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()

    for item in NEW_BLOGS:
        filepath = item['file']
        assert os.path.exists(filepath), f"File {filepath} does not exist"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Title
        title = soup.find('title').get_text().strip()
        assert title == item['title'], f"Title mismatch in {filepath}: '{title}' vs expected '{item['title']}'"
        assert len(title) <= 60, f"Title length exceeds 60: {len(title)}"
        
        # 2. Description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        assert desc_tag is not None, f"Missing meta description in {filepath}"
        desc = desc_tag['content'].strip()
        assert len(desc) <= 160, f"Description length exceeds 160: {len(desc)}"
        
        # 3. Canonical
        canon_tag = soup.find('link', attrs={'rel': 'canonical'})
        assert canon_tag is not None, f"Missing canonical tag in {filepath}"
        assert canon_tag['href'] == item['canonical'], f"Canonical mismatch in {filepath}"
        
        # 4. H1
        h1s = soup.find_all('h1')
        assert len(h1s) == 1, f"Expected 1 H1 in {filepath}, found {len(h1s)}"
        
        # 5. Heading hierarchy
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        h_levels = [int(h.name[1]) for h in headings]
        for i in range(len(h_levels) - 1):
            assert h_levels[i+1] <= h_levels[i] + 1, f"Heading skip in {filepath}: {h_levels[i]} -> {h_levels[i+1]}"
            
        # 6. Structured data
        script = soup.find('script', type='application/ld+json')
        assert script is not None, f"Missing JSON-LD in {filepath}"
        data = json.loads(script.string)
        assert data.get('@type') == 'BlogPosting', f"Expected BlogPosting schema in {filepath}"
        assert data.get('headline'), f"Missing headline in schema in {filepath}"
        assert data.get('mainEntityOfPage') == item['canonical'], f"Schema mainEntityOfPage mismatch in {filepath}"
        
        # 7. Contextual tool link
        tool_links = [a['href'] for a in soup.find_all('a', href=True) if item['tool_link'] in a['href']]
        assert len(tool_links) >= 1, f"Missing link to target tool {item['tool_link']} in {filepath}"
        
        # 8. Sitemap inclusion
        filename = os.path.basename(filepath)
        assert filename in sitemap_content, f"{filename} not found in sitemap.xml"
        
        # 9. Blog index discoverability
        assert filename in index_content, f"{filename} not found in blog/index.html"
        
        print(f"✅ {filename}: PASS (Title: {len(title)}c, Desc: {len(desc)}c, 1 H1, Schema OK, Tool Linked, Sitemap OK, Index OK)")

    print("\n🎉 ALL 5 NEW STRATEGIC BLOG ARTICLES PASSED ALL TESTS FLAWLESSLY!")

if __name__ == '__main__':
    test_new_blogs()
