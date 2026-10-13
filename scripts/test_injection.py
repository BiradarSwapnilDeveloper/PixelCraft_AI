import os, re
import tool_content_batch1
import tool_content_batch2
import tool_content_batch3
import tool_content_batch4

ALL_BATCHES = {}
ALL_BATCHES.update(tool_content_batch1.BATCH_1)
ALL_BATCHES.update(tool_content_batch2.BATCH_2)
ALL_BATCHES.update(tool_content_batch3.BATCH_3)
ALL_BATCHES.update(tool_content_batch4.BATCH_4)

STANDARD_FOOTER = '''
<footer class="footer" style="background: var(--surface-card); padding: 50px 20px 30px; text-align: center; border-top: 1px solid var(--border-color); margin-top: 60px;">
  <div style="max-width: 1200px; margin: 0 auto;">
    <div style="display: flex; justify-content: center; gap: 28px; flex-wrap: wrap; margin-bottom: 24px;">
      <a href="../about-us.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">About Us</a>
      <a href="../privacy-policy.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Privacy Policy</a>
      <a href="../terms-conditions.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Terms of Service</a>
      <a href="../disclaimer.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Disclaimer</a>
      <a href="../cookies-policy.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Cookies Policy</a>
      <a href="../blog/index.html" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Research</a>
      <a href="../index.html#contact" style="color: var(--text-muted); text-decoration: none; font-weight: 500;">Contact</a>
    </div>
    <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; margin: 0;">
      &copy; 2026 PixelCraft AI. All rights reserved.<br>
      A Decentralized Privacy, Cryptography &amp; Digital Security Toolset.
    </p>
  </div>
</footer>
'''

for filename in sorted(ALL_BATCHES.keys()):
    filepath = os.path.join('../public/tools', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Strip old SEO/AdSense blocks
    c = re.sub(r'<!-- SEO/ADSENSE RICH TEXT INJECTION -->.*?<!-- END SEO/ADSENSE RICH TEXT -->', '', content, flags=re.DOTALL)
    c = re.sub(r'<!-- SEO CONTENT FOR [A-Z0-9\-_.]+\.HTML -->\s*<section style="max-width: 1200px;.*?<!-- END SEO CONTENT -->', '', c, flags=re.DOTALL)
    c = re.sub(r'<!-- SEO CONTENT FOR [A-Z0-9\-_.]+\.HTML -->\s*<section style="max-width: 1200px;.*?</section>', '', c, flags=re.DOTALL)
    c = re.sub(r'<!-- RELATED TOOLS FOR SEO INTERNAL LINKING -->.*?<!-- END RELATED TOOLS -->', '', c, flags=re.DOTALL)
    c = re.sub(r'<footer class="footer".*?</footer>', '', c, flags=re.DOTALL)
    c = re.sub(r'<!-- GLOBAL FOOTER -->.*?<!-- MASSIVE LEGAL FOOTER FOR ADSENSE -->', '', c, flags=re.DOTALL)
    
    # 2. Extract tail: <script src="../js/cookie-consent.js"></script>\s*</body>\s*</html>
    c = re.sub(r'<script src="\.\./js/cookie-consent\.js"></script>\s*</body>\s*</html>\s*$', '', c.strip(), flags=re.DOTALL)
    c = re.sub(r'</body>\s*</html>\s*$', '', c.strip(), flags=re.DOTALL)
    
    batch_data = ALL_BATCHES[filename]
    related_html = batch_data['related'].strip()
    guide_html = batch_data['guide'].strip()
    
    # Assemble full document
    new_doc = f"{c.rstrip()}\n\n{related_html}\n\n{guide_html}\n\n{STANDARD_FOOTER.strip()}\n\n<script src=\"../js/cookie-consent.js\"></script>\n</body>\n</html>\n"
    
    # Count words in guide
    guide_text = re.sub(r'<[^>]+>', ' ', guide_html)
    words = len(guide_text.split())
    
    print(f"Validated {filename:30}: Guide Words: {words:4} | New Length: {len(new_doc):6}")
