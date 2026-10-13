import tool_content_batch4

# phishing-scanner
phish_check = '''
      <div style="margin-top: 24px; padding: 22px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
        <h4 style="color: var(--text-heading); font-size: 1.2rem; margin-bottom: 12px;">Operational Security Incident Response Checklist</h4>
        <ul style="padding-left: 20px; color: var(--text-body); font-size: 0.95rem; line-height: 1.8;">
          <li><strong>Punycode Verification:</strong> Verify that the host domain does not begin with <code>xn--</code> unless specifically expected from legitimate non-Latin regional organizations.</li>
          <li><strong>Entropy Scoring:</strong> Confirm that the domain Shannon entropy does not exceed 3.8, ruling out automated Domain Generation Algorithms (DGA).</li>
          <li><strong>IP-Literal Detection:</strong> Ensure the URL authority does not contain raw IPv4 or bracketed IPv6 addresses bypassing DNS reputation filters.</li>
          <li><strong>Delimiter Inspection:</strong> Check for obfuscated authentication delimiters (<code>@</code>, <code>%40</code>, <code>//</code>) attempting authority diversion.</li>
          <li><strong>Sinkhole Isolation:</strong> Never navigate to suspect URLs in production desktop browsers without sandboxed network isolation or dedicated threat intel tooling.</li>
        </ul>
      </div>
'''

# smart-resize
resize_check = '''
      <div style="margin-top: 24px; padding: 22px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
        <h4 style="color: var(--text-heading); font-size: 1.2rem; margin-bottom: 12px;">Multi-Platform Production Resizing Checklist</h4>
        <ul style="padding-left: 20px; color: var(--text-body); font-size: 0.95rem; line-height: 1.8;">
          <li><strong>Social Card Dimensions:</strong> Verify that Open Graph banner artwork strictly matches $1200 \times 630\text{ pixels}$ with critical typography within the central safe area.</li>
          <li><strong>Mobile DPR Compensation:</strong> Export high-density assets at $2\times$ or $3\times$ hardware pixel resolutions to prevent blurring on OLED and Retina displays.</li>
          <li><strong>Aspect Ratio Locking:</strong> Double-check that proportional scaling constraints are enabled to prevent vertical or horizontal image stretching.</li>
          <li><strong>Format Compatibility:</strong> Select modern WebP format for web delivery or lossless PNG for UI icons and screenshots requiring transparency.</li>
          <li><strong>Batch Verification:</strong> Review downscaled asset file sizes to ensure individual thumbnails remain under 80KB for fast mobile cellular page loads.</li>
        </ul>
      </div>
'''

# watermark-adder
water_check = '''
      <div style="margin-top: 24px; padding: 22px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
        <h4 style="color: var(--text-heading); font-size: 1.2rem; margin-bottom: 12px;">Intellectual Property &amp; DMCA Compliance Checklist</h4>
        <ul style="padding-left: 20px; color: var(--text-body); font-size: 0.95rem; line-height: 1.8;">
          <li><strong>Visible Watermark Placement:</strong> Ensure semi-transparent branding overlays high-entropy focal points to resist automated AI inpainting tools.</li>
          <li><strong>Sub-Pixel Contrast Shadow:</strong> Verify that typography incorporates black drop shadow outlines to maintain readability against both bright skies and deep shadows.</li>
          <li><strong>EXIF Copyright Synchronization:</strong> Embed creator byline, copyright year, and licensing URL tags into the image container headers.</li>
          <li><strong>DMCA Section 1202 Protection:</strong> Maintain master un-watermarked raw originals in secure offline cold storage as non-repudiable legal evidence.</li>
          <li><strong>Lossless Master Archive:</strong> Always keep a pristine, uncompressed master backup before applying watermarks for public web syndication.</li>
        </ul>
      </div>
'''

c_phish = tool_content_batch4.BATCH_4['phishing-scanner.html']['guide']
idx = c_phish.rfind('</article>')
tool_content_batch4.BATCH_4['phishing-scanner.html']['guide'] = c_phish[:idx] + phish_check + '\n\n' + c_phish[idx:]

c_resize = tool_content_batch4.BATCH_4['smart-resize.html']['guide']
idx = c_resize.rfind('</article>')
tool_content_batch4.BATCH_4['smart-resize.html']['guide'] = c_resize[:idx] + resize_check + '\n\n' + c_resize[idx:]

c_water = tool_content_batch4.BATCH_4['watermark-adder.html']['guide']
idx = c_water.rfind('</article>')
tool_content_batch4.BATCH_4['watermark-adder.html']['guide'] = c_water[:idx] + water_check + '\n\n' + c_water[idx:]

with open('tool_content_batch4.py', 'w', encoding='utf-8') as f:
    f.write('BATCH_4 = {}\n\n')
    for k, v in tool_content_batch4.BATCH_4.items():
        f.write(f'BATCH_4[{repr(k)}] = {{\n')
        f.write(f'    "related": {repr(v["related"])},\n')
        f.write(f'    "guide": {repr(v["guide"])}\n')
        f.write('}\n\n')

print("Batch 4 polished successfully.")
