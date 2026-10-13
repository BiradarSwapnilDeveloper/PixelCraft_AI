import tool_content_batch2

current = tool_content_batch2.BATCH_2['format-converter.html']['guide']
extra = '''
        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q8: How does progressive rendering compare between interlaced PNG and progressive JPEG?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            Progressive JPEG stores spectral selection and successive approximation coefficients across multiple spectral scans (typically 3 to 10 passes). On slow cellular networks, the browser renders a low-resolution full-frame blur immediately, progressively refining fine spatial details as packets arrive. In contrast, interlaced PNG utilizes Adam7 interlacing, organizing pixels into a 7-pass 8x8 pattern grid. While both improve perceived loading speed, progressive JPEGs typically compress 2% to 3% tighter than baseline JPEGs, whereas Adam7 PNGs swell file sizes by roughly 10% due to disrupted scanline filtering efficiency.
          </p>
        </div>
'''
idx = current.rfind('</article>')
tool_content_batch2.BATCH_2['format-converter.html']['guide'] = current[:idx] + extra + '\n\n' + current[idx:]

with open('tool_content_batch2.py', 'w', encoding='utf-8') as f:
    f.write('BATCH_2 = {}\n\n')
    for k, v in tool_content_batch2.BATCH_2.items():
        f.write(f'BATCH_2[{repr(k)}] = {{\n')
        f.write(f'    "related": {repr(v["related"])},\n')
        f.write(f'    "guide": {repr(v["guide"])}\n')
        f.write('}\n\n')
print('Updated format-converter')
