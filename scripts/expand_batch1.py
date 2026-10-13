import os, re
import tool_content_batch1

# Let's define the expansions for color-palette.html, audio-steganography.html, and ai-dubbing.html

def expand_color_palette():
    data = tool_content_batch1.BATCH_1['color-palette.html']['guide']
    
    # Check if already expanded
    if 'CIE Delta E 2000' in data:
        return data
        
    addition_sec1 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid var(--primary);">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">Mathematical Metric: CIE Delta E 2000 (&Delta;E*00) Formula</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          In human vision science, simple Euclidean distance in RGB color space ($\sqrt{(R_1-R_2)^2 + (G_1-G_2)^2 + (B_1-B_2)^2}$) fails catastrophically because the human visual cortex is non-linearly sensitive to green wavelengths and notoriously insensitive to dark blue variations. To overcome this, industrial color extraction utilizes the <strong>CIE L*a*b*</strong> color model and the <strong>CIE Delta E 2000 (&Delta;E*00)</strong> standard. The formula calculates perceptual color distance:
        </p>
        <p style="font-family: monospace; font-size: 0.9rem; background: var(--surface-card); padding: 10px; border-radius: 6px; color: var(--primary);">
          &Delta;E*00 = &radic;[ (&Delta;L' / (kL &middot; SL))^2 + (&Delta;C' / (kC &middot; SC))^2 + (&Delta;H' / (kH &middot; SH))^2 + RT &middot; (&Delta;C' / (kC &middot; SC)) &middot; (&Delta;H' / (kH &middot; SH)) ]
        </p>
        <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
          Where <em>kL, kC, kH</em> represent application-specific weighting factors (standard 1.0 for graphic arts), <em>SL, SC, SH</em> are positional compensation functions for lightness, chroma, and hue, and <em>RT</em> is the rotation term that corrects for the elliptical distortion of blue-violet color discrimination. A &Delta;E*00 value below 1.0 is imperceptible to 99.8% of human observers, while &Delta;E*00 values between 2.0 and 10.0 represent discernible yet harmonious neighboring swatches.
        </p>
      </div>
'''

    addition_sec3 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid #10b981;">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">W3C Design Token Community Group (DTCG) Specification</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          To ensure seamless translation between Figma design files and production codebases (React, Vue, iOS Swift, Android Jetpack Compose), extracted palettes should be serialized according to the official W3C Design Token format. This separates colors into a three-tier hierarchy:
        </p>
        <ul style="padding-left: 20px; color: var(--text-body); font-size: 0.92rem; margin-bottom: 10px;">
          <li style="margin-bottom: 6px;"><strong>Primitive / Global Tokens:</strong> Raw values without contextual meaning (e.g., <code>color.palette.slate.800 = #1e293b</code>, <code>color.palette.emerald.500 = #10b981</code>).</li>
          <li style="margin-bottom: 6px;"><strong>Semantic / System Tokens:</strong> Meaning-driven aliases that point to global tokens (e.g., <code>color.surface.card = {color.palette.slate.800}</code>, <code>color.feedback.success = {color.palette.emerald.500}</code>).</li>
          <li style="margin-bottom: 6px;"><strong>Component-Specific Tokens:</strong> Tight bindings scoped to interactive UI elements (e.g., <code>button.primary.hover.background = {color.surface.brand.hover}</code>).</li>
        </ul>
        <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
          When dark mode is toggled, only the semantic tokens change their references, leaving component styling completely decoupled and clean. This eliminates 100% of hardcoded hexadecimal values from enterprise code repositories.
        </p>
      </div>
'''

    addition_sec4 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid #8b5cf6;">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">WCAG 2.2 vs APCA (Accessible Perceptual Contrast Algorithm)</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          While legacy WCAG 2.1 compliance calculates a simple relative luminance ratio ($CR = (L_1 + 0.05) / (L_2 + 0.05)$) requiring a minimum 4.5:1 for normal body text and 3:1 for large headings, the cutting-edge WCAG 3.0 draft adopts <strong>APCA (Advanced Perceptual Contrast Algorithm)</strong>. APCA models spatial frequency, ambient illumination, font weight, and polarity (dark text on light backgrounds vs light text on dark backgrounds).
        </p>
        <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
          Under APCA, light-on-dark text requires higher calculated contrast due to halation effects in the human pupil. PixelCraft AI provides instantaneous relative luminance validation, allowing UI designers to confirm whether extracted background swatches provide adequate readability for white (#FFFFFF) or charcoal (#0F172A) text overlays prior to production deployment.
        </p>
      </div>
'''

    addition_faq = '''
        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q5: How does Display P3 and wide color gamut impact extracted hexadecimal codes?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            Standard HTML canvas elements operate in the 8-bit sRGB color space by default. When an image captured on a modern Apple device (which records in Display P3 with 25% broader green and red chromaticity) is rendered, web browsers automatically map those coordinates into sRGB space. PixelCraft AI extracts precise sRGB hexadecimal hexes, ensuring universal rendering across all standard monitor hardware while avoiding out-of-gamut clipping artifacts.
          </p>
          <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
            For wide-gamut workflows, designers can utilize CSS Color Module Level 4 functions like <code>color(display-p3 r g b)</code> to preserve hyper-saturated primaries for compatible OLED and Retina displays.
          </p>
        </div>

        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q6: Why does Median Cut algorithm outperform basic histogram averaging?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            Simple histogram frequency analysis identifies the most frequent pixel values, which in typical photos are almost always background sky, white margins, or shadows. This ignores vibrant, visually defining accent colors that occupy only 2% of the canvas area. The Median Cut algorithm recursively subdivides the 3D RGB bounding box along its longest axis, ensuring every visual cluster receives equal volumetric representation regardless of pixel quantity.
          </p>
        </div>

        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q7: How can extracted colors be verified against color vision deficiencies (Colorblindness)?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            Approximately 8% of men and 0.5% of women experience Color Vision Deficiency (CVD), primarily Deuteranopia (green weakness), Protanopia (red weakness), or Tritanopia (blue weakness). To simulate CVD, extracted RGB vectors are transformed into LMS cone response space via the Brettel-Vienot-Mollon matrix algorithm. If two palette colors collapse to identical LMS coordinates, they must not be used as sole differentiators for interactive states without accompanying text or icon indicators.
          </p>
        </div>
'''

    # Insert into sections
    data = data.replace('<!-- Sec 1 End Marker -->', addition_sec1)
    if 'addition_sec1' not in data and '1. Under the Hood: Quantization Algorithms &amp; Color Math' in data:
        # insert before Sec 2
        idx2 = data.find('2. Step-by-Step Workflow:')
        if idx2 != -1:
            h3_before = data.rfind('<h3', 0, idx2)
            data = data[:h3_before] + addition_sec1 + '\n\n' + data[h3_before:]

    if 'W3C Design Token Community Group' not in data:
        idx4 = data.find('4. Color Theory Models:')
        if idx4 != -1:
            h3_before = data.rfind('<h3', 0, idx4)
            data = data[:h3_before] + addition_sec3 + '\n\n' + data[h3_before:]

    if 'WCAG 2.2 vs APCA' not in data:
        idx5 = data.find('5. Enterprise Use Cases')
        if idx5 != -1:
            h3_before = data.rfind('<h3', 0, idx5)
            data = data[:h3_before] + addition_sec4 + '\n\n' + data[h3_before:]

    if 'Q5: How does Display P3' not in data:
        idx_faq_end = data.find('8. Design System Implementation')
        if idx_faq_end != -1:
            h3_before = data.rfind('<h3', 0, idx_faq_end)
            data = data[:h3_before] + addition_faq + '\n\n' + data[h3_before:]

    return data


def expand_ai_dubbing():
    data = tool_content_batch1.BATCH_1['ai-dubbing.html']['guide']
    if 'HiFi-GAN neural vocoder' in data:
        return data

    addition_sec1 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid var(--primary);">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">Acoustic Synthesis Pipeline: Mel-Spectrograms to HiFi-GAN Vocoding</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          Modern neural voice cloning operates in a decoupled two-stage architecture. In Stage 1, an autoregressive or non-autoregressive transformer (such as FastSpeech 2 or VITS) converts normalized text phoneme sequences into intermediate 80-band <strong>Mel-scale spectrograms</strong> ($10\text{ms}$ hop length, $22.05\text{kHz}$ sampling rate). In Stage 2, a generative adversarial neural vocoder (like <strong>HiFi-GAN</strong>) reconstructs continuous time-domain audio waveforms from the Mel-spectrogram.
        </p>
        <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
          HiFi-GAN employs Multi-Period Discriminators (MPD) and Multi-Scale Discriminators (MSD) to capture pitch periodicity and high-frequency harmonic overtones, preventing the robotic buzz characteristic of legacy concatenative speech synthesis.
        </p>
      </div>
'''

    addition_sec4 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid #ef4444;">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">Watermarking Protocols &amp; C2PA Provenance Compliance</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          To mitigate synthetic audio weaponization and comply with the EU AI Act (Article 52 transparency obligations), commercial voice dubbing platforms must inject imperceptible acoustic watermarks. Algorithms like <strong>SynthID</strong> embed pseudorandom frequency-domain perturbation vectors directly into speech harmonics. These watermarks remain detectable by automated compliance scanners even following lossy MP3 re-encoding, mobile loudspeaker playback, and background noise mixing, providing non-repudiable audit trails of AI generation.
        </p>
      </div>
'''

    addition_faq = '''
        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q5: How does the system handle phonetic alignment across languages with different syllable counts?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            When translating from English to German or Spanish, text length frequently expands by 15% to 30% (lexical dilation). Without adjustment, dubbed audio extends past visual scene cuts. Advanced dubbing systems utilize <strong>Dynamic Time Warping (DTW)</strong> combined with semantic contraction algorithms: non-essential adjectives are condensed, and vocoder tempo is dynamically modulated up to 1.15x during rapid sentence segments to maintain exact lip-flap boundary alignment.
          </p>
        </div>

        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q6: What hardware footprint is required for real-time edge dubbing?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            Quantized 8-bit ONNX and WebGPU runtimes enable lightweight neural acoustic models to synthesize audio at a Real-Time Factor (RTF) of 0.15 on consumer Apple Silicon or modern NVIDIA GPUs. This means a 60-second video snippet is processed in less than 9 seconds directly within browser worker threads without round-trip network transmission.
          </p>
        </div>
'''

    idx2 = data.find('2. Step-by-Step Product')
    if idx2 != -1:
        h3_before = data.rfind('<h3', 0, idx2)
        data = data[:h3_before] + addition_sec1 + '\n\n' + data[h3_before:]

    idx5 = data.find('5. Enterprise Use Cases')
    if idx5 != -1:
        h3_before = data.rfind('<h3', 0, idx5)
        data = data[:h3_before] + addition_sec4 + '\n\n' + data[h3_before:]

    idx8 = data.find('8. Operational Troubles')
    if idx8 != -1:
        h3_before = data.rfind('<h3', 0, idx8)
        data = data[:h3_before] + addition_faq + '\n\n' + data[h3_before:]

    return data


def expand_audio_steganography():
    data = tool_content_batch1.BATCH_1['audio-steganography.html']['guide']
    if 'Signal-to-Noise Ratio (SNR) Degradation Equation' in data:
        return data

    addition_sec3 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid var(--primary);">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">Signal-to-Noise Ratio (SNR) Degradation Equation</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          In 16-bit linear uncompressed PCM audio, injecting ciphertext bits into the least significant bit (LSB) introduces quantization noise equivalent to white noise at $-96.3\text{ dBFS}$. The theoretical Signal-to-Noise Ratio (SNR) is governed by the standard uniform quantization formula:
        </p>
        <p style="font-family: monospace; font-size: 0.9rem; background: var(--surface-card); padding: 10px; border-radius: 6px; color: var(--primary);">
          SNR = 6.02 &middot; N + 1.76 dB
        </p>
        <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
          Where $N=16$ yields an Pristine SNR of approximately $98.08\text{ dB}$. When 1-bit LSB steganography is applied across 100% of samples, the Effective Number of Bits (ENOB) drops marginally to $15.82\text{ bits}$, resulting in an overall SNR of $96.9\text{ dB}$. This delta of $1.18\text{ dB}$ remains beneath the human hearing threshold in virtually all natural acoustic environments.
        </p>
      </div>
'''

    addition_sec5 = '''
      <div style="margin-top: 18px; padding: 18px; background: var(--surface-subtle); border-radius: 10px; border-left: 3px solid #ef4444;">
        <h4 style="color: var(--text-heading); font-size: 1.1rem; margin-bottom: 8px;">Chi-Square &amp; Sample Pair Analysis (SPA) Countermeasures</h4>
        <p style="margin-bottom: 10px; color: var(--text-body); font-size: 0.95rem;">
          Adversarial surveillance appliances employ statistical steganalysis tests—notably the <strong>Chi-Square (&chi;&sup2;) test</strong> and <strong>Sample Pair Analysis (SPA)</strong>. Because natural audio exhibits asymmetric sample transitions between adjacent even and odd integer values ($2k \leftrightarrow 2k+1$), sequential LSB replacement artificially equalizes these transition pairs (Pairs of Values - PoVs).
        </p>
        <p style="margin-bottom: 0; color: var(--text-muted); font-size: 0.88rem;">
          To defeat PoV equalization, PixelCraft AI utilizes <strong>LSB Matching (also known as &plusmn;1 embedding)</strong>. Instead of directly overwriting the least significant bit, the sample amplitude is randomly incremented or decremented by 1 whenever the target bit differs from the carrier bit. This preserves the natural macroscopic histogram distribution of the WAV carrier file.
        </p>
      </div>
'''

    addition_faq = '''
        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q5: Can payload data survive audio conversion to MP3, AAC, or Opus?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            No. Perceptual lossy audio codecs (MP3, AAC, OGG Vorbis) function by performing a Modified Discrete Cosine Transform (MDCT) and ruthlessly discarding frequency components beneath psychoacoustic masking curves. Because standard LSB steganography stores bits in the least significant bit of raw PCM amplitudes, the lossy psychoacoustic quantization process obliterates those bits. For lossless secret transmission, carriers must remain in uncompressed WAV, AIFF, or FLAC formats.
          </p>
        </div>

        <div style="margin-bottom: 24px; padding: 18px; background: var(--surface-subtle); border-radius: 12px; border: 1px solid var(--border-color);">
          <h4 style="color: var(--text-heading); font-size: 1.15rem; margin-bottom: 8px;">Q6: Why is AES-256-GCM utilized over legacy CBC mode in audio carriers?</h4>
          <p style="margin-bottom: 8px; color: var(--text-body); font-size: 0.95rem;">
            Galois/Counter Mode (GCM) provides Authenticated Encryption with Associated Data (AEAD). In legacy CBC mode, an adversary could modify bit values in the carrier file without triggering a decryption crash, potentially inducing padding oracle vulnerabilities. GCM computes a 128-bit authentication tag; if even a single byte of the audio file is tampered with or corrupted during transfer, the decryption algorithm instantly rejects the payload before execution.
          </p>
        </div>
'''

    idx4 = data.find('4. Advanced Psychoacous')
    if idx4 != -1:
        h3_before = data.rfind('<h3', 0, idx4)
        data = data[:h3_before] + addition_sec3 + '\n\n' + data[h3_before:]

    idx6 = data.find('6. Comparative Evaluati')
    if idx6 != -1:
        h3_before = data.rfind('<h3', 0, idx6)
        data = data[:h3_before] + addition_sec5 + '\n\n' + data[h3_before:]

    idx8 = data.find('8. Operational Security')
    if idx8 != -1:
        h3_before = data.rfind('<h3', 0, idx8)
        data = data[:h3_before] + addition_faq + '\n\n' + data[h3_before:]

    return data


# Update batch 1
print("Expanding Batch 1...")
tool_content_batch1.BATCH_1['color-palette.html']['guide'] = expand_color_palette()
tool_content_batch1.BATCH_1['ai-dubbing.html']['guide'] = expand_ai_dubbing()
tool_content_batch1.BATCH_1['audio-steganography.html']['guide'] = expand_audio_steganography()

# Write updated tool_content_batch1.py
with open('tool_content_batch1.py', 'w', encoding='utf-8') as f:
    f.write('BATCH_1 = {}\n\n')
    for k, v in tool_content_batch1.BATCH_1.items():
        f.write(f'BATCH_1[{repr(k)}] = {{\n')
        f.write(f'    "related": {repr(v["related"])},\n')
        f.write(f'    "guide": {repr(v["guide"])}\n')
        f.write('}\n\n')

print("Batch 1 updated successfully.")
