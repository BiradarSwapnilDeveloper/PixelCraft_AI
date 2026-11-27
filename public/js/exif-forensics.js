/**
 * PixelCraft AI — Client-Side Forensic EXIF, Binary, Astronomical & AI Provenance Engine
 * 100% browser-local execution (zero server uploads).
 */
(function (global) {
  'use strict';

  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes) || bytes < 0) return '0 B';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function decodeBytesLatin1(bytes, start, end) {
    const slice = bytes.subarray(start, end);
    let out = '';
    const CHUNK = 8192;
    for (let i = 0; i < slice.length; i += CHUNK) {
      out += String.fromCharCode.apply(null, slice.subarray(i, i + CHUNK));
    }
    return out;
  }

  function decodeBytesUtf8(bytes, start, end) {
    const slice = bytes.subarray(start, end);
    try {
      return new TextDecoder('utf-8', { fatal: false }).decode(slice);
    } catch (_) {
      return decodeBytesLatin1(bytes, start, end);
    }
  }

  async function decompressDeflate(bytes) {
    if (typeof DecompressionStream === 'undefined') return null;
    try {
      const ds = new DecompressionStream('deflate');
      const writer = ds.writable.getWriter();
      writer.write(bytes);
      writer.close();
      const buf = await new Response(ds.readable).arrayBuffer();
      return new Uint8Array(buf);
    } catch (_) {
      try {
        const dsRaw = new DecompressionStream('deflate-raw');
        const writer = dsRaw.writable.getWriter();
        writer.write(bytes);
        writer.close();
        const buf = await new Response(dsRaw.readable).arrayBuffer();
        return new Uint8Array(buf);
      } catch (__) {
        return null;
      }
    }
  }

  // =========================================================================
  // 1. CRYPTOGRAPHIC HASHING (SHA-256 & SHA-512)
  // =========================================================================
  async function computeFileHashes(arrayBuffer) {
    const toHex = (buf) =>
      Array.from(new Uint8Array(buf))
        .map((b) => b.toString(16).padStart(2, '0'))
        .join('');
    if (!global.crypto || !global.crypto.subtle) {
      return { sha256: 'WebCrypto unavailable (requires HTTPS/localhost)', sha512: 'Unavailable' };
    }
    try {
      const [h256, h512] = await Promise.all([
        global.crypto.subtle.digest('SHA-256', arrayBuffer),
        global.crypto.subtle.digest('SHA-512', arrayBuffer)
      ]);
      return { sha256: toHex(h256), sha512: toHex(h512) };
    } catch (e) {
      return { sha256: 'Hash error', sha512: 'Hash error' };
    }
  }

  // =========================================================================
  // 2. SHANNON ENTROPY & MAGIC SIGNATURE DETECTION
  // =========================================================================
  function computeShannonEntropy(bytes) {
    if (!bytes || bytes.length === 0) return 0;
    const freq = new Uint32Array(256);
    const len = Math.min(bytes.length, 512 * 1024); // Cap for speed on giant blobs
    for (let i = 0; i < len; i++) freq[bytes[i]]++;
    let entropy = 0;
    for (let i = 0; i < 256; i++) {
      if (freq[i] === 0) continue;
      const p = freq[i] / len;
      entropy -= p * Math.log2(p);
    }
    return entropy;
  }

  function detectMagicSignature(bytes) {
    if (!bytes || bytes.length < 4) return 'Unknown / Small Fragment';
    const b0 = bytes[0], b1 = bytes[1], b2 = bytes[2], b3 = bytes[3];
    if (b0 === 0x50 && b1 === 0x4b && (b2 === 0x03 || b2 === 0x05)) return 'ZIP Archive (PKZIP / DOCX / APK)';
    if (b0 === 0x52 && b1 === 0x61 && b2 === 0x72 && b3 === 0x21) return 'RAR Archive';
    if (b0 === 0x37 && b1 === 0x7a && b2 === 0xbc && b3 === 0xaf) return '7-Zip Archive';
    if (b0 === 0x1f && b1 === 0x8b) return 'GZIP Compressed Stream';
    if (b0 === 0x25 && b1 === 0x50 && b2 === 0x44 && b3 === 0x46) return 'PDF Document (%PDF)';
    if (b0 === 0xff && b1 === 0xd8 && b2 === 0xff) return 'Embedded JPEG Image';
    if (b0 === 0x89 && b1 === 0x50 && b2 === 0x4e && b3 === 0x47) return 'Embedded PNG Image';
    if (bytes.length >= 12) {
      const ftyp = String.fromCharCode(bytes[4], bytes[5], bytes[6], bytes[7]);
      if (ftyp === 'ftyp') {
        const brand = String.fromCharCode(bytes[8], bytes[9], bytes[10], bytes[11]);
        return `ISO BMFF / MP4 Video Container (ftyp${brand})`;
      }
    }
    // Check if mostly printable ASCII/UTF-8
    let printable = 0;
    const sampleLen = Math.min(bytes.length, 256);
    for (let i = 0; i < sampleLen; i++) {
      const c = bytes[i];
      if ((c >= 32 && c <= 126) || c === 9 || c === 10 || c === 13) printable++;
    }
    if (printable / sampleLen > 0.85) return 'Plaintext / Script / JSON Payload';
    const ent = computeShannonEntropy(bytes);
    if (ent > 7.7) return `High-Entropy Encrypted / Compressed Blob (${ent.toFixed(2)} bits/B)`;
    return `Binary Data (${ent.toFixed(2)} bits/B entropy)`;
  }

  function formatHexDump(bytes, baseOffset, maxBytes) {
    const limit = Math.min(bytes.length, maxBytes || 512);
    const lines = [];
    for (let i = 0; i < limit; i += 16) {
      const off = (baseOffset + i).toString(16).padStart(8, '0').toUpperCase();
      let hexPart = '';
      let asciiPart = '';
      for (let j = 0; j < 16; j++) {
        if (i + j < limit) {
          const v = bytes[i + j];
          hexPart += v.toString(16).padStart(2, '0').toUpperCase() + ' ';
          asciiPart += v >= 32 && v <= 126 ? String.fromCharCode(v) : '.';
        } else {
          hexPart += '   ';
          asciiPart += ' ';
        }
        if (j === 7) hexPart += ' ';
      }
      lines.push(`${off}  ${hexPart} |${asciiPart}|`);
    }
    if (bytes.length > limit) {
      lines.push(`... (${formatBytes(bytes.length - limit)} additional bytes omitted from preview)`);
    }
    return lines.join('\n');
  }

  // =========================================================================
  // 3. JPEG QUANTIZATION TABLE (DQT) QUALITY & DNA PROFILER
  // =========================================================================
  // Standard IJG Luminance table in JPEG zig-zag order (ITU-T T.81 Table K.1)
  const STD_LUM_ZIGZAG = [
    16, 11, 12, 14, 12, 10, 16, 14,
    13, 14, 18, 17, 16, 19, 24, 40,
    26, 24, 22, 22, 24, 49, 35, 37,
    29, 40, 58, 51, 61, 60, 57, 51,
    56, 55, 64, 72, 92, 78, 64, 68,
    87, 69, 55, 56, 80, 109, 81, 87,
    95, 98, 103, 104, 103, 62, 77, 113,
    121, 112, 100, 120, 92, 101, 103, 99
  ];

  // Zig-zag index to 8x8 row-major index
  const ZIGZAG_TO_ROWMAJOR = [
    0, 1, 8, 16, 9, 2, 3, 10,
    17, 24, 32, 25, 18, 11, 4, 5,
    12, 19, 26, 33, 40, 48, 41, 34,
    27, 20, 13, 6, 7, 14, 21, 28,
    35, 42, 49, 56, 57, 50, 43, 36,
    29, 22, 15, 23, 30, 37, 44, 51,
    58, 59, 52, 45, 38, 31, 39, 46,
    53, 60, 61, 54, 47, 55, 62, 63
  ];

  function zigzagToMatrix8x8(zigzag64) {
    const grid = new Array(64).fill(0);
    for (let i = 0; i < Math.min(64, zigzag64.length); i++) {
      grid[ZIGZAG_TO_ROWMAJOR[i]] = zigzag64[i];
    }
    return grid;
  }

  function analyzeDqtTables(dqtTables, sofInfo, hasExif) {
    if (!dqtTables || dqtTables.length === 0) return null;
    const lum = dqtTables.find((t) => t.id === 0) || dqtTables[0];
    const chrom = dqtTables.find((t) => t.id === 1) || dqtTables[1] || null;

    let ratioSum = 0;
    let count = 0;
    let onesCount = 0;
    let ijgMatchScore = 0;

    for (let i = 0; i < 64; i++) {
      const val = lum.values[i];
      if (val === 1) onesCount++;
      ratioSum += val / STD_LUM_ZIGZAG[i];
      count++;
    }
    const meanScale = ratioSum / count;
    let estimatedQuality;
    if (onesCount === 64) {
      estimatedQuality = 100;
    } else if (meanScale <= 1.0) {
      estimatedQuality = Math.max(50, Math.min(100, Math.round(100 - meanScale * 50)));
    } else {
      estimatedQuality = Math.max(1, Math.min(50, Math.round(50 / meanScale)));
    }

    // Measure deviation from standard IJG scaled table (distinguishes Photoshop/Apple/Custom encoders)
    const expectedScaleFactor = estimatedQuality >= 50 ? (200 - 2 * estimatedQuality) / 100 : 50 / estimatedQuality;
    let relDiffSum = 0;
    for (let i = 0; i < 64; i++) {
      const expected = Math.max(1, Math.round(STD_LUM_ZIGZAG[i] * expectedScaleFactor));
      relDiffSum += Math.abs(lum.values[i] - expected) / expected;
    }
    const ijgDeviation = relDiffSum / 64;
    ijgMatchScore = Math.max(0, Math.round((1 - Math.min(1, ijgDeviation)) * 100));

    // Subsampling description
    let subsampling = 'Unknown';
    if (sofInfo && sofInfo.components && sofInfo.components.length >= 3) {
      const y = sofInfo.components[0];
      const cb = sofInfo.components[1];
      const cr = sofInfo.components[2];
      if (y.h === 2 && y.v === 2 && cb.h === 1 && cb.v === 1 && cr.h === 1 && cr.v === 1) subsampling = '4:2:0 (Web / Social / Mobile Standard)';
      else if (y.h === 2 && y.v === 1 && cb.h === 1 && cb.v === 1) subsampling = '4:2:2 (DSLR / Broadcast High)';
      else if (y.h === 1 && y.v === 1 && cb.h === 1 && cb.v === 1) subsampling = '4:4:4 (No Chroma Subsampling / Pro)';
      else subsampling = `${y.h}x${y.v}, ${cb.h}x${cb.v}, ${cr.h}x${cr.v}`;
    } else if (sofInfo && sofInfo.components && sofInfo.components.length === 1) {
      subsampling = 'Grayscale (1 Component)';
    }

    // Heuristic DNA profile
    const hints = [];
    if (ijgMatchScore >= 92) {
      hints.push('Closely follows standard IJG / libjpeg quantization scaling (common in Web browsers, WhatsApp, Telegram, Python PIL, ImageMagick).');
    } else {
      hints.push('Uses custom non-IJG quantization tables (typical of Adobe Photoshop Save-for-Web, Apple ImageIO, or hardware camera ISP).');
    }
    if (!hasExif && subsampling.startsWith('4:2:0') && estimatedQuality >= 68 && estimatedQuality <= 87) {
      hints.push('Metadata-stripped 4:2:0 Q' + estimatedQuality + ' signature closely resembles social/messaging re-compression (WhatsApp / Instagram / X).');
    } else if (estimatedQuality >= 94 && subsampling.startsWith('4:4:4')) {
      hints.push('High-fidelity 4:4:4 Q' + estimatedQuality + ' profile consistent with original export or pro desktop editing.');
    }

    // Simple DQT fingerprint hash
    const fpRaw = lum.values.join(',') + (chrom ? '|' + chrom.values.join(',') : '');
    let hash = 2166136261;
    for (let i = 0; i < fpRaw.length; i++) {
      hash ^= fpRaw.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    const dqtFingerprint = (hash >>> 0).toString(16).padStart(8, '0').toUpperCase();

    return {
      estimatedQuality,
      ijgMatchScore,
      subsampling,
      dqtFingerprint,
      luminance8x8: zigzagToMatrix8x8(lum.values),
      chrominance8x8: chrom ? zigzagToMatrix8x8(chrom.values) : null,
      tableCount: dqtTables.length,
      hints
    };
  }

  // =========================================================================
  // 4. DEEP BINARY STRUCTURE ANALYZER (JPEG / PNG / WEBP / RIFF / HEIC)
  // =========================================================================
  const JPEG_MARKER_NAMES = {
    0xd8: 'SOI (Start of Image)',
    0xd9: 'EOI (End of Image)',
    0xe0: 'APP0 (JFIF / JFXX)',
    0xe1: 'APP1 (EXIF / Adobe XMP)',
    0xe2: 'APP2 (ICC Color Profile / MPF)',
    0xe3: 'APP3 (Meta / Kodak)',
    0xe4: 'APP4 (Scalado / FlashPix)',
    0xeb: 'APP11 (JUMBF / C2PA Content Credentials)',
    0xed: 'APP13 (Adobe Photoshop / IPTC)',
    0xee: 'APP14 (Adobe Color Transform)',
    0xdb: 'DQT (Quantization Table)',
    0xc4: 'DHT (Huffman Table)',
    0xc0: 'SOF0 (Baseline DCT Frame)',
    0xc1: 'SOF1 (Extended Sequential DCT)',
    0xc2: 'SOF2 (Progressive DCT Frame)',
    0xdd: 'DRI (Restart Interval)',
    0xda: 'SOS (Start of Scan / Compressed Pixels)',
    0xfe: 'COM (JPEG Comment)'
  };

  async function analyzeBinaryStructure(arrayBuffer) {
    const bytes = new Uint8Array(arrayBuffer);
    const len = bytes.length;
    const result = {
      format: 'Unknown Binary',
      segments: [],
      pngTextChunks: [],
      xmpStrings: [],
      dqtTables: [],
      sofInfo: null,
      hasExifSegment: false,
      hasIccSegment: false,
      hasIptcSegment: false,
      hasC2paJumbf: false,
      eoiOffset: null,
      trailingBytes: null,
      trailingOffset: null,
      trailingMagic: null,
      trailingEntropy: 0,
      dqtAnalysis: null
    };

    if (len < 12) return result;

    // --- CASE A: JPEG ---
    if (bytes[0] === 0xff && bytes[1] === 0xd8) {
      result.format = 'JPEG';
      result.segments.push({ marker: 'FFD8', name: 'SOI (Start of Image)', offset: 0, length: 2, detail: 'JPEG Magic Header' });
      let offset = 2;
      let hitEoi = false;

      while (offset < len - 1) {
        // Align to 0xFF marker prefix
        if (bytes[offset] !== 0xff) {
          offset++;
          continue;
        }
        while (offset < len && bytes[offset] === 0xff) offset++;
        if (offset >= len) break;

        const markerCode = bytes[offset];
        const markerStart = offset - 1;
        offset++;

        if (markerCode === 0x00) continue; // Stuffed byte
        if (markerCode === 0xd9) {
          result.segments.push({ marker: 'FFD9', name: 'EOI (End of Image)', offset: markerStart, length: 2, detail: 'True JPEG End' });
          result.eoiOffset = offset;
          hitEoi = true;
          break;
        }
        if (markerCode >= 0xd0 && markerCode <= 0xd7) continue; // RSTn
        if (markerCode === 0x01) continue; // TEM

        if (offset + 2 > len) break;
        const segLen = (bytes[offset] << 8) | bytes[offset + 1];
        if (segLen < 2) break;
        const payloadStart = offset + 2;
        const segEnd = Math.min(len, offset + segLen);
        const totalSegLen = segEnd - markerStart;
        const hexMarker = 'FF' + markerCode.toString(16).padStart(2, '0').toUpperCase();
        let name = JPEG_MARKER_NAMES[markerCode] || `Marker 0x${hexMarker}`;
        let detail = `${segLen} B payload`;

        if (markerCode === 0xe1 && payloadStart + 6 <= segEnd) {
          const sig6 = decodeBytesLatin1(bytes, payloadStart, Math.min(segEnd, payloadStart + 32));
          if (sig6.startsWith('Exif\0\0')) {
            name = 'APP1 (EXIF TIFF Block)';
            result.hasExifSegment = true;
            const endian = sig6.slice(6, 8) === 'II' ? 'Little-Endian (II)' : sig6.slice(6, 8) === 'MM' ? 'Big-Endian (MM)' : 'TIFF';
            detail = `${endian} • ${segLen} B`;
          } else if (sig6.startsWith('http://ns.adobe.com/xap/1.0/\0') || sig6.startsWith('http://ns.adobe.com/xmp/extension/\0')) {
            name = 'APP1 (Adobe XMP XML)';
            const nul = bytes.indexOf(0, payloadStart);
            if (nul !== -1 && nul + 1 < segEnd) {
              const xmlStr = decodeBytesUtf8(bytes, nul + 1, segEnd);
              result.xmpStrings.push(xmlStr);
            }
            detail = `XML Metadata • ${segLen} B`;
          }
        } else if (markerCode === 0xe2) {
          const sig = decodeBytesLatin1(bytes, payloadStart, Math.min(segEnd, payloadStart + 16));
          if (sig.startsWith('ICC_PROFILE')) {
            name = 'APP2 (ICC Color Profile)';
            result.hasIccSegment = true;
          } else if (sig.startsWith('MPF\0')) {
            name = 'APP2 (MPF Multi-Picture)';
          }
        } else if (markerCode === 0xed) {
          result.hasIptcSegment = true;
        } else if (markerCode === 0xeb) {
          const sig = decodeBytesLatin1(bytes, payloadStart, Math.min(segEnd, payloadStart + 32));
          if (sig.includes('jumb') || sig.includes('c2pa') || sig.includes('JP')) {
            result.hasC2paJumbf = true;
            name = 'APP11 (JUMBF / C2PA Provenance)';
          }
        } else if (markerCode === 0xfe) {
          const comment = decodeBytesUtf8(bytes, payloadStart, Math.min(segEnd, payloadStart + 160)).replace(/[\x00-\x1f]/g, ' ');
          detail = `"${comment.slice(0, 70)}${comment.length > 70 ? '…' : ''}"`;
          result.pngTextChunks.push({ chunk: 'JPEG COM', keyword: 'Comment', text: decodeBytesUtf8(bytes, payloadStart, segEnd) });
        } else if (markerCode === 0xdb) {
          // Parse DQT tables inside this APP/DQT segment
          let p = payloadStart;
          while (p < segEnd) {
            const pqTq = bytes[p++];
            const precision = (pqTq >> 4) & 0x0f;
            const tableId = pqTq & 0x0f;
            const elemBytes = precision === 0 ? 1 : 2;
            if (p + 64 * elemBytes > segEnd) break;
            const vals = [];
            for (let k = 0; k < 64; k++) {
              vals.push(elemBytes === 1 ? bytes[p + k] : (bytes[p + 2 * k] << 8) | bytes[p + 2 * k + 1]);
            }
            result.dqtTables.push({ id: tableId, precision: precision === 0 ? 8 : 16, values: vals });
            p += 64 * elemBytes;
          }
          detail = `${result.dqtTables.length} Quantization Table(s)`;
        } else if (markerCode === 0xc0 || markerCode === 0xc1 || markerCode === 0xc2) {
          if (payloadStart + 6 <= segEnd) {
            const precision = bytes[payloadStart];
            const height = (bytes[payloadStart + 1] << 8) | bytes[payloadStart + 2];
            const width = (bytes[payloadStart + 3] << 8) | bytes[payloadStart + 4];
            const numComp = bytes[payloadStart + 5];
            const components = [];
            let cp = payloadStart + 6;
            for (let c = 0; c < numComp && cp + 3 <= segEnd; c++) {
              const cid = bytes[cp];
              const hv = bytes[cp + 1];
              const qt = bytes[cp + 2];
              components.push({ id: cid, h: (hv >> 4) & 0xf, v: hv & 0xf, qt });
              cp += 3;
            }
            result.sofInfo = {
              type: markerCode === 0xc2 ? 'Progressive DCT' : 'Baseline DCT',
              precision,
              width,
              height,
              components
            };
            detail = `${width}×${height}, ${precision}-bit, ${numComp} ch (${result.sofInfo.type})`;
          }
        }

        if (markerCode === 0xda) {
          // SOS: scan forward past entropy-coded scan until real non-stuffed, non-RST marker
          let scanPtr = segEnd;
          while (scanPtr < len - 1) {
            if (bytes[scanPtr] === 0xff) {
              const nextB = bytes[scanPtr + 1];
              if (nextB === 0x00 || (nextB >= 0xd0 && nextB <= 0xd7) || nextB === 0xff) {
                scanPtr += nextB === 0xff ? 1 : 2;
                continue;
              }
              break;
            }
            scanPtr++;
          }
          if (scanPtr >= len - 1) scanPtr = len;
          result.segments.push({
            marker: hexMarker,
            name,
            offset: markerStart,
            length: scanPtr - markerStart,
            detail: `Image Scan Data (${formatBytes(scanPtr - markerStart)})`
          });
          offset = scanPtr;
          continue;
        }

        result.segments.push({ marker: hexMarker, name, offset: markerStart, length: totalSegLen, detail });
        offset = segEnd;
      }

      if (hitEoi && result.eoiOffset < len) {
        const trailing = bytes.subarray(result.eoiOffset);
        result.trailingBytes = trailing;
        result.trailingOffset = result.eoiOffset;
        result.trailingEntropy = computeShannonEntropy(trailing);
        result.trailingMagic = detectMagicSignature(trailing);
      }
      result.dqtAnalysis = analyzeDqtTables(result.dqtTables, result.sofInfo, result.hasExifSegment);
      return result;
    }

    // --- CASE B: PNG ---
    if (
      bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47 &&
      bytes[4] === 0x0d && bytes[5] === 0x0a && bytes[6] === 0x1a && bytes[7] === 0x0a
    ) {
      result.format = 'PNG';
      result.segments.push({ marker: '89504E47', name: 'PNG Signature', offset: 0, length: 8, detail: '8-byte Magic Header' });
      let offset = 8;
      let hitIend = false;

      while (offset + 12 <= len) {
        const chunkLen = ((bytes[offset] << 24) | (bytes[offset + 1] << 16) | (bytes[offset + 2] << 8) | bytes[offset + 3]) >>> 0;
        const type = String.fromCharCode(bytes[offset + 4], bytes[offset + 5], bytes[offset + 6], bytes[offset + 7]);
        const dataStart = offset + 8;
        const dataEnd = dataStart + chunkLen;
        if (dataEnd + 4 > len) break;

        let detail = `${formatBytes(chunkLen)} payload`;
        if (type === 'IHDR' && chunkLen >= 13) {
          const w = ((bytes[dataStart] << 24) | (bytes[dataStart + 1] << 16) | (bytes[dataStart + 2] << 8) | bytes[dataStart + 3]) >>> 0;
          const h = ((bytes[dataStart + 4] << 24) | (bytes[dataStart + 5] << 16) | (bytes[dataStart + 6] << 8) | bytes[dataStart + 7]) >>> 0;
          const bitDepth = bytes[dataStart + 8];
          const colorType = bytes[dataStart + 9];
          detail = `${w}×${h}, ${bitDepth}-bit, colorType=${colorType}`;
        } else if (type === 'tEXt') {
          const nul = bytes.indexOf(0, dataStart);
          if (nul !== -1 && nul < dataEnd) {
            const keyword = decodeBytesLatin1(bytes, dataStart, nul);
            const text = decodeBytesUtf8(bytes, nul + 1, dataEnd);
            result.pngTextChunks.push({ chunk: 'tEXt', keyword, text });
            if (keyword.includes('XML:com.adobe.xmp')) result.xmpStrings.push(text);
            detail = `Key: "${keyword}" (${formatBytes(text.length)})`;
          }
        } else if (type === 'zTXt') {
          const nul = bytes.indexOf(0, dataStart);
          if (nul !== -1 && nul + 2 <= dataEnd) {
            const keyword = decodeBytesLatin1(bytes, dataStart, nul);
            const decomp = await decompressDeflate(bytes.subarray(nul + 2, dataEnd));
            const text = decomp ? decodeBytesUtf8(decomp, 0, decomp.length) : '[Compressed zTXt - browser inflate unavailable]';
            result.pngTextChunks.push({ chunk: 'zTXt', keyword, text });
            if (keyword.includes('XML:com.adobe.xmp') && decomp) result.xmpStrings.push(text);
            detail = `Key: "${keyword}" (compressed)`;
          }
        } else if (type === 'iTXt') {
          const nul1 = bytes.indexOf(0, dataStart);
          if (nul1 !== -1 && nul1 + 3 <= dataEnd) {
            const keyword = decodeBytesUtf8(bytes, dataStart, nul1);
            const compFlag = bytes[nul1 + 1];
            const nulLang = bytes.indexOf(0, nul1 + 3);
            const nulTrans = nulLang !== -1 ? bytes.indexOf(0, nulLang + 1) : -1;
            if (nulTrans !== -1 && nulTrans + 1 <= dataEnd) {
              const textStart = nulTrans + 1;
              let text = '';
              if (compFlag === 1) {
                const decomp = await decompressDeflate(bytes.subarray(textStart, dataEnd));
                text = decomp ? decodeBytesUtf8(decomp, 0, decomp.length) : '[Compressed iTXt]';
              } else {
                text = decodeBytesUtf8(bytes, textStart, dataEnd);
              }
              result.pngTextChunks.push({ chunk: 'iTXt', keyword, text });
              if (keyword.includes('XML:com.adobe.xmp')) result.xmpStrings.push(text);
              detail = `Key: "${keyword}" (${formatBytes(text.length)})`;
            }
          }
        } else if (type === 'eXIf') {
          result.hasExifSegment = true;
          detail = `Embedded TIFF EXIF (${formatBytes(chunkLen)})`;
        } else if (type === 'iCCP') {
          result.hasIccSegment = true;
        } else if (type === 'caBX' || type === 'c2pa') {
          result.hasC2paJumbf = true;
          detail = `C2PA Content Credentials (${formatBytes(chunkLen)})`;
        }

        result.segments.push({ marker: type, name: `PNG ${type}`, offset, length: 12 + chunkLen, detail });
        offset = dataEnd + 4;
        if (type === 'IEND') {
          result.eoiOffset = offset;
          hitIend = true;
          break;
        }
      }

      if (hitIend && result.eoiOffset < len) {
        const trailing = bytes.subarray(result.eoiOffset);
        result.trailingBytes = trailing;
        result.trailingOffset = result.eoiOffset;
        result.trailingEntropy = computeShannonEntropy(trailing);
        result.trailingMagic = detectMagicSignature(trailing);
      }
      return result;
    }

    // --- CASE C: WEBP (RIFF) ---
    if (decodeBytesLatin1(bytes, 0, 4) === 'RIFF' && decodeBytesLatin1(bytes, 8, 12) === 'WEBP') {
      result.format = 'WebP';
      const riffSize = bytes[4] | (bytes[5] << 8) | (bytes[6] << 16) | (bytes[7] << 24);
      const expectedEnd = Math.min(len, riffSize + 8);
      result.segments.push({ marker: 'RIFF', name: 'RIFF/WEBP Header', offset: 0, length: 12, detail: `Declared size: ${formatBytes(riffSize + 8)}` });
      let offset = 12;
      while (offset + 8 <= expectedEnd) {
        const fourcc = decodeBytesLatin1(bytes, offset, offset + 4);
        const cSize = (bytes[offset + 4] | (bytes[offset + 5] << 8) | (bytes[offset + 6] << 16) | (bytes[offset + 7] << 24)) >>> 0;
        const cStart = offset + 8;
        const cEnd = Math.min(len, cStart + cSize);
        if (fourcc === 'EXIF') result.hasExifSegment = true;
        if (fourcc === 'ICCP') result.hasIccSegment = true;
        if (fourcc === 'XMP ') {
          result.xmpStrings.push(decodeBytesUtf8(bytes, cStart, cEnd));
        }
        result.segments.push({ marker: fourcc, name: `RIFF Chunk ${fourcc}`, offset, length: 8 + cSize, detail: `${formatBytes(cSize)} payload` });
        offset = cEnd + (cSize % 2);
      }
      result.eoiOffset = expectedEnd;
      if (expectedEnd < len) {
        const trailing = bytes.subarray(expectedEnd);
        result.trailingBytes = trailing;
        result.trailingOffset = expectedEnd;
        result.trailingEntropy = computeShannonEntropy(trailing);
        result.trailingMagic = detectMagicSignature(trailing);
      }
      return result;
    }

    // --- CASE D: TIFF / DNG / HEIC / RAW ---
    const head4 = decodeBytesLatin1(bytes, 0, 4);
    if (head4.startsWith('II') || head4.startsWith('MM')) {
      result.format = 'TIFF / RAW';
      result.hasExifSegment = true;
      result.segments.push({ marker: head4.slice(0, 2), name: 'TIFF Header', offset: 0, length: len, detail: head4.startsWith('II') ? 'Little-Endian' : 'Big-Endian' });
    } else if (decodeBytesLatin1(bytes, 4, 8) === 'ftyp') {
      const brand = decodeBytesLatin1(bytes, 8, 12);
      result.format = `ISOBMFF (${brand})`;
      // Scan quickly for c2pa/jumb signature inside ISOBMFF
      const rawProbe = decodeBytesLatin1(bytes, 0, Math.min(len, 512 * 1024));
      if (rawProbe.includes('c2pa') || rawProbe.includes('jumb')) result.hasC2paJumbf = true;
      result.segments.push({ marker: 'ftyp', name: `Container (${brand})`, offset: 0, length: len, detail: formatBytes(len) });
    }
    return result;
  }

  // =========================================================================
  // 5. XMP XML FORENSIC PARSER (EDIT TIMELINE, LIGHTROOM, DOCUMENT IDs, REGIONS)
  // =========================================================================
  function extractXmpForensics(xmpStrings) {
    const packets = (Array.isArray(xmpStrings) ? xmpStrings : [xmpStrings || '']).filter((s) => s && s.trim());
    const combined = packets.join('\n');
    const out = {
      hasXmp: packets.length > 0,
      rawXml: combined,
      documentId: null,
      originalDocumentId: null,
      instanceId: null,
      creatorTool: null,
      historyEvents: [],
      photoshopHistoryText: null,
      crsEdits: {},
      digitalSourceType: null,
      regions: []
    };
    if (!packets.length || typeof DOMParser === 'undefined') return out;

    packets.forEach((xmlPacket) => {
      try {
        const cleaned = xmlPacket.replace(/<\?xpacket[\s\S]*?\?>/gi, '').trim();
        if (!cleaned) return;
        const doc = new DOMParser().parseFromString(cleaned, 'text/xml');
        if (doc.getElementsByTagName('parsererror').length > 0) return;
        const allEls = doc.getElementsByTagName('*');

        const getAttrOrText = (localName) => {
          for (let i = 0; i < allEls.length; i++) {
            const el = allEls[i];
            if (el.localName === localName && el.textContent && el.textContent.trim()) {
              return el.textContent.trim();
            }
            for (let a = 0; a < el.attributes.length; a++) {
              const attr = el.attributes[a];
              if (attr.localName === localName && attr.value) return attr.value.trim();
            }
          }
          return null;
        };

        out.documentId = out.documentId || getAttrOrText('DocumentID');
        out.originalDocumentId = out.originalDocumentId || getAttrOrText('OriginalDocumentID');
        out.instanceId = out.instanceId || getAttrOrText('InstanceID');
        out.creatorTool = out.creatorTool || getAttrOrText('CreatorTool');
        out.digitalSourceType = out.digitalSourceType || getAttrOrText('DigitalSourceType');
        out.photoshopHistoryText = out.photoshopHistoryText || getAttrOrText('History');

        for (let i = 0; i < allEls.length; i++) {
          const el = allEls[i];
          const hasEvtAttr = Array.from(el.attributes).some((a) => a.name.startsWith('stEvt:'));
          const hasEvtChild = Array.from(el.children).some((c) => c.prefix === 'stEvt' || c.localName === 'action');
          if (hasEvtAttr || hasEvtChild) {
            const evt = {};
            Array.from(el.attributes).forEach((a) => {
              if (a.name.startsWith('stEvt:')) evt[a.localName] = a.value;
            });
            Array.from(el.children).forEach((c) => {
              if (c.prefix === 'stEvt' || ['action', 'when', 'softwareAgent', 'changed', 'parameters', 'instanceID'].includes(c.localName)) {
                evt[c.localName] = c.textContent.trim();
              }
            });
            if (evt.action || evt.when || evt.softwareAgent) {
              out.historyEvents.push(evt);
            }
          }

          Array.from(el.attributes).forEach((a) => {
            if (a.name.startsWith('crs:') && a.value !== '' && a.value !== '0') {
              out.crsEdits[a.localName] = a.value;
            }
          });
          if (el.prefix === 'crs' && el.children.length === 0 && el.textContent && el.textContent.trim()) {
            out.crsEdits[el.localName] = el.textContent.trim();
          }

          if (el.localName === 'Area' || el.getAttribute('stArea:x')) {
            const x = parseFloat(el.getAttribute('stArea:x') || '');
            const y = parseFloat(el.getAttribute('stArea:y') || '');
            const w = parseFloat(el.getAttribute('stArea:w') || '');
            const h = parseFloat(el.getAttribute('stArea:h') || '');
            if (Number.isFinite(x) && Number.isFinite(y) && Number.isFinite(w) && Number.isFinite(h)) {
              const parent = el.parentElement;
              const label = parent ? (parent.getAttribute('mwg-rs:Name') || parent.getAttribute('mwg-rs:Type') || 'Region') : 'Region';
              out.regions.push({ x, y, w, h, label, normalizedCenter: true });
            }
          }
        }
      } catch (_) {}
    });
    return out;
  }

  // =========================================================================
  // 6. AI PROVENANCE, STABLE DIFFUSION / COMFYUI / FIREFLY / C2PA ANALYZER
  // =========================================================================
  function parseA1111Parameters(raw) {
    const lines = raw.split(/\r?\n/);
    let negIdx = lines.findIndex((l) => l.startsWith('Negative prompt:'));
    let stepsIdx = lines.findIndex((l) => /\bSteps:\s*\d+/i.test(l));

    let positive = '';
    let negative = '';
    let paramsStr = '';

    if (negIdx !== -1) {
      positive = lines.slice(0, negIdx).join('\n').trim();
      const endNeg = stepsIdx !== -1 ? stepsIdx : lines.length;
      negative = lines.slice(negIdx, endNeg).join('\n').replace(/^Negative prompt:\s*/i, '').trim();
    } else if (stepsIdx !== -1) {
      positive = lines.slice(0, stepsIdx).join('\n').trim();
    } else {
      positive = raw.trim();
    }

    if (stepsIdx !== -1) paramsStr = lines.slice(stepsIdx).join(', ');
    const parsedParams = {};
    if (paramsStr) {
      const pairs = paramsStr.match(/([A-Za-z0-9 _-]+):\s*("[^"]*"|[^,]+)/g) || [];
      pairs.forEach((p) => {
        const idx = p.indexOf(':');
        if (idx > 0) {
          parsedParams[p.slice(0, idx).trim()] = p.slice(idx + 1).trim().replace(/^"|"$/g, '');
        }
      });
    }
    return { positive, negative, params: parsedParams };
  }

  function summarizeComfyGraph(graphObj) {
    const summary = { checkpoints: [], loras: [], prompts: [], samplers: [], nodeCount: 0 };
    if (!graphObj || typeof graphObj !== 'object') return summary;

    // Handle both API prompt dict { "1": { class_type, inputs } } and UI workflow { nodes: [...] }
    if (Array.isArray(graphObj.nodes)) {
      summary.nodeCount = graphObj.nodes.length;
      graphObj.nodes.forEach((n) => {
        const t = n.type || '';
        if (/CheckpointLoader|UNETLoader/i.test(t) && n.widgets_values) summary.checkpoints.push(n.widgets_values[0]);
        if (/LoraLoader/i.test(t) && n.widgets_values) summary.loras.push(n.widgets_values[0]);
        if (/CLIPTextEncode/i.test(t) && n.widgets_values && n.widgets_values[0]) summary.prompts.push(String(n.widgets_values[0]));
        if (/KSampler/i.test(t) && n.widgets_values) summary.samplers.push(`${t} (Seed: ${n.widgets_values[0]})`);
      });
    } else {
      const entries = Object.values(graphObj);
      summary.nodeCount = entries.length;
      entries.forEach((n) => {
        if (!n || typeof n !== 'object') return;
        const t = n.class_type || '';
        const inp = n.inputs || {};
        if (/CheckpointLoader|UNETLoader/i.test(t) && (inp.ckpt_name || inp.unet_name)) {
          summary.checkpoints.push(inp.ckpt_name || inp.unet_name);
        }
        if (/LoraLoader/i.test(t) && inp.lora_name) summary.loras.push(inp.lora_name);
        if (/CLIPTextEncode/i.test(t) && typeof inp.text === 'string' && inp.text.trim()) {
          summary.prompts.push(inp.text.trim());
        }
        if (/KSampler/i.test(t)) {
          summary.samplers.push(`Steps: ${inp.steps ?? '?'} • CFG: ${inp.cfg ?? '?'} • Sampler: ${inp.sampler_name ?? '?'} • Seed: ${inp.seed ?? inp.noise_seed ?? '?'}`);
        }
      });
    }
    return summary;
  }

  function analyzeAiProvenance(exifrData, binaryInfo, xmpInfo) {
    const findings = [];
    let verdict = 'No AI Provenance Found';
    let verdictType = 'neutral'; // neutral | ai-generated | ai-edited | edited
    let positivePrompt = null;
    let negativePrompt = null;
    let generationParams = null;
    let comfyWorkflow = null;
    let comfySummary = null;

    const allTexts = [];
    const seenKeys = new Set();
    const pushText = (chunk, keyword, text) => {
      const kw = (keyword || '').toLowerCase();
      const t = (text || '').trim();
      if (!t) return;
      const sig = kw + '\0' + t;
      if (seenKeys.has(sig)) return;
      seenKeys.add(sig);
      allTexts.push({ chunk, keyword, text: t });
    };
    if (binaryInfo && binaryInfo.pngTextChunks) {
      binaryInfo.pngTextChunks.forEach((c) => pushText(c.chunk, c.keyword, c.text));
    }
    if (exifrData) {
      ['UserComment', 'ImageDescription', 'Software', 'Artist', 'Make', 'Model', 'Parameters', 'parameters', 'Workflow', 'workflow', 'Prompt', 'prompt']
        .forEach((k) => {
          if (exifrData[k] !== undefined && exifrData[k] !== null) {
            const val = typeof exifrData[k] === 'string' ? exifrData[k] : (exifrData[k] instanceof Uint8Array ? decodeBytesUtf8(exifrData[k], 0, exifrData[k].length) : String(exifrData[k]));
            pushText('EXIF', k, val);
          }
        });
    }

    // Check PNG / EXIF chunks for A1111, ComfyUI, NovelAI, Midjourney
    allTexts.forEach((item) => {
      const kw = (item.keyword || '').toLowerCase();
      const txt = (item.text || '').trim();
      if (!txt) return;

      if (kw === 'parameters' || (txt.includes('Steps:') && txt.includes('Sampler:'))) {
        const parsed = parseA1111Parameters(txt);
        positivePrompt = parsed.positive || positivePrompt;
        negativePrompt = parsed.negative || negativePrompt;
        generationParams = parsed.params;
        verdict = 'AI-Generated (Stable Diffusion / A1111 / Forge)';
        verdictType = 'ai-generated';
        findings.push('Detected Automatic1111 / Forge generation parameters chunk.');
      } else if ((kw === 'workflow' || kw === 'prompt') && (txt.startsWith('{') || txt.startsWith('['))) {
        try {
          const obj = JSON.parse(txt);
          if (!comfyWorkflow || kw === 'workflow') comfyWorkflow = obj;
          const sum = summarizeComfyGraph(obj);
          if (sum.nodeCount > 0) {
            comfySummary = comfySummary && comfySummary.prompts.length >= sum.prompts.length ? comfySummary : sum;
            verdict = 'AI-Generated (ComfyUI Node Workflow)';
            verdictType = 'ai-generated';
            findings.push(`Extracted ComfyUI JSON (${kw}) with ${sum.nodeCount} nodes.`);
          }
        } catch (_) {}
      } else if (txt.includes('NovelAI') || (kw === 'software' && txt === 'NovelAI')) {
        verdict = 'AI-Generated (NovelAI)';
        verdictType = 'ai-generated';
        findings.push('NovelAI generation tag detected.');
      } else if (txt.toLowerCase().includes('midjourney') || /--ar\s+\d+:\d+|--v\s+\d/.test(txt)) {
        verdict = 'AI-Generated (Midjourney)';
        verdictType = 'ai-generated';
        positivePrompt = positivePrompt || txt;
        findings.push('Midjourney prompt/parameter pattern detected.');
      }
    });

    // Check C2PA / IPTC DigitalSourceType / Adobe Firefly / SynthID / Apple/Samsung AI
    if (binaryInfo && binaryInfo.hasC2paJumbf) {
      findings.push('C2PA / JUMBF Content Credentials cryptographically signed container detected.');
      if (verdictType === 'neutral') {
        verdict = 'C2PA Content Credentials Present';
        verdictType = 'ai-edited';
      }
    }
    if (xmpInfo && xmpInfo.digitalSourceType) {
      findings.push(`IPTC DigitalSourceType: ${xmpInfo.digitalSourceType}`);
      if (/trainedAlgorithmicMedia|algorithmic|compositeWithTrainedAlgorithmicMedia/i.test(xmpInfo.digitalSourceType)) {
        verdict = 'AI-Generated / Generative AI Media (IPTC C2PA)';
        verdictType = 'ai-generated';
      }
    }
    const rawCombined = (xmpInfo ? xmpInfo.rawXml : '') + ' ' + JSON.stringify(exifrData || {});
    if (/Firefly|Generative Fill|Generative Expand/i.test(rawCombined)) {
      findings.push('Adobe Firefly / Photoshop Generative AI edit marker detected.');
      if (verdictType === 'neutral') {
        verdict = 'AI-Edited (Adobe Firefly / Generative Fill)';
        verdictType = 'ai-edited';
      }
    }
    if (/Galaxy AI|Magic Eraser|Best Take|Reimagine|Image Playground|Made with Google AI/i.test(rawCombined)) {
      findings.push('On-device Smartphone AI editing signature detected.');
      if (verdictType === 'neutral') {
        verdict = 'AI-Edited (Device Computational AI)';
        verdictType = 'ai-edited';
      }
    }
    if (verdictType === 'neutral' && ((xmpInfo && xmpInfo.historyEvents.length > 0) || (exifrData && /Photoshop|Lightroom|GIMP|Affinity|Snapseed|Canva/i.test(String(exifrData.Software || ''))))) {
      verdict = 'Post-Processed / Software Edited';
      verdictType = 'edited';
      findings.push('Desktop/mobile photo editor history or Software tag detected.');
    }

    return {
      verdict,
      verdictType,
      findings,
      positivePrompt,
      negativePrompt,
      generationParams,
      comfyWorkflow,
      comfySummary,
      rawTextChunks: allTexts
    };
  }

  // =========================================================================
  // 7. EMBEDDED MEDIA: MOTION PHOTO MP4, GDEPTH MAP, MPF
  // =========================================================================
  function scanEmbeddedMedia(arrayBuffer, xmpInfo, exifrData) {
    const bytes = new Uint8Array(arrayBuffer);
    const out = {
      motionVideoBlob: null,
      motionVideoSize: 0,
      motionVideoOffset: null,
      depthMapDataUrl: null,
      depthMapMime: null
    };

    // 1. Check GCamera:MicroVideoOffset or Container Directory video length in XMP
    let mp4Start = null;
    if (xmpInfo && xmpInfo.rawXml) {
      const mMicro = xmpInfo.rawXml.match(/GCamera:MicroVideoOffset="(\d+)"/i);
      if (mMicro) {
        const tailLen = parseInt(mMicro[1], 10);
        if (tailLen > 1000 && tailLen < bytes.length) {
          mp4Start = bytes.length - tailLen;
        }
      }
      if (mp4Start === null) {
        // MotionPhoto v2 Container:Item Semantic="MotionPhoto" Length="..."
        const mItem = xmpInfo.rawXml.match(/Item:Mime="video\/mp4"[^>]*Item:Length="(\d+)"|Item:Length="(\d+)"[^>]*Item:Mime="video\/mp4"/i);
        if (mItem) {
          const tailLen = parseInt(mItem[1] || mItem[2], 10);
          if (tailLen > 1000 && tailLen < bytes.length) {
            mp4Start = bytes.length - tailLen;
          }
        }
      }
      // Check GDepth:Data base64 depth map
      const mDepth = xmpInfo.rawXml.match(/GDepth:Data="([A-Za-z0-9+/=]+)"/i);
      const mDepthMime = xmpInfo.rawXml.match(/GDepth:Mime="([^"]+)"/i);
      if (mDepth && mDepth[1].length > 50) {
        const mime = mDepthMime ? mDepthMime[1] : 'image/png';
        out.depthMapMime = mime;
        out.depthMapDataUrl = `data:${mime};base64,${mDepth[1]}`;
      }
    }

    // 2. Fallback binary search for MP4 'ftyp' header inside JPEG/file (after first 4KB)
    if (mp4Start === null && bytes.length > 8192) {
      for (let i = 4096; i < bytes.length - 12; i++) {
        if (bytes[i] === 0x66 && bytes[i + 1] === 0x74 && bytes[i + 2] === 0x79 && bytes[i + 3] === 0x70) {
          const brand = String.fromCharCode(bytes[i + 4], bytes[i + 5], bytes[i + 6], bytes[i + 7]);
          if (/^(mp42|isom|iso2|M4V |qt  |avc1)$/.test(brand) && i >= 4) {
            mp4Start = i - 4;
            break;
          }
        }
      }
    }

    if (mp4Start !== null && mp4Start > 0 && mp4Start < bytes.length - 128) {
      const mp4Slice = bytes.subarray(mp4Start);
      out.motionVideoBlob = new Blob([mp4Slice], { type: 'video/mp4' });
      out.motionVideoSize = mp4Slice.length;
      out.motionVideoOffset = mp4Start;
    }

    return out;
  }

  // =========================================================================
  // 8. ASTRONOMICAL SUN-SHADOW & TIMESTAMP LIE DETECTOR
  // =========================================================================
  function parseExifDateParts(val) {
    if (!val) return null;
    if (val instanceof Date && !isNaN(val.getTime())) {
      return {
        year: val.getFullYear(),
        month: val.getMonth() + 1,
        day: val.getDate(),
        hour: val.getHours(),
        min: val.getMinutes(),
        sec: val.getSeconds()
      };
    }
    const m = String(val).match(/(\d{4})[:\-](\d{2})[:\-](\d{2})[T\s](\d{2}):(\d{2}):(\d{2})/);
    if (!m) return null;
    return {
      year: +m[1], month: +m[2], day: +m[3],
      hour: +m[4], min: +m[5], sec: +m[6]
    };
  }

  function parseUtcOffsetMinutes(offsetStr) {
    if (!offsetStr) return null;
    const m = String(offsetStr).trim().match(/^([+-])(\d{2}):?(\d{2})$/);
    if (!m) return null;
    const sign = m[1] === '-' ? -1 : 1;
    return sign * (parseInt(m[2], 10) * 60 + parseInt(m[3], 10));
  }

  function calculateSolarPosition(utcDate, lat, lng) {
    const rad = Math.PI / 180;
    const deg = 180 / Math.PI;
    const jd = utcDate.getTime() / 86400000 + 2440587.5;
    const t = (jd - 2451545.0) / 36525.0;

    const l0 = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360;
    const m = 357.52911 + t * (35999.05029 - 0.0001537 * t);
    const e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t);

    const sinM = Math.sin(m * rad);
    const c =
      sinM * (1.914602 - t * (0.004817 + 0.000014 * t)) +
      Math.sin(2 * m * rad) * (0.019993 - 0.000101 * t) +
      Math.sin(3 * m * rad) * 0.000289;

    const trueLong = l0 + c;
    const omega = 125.04 - 1934.136 * t;
    const appLong = trueLong - 0.00569 - 0.00478 * Math.sin(omega * rad);

    const eps0 = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60;
    const eps = eps0 + 0.00256 * Math.cos(omega * rad);

    const decl = Math.asin(Math.sin(eps * rad) * Math.sin(appLong * rad));
    const y = Math.tan((eps * rad) / 2) ** 2;
    const eqTime =
      4 *
      deg *
      (y * Math.sin(2 * l0 * rad) -
        2 * e * sinM +
        4 * e * y * sinM * Math.cos(2 * l0 * rad) -
        0.5 * y * y * Math.sin(4 * l0 * rad) -
        1.25 * e * e * Math.sin(2 * m * rad));

    const utcMin = utcDate.getUTCHours() * 60 + utcDate.getUTCMinutes() + utcDate.getUTCSeconds() / 60;
    const trueSolarTime = (((utcMin + eqTime + 4 * lng) % 1440) + 1440) % 1440;
    let hourAngle = trueSolarTime / 4 - 180;
    if (hourAngle < -180) hourAngle += 360;

    const latR = lat * rad;
    const cosZen = Math.max(-1, Math.min(1, Math.sin(latR) * Math.sin(decl) + Math.cos(latR) * Math.cos(decl) * Math.cos(hourAngle * rad)));
    const zenith = Math.acos(cosZen) * deg;
    let elevation = 90 - zenith;

    // Atmospheric refraction correction
    if (elevation > -0.575 && elevation < 85) {
      const te = Math.tan(elevation * rad);
      const ref = elevation > 5 ? 58.1 / te - 0.07 / te ** 3 + 0.000086 / te ** 5 : 1735 + elevation * (-518.2 + elevation * (103.4 + elevation * (-12.79 + elevation * 0.711)));
      elevation += ref / 3600;
    }

    const sinZen = Math.sin(zenith * rad);
    let azimuth = 180;
    if (Math.abs(sinZen) > 1e-6 && Math.abs(Math.cos(latR)) > 1e-6) {
      const cosAz = Math.max(-1, Math.min(1, (Math.sin(latR) * cosZen - Math.sin(decl)) / (Math.cos(latR) * sinZen)));
      const azBase = Math.acos(cosAz) * deg;
      azimuth = hourAngle > 0 ? (azBase + 180) % 360 : (540 - azBase) % 360;
    }

    const shadowAzimuth = (azimuth + 180) % 360;
    const shadowRatio = elevation > 1 ? 1 / Math.tan(elevation * rad) : null;

    let phase = 'Night (Below Horizon)';
    if (elevation >= 6) phase = 'Daylight';
    else if (elevation >= -0.833) phase = 'Golden Hour / Horizon';
    else if (elevation >= -6) phase = 'Blue Hour / Civil Twilight';
    else if (elevation >= -12) phase = 'Nautical Twilight';
    else if (elevation >= -18) phase = 'Astronomical Twilight';

    return {
      azimuth,
      elevation,
      shadowAzimuth,
      shadowRatio,
      shadowLengthFor170cm: shadowRatio !== null ? (1.7 * shadowRatio).toFixed(2) + ' m' : 'Infinite / Dark',
      phase
    };
  }

  function auditTimestamps(exifrData, lat, lng, manualOffsetMin) {
    const warnings = [];
    const dto = parseExifDateParts(exifrData && exifrData.DateTimeOriginal);
    const mod = parseExifDateParts(exifrData && (exifrData.ModifyDate || exifrData.DateTime));
    const offsetStr = exifrData && (exifrData.OffsetTimeOriginal || exifrData.OffsetTime);
    const parsedOffsetMin = parseUtcOffsetMinutes(offsetStr);

    let utcDate = null;
    let timeSource = 'None';

    // Check GPS UTC timestamp first
    let gpsUtcDate = null;
    if (exifrData && exifrData.GPSDateStamp && exifrData.GPSTimeStamp) {
      const dm = String(exifrData.GPSDateStamp).match(/(\d{4})[:\-](\d{2})[:\-](\d{2})/);
      const ts = exifrData.GPSTimeStamp;
      let hh = 0, mm = 0, ss = 0;
      if (Array.isArray(ts) && ts.length >= 3) {
        hh = Math.floor(ts[0]); mm = Math.floor(ts[1]); ss = Math.floor(ts[2]);
      } else if (typeof ts === 'string') {
        const tm = ts.match(/(\d+):(\d+):(\d+)/);
        if (tm) { hh = +tm[1]; mm = +tm[2]; ss = +tm[3]; }
      }
      if (dm) {
        gpsUtcDate = new Date(Date.UTC(+dm[1], +dm[2] - 1, +dm[3], hh, mm, ss));
      }
    }

    let usedOffsetMin = manualOffsetMin !== null && manualOffsetMin !== undefined
      ? manualOffsetMin
      : (parsedOffsetMin !== null ? parsedOffsetMin : (Number.isFinite(lng) ? Math.round(lng / 15) * 60 : 0));

    if (gpsUtcDate && (manualOffsetMin === null || manualOffsetMin === undefined)) {
      utcDate = gpsUtcDate;
      timeSource = 'GPS Satellite UTC Stamp (Exact)';
    } else if (dto) {
      const localMs = Date.UTC(dto.year, dto.month - 1, dto.day, dto.hour, dto.min, dto.sec);
      utcDate = new Date(localMs - usedOffsetMin * 60000);
      if (manualOffsetMin !== null && manualOffsetMin !== undefined) {
        timeSource = `EXIF DateTimeOriginal + Manual UTC${usedOffsetMin >= 0 ? '+' : ''}${(usedOffsetMin / 60).toFixed(1)}`;
      } else if (parsedOffsetMin !== null) {
        timeSource = `EXIF DateTimeOriginal (${offsetStr})`;
      } else {
        timeSource = `EXIF DateTimeOriginal + Est. Solar TZ (UTC${usedOffsetMin >= 0 ? '+' : ''}${Math.round(usedOffsetMin / 60)})`;
      }
    }

    if (dto && mod) {
      const dtoMs = Date.UTC(dto.year, dto.month - 1, dto.day, dto.hour, dto.min, dto.sec);
      const modMs = Date.UTC(mod.year, mod.month - 1, mod.day, mod.hour, mod.min, mod.sec);
      if (modMs < dtoMs - 60000) {
        warnings.push('Clock Anomaly: ModifyDate is EARLIER than DateTimeOriginal (possible timestamp spoofing or wrong device clock).');
      } else if (modMs - dtoMs > 3600000) {
        const hrs = ((modMs - dtoMs) / 3600000).toFixed(1);
        warnings.push(`Post-Capture Modification: File modified ${hrs} hours after original shutter click.`);
      }
    }

    if (gpsUtcDate && dto && parsedOffsetMin !== null) {
      const localUtcMs = Date.UTC(dto.year, dto.month - 1, dto.day, dto.hour, dto.min, dto.sec) - parsedOffsetMin * 60000;
      const diffMin = Math.abs(gpsUtcDate.getTime() - localUtcMs) / 60000;
      if (diffMin > 30) {
        warnings.push(`GPS vs EXIF Clock Mismatch: GPS UTC and DateTimeOriginal differ by ${Math.round(diffMin)} minutes!`);
      }
    }

    if (Number.isFinite(lng) && parsedOffsetMin !== null) {
      const solarTzHours = Math.round(lng / 15);
      const exifTzHours = parsedOffsetMin / 60;
      if (Math.abs(solarTzHours - exifTzHours) >= 2.5) {
        warnings.push(`Timezone Anomaly: GPS longitude suggests ~UTC${solarTzHours >= 0 ? '+' : ''}${solarTzHours}, but OffsetTimeOriginal is ${offsetStr}.`);
      }
    }

    const solar = utcDate && Number.isFinite(lat) && Number.isFinite(lng) ? calculateSolarPosition(utcDate, lat, lng) : null;
    return { utcDate, timeSource, usedOffsetMin, warnings, solar, gpsUtcDate };
  }

  // =========================================================================
  // 9. OPTICS, DEPTH OF FIELD & EXPOSURE PHYSICS CALCULATOR
  // =========================================================================
  function calculateOpticsPhysics(exifrData, customSubjectDistM) {
    if (!exifrData) return null;
    const fl = Number(exifrData.FocalLength);
    const fl35 = Number(exifrData.FocalLengthIn35mmFormat);
    const fNum = Number(exifrData.FNumber);
    const exp = Number(exifrData.ExposureTime);
    const iso = Number(exifrData.ISO);
    const exifDist = Number(exifrData.SubjectDistance);

    const cropFactor = fl > 0 && fl35 > 0 ? fl35 / fl : null;
    const eqAperture = cropFactor && fNum > 0 ? fNum * cropFactor : null;
    const effFl35 = fl35 > 0 ? fl35 : (fl > 0 ? fl : null);
    const diagFovDeg = effFl35 ? (2 * Math.atan(43.27 / (2 * effFl35)) * 180) / Math.PI : null;
    const horizFovDeg = effFl35 ? (2 * Math.atan(36 / (2 * effFl35)) * 180) / Math.PI : null;

    let ev100 = null;
    if (fNum > 0 && exp > 0) {
      const evAtIso = Math.log2((fNum * fNum) / exp);
      ev100 = iso > 0 ? evAtIso - Math.log2(iso / 100) : evAtIso;
    }

    // Circle of Confusion (0.029mm for 35mm full frame, scaled by crop factor)
    const cocMm = cropFactor ? 0.029 / cropFactor : 0.029;
    const distM = customSubjectDistM > 0 ? customSubjectDistM : (exifDist > 0 ? exifDist : 3.0);
    let hyperfocalM = null, dofNearM = null, dofFarM = null;
    if (fl > 0 && fNum > 0) {
      const H_mm = (fl * fl) / (fNum * cocMm) + fl;
      hyperfocalM = H_mm / 1000;
      const s_mm = distM * 1000;
      dofNearM = (s_mm * (H_mm - fl)) / (H_mm + s_mm - 2 * fl) / 1000;
      dofFarM = s_mm >= H_mm ? Infinity : ((s_mm * (H_mm - fl)) / (H_mm - s_mm)) / 1000;
    }

    return {
      focalLength: fl || null,
      focalLength35: fl35 || null,
      cropFactor,
      eqAperture,
      diagFovDeg,
      horizFovDeg,
      ev100,
      subjectDistM: distM,
      fromExifDistance: exifDist > 0 && !(customSubjectDistM > 0),
      hyperfocalM,
      dofNearM,
      dofFarM
    };
  }

  // =========================================================================
  // 10. GHOST THUMBNAIL dHASH & ASPECT DIFF DETECTOR
  // =========================================================================
  function computeCanvasDHash(imgEl) {
    const c = document.createElement('canvas');
    c.width = 9;
    c.height = 8;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(imgEl, 0, 0, 9, 8);
    const data = ctx.getImageData(0, 0, 9, 8).data;
    let bits = '';
    for (let y = 0; y < 8; y++) {
      for (let x = 0; x < 8; x++) {
        const i1 = (y * 9 + x) * 4;
        const i2 = (y * 9 + x + 1) * 4;
        const g1 = 0.299 * data[i1] + 0.587 * data[i1 + 1] + 0.114 * data[i1 + 2];
        const g2 = 0.299 * data[i2] + 0.587 * data[i2 + 1] + 0.114 * data[i2 + 2];
        bits += g1 > g2 ? '1' : '0';
      }
    }
    return bits;
  }

  function compareMainAndThumbnail(mainImg, thumbImg) {
    if (!mainImg || !thumbImg || !mainImg.naturalWidth || !thumbImg.naturalWidth) return null;
    const mainAspect = mainImg.naturalWidth / mainImg.naturalHeight;
    const thumbAspect = thumbImg.naturalWidth / thumbImg.naturalHeight;
    // Account for 90-deg rotation edge case
    const aspectDiffDirect = Math.abs(mainAspect - thumbAspect) / Math.max(mainAspect, thumbAspect);
    const aspectDiffRot = Math.abs(mainAspect - 1 / thumbAspect) / Math.max(mainAspect, 1 / thumbAspect);
    const minAspectDiff = Math.min(aspectDiffDirect, aspectDiffRot);

    const h1 = computeCanvasDHash(mainImg);
    const h2 = computeCanvasDHash(thumbImg);
    let hamming = 0;
    for (let i = 0; i < 64; i++) if (h1[i] !== h2[i]) hamming++;

    const isMismatch = minAspectDiff > 0.08 || hamming > 14;
    return {
      mainDims: `${mainImg.naturalWidth}×${mainImg.naturalHeight}`,
      thumbDims: `${thumbImg.naturalWidth}×${thumbImg.naturalHeight}`,
      aspectDiffPct: (minAspectDiff * 100).toFixed(1),
      hammingDistance: hamming,
      similarityPct: Math.round(((64 - hamming) / 64) * 100),
      isMismatch
    };
  }

  // =========================================================================
  // 11. HARDWARE TELEMETRY (SHUTTER COUNT, SERIALS, RUN-TIME, TILT, AF BOXES)
  // =========================================================================
  function getTagVal(tagsObj, keys) {
    if (!tagsObj) return null;
    for (const k of keys) {
      const entry = tagsObj[k];
      if (entry !== undefined && entry !== null) {
        if (typeof entry === 'object' && 'description' in entry) {
          if (entry.description !== '' && entry.description !== undefined) return entry.description;
          if (entry.value !== undefined) return entry.value;
        }
        return entry;
      }
    }
    return null;
  }

  function extractHardwareTelemetry(exifrData, exifReaderExpanded, xmpInfo) {
    const flatReader = {};
    if (exifReaderExpanded) {
      ['exif', 'file', 'ifd0', 'makerNotes', 'xmp', 'iptc', 'gps'].forEach((grp) => {
        if (exifReaderExpanded[grp] && typeof exifReaderExpanded[grp] === 'object') {
          Object.assign(flatReader, exifReaderExpanded[grp]);
        }
      });
    }

    const shutterCount = getTagVal(flatReader, [
      'ShutterCount', 'ImageCount', 'TotalShutterReleases', 'MechanicalShutterCount',
      'ShutterCount2', 'ShutterCount3', 'FileNumber'
    ]) || (exifrData && (exifrData.ShutterCount || exifrData.ImageNumber || exifrData.ImageCount));

    const bodySerial = getTagVal(flatReader, [
      'SerialNumber', 'BodySerialNumber', 'InternalSerialNumber', 'CameraSerialNumber', 'DriveSerialNumber'
    ]) || (exifrData && (exifrData.SerialNumber || exifrData.BodySerialNumber || exifrData.InternalSerialNumber));

    const lensSerial = getTagVal(flatReader, ['LensSerialNumber', 'LensID']) || (exifrData && exifrData.LensSerialNumber);
    const ownerName = getTagVal(flatReader, ['OwnerName', 'CameraOwnerName', 'Artist', 'Creator']) ||
      (exifrData && (exifrData.CameraOwnerName || exifrData.OwnerName || exifrData.Artist || exifrData.Copyright));

    const runTimeRaw = getTagVal(flatReader, ['RunTimeValue', 'RunTime']) || (exifrData && exifrData.RunTimeValue);
    let deviceUptime = null;
    if (typeof runTimeRaw === 'number' && runTimeRaw > 0) {
      // Apple RunTimeScale is typically 1,000,000,000 (ns) -> check magnitude
      const sec = runTimeRaw > 1e8 ? runTimeRaw / 1e9 : runTimeRaw;
      const hrs = Math.floor(sec / 3600);
      const mins = Math.floor((sec % 3600) / 60);
      deviceUptime = `${hrs}h ${mins}m since last reboot`;
    }

    // Acceleration / Roll / Pitch
    let rollDeg = null;
    const accel = (exifrData && exifrData.AccelerationVector) || getTagVal(flatReader, ['AccelerationVector']);
    if (Array.isArray(accel) && accel.length >= 2) {
      rollDeg = (Math.atan2(accel[0], -accel[1]) * 180) / Math.PI;
    } else if (exifrData && typeof exifrData.RollAngle === 'number') {
      rollDeg = exifrData.RollAngle;
    }

    // AF / Face Detection Boxes
    const focusBoxes = [];
    if (exifrData && Array.isArray(exifrData.SubjectArea) && exifrData.SubjectArea.length >= 2) {
      const [cx, cy, w, h] = exifrData.SubjectArea;
      const imgW = exifrData.ExifImageWidth || exifrData.ImageWidth;
      const imgH = exifrData.ExifImageHeight || exifrData.ImageHeight;
      if (imgW && imgH) {
        focusBoxes.push({
          x: cx / imgW,
          y: cy / imgH,
          w: (w || imgW * 0.12) / imgW,
          h: (h || imgH * 0.12) / imgH,
          label: 'AF Subject Area',
          normalizedCenter: true
        });
      }
    }
    if (xmpInfo && xmpInfo.regions && xmpInfo.regions.length > 0) {
      xmpInfo.regions.forEach((r) => focusBoxes.push(r));
    }

    return {
      shutterCount: shutterCount !== null && shutterCount !== undefined ? String(shutterCount) : null,
      bodySerial: bodySerial ? String(bodySerial) : null,
      lensSerial: lensSerial ? String(lensSerial) : null,
      ownerName: ownerName ? String(ownerName) : null,
      deviceUptime,
      rollDeg,
      focusBoxes
    };
  }

  // =========================================================================
  // 12. PRIVACY "DOXX RISK SCORE" (0–100)
  // =========================================================================
  function computePrivacyRisk({ exifrData, hwTelemetry, thumbDiff, embeddedMedia, binaryInfo, xmpInfo }) {
    let score = 0;
    const factors = [];

    if (exifrData && Number.isFinite(exifrData.latitude) && Number.isFinite(exifrData.longitude)) {
      score += 40;
      factors.push({ pts: 40, level: 'critical', title: 'Exact GPS Coordinates Exposed', detail: `${exifrData.latitude.toFixed(5)}°, ${exifrData.longitude.toFixed(5)}° pinpoints exact physical location.` });
    }
    if (hwTelemetry && (hwTelemetry.bodySerial || hwTelemetry.lensSerial)) {
      score += 20;
      factors.push({ pts: 20, level: 'high', title: 'Hardware Serial Number(s) Embedded', detail: `Allows correlating anonymous photos to the same physical camera/lens.` });
    }
    if (hwTelemetry && hwTelemetry.ownerName) {
      score += 15;
      factors.push({ pts: 15, level: 'high', title: 'Author / Owner / Copyright Identity', detail: `Exposes "${hwTelemetry.ownerName}".` });
    }
    if (thumbDiff && thumbDiff.isMismatch) {
      score += 15;
      factors.push({ pts: 15, level: 'critical', title: 'Uncropped Ghost Thumbnail Leak', detail: `Embedded IFD1 preview differs from main image (${thumbDiff.aspectDiffPct}% aspect / ${thumbDiff.hammingDistance}/64 hash delta).` });
    }
    if (embeddedMedia && embeddedMedia.motionVideoBlob) {
      score += 10;
      factors.push({ pts: 10, level: 'medium', title: 'Hidden Motion Video Embedded', detail: `${formatBytes(embeddedMedia.motionVideoSize)} MP4 video clip is bundled inside this photo.` });
    }
    if (binaryInfo && binaryInfo.trailingBytes && binaryInfo.trailingBytes.length > 0 && !(embeddedMedia && embeddedMedia.motionVideoBlob)) {
      score += 10;
      factors.push({ pts: 10, level: 'high', title: 'Trailing Data After Image End', detail: `${formatBytes(binaryInfo.trailingBytes.length)} appended after EOI/IEND (${binaryInfo.trailingMagic}).` });
    }
    if (exifrData && exifrData.DateTimeOriginal) {
      score += 10;
      factors.push({ pts: 10, level: 'low', title: 'Exact Capture Timestamp', detail: String(exifrData.DateTimeOriginal) });
    }
    if (xmpInfo && (xmpInfo.originalDocumentId || xmpInfo.historyEvents.length > 0)) {
      score += 5;
      factors.push({ pts: 5, level: 'low', title: 'XMP Document History / UUIDs', detail: `${xmpInfo.historyEvents.length} edit event(s) / document lineage IDs recorded.` });
    }

    score = Math.min(100, score);
    let rating = 'Low Risk (Clean)';
    let color = 'var(--success)';
    if (score >= 65) { rating = 'CRITICAL PRIVACY LEAK'; color = 'var(--danger)'; }
    else if (score >= 35) { rating = 'MODERATE EXPOSURE'; color = 'var(--warning)'; }
    else if (score > 0) { rating = 'LOW EXPOSURE'; color = 'var(--primary)'; }

    return { score, rating, color, factors };
  }

  // =========================================================================
  // 13. SURGICAL METADATA STRIPPER (LOSSLESS SEGMENT / PIEXIF / CANVAS)
  // =========================================================================
  function stripJpegSegmentsLossless(arrayBuffer, options) {
    const bytes = new Uint8Array(arrayBuffer);
    const len = bytes.length;
    if (bytes[0] !== 0xff || bytes[1] !== 0xd8) return null;

    const keepIcc = options && options.keepIcc !== false;
    const chunks = [bytes.subarray(0, 2)]; // SOI
    let offset = 2;

    while (offset < len - 1) {
      if (bytes[offset] !== 0xff) { offset++; continue; }
      while (offset < len && bytes[offset] === 0xff) offset++;
      if (offset >= len) break;
      const markerCode = bytes[offset];
      const markerStart = offset - 1;
      offset++;

      if (markerCode === 0x00) continue;
      if (markerCode === 0xd9) {
        chunks.push(new Uint8Array([0xff, 0xd9]));
        break;
      }
      if (markerCode >= 0xd0 && markerCode <= 0xd7) continue;
      if (offset + 2 > len) break;

      const segLen = (bytes[offset] << 8) | bytes[offset + 1];
      if (segLen < 2) break;
      const payloadStart = offset + 2;
      const segEnd = Math.min(len, offset + segLen);

      if (markerCode === 0xda) {
        // Keep SOS + all entropy scan data right up to EOI (and append clean EOI)
        let scanPtr = segEnd;
        let foundEoi = false;
        while (scanPtr < len - 1) {
          if (bytes[scanPtr] === 0xff) {
            const nb = bytes[scanPtr + 1];
            if (nb === 0x00 || (nb >= 0xd0 && nb <= 0xd7) || nb === 0xff) {
              scanPtr += nb === 0xff ? 1 : 2;
              continue;
            }
            if (nb === 0xd9) {
              chunks.push(bytes.subarray(markerStart, scanPtr + 2));
              foundEoi = true;
              break;
            }
            break;
          }
          scanPtr++;
        }
        if (foundEoi) break;
        if (scanPtr >= len - 1) scanPtr = len;
        chunks.push(bytes.subarray(markerStart, scanPtr));
        offset = scanPtr;
        continue;
      }

      // Decide whether to keep or strip this marker
      let keep = true;
      if (markerCode === 0xe1 || markerCode === 0xec || markerCode === 0xed || markerCode === 0xeb || markerCode === 0xfe) {
        keep = false; // Strip APP1 (EXIF/XMP), APP12, APP13 (IPTC), APP11 (JUMBF), COM
      } else if (markerCode === 0xe2) {
        const sig = decodeBytesLatin1(bytes, payloadStart, Math.min(segEnd, payloadStart + 12));
        keep = keepIcc && sig.startsWith('ICC_PROFILE');
      } else if (markerCode >= 0xe3 && markerCode <= 0xef && markerCode !== 0xee) {
        keep = false;
      }

      if (keep) chunks.push(bytes.subarray(markerStart, segEnd));
      offset = segEnd;
    }

    return new Blob(chunks, { type: 'image/jpeg' });
  }

  function stripPngChunksLossless(arrayBuffer) {
    const bytes = new Uint8Array(arrayBuffer);
    const len = bytes.length;
    if (!(bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47)) return null;
    const chunks = [bytes.subarray(0, 8)];
    let offset = 8;
    const stripTypes = new Set(['tEXt', 'zTXt', 'iTXt', 'eXIf', 'tIME', 'caBX', 'c2pa']);

    while (offset + 12 <= len) {
      const chunkLen = ((bytes[offset] << 24) | (bytes[offset + 1] << 16) | (bytes[offset + 2] << 8) | bytes[offset + 3]) >>> 0;
      const type = String.fromCharCode(bytes[offset + 4], bytes[offset + 5], bytes[offset + 6], bytes[offset + 7]);
      const chunkEnd = offset + 12 + chunkLen;
      if (chunkEnd > len) break;
      if (!stripTypes.has(type)) chunks.push(bytes.subarray(offset, chunkEnd));
      offset = chunkEnd;
      if (type === 'IEND') break;
    }
    return new Blob(chunks, { type: 'image/png' });
  }

  async function surgicalStripImage(file, arrayBuffer, mode, imgEl) {
    if (mode === 'lossless-all') {
      const jpgClean = stripJpegSegmentsLossless(arrayBuffer, { keepIcc: true });
      if (jpgClean) return { blob: jpgClean, ext: 'jpg', note: 'Lossless JPEG segment scrub (0% pixel re-compression)' };
      const pngClean = stripPngChunksLossless(arrayBuffer);
      if (pngClean) return { blob: pngClean, ext: 'png', note: 'Lossless PNG chunk scrub (0% pixel re-compression)' };
    }

    if (mode === 'surgical-keep-camera' && global.piexif) {
      const jpgBase = stripJpegSegmentsLossless(arrayBuffer, { keepIcc: true });
      if (jpgBase) {
        // Read original dataUrl for piexif, extract clean EXIF subset, insert into lossless base
        const origDataUrl = await new Promise((resolve) => {
          const r = new FileReader();
          r.onload = () => resolve(r.result);
          r.readAsDataURL(new Blob([arrayBuffer], { type: 'image/jpeg' }));
        });
        const baseDataUrl = await new Promise((resolve) => {
          const r = new FileReader();
          r.onload = () => resolve(r.result);
          r.readAsDataURL(jpgBase);
        });
        try {
          const exifObj = global.piexif.load(origDataUrl);
          // Wipe GPS, Thumbnail (1st), Serials, Owner, MakerNote, UserComment
          exifObj['GPS'] = {};
          exifObj['1st'] = {};
          exifObj['thumbnail'] = null;
          if (exifObj['0th']) {
            delete exifObj['0th'][global.piexif.ImageIFD.Artist];
            delete exifObj['0th'][global.piexif.ImageIFD.Copyright];
            delete exifObj['0th'][global.piexif.ImageIFD.Software];
            delete exifObj['0th'][global.piexif.ImageIFD.HostComputer];
            delete exifObj['0th'][global.piexif.ImageIFD.ImageDescription];
          }
          if (exifObj['Exif']) {
            delete exifObj['Exif'][global.piexif.ExifIFD.MakerNote];
            delete exifObj['Exif'][global.piexif.ExifIFD.UserComment];
            delete exifObj['Exif'][global.piexif.ExifIFD.CameraOwnerName];
            delete exifObj['Exif'][global.piexif.ExifIFD.BodySerialNumber];
            delete exifObj['Exif'][global.piexif.ExifIFD.LensSerialNumber];
            delete exifObj['Exif'][global.piexif.ExifIFD.ImageUniqueID];
          }
          const dumped = global.piexif.dump(exifObj);
          const patched = global.piexif.insert(dumped, baseDataUrl);
          const res = await fetch(patched);
          return { blob: await res.blob(), ext: 'jpg', note: 'Surgical scrub: Camera & exposure kept; GPS, Serials, Owner, MakerNote & Thumbnail wiped!' };
        } catch (_) {
          // Fallback to lossless-all if piexif couldn't parse exotic IFD
          return { blob: jpgBase, ext: 'jpg', note: 'Exotic EXIF layout detected — fell back to full lossless metadata strip.' };
        }
      }
    }

    // Mode: canvas-reencode (or fallback for WebP/HEIC/TIFF)
    if (!imgEl || !imgEl.naturalWidth) throw new Error('Image canvas not ready for re-encoding.');
    const c = document.createElement('canvas');
    c.width = imgEl.naturalWidth;
    c.height = imgEl.naturalHeight;
    const ctx = c.getContext('2d');
    ctx.drawImage(imgEl, 0, 0);
    const outMime = file.type === 'image/png' ? 'image/png' : (file.type === 'image/webp' ? 'image/webp' : 'image/jpeg');
    const outExt = outMime === 'image/png' ? 'png' : (outMime === 'image/webp' ? 'webp' : 'jpg');
    const blob = await new Promise((resolve) => c.toBlob(resolve, outMime, 0.94));
    return { blob, ext: outExt, note: 'Full HTML5 Canvas pixel re-encode (destroys all headers, DQT DNA & trailing payloads).' };
  }

  // =========================================================================
  // 14. BATCH DIFF, HAVERSINE DISTANCE & SAME-CAMERA CORRELATION
  // =========================================================================
  function haversineKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const rad = Math.PI / 180;
    const dLat = (lat2 - lat1) * rad;
    const dLon = (lon2 - lon1) * rad;
    const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  function diffMetadataRecords(recA, recB) {
    const mapA = (recA && recA.exifr) || {};
    const mapB = (recB && recB.exifr) || {};
    const keys = Array.from(new Set([...Object.keys(mapA), ...Object.keys(mapB)])).sort();
    const rows = [];
    const fmt = (v) => {
      if (v === undefined || v === null) return '—';
      if (v instanceof Date) return v.toISOString();
      if (v instanceof Uint8Array) return `[Binary ${v.length} B]`;
      if (typeof v === 'object') return JSON.stringify(v);
      return String(v);
    };
    keys.forEach((k) => {
      const va = fmt(mapA[k]);
      const vb = fmt(mapB[k]);
      let status = 'same';
      if (va === '—' && vb !== '—') status = 'added';
      else if (va !== '—' && vb === '—') status = 'removed';
      else if (va !== vb) status = 'changed';
      rows.push({ key: k, a: va, b: vb, status });
    });
    return rows;
  }

  function correlateBatch(records) {
    const serialGroups = {};
    const dqtGroups = {};
    const gpsPoints = [];

    records.forEach((r, idx) => {
      const serial = r.hwTelemetry && (r.hwTelemetry.bodySerial || r.hwTelemetry.lensSerial);
      if (serial) {
        if (!serialGroups[serial]) serialGroups[serial] = [];
        serialGroups[serial].push({ index: idx, name: r.file.name });
      }
      const dqtFp = r.binaryInfo && r.binaryInfo.dqtAnalysis && r.binaryInfo.dqtAnalysis.dqtFingerprint;
      if (dqtFp) {
        if (!dqtGroups[dqtFp]) dqtGroups[dqtFp] = [];
        dqtGroups[dqtFp].push({ index: idx, name: r.file.name });
      }
      if (r.exifr && Number.isFinite(r.exifr.latitude) && Number.isFinite(r.exifr.longitude)) {
        const dt = r.timeAudit && r.timeAudit.utcDate ? r.timeAudit.utcDate.getTime() : idx;
        gpsPoints.push({
          index: idx,
          name: r.file.name,
          lat: r.exifr.latitude,
          lng: r.exifr.longitude,
          ts: dt,
          dateLabel: r.exifr.DateTimeOriginal ? String(r.exifr.DateTimeOriginal) : `Photo #${idx + 1}`
        });
      }
    });

    gpsPoints.sort((a, b) => a.ts - b.ts);
    const legs = [];
    for (let i = 1; i < gpsPoints.length; i++) {
      const p1 = gpsPoints[i - 1], p2 = gpsPoints[i];
      const distKm = haversineKm(p1.lat, p1.lng, p2.lat, p2.lng);
      const dtHrs = Math.abs(p2.ts - p1.ts) / 3600000;
      const speedKmh = dtHrs > 0.001 && p1.ts > 1e11 && p2.ts > 1e11 ? distKm / dtHrs : null;
      legs.push({ from: p1.name, to: p2.name, distKm, speedKmh });
    }

    return { serialGroups, dqtGroups, gpsPoints, legs };
  }

  global.PixelCraftExifForensics = {
    escapeHtml,
    formatBytes,
    formatHexDump,
    computeFileHashes,
    analyzeBinaryStructure,
    extractXmpForensics,
    analyzeAiProvenance,
    scanEmbeddedMedia,
    calculateSolarPosition,
    auditTimestamps,
    calculateOpticsPhysics,
    compareMainAndThumbnail,
    extractHardwareTelemetry,
    computePrivacyRisk,
    surgicalStripImage,
    haversineKm,
    diffMetadataRecords,
    correlateBatch
  };
})(typeof window !== 'undefined' ? window : globalThis);
