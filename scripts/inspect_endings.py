import os, re
import tool_content_batch1

for filename in sorted(os.listdir('../public/tools')):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('../public/tools', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # clean as in test_injection
    content_clean = re.sub(r'<!-- SEO/ADSENSE RICH TEXT INJECTION -->.*?<!-- END SEO/ADSENSE RICH TEXT -->', '', content, flags=re.DOTALL)
    content_clean = re.sub(r'<!-- SEO CONTENT FOR [A-Z0-9\-_.]+\.HTML -->\s*<section style="max-width: 1200px;.*?<!-- END SEO CONTENT -->', '', content_clean, flags=re.DOTALL)
    content_clean = re.sub(r'<!-- SEO CONTENT FOR [A-Z0-9\-_.]+\.HTML -->\s*<section style="max-width: 1200px;.*?</section>', '', content_clean, flags=re.DOTALL)
    content_clean = re.sub(r'<!-- RELATED TOOLS FOR SEO INTERNAL LINKING -->.*?<!-- END RELATED TOOLS -->', '', content_clean, flags=re.DOTALL)
    content_clean = re.sub(r'<footer class="footer".*?</footer>', '', content_clean, flags=re.DOTALL)
    content_clean = re.sub(r'<!-- GLOBAL FOOTER -->.*?<!-- MASSIVE LEGAL FOOTER FOR ADSENSE -->', '', content_clean, flags=re.DOTALL)
    
    content_clean = content_clean.strip()
    print(f"=== {filename} ===")
    print("  utils.js count:", content_clean.count("utils.js"))
    print("  Ends with:", repr(content_clean[-90:]))
