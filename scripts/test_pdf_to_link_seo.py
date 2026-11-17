import os, re, json
from bs4 import BeautifulSoup

def test_pdf_to_link():
    filepath = 'public/tools/pdf-to-link.html'
    assert os.path.exists(filepath), f"File {filepath} not found"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Title & Meta
    title = soup.find('title').text.strip()
    assert len(title) <= 60, f"Title length {len(title)} exceeds 60: '{title}'"
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    assert len(meta_desc) <= 160, f"Description length {len(meta_desc)} exceeds 160: '{meta_desc}'"
    
    # 2. Heading hierarchy
    h1s = soup.find_all('h1')
    assert len(h1s) == 1, f"Expected 1 H1, found {len(h1s)}"
    
    # 3. Schema.org FAQPage parity
    schema_questions = []
    script = soup.find('script', type='application/ld+json')
    data = json.loads(script.string)
    for item in data.get('@graph', []):
        if item.get('@type') == 'FAQPage':
            for q in item.get('mainEntity', []):
                schema_questions.append(q.get('name'))
    
    guide = soup.find('section', class_='tool-guide-section')
    assert guide is not None, "Missing tool-guide-section"
    
    visible_questions = []
    for h4 in guide.find_all('h4'):
        text = h4.text.strip()
        if re.match(r'Q\d+:', text):
            q_clean = re.sub(r'Q\d+:\s*', '', text)
            visible_questions.append(q_clean)
            
    print(f"Schema FAQ questions count: {len(schema_questions)}")
    print(f"Visible FAQ questions count: {len(visible_questions)}")
    assert len(schema_questions) == len(visible_questions), f"FAQ count mismatch: {len(schema_questions)} schema vs {len(visible_questions)} visible"
    
    for sq, vq in zip(schema_questions, visible_questions):
        assert sq == vq, f"Question mismatch:\nSchema: '{sq}'\nVisible: '{vq}'"
        
    # 4. Guide word count
    guide_clean = re.sub(r'<[^>]+>', ' ', str(guide))
    guide_words = len(guide_clean.split())
    print(f"Guide word count: {guide_words} words")
    assert guide_words >= 1850, f"Guide words {guide_words} below 1850"
    
    # 5. Verify zero cross-tool leakage
    assert 'compressToTargetBytes' not in html, "Image Compressor logic leaked into PDF to Link!"
    assert 'btn-preset-kb' not in html, "Image Compressor preset classes leaked into PDF to Link!"
    assert 'isConverting' not in html, "Format Converter lock leaked into PDF to Link!"
    assert 'socialPresets' not in html, "Smart Resize presets leaked into PDF to Link!"
    assert 'new jsPDF' not in html, "jsPDF leaked into PDF to Link!"
    assert 'Exifr.parse' not in html, "Exifr leaked into PDF to Link!"
    
    print("✅ All pdf-to-link.html tests PASSED flawlessly!")

if __name__ == '__main__':
    test_pdf_to_link()
