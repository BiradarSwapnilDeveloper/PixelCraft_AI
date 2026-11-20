import os
import json
import re
from bs4 import BeautifulSoup

DATA = {
    'image-compressor.html': {
        'title': 'Compress Image Size in KB Online Free | PixelCraft AI',
        'desc': 'Compress JPG, PNG & WebP images to exact target KB online. Fast in-browser compression with zero server uploads and real-time preview. Free & private.',
        'h1_target': '<h1>Image Compressor</h1>',
        'h1_replace': '<h1>Image Compressor — Reduce Image Size in KB Online</h1>',
        'hero_old': 'Reduce image file size without visible quality loss. See real-time before/after size comparison. Fast & secure. All processing happens locally on your device ensuring enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Compress JPG, PNG, and WebP images to exact KB targets without visible quality loss. Use one-click presets for IBPS, SSC, and UPSC application photos (50KB) and signatures (20KB), or adjust the quality slider with real-time before/after comparison. All processing runs locally in browser memory with zero server uploads.'
    },
    'format-converter.html': {
        'title': 'Image Format Converter: PNG, JPG & WebP | PixelCraft AI',
        'desc': 'Convert images between PNG, JPG, WebP, AVIF & HEIC online for free. Instant batch conversion directly in your browser with zero server uploads. Free & fast.',
        'h1_target': '<h1>Image Format Converter</h1>',
        'h1_replace': '<h1>Image Format Converter — Batch Convert PNG, JPG & WebP</h1>',
        'hero_old': 'Convert images between PNG, JPG, WebP and AVIF formats instantly in your browser. Fast & secure. All processing happens locally on your device ensuring enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Convert images seamlessly between PNG, JPG, WebP, AVIF, and HEIC formats directly in your browser. Batch transcode multiple files at once for web performance, digital publishing, or document submission. Fast client-side conversion with zero server uploads and zero data retention.'
    },
    'qr-generator.html': {
        'title': 'Website QR Code Generator: Custom Logo & Colors | PixelCraft',
        'desc': 'Generate custom QR codes from website links & URLs with brand logos and custom colors. Download high-resolution PNG and vector SVG formats. 100% free & local.',
        'h1_target': '<h1>Free Website QR Code Generator</h1>',
        'h1_replace': '<h1>Custom Website QR Code Generator with Logo & Colors</h1>',
        'hero_old': 'Transform website URLs and links into scannable custom QR codes. Customize colors, add your brand logo, choose modern dot shapes, and download print-ready PNG or infinite vector SVG. 100% private, client-side, and free forever.',
        'hero_new': 'Generate custom QR codes from website URLs and links with your custom brand colors, center logo, and high error correction (Level H). Download crisp high-resolution PNG or vector SVG files ready for digital sharing and professional print. 100% private, client-side, and free.'
    },
    'smart-resize.html': {
        'title': 'Photo Resizer: Resize Images in Pixels, CM & KB | PixelCraft',
        'desc': 'Resize photos by exact pixels, millimeters, or aspect ratios. Perfect for passport photos, exam application forms & social media presets. In-browser & free.',
        'h1_target': '<h1>Photo Resizer &amp; Aspect Ratio Optimizer</h1>',
        'h1_replace': '<h1>Photo Resizer &amp; Aspect Ratio Optimizer for Passport &amp; Forms</h1>',
        'hero_old': 'Resize photos and graphics by exact width, height, aspect ratio, or social media presets. Format passport photos, exam signatures, banners, and posts with instant client-side processing.',
        'hero_new': 'Resize photos and digital graphics by exact pixels, millimeters, or aspect ratios. Features dedicated presets for Indian passport photos (35×45 mm), exam application signatures, and social media platforms (Instagram, YouTube, LinkedIn). Fast, private browser execution.'
    },
    'images-to-pdf.html': {
        'title': 'Images to PDF Converter: Merge Photos to PDF | PixelCraft AI',
        'desc': 'Convert JPG, PNG & photos into a single clean PDF online. Drag to reorder pages, customize margins, and export with zero watermarks. Private in-browser tool.',
        'h1_target': '<h1>Images to PDF Converter</h1>',
        'h1_replace': '<h1>Images to PDF Converter — Merge Multiple Photos to PDF</h1>',
        'hero_old': 'Convert multiple images into a secure, high-quality PDF. Drag to reorder, set page sizes, and add password protection. Fast & secure. All processing happens locally on your device ensuring enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Merge multiple JPG, PNG, and WebP images into a clean, single PDF document in seconds. Drag and drop thumbnails to reorder pages, adjust page layout and margins, and export high-resolution PDFs with zero watermarks. Executes 100% client-side for maximum privacy.'
    },
    'exif-viewer.html': {
        'title': 'EXIF Data Viewer: Inspect Photo Metadata & GPS | PixelCraft',
        'desc': 'Inspect camera telemetry, GPS coordinates, exposure settings, shutter speed, and hidden EXIF/IPTC metadata from photos. 100% private in-browser inspection.',
        'h1_target': '<h1>EXIF Data Viewer</h1>',
        'h1_replace': '<h1>EXIF Data Viewer — Inspect Camera Settings &amp; Geolocation</h1>',
        'hero_old': 'View hidden metadata inside your photos: camera, date, GPS coordinates, exposure settings and more. Fast & secure. All processing happens locally on your device ensuring enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Inspect hidden metadata inside photos: camera manufacturer, lens model, shutter speed, ISO, timestamp, and embedded GPS coordinates. Verify what private telemetry is stored in your images before sharing online. Runs entirely on your device with complete privacy.'
    },
    'phishing-scanner.html': {
        'title': 'Phishing Link Scanner: Check Suspicious URLs | PixelCraft AI',
        'desc': 'Scan suspicious URLs and links for homograph attacks, deceptive domains, and scam redirects using heuristic threat analysis. Instant URL safety assessment.',
        'h1_target': '<h1>Deep Phishing &amp; Malware Scanner</h1>',
        'h1_replace': '<h1>Deep Phishing Link &amp; Suspicious URL Scanner</h1>',
        'hero_old': 'Advanced AI heuristic engine to detect homograph attacks, typosquatting, unmasked shorteners, and malicious domains. Scans are processed in isolated server memory and discarded immediately without logging browsing history.',
        'hero_new': 'Inspect suspicious links and web addresses for IDN homograph spoofing, typosquatting domains, and deceptive redirects using heuristic threat analysis. Evaluates URL entropy and risk indicators in isolated server memory with zero tracking of your browsing history.'
    },
    'ai-dubbing.html': {
        'title': 'AI Voice & Video Dubbing: Multi-Language Speech | PixelCraft',
        'desc': 'Translate and dub audio & video speech into Hindi, English, Spanish, and French. Neural voice translation with synchronized preview and audio export.',
        'h1_target': '<h1>AI Audio &amp; Video Dubbing</h1>',
        'h1_replace': '<h1>AI Audio &amp; Video Dubbing — Neural Speech Localization</h1>',
        'hero_old': 'Upload a media file to automatically transcribe, translate, and synthesize speech in your target language.',
        'hero_new': 'Translate and dub spoken audio and video recordings into Hindi, English, Spanish, French, and other global languages. Uses neural speech recognition and voice synthesis to generate synchronized translated speech with real-time playback and audio download.'
    },
    'pdf-to-link.html': {
        'title': 'PDF to Link Converter: Share PDF via Web Link | PixelCraft',
        'desc': 'Convert PDF files into shareable web links and QR codes instantly. Share resumes, guides, and documents easily with automatic 24-hour privacy purge.',
        'h1_target': '<h1 style="background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PDF to Link Converter</h1>',
        'h1_replace': '<h1 style="background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PDF to Link Converter — Share Documents via Secure URL</h1>',
        'hero_old': 'Upload any PDF document and instantly get a beautiful, shareable link and QR code.100% Free, secure, and blazing fast. Fast & secure. Temporarily uploads to our secure servers and deletes after 24 hours for enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Turn PDF documents, portfolios, and reports into clean, shareable web links and scannable QR codes instantly. Share documents easily across messaging platforms and social channels with automatic 24-hour privacy destruction and zero permanent storage.'
    },
    'audio-steganography.html': {
        'title': 'Audio & Video Steganography: Hide Secret Data | PixelCraft',
        'desc': 'Embed AES-256 encrypted messages and files inside WAV audio and MP4 video containers without audible distortion. Client-side cryptographic processing.',
        'h1_target': '<h1>Audio &amp; Video Steganography</h1>',
        'h1_replace': '<h1>Audio &amp; Video Steganography — Hide Secret Payloads in Media</h1>',
        'hero_old': 'Embed encrypted classified payloads into media files with Quantization Index Modulation and AES-256 cryptography.',
        'hero_new': 'Embed encrypted confidential messages and files inside WAV audio tracks and MP4 video containers without audible distortion. Utilizes AES-256 encryption and client-side container multiplexing so your hidden payload remains secure and undetectable.'
    },
    'watermark-adder.html': {
        'title': 'Watermark Adder: Add Text & Copyright to Photos | PixelCraft',
        'desc': 'Add custom text and copyright watermarks to photos online for free. Customize font, opacity, rotation, and position directly in your browser. 100% private.',
        'h1_target': '<h1>Watermark Adder</h1>',
        'h1_replace': '<h1>Watermark Adder — Protect Photos with Custom Text Watermarks</h1>',
        'hero_old': 'Protect your images with a custom text watermark. Control position, opacity, and font. Fast & secure. All processing happens locally on your device ensuring enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Protect your creative photography and digital artwork with customized text and copyright watermarks. Adjust font family, size, color, opacity, rotation angle, and position with live canvas preview. Batch watermarking executes entirely on your device.'
    },
    'color-palette.html': {
        'title': 'Color Palette Extractor: Extract HEX Codes | PixelCraft AI',
        'desc': 'Extract dominant color palettes, HEX, and RGB codes from photos and graphics instantly. Features one-click HEX copying and PNG palette export for designers.',
        'h1_target': '<h1>Color Palette Extractor</h1>',
        'h1_replace': '<h1>Color Palette Extractor — Extract HEX &amp; RGB Codes from Images</h1>',
        'hero_old': 'Upload any image and instantly extract its dominant colors with HEX and RGB codes. Fast & secure. All processing happens locally on your device ensuring enhanced privacy. Enjoy premium features instantly, completely free and without any registration.',
        'hero_new': 'Extract dominant color palettes, HEX codes, RGB values, and CSS tokens from any image or brand graphic. Features median-cut color clustering, one-click HEX clipboard copying, and PNG palette exports tailored for UI/UX designers, developers, and artists.'
    },
    'digital-fingerprint-wiper.html': {
        'title': 'Digital Fingerprint Wiper: Scrub Camera Noise | PixelCraft',
        'desc': 'Disrupt PRNU sensor signatures and camera hardware fingerprints using frequency noise perturbation. Anonymize photos before sharing online with zero uploads.',
        'h1_target': '<h1 class="tool-header">\n          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>\n          Digital Fingerprint Wiper\n        </h1>',
        'h1_replace': '<h1 class="tool-header">\n          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>\n          Digital Fingerprint Wiper — Scrub Sensor Noise &amp; PRNU Signatures\n        </h1>',
        'hero_old': 'Securely remove sensitive metadata (EXIF) and anonymize your images. This tool adds an invisible protective layer to help prevent unauthorized tracking while keeping your photos looking exactly the same.',
        'hero_new': 'Disrupt PRNU (Photo-Response Non-Uniformity) camera sensor fingerprints and physical device tracking signatures. Injects controlled frequency noise perturbation to scrub hardware forensic identifiers while preserving visible image clarity.'
    },
    'forensic-sanitizer.html': {
        'title': 'Forensic Image Sanitizer: Strip Hidden Metadata | PixelCraft',
        'desc': 'Deep sanitize images by stripping embedded metadata, polyglot payloads, and ICC tracking markers. Sealed cryptographic verification with zero data retention.',
        'h1_target': '<h1>Forensic Image Sanitizer</h1>',
        'h1_replace': '<h1>Forensic Image Sanitizer — Strip Hidden Payloads &amp; Metadata</h1>',
        'hero_old': 'Analyze structural hex payloads, scrub EXIF/IPTC/XMP tracking coordinates, and embed a verifiable cryptographic seal.',
        'hero_new': 'Deep sanitize digital media files by stripping hidden hex payloads, polyglot scripts, ICC color profile trackers, and metadata structures. Generates a verifiable cryptographic SHA-256 seal confirming file integrity with zero server data retention.'
    },
    'advanced-decoy.html': {
        'title': 'Decoy Steganography: Dual Encryption & Canaries | PixelCraft',
        'desc': 'Embed confidential secrets and innocent decoy payloads inside images with dual-password encryption and canary token detection. Private client-side execution.',
        'h1_target': '<h1>Advanced Decoy Steganography</h1>',
        'h1_replace': '<h1>Advanced Decoy Steganography — Dual-Payload Plausible Deniability</h1>',
        'hero_old': 'Plausible deniability encryption with dual-channel payload injection using Quantization Index Modulation.',
        'hero_new': 'Implement plausible deniability steganography by embedding dual-channel payloads inside images: an innocent decoy message under one password and your true confidential payload under another. Includes canary token triggers to detect unauthorized inspection.'
    }
}

IMAGE_COMPRESSOR_FAQS = [
  {
    "@type": "Question",
    "name": "Photo ka size 50KB kaise kare? (How do I compress an image to 50KB?)",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Photo ka size 50KB karne ke liye: apna JPG ya PNG photo upload kare, upar diye gaye \"50KB (Govt Exam Photo / IBPS / UPSC)\" preset button par click kare. Tool automatically binary search karke image quality adjust karega taaki file 50KB ke andar save ho sake (jo IBPS 20-50KB ceiling aur UPSC observed 20-300KB range dono me fit hota hai). Fir Download Compressed Image button dabaye."
    }
  },
  {
    "@type": "Question",
    "name": "Online form ke liye signature ka size 20KB kaise banaye?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Signature ka size 10KB–20KB karne ke liye: signature photo upload kare aur \"20KB (Signature)\" preset select kare. Agar photo mobile se li gayi badi file hai, toh pehle Smart Resizer me jakar dimensions ko 140×60px crop kare, fir yaha compress kare taaki portal par bina error upload ho sake."
    }
  },
  {
    "@type": "Question",
    "name": "Mobile me photo ka size kaise kam kare bina quality kharab kiye?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Apne Android ya iPhone browser me PixelCraft AI open kare, photo select kare aur quality slider ko 75% par set kare. PixelCraft AI browser memory me hi execute hota hai, isliye bina kisi app download ya quality degrade kiye aapka photo turant compress ho jata hai."
    }
  },
  {
    "@type": "Question",
    "name": "Why did my image not reach exactly 20KB or 50KB? (Troubleshooting Target Sizes)",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Lossy JPEG compression modifies color quantization matrices while preserving original pixel dimensions ($W \\times H$). If a high-resolution 12MP smartphone photo (4000×3000px) is uploaded, even at 5% quality the minimum container overhead might be 60KB. In such cases, downsampling pixel dimensions is required to reach strict 20KB targets."
    }
  },
  {
    "@type": "Question",
    "name": "What is the recommended compression quality for web hero banners?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "For high-impact full-width hero backgrounds, set the quality slider between 72% and 78%. At this level, visual differences are imperceptible to users on standard and Retina displays, while file weight is reduced by 70–80% compared to uncompressed camera exports."
    }
  },
  {
    "@type": "Question",
    "name": "Why does client-side compression preserve privacy better than cloud services?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Traditional compression websites require uploading your confidential ID photos, marks cards, and personal pictures to remote servers. PixelCraft AI executes the compression algorithm locally inside your device browser memory via WebAssembly: zero bytes of your photo are ever uploaded to any server."
    }
  },
  {
    "@type": "Question",
    "name": "Does compressing an image strip its EXIF and geolocation metadata?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Yes. When an image is rendered to an HTML5 Canvas and re-encoded, the browser creates a clean container from raw pixel buffers, automatically stripping camera serial numbers, GPS location coordinates, and metadata tags before export."
    }
  }
]

def update_tool(filename, config):
    filepath = os.path.join('public', 'tools', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Update <title>
    content = re.sub(r'<title>[^<]+</title>', f'<title>{config["title"]}</title>', content)
    
    # 2. Update meta description
    content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
        f'<meta name="description" content="{config["desc"]}"/>',
        content
    )
    
    # 3. Update OpenGraph & Twitter title & description
    content = re.sub(
        r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>',
        f'<meta property="og:title" content="{config["title"]}" />',
        content
    )
    content = re.sub(
        r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>',
        f'<meta property="og:description" content="{config["desc"]}" />',
        content
    )
    content = re.sub(
        r'<meta\s+name="twitter:title"\s+content="[^"]*"\s*/?>',
        f'<meta name="twitter:title" content="{config["title"]}" />',
        content
    )
    content = re.sub(
        r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>',
        f'<meta name="twitter:description" content="{config["desc"]}" />',
        content
    )
    
    # 4. Update H1
    if config['h1_target'] in content:
        content = content.replace(config['h1_target'], config['h1_replace'])
    else:
        # Fallback regex for H1 text replacement
        print(f"Notice: exact h1_target not found in {filename}, attempting normalized replacement")
        soup = BeautifulSoup(content, 'html.parser')
        h1 = soup.find('h1')
        if h1:
            raw_h1 = str(h1)
            content = content.replace(raw_h1, config['h1_replace'])
            
    # 5. Update Hero Paragraph
    if config['hero_old'] in content:
        content = content.replace(config['hero_old'], config['hero_new'])
    else:
        print(f"Notice: exact hero_old not found in {filename}")
        
    # 6. Update JSON-LD Script
    soup = BeautifulSoup(content, 'html.parser')
    json_script = soup.find('script', type='application/ld+json')
    if json_script and json_script.string:
        try:
            data = json.loads(json_script.string)
            if '@graph' in data:
                for item in data['@graph']:
                    if item.get('@type') == 'WebPage':
                        item['name'] = config['title']
                        item['description'] = config['desc']
                    elif item.get('@type') == 'SoftwareApplication':
                        item['description'] = config['desc']
                    elif item.get('@type') == 'FAQPage':
                        if filename == 'image-compressor.html':
                            item['mainEntity'] = IMAGE_COMPRESSOR_FAQS
                        elif filename == 'qr-generator.html':
                            for q in item.get('mainEntity', []):
                                if q.get('name', '').startswith('Website ka QR code kaise banaye'):
                                    q['name'] = 'Website ka QR code kaise banaye online free me? (How to create a free website QR code online?)'
                                    
            new_json_str = json.dumps(data, indent=2, ensure_ascii=False)
            # Replace old script text with new script text
            # Find the script tag in content
            s_open = content.find('<script type="application/ld+json">')
            if s_open != -1:
                s_close = content.find('</script>', s_open)
                content = content[:s_open + len('<script type="application/ld+json">')] + '\n' + new_json_str + '\n  ' + content[s_close:]
        except Exception as e:
            print(f"Error parsing JSON-LD in {filename}: {e}")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ Successfully updated {filename}")

if __name__ == '__main__':
    for filename, config in DATA.items():
        update_tool(filename, config)
    print("\nAll 15 tools updated successfully.")
