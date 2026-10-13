import tool_content_batch3

# image-filters
filt_tip = '''
      <div style="margin-top: 24px; padding: 20px; background: var(--surface-subtle); border-radius: 12px; border-left: 4px solid #ef4444;">
        <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">WebGL Context Loss &amp; Memory Management</h4>
        <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
          Mobile operating systems (particularly iOS Safari and Android Chrome) aggressively reclaim GPU texture memory when background tabs consume resources. If the browser fires a <code>webglcontextlost</code> event, PixelCraft AI listens for the signal and automatically falls back to CPU-based WebAssembly SIMD pixel rendering. This fail-safe architecture ensures that users never experience frozen canvases, black preview boxes, or lost editing progress during extended creative retouching sessions.
        </p>
      </div>
'''

# pdf-to-link
link_tip = '''
      <div style="margin-top: 24px; padding: 20px; background: var(--surface-subtle); border-radius: 12px; border-left: 4px solid #3b82f6;">
        <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Memory Lifecycle: Blob URL Revocation &amp; Heap Cleanup</h4>
        <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
          In browser memory architectures, creating ephemeral URLs via <code>URL.createObjectURL(decryptedBlob)</code> registers an internal heap pointer that persists until the window document is unloaded. When handling confidential financial statements or medical PDF scans, lingering in-memory blobs can represent an unintended side-channel vulnerability if another user shares the same terminal. PixelCraft AI invokes <code>URL.revokeObjectURL()</code> immediately following viewer rendering or document download, explicitly zeroing out cryptographic references and ensuring immediate garbage collection from host workstation RAM.
        </p>
      </div>
'''

c_filt = tool_content_batch3.BATCH_3['image-filters.html']['guide']
idx = c_filt.rfind('</article>')
tool_content_batch3.BATCH_3['image-filters.html']['guide'] = c_filt[:idx] + filt_tip + '\n\n' + c_filt[idx:]

c_link = tool_content_batch3.BATCH_3['pdf-to-link.html']['guide']
idx = c_link.rfind('</article>')
tool_content_batch3.BATCH_3['pdf-to-link.html']['guide'] = c_link[:idx] + link_tip + '\n\n' + c_link[idx:]

with open('tool_content_batch3.py', 'w', encoding='utf-8') as f:
    f.write('BATCH_3 = {}\n\n')
    for k, v in tool_content_batch3.BATCH_3.items():
        f.write(f'BATCH_3[{repr(k)}] = {{\n')
        f.write(f'    "related": {repr(v["related"])},\n')
        f.write(f'    "guide": {repr(v["guide"])}\n')
        f.write('}\n\n')

print("Batch 3 polished.")
