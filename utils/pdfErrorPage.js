/**
 * Renders the enhanced, responsive, theme-aware 404 / 400 Unavailable PDF Link page
 * for PixelCraft AI (/p/:id and /p/).
 */

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

const SUGGESTED_TOOLS = [
  {
    category: 'pdf',
    badge: '24h Ephemeral',
    badgeTone: 'blue',
    name: 'PDF to Link Converter',
    href: '/tools/pdf-to-link.html',
    desc: 'Upload any PDF (up to 50MB) and generate a fresh shareable link & QR code with automatic 24-hour cleanup.',
    cta: 'Create New Link',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>`
  },
  {
    category: 'pdf',
    badge: '100% Client-Side',
    badgeTone: 'indigo',
    name: 'Images to PDF',
    href: '/tools/images-to-pdf.html',
    desc: 'Merge scanned photos, receipts, and ID pages into a clean, multi-page PDF directly inside your browser.',
    cta: 'Compile PDF',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>`
  },
  {
    category: 'pdf',
    badge: '100% Client-Side',
    badgeTone: 'cyan',
    name: 'Custom QR Code Studio',
    href: '/tools/qr-generator.html',
    desc: '15 QR modes including URL + UTM builder, Wi-Fi, UPI, branded logos, batch ZIP & AES-256 encrypted QR vaults.',
    cta: 'Open QR Studio',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="5" height="5" x="3" y="3" rx="1"></rect><rect width="5" height="5" x="16" y="3" rx="1"></rect><rect width="5" height="5" x="3" y="16" rx="1"></rect><path d="M21 16h-3a2 2 0 0 0-2 2v3"></path><path d="M21 21v.01"></path></svg>`
  },
  {
    category: 'privacy',
    badge: 'Threat Intel',
    badgeTone: 'rose',
    name: 'Phishing & Malware Scanner',
    href: '/tools/phishing-scanner.html',
    desc: 'Inspect suspicious URLs inside an isolated sandbox for homograph spoofing, redirect chains & scam domains.',
    cta: 'Scan URL',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`
  },
  {
    category: 'privacy',
    badge: 'Volatile RAM',
    badgeTone: 'emerald',
    name: 'Forensic Metadata Sanitizer',
    href: '/tools/forensic-sanitizer.html',
    desc: 'Strip hidden metadata, ICC color profiles, and forensic tracking markers in memory with zero disk retention.',
    cta: 'Sanitize File',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="m9 12 2 2 4-4"></path></svg>`
  },
  {
    category: 'privacy',
    badge: '100% Client-Side',
    badgeTone: 'emerald',
    name: 'Digital Fingerprint Wiper',
    href: '/tools/digital-fingerprint-wiper.html',
    desc: 'Remove EXIF tags, GPS location telemetry, and PRNU camera sensor noise from photos before sharing.',
    cta: 'Wipe EXIF',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10"></path><path d="M12 6a6 6 0 1 0 6 6"></path><circle cx="12" cy="12" r="2"></circle><path d="M22 2 12 12"></path></svg>`
  },
  {
    category: 'media',
    badge: '100% Client-Side',
    badgeTone: 'indigo',
    name: 'Image Compressor',
    href: '/tools/image-compressor.html',
    desc: 'Reduce JPG, PNG & WebP file sizes up to 80% or hit exact KB limits for forms and portals in browser RAM.',
    cta: 'Compress Image',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 14 10 14 10 20"></polyline><polyline points="20 10 14 10 14 4"></polyline><line x1="14" y1="10" x2="21" y2="3"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>`
  },
  {
    category: 'media',
    badge: '100% Client-Side',
    badgeTone: 'blue',
    name: 'Format Converter',
    href: '/tools/format-converter.html',
    desc: 'Convert seamlessly between PNG, JPG, WebP, AVIF, and SVG locally with zero file uploads.',
    cta: 'Convert Format',
    icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>`
  }
];

const GOVERNANCE_DOCS = [
  {
    tag: 'Architecture Spec',
    tone: 'cyan',
    title: 'Security Whitepaper (v3.5)',
    href: '/security-whitepaper.html',
    desc: 'Deep technical specification of zero-knowledge client pipelines, AES-256 Encrypt-then-MAC, PRNU scrubbing, and SSRF defense.',
    cta: 'Read Whitepaper',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>`
  },
  {
    tag: 'Verified Inventory',
    tone: 'emerald',
    title: 'Data Practices & Retention',
    href: '/data-practices.html',
    desc: 'Code-verified breakdown of every tool, volatile memory buffer, zero MongoDB PDF policy, and the 24-hour cleanup schedule.',
    cta: 'View Data Practices',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>`
  },
  {
    tag: 'GDPR • DPDPA 2023',
    tone: 'blue',
    title: 'Privacy Policy',
    href: '/privacy-policy.html',
    desc: 'Details on client-side isolation, ephemeral HTTPS transport, automatic file purging, and your statutory data rights.',
    cta: 'Read Privacy Policy',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>`
  },
  {
    tag: 'Legal Agreement',
    tone: 'indigo',
    title: 'Terms & Conditions',
    href: '/terms-conditions.html',
    desc: 'Acceptable Use Policy, temporary link sharing rules, Intermediary Safe Harbor disclosures, and user responsibilities.',
    cta: 'Read Terms',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>`
  },
  {
    tag: 'Consent & Storage',
    tone: 'amber',
    title: 'Cookies Policy',
    href: '/cookies-policy.html',
    desc: 'Transparent documentation of session cookies, localStorage theme keys, and Consent Mode v2 controls.',
    cta: 'View Cookies Policy',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M8.5 8.5h.01"></path><path d="M16 15.5h.01"></path><path d="M12 12h.01"></path><path d="M11 17h.01"></path><path d="M15 9h.01"></path></svg>`
  },
  {
    tag: 'Support & Abuse',
    tone: 'rose',
    title: 'Disclaimer & Contact',
    href: '/contact-us.html',
    desc: 'Need to report an abusive link, ask a technical question, or read service disclaimers? Reach our team (< 24–48h SLA).',
    cta: 'Contact Support',
    secondaryHref: '/disclaimer.html',
    secondaryLabel: 'Disclaimer',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`
  }
];

const BLOG_ARTICLES = [
  {
    badge: 'Document Security',
    readTime: '9 Min Read',
    title: 'The Ultimate PDF Security Guide: True Redaction vs Black Boxes',
    href: '/blog/securing-pdfs-redaction-metadata-stripping-and-encryption.html',
    desc: 'Why drawing black boxes fails to protect sensitive text—and how true byte-level redaction & metadata stripping work.'
  },
  {
    badge: 'Zero-Knowledge',
    readTime: '8 Min Read',
    title: 'Zero-Knowledge Architecture: Client-Side vs Server Processing',
    href: '/blog/browser-side-vs-server-side-file-processing.html',
    desc: 'Understand why browser-based WebAssembly & Web Workers minimize data exposure compared to permanent cloud converters.'
  },
  {
    badge: 'Document Privacy',
    readTime: '8 Min Read',
    title: 'Compiling Images into PDF Packages: Resolution, Margins & Flattening',
    href: '/blog/compiling-scanned-images-to-pdf-documents.html',
    desc: 'Best practices for converting photos and scanned documents into clean, watermark-free PDF packages.'
  },
  {
    badge: 'QR & Threat Defense',
    readTime: 'Deep Dive',
    title: 'Next-Gen QR Engineering, Social Gradients & Quishing Defense',
    href: '/blog/qr-code-security-quishing-and-malicious-redirects.html',
    desc: 'Learn how QR phishing (Quishing) attacks work and how to verify links safely before opening shared URLs.'
  }
];

function renderToolCards() {
  return SUGGESTED_TOOLS.map(tool => `
    <a href="${tool.href}" class="tool-card" data-cat="${tool.category}">
      <div class="tool-card-top">
        <div class="icon-box tone-${tool.badgeTone}">${tool.icon}</div>
        <span class="pill-tag tone-${tool.badgeTone}">${escapeHtml(tool.badge)}</span>
      </div>
      <h3>${escapeHtml(tool.name)}</h3>
      <p>${escapeHtml(tool.desc)}</p>
      <div class="card-foot">
        <span class="card-link-cta">${escapeHtml(tool.cta)} <span>&rarr;</span></span>
      </div>
    </a>
  `).join('');
}

function renderGovernanceCards() {
  return GOVERNANCE_DOCS.map(doc => `
    <div class="gov-card">
      <div class="gov-card-head">
        <div class="icon-box sm tone-${doc.tone}">${doc.icon}</div>
        <span class="pill-tag tone-${doc.tone}">${escapeHtml(doc.tag)}</span>
      </div>
      <h3>${escapeHtml(doc.title)}</h3>
      <p>${escapeHtml(doc.desc)}</p>
      <div class="gov-card-actions">
        <a href="${doc.href}" class="gov-link">${escapeHtml(doc.cta)} &rarr;</a>
        ${doc.secondaryHref ? `<a href="${doc.secondaryHref}" class="gov-link-muted">${escapeHtml(doc.secondaryLabel)}</a>` : ''}
      </div>
    </div>
  `).join('');
}

function renderBlogCards() {
  return BLOG_ARTICLES.map(post => `
    <a href="${post.href}" class="blog-card">
      <div class="blog-card-top">
        <span class="pill-tag tone-indigo">${escapeHtml(post.badge)}</span>
        <span class="read-time">${escapeHtml(post.readTime)}</span>
      </div>
      <h3>${escapeHtml(post.title)}</h3>
      <p>${escapeHtml(post.desc)}</p>
      <div class="card-foot">
        <span class="card-link-cta">Read Article <span>&rarr;</span></span>
      </div>
    </a>
  `).join('');
}

function renderPdfUnavailablePage(options = {}) {
  const {
    statusCode = 404,
    reasonType = 'expired',
    fileId = '',
    headline = '404 — PDF Link Expired or Not Found',
    message = 'This PDF link is invalid, expired, or has been removed.'
  } = options;

  const isBadFormat = statusCode === 400 || reasonType === 'invalid';
  const safeIdDisplay = fileId ? `/p/${escapeHtml(fileId)}` : (isBadFormat ? 'Malformed Link Token' : '/p/—');
  const statusPillText = isBadFormat
    ? 'HTTP 400 • INVALID LINK FORMAT'
    : 'HTTP 404 • EPHEMERAL LINK EXPIRED OR PURGED';
  const statusValueText = isBadFormat ? '400 Bad Request' : '404 Purged / Not Found';

  return `<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow, noarchive" />
  <meta name="googlebot" content="noindex, nofollow, noarchive" />
  <meta name="theme-color" content="#0b0f19" />
  <title>${escapeHtml(headline)} | PixelCraft AI</title>
  <link rel="icon" href="/logo.jpg?v=5" />
  <link rel="manifest" href="/manifest.json" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  <script>
    (function () {
      try {
        var saved = localStorage.getItem('pixelcraft-theme');
        var theme = (saved === 'light' || saved === 'dark') ? saved : 'dark';
        document.documentElement.setAttribute('data-theme', theme);
      } catch (e) {
        document.documentElement.setAttribute('data-theme', 'dark');
      }
    })();
  </script>
  <style>
    :root,
    [data-theme="dark"] {
      --bg-page: #070b14;
      --bg-elevated: rgba(17, 24, 39, 0.82);
      --bg-subtle: rgba(30, 41, 59, 0.55);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --nav-bg: rgba(9, 13, 24, 0.86);
      --border: rgba(148, 163, 184, 0.16);
      --border-strong: rgba(148, 163, 184, 0.28);
      --text-heading: #f8fafc;
      --text-body: #cbd5e1;
      --text-muted: #94a3b8;
      --primary: #3b82f6;
      --primary-hover: #60a5fa;
      --primary-soft: rgba(59, 130, 246, 0.14);
      --indigo: #818cf8;
      --indigo-soft: rgba(99, 102, 241, 0.14);
      --cyan: #22d3ee;
      --cyan-soft: rgba(6, 182, 212, 0.14);
      --emerald: #34d399;
      --emerald-soft: rgba(16, 185, 129, 0.14);
      --amber: #fbbf24;
      --amber-soft: rgba(245, 158, 11, 0.14);
      --rose: #fb7185;
      --rose-soft: rgba(244, 63, 94, 0.14);
      --shadow-card: 0 12px 40px rgba(0, 0, 0, 0.45);
      --shadow-glow: 0 0 60px rgba(59, 130, 246, 0.14);
      --grid-line: rgba(148, 163, 184, 0.05);
    }

    [data-theme="light"] {
      --bg-page: #f8fafc;
      --bg-elevated: rgba(255, 255, 255, 0.94);
      --bg-subtle: #f1f5f9;
      --bg-card-hover: #ffffff;
      --nav-bg: rgba(255, 255, 255, 0.92);
      --border: #e2e8f0;
      --border-strong: #cbd5e1;
      --text-heading: #0f172a;
      --text-body: #334155;
      --text-muted: #64748b;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --primary-soft: #eff6ff;
      --indigo: #4f46e5;
      --indigo-soft: #eef2ff;
      --cyan: #0891b2;
      --cyan-soft: #ecfeff;
      --emerald: #059669;
      --emerald-soft: #ecfdf5;
      --amber: #d97706;
      --amber-soft: #fffbeb;
      --rose: #e11d48;
      --rose-soft: #fff1f2;
      --shadow-card: 0 10px 30px rgba(15, 23, 42, 0.06);
      --shadow-glow: 0 8px 40px rgba(37, 99, 235, 0.08);
      --grid-line: rgba(15, 23, 42, 0.035);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
      overflow-x: clip;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-page);
      color: var(--text-body);
      line-height: 1.6;
      min-height: 100vh;
      overflow-x: clip;
      position: relative;
      transition: background-color 0.25s ease, color 0.25s ease;
    }

    .bg-backdrop {
      position: fixed;
      inset: 0;
      z-index: -1;
      pointer-events: none;
      background-image:
        radial-gradient(circle at 15% 12%, rgba(59, 130, 246, 0.14), transparent 38%),
        radial-gradient(circle at 85% 10%, rgba(139, 92, 246, 0.12), transparent 36%),
        radial-gradient(circle at 50% 45%, rgba(244, 63, 94, 0.07), transparent 45%),
        linear-gradient(to right, var(--grid-line) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid-line) 1px, transparent 1px);
      background-size: auto, auto, auto, 42px 42px, 42px 42px;
    }

    h1, h2, h3, h4, .brand-name {
      font-family: 'Outfit', sans-serif;
      color: var(--text-heading);
      letter-spacing: -0.02em;
    }

    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82em;
      padding: 2px 6px;
      border-radius: 6px;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      color: var(--cyan);
      word-break: break-word;
    }

    /* Navbar */
    .navbar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--nav-bg);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-bottom: 1px solid var(--border);
    }

    .nav-inner {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
      height: 68px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      flex-shrink: 0;
    }

    .brand img {
      width: 34px;
      height: 34px;
      border-radius: 9px;
      border: 1px solid var(--border-strong);
      object-fit: cover;
    }

    .brand-name {
      font-size: 1.18rem;
      font-weight: 800;
    }

    .brand-pill {
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 3px 8px;
      border-radius: 999px;
      background: var(--primary-soft);
      color: var(--primary);
      border: 1px solid rgba(59, 130, 246, 0.25);
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 6px;
      list-style: none;
    }

    .nav-links a {
      text-decoration: none;
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 500;
      padding: 7px 12px;
      border-radius: 8px;
      transition: all 0.18s ease;
      white-space: nowrap;
    }

    .nav-links a:hover {
      color: var(--primary);
      background: var(--bg-subtle);
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }

    .icon-btn {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--bg-subtle);
      color: var(--text-heading);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1rem;
      transition: all 0.18s ease;
    }

    .icon-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }

    .nav-cta {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 10px;
      background: linear-gradient(135deg, #2563eb, #6366f1);
      color: #ffffff;
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      white-space: nowrap;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
      transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .nav-cta:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    .hamburger-btn {
      display: none;
    }

    .mobile-menu {
      display: none;
      border-top: 1px solid var(--border);
      background: var(--bg-page);
      padding: 12px 16px 18px;
    }

    .mobile-menu.open {
      display: block;
    }

    .mobile-menu-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .mobile-menu a {
      text-decoration: none;
      color: var(--text-heading);
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 0.88rem;
      font-weight: 600;
      text-align: center;
    }

    /* Main Layout */
    .container {
      max-width: 1160px;
      margin: 0 auto;
      padding: 34px 20px 72px;
    }

    /* Hero Diagnostic Card */
    .hero-card {
      background: var(--bg-elevated);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-strong);
      border-radius: 24px;
      padding: 40px 36px;
      box-shadow: var(--shadow-card), var(--shadow-glow);
      position: relative;
      overflow: hidden;
      margin-bottom: 44px;
    }

    .hero-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #f43f5e, #8b5cf6, #3b82f6, #06b6d4);
    }

    .hero-top {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: var(--rose-soft);
      border: 1px solid rgba(244, 63, 94, 0.32);
      color: var(--rose);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
      font-weight: 600;
      letter-spacing: 0.04em;
      margin-bottom: 20px;
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--rose);
      box-shadow: 0 0 12px var(--rose);
      animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.3); opacity: 0.45; }
    }

    .hero-emblem {
      width: 74px;
      height: 74px;
      border-radius: 20px;
      background: linear-gradient(145deg, rgba(244, 63, 94, 0.16), rgba(59, 130, 246, 0.16));
      border: 1px solid var(--border-strong);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--rose);
      margin-bottom: 18px;
      box-shadow: 0 8px 24px rgba(244, 63, 94, 0.15);
    }

    .hero-top h1 {
      font-size: clamp(1.65rem, 3.6vw, 2.55rem);
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 12px;
    }

    .hero-primary-msg {
      font-size: 1.06rem;
      font-weight: 600;
      color: var(--text-heading);
      margin-bottom: 8px;
    }

    .hero-sub-msg {
      max-width: 680px;
      color: var(--text-muted);
      font-size: 0.96rem;
      line-height: 1.65;
      margin-bottom: 26px;
    }

    .telemetry-strip {
      width: 100%;
      max-width: 860px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 28px;
    }

    .telemetry-item {
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 14px;
      text-align: left;
    }

    .telemetry-label {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 4px;
    }

    .telemetry-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-heading);
      word-break: break-all;
    }

    .telemetry-val.accent-rose { color: var(--rose); }
    .telemetry-val.accent-emerald { color: var(--emerald); }
    .telemetry-val.accent-cyan { color: var(--cyan); }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
      margin-bottom: 28px;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 22px;
      border-radius: 12px;
      font-size: 0.94rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .btn-primary {
      background: linear-gradient(135deg, #2563eb, #6366f1);
      color: #ffffff;
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 26px rgba(37, 99, 235, 0.45);
    }

    .btn-secondary {
      background: var(--bg-subtle);
      color: var(--text-heading);
      border-color: var(--border-strong);
    }

    .btn-secondary:hover {
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-2px);
    }

    /* Quick Link Checker */
    .recovery-box {
      max-width: 680px;
      margin: 0 auto;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px 18px;
    }

    .recovery-label {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      flex-wrap: wrap;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-heading);
      margin-bottom: 10px;
    }

    .recovery-hint {
      font-size: 0.76rem;
      font-weight: 500;
      color: var(--text-muted);
    }

    .recovery-form {
      display: flex;
      gap: 10px;
    }

    .recovery-input {
      flex: 1;
      min-width: 0;
      background: var(--bg-page);
      border: 1px solid var(--border-strong);
      color: var(--text-heading);
      border-radius: 10px;
      padding: 10px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .recovery-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-soft);
    }

    .recovery-feedback {
      margin-top: 8px;
      font-size: 0.8rem;
      color: var(--rose);
      display: none;
      text-align: left;
    }

    /* Section Headings */
    .section {
      margin-bottom: 52px;
    }

    .section-head {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 22px;
    }

    .section-kicker {
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--primary);
      margin-bottom: 6px;
    }

    .section-title {
      font-size: clamp(1.3rem, 2.5vw, 1.75rem);
      font-weight: 800;
      line-height: 1.25;
    }

    .section-subtitle {
      color: var(--text-muted);
      font-size: 0.94rem;
      margin-top: 6px;
      max-width: 680px;
    }

    .section-more-link {
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--primary);
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 7px 14px;
      border-radius: 999px;
      background: var(--primary-soft);
      border: 1px solid rgba(59, 130, 246, 0.25);
      transition: all 0.18s ease;
    }

    .section-more-link:hover {
      transform: translateX(2px);
    }

    /* Why + Lifecycle Grid */
    .reasons-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
      margin-bottom: 22px;
    }

    .info-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 22px;
      box-shadow: var(--shadow-card);
    }

    .info-card-step {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 0.76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 10px;
    }

    .info-card h3 {
      font-size: 1.08rem;
      font-weight: 700;
      margin-bottom: 8px;
    }

    .info-card p {
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    .lifecycle-bar {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 22px 24px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
      box-shadow: var(--shadow-card);
    }

    .life-step {
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }

    .life-num {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      font-weight: 700;
      flex-shrink: 0;
    }

    .life-step h4 {
      font-size: 0.96rem;
      margin-bottom: 4px;
    }

    .life-step p {
      font-size: 0.84rem;
      color: var(--text-muted);
      line-height: 1.5;
    }

    .next-actions-grid {
      margin-top: 18px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }

    .next-action-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-left: 3px solid var(--primary);
      border-radius: 14px;
      padding: 18px 20px;
    }

    .next-action-card.sender {
      border-left-color: var(--emerald);
    }

    .next-action-card h4 {
      font-size: 0.98rem;
      margin-bottom: 6px;
    }

    .next-action-card p {
      font-size: 0.86rem;
      color: var(--text-muted);
      line-height: 1.55;
    }

    /* Tone classes */
    .tone-blue { background: var(--primary-soft); color: var(--primary); border-color: rgba(59, 130, 246, 0.28); }
    .tone-indigo { background: var(--indigo-soft); color: var(--indigo); border-color: rgba(99, 102, 241, 0.28); }
    .tone-cyan { background: var(--cyan-soft); color: var(--cyan); border-color: rgba(6, 182, 212, 0.28); }
    .tone-emerald { background: var(--emerald-soft); color: var(--emerald); border-color: rgba(16, 185, 129, 0.28); }
    .tone-amber { background: var(--amber-soft); color: var(--amber); border-color: rgba(245, 158, 11, 0.28); }
    .tone-rose { background: var(--rose-soft); color: var(--rose); border-color: rgba(244, 63, 94, 0.28); }

    .icon-box {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      border: 1px solid transparent;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .icon-box.sm {
      width: 38px;
      height: 38px;
      border-radius: 10px;
    }

    .pill-tag {
      display: inline-flex;
      align-items: center;
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid transparent;
      white-space: nowrap;
    }

    /* Filter Tabs */
    .filter-tabs {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }

    .filter-tab {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 15px;
      border-radius: 999px;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.18s ease;
      font-family: inherit;
    }

    .filter-tab:hover {
      border-color: var(--primary);
      color: var(--primary);
    }

    .filter-tab.active {
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    }

    /* Tools Grid */
    .tools-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
      gap: 18px;
    }

    .tool-card,
    .gov-card,
    .blog-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      text-decoration: none;
      color: inherit;
      box-shadow: var(--shadow-card);
      transition: transform 0.22s ease, border-color 0.22s ease, background 0.22s ease;
    }

    .tool-card:hover,
    .blog-card:hover {
      transform: translateY(-4px);
      border-color: var(--primary);
      background: var(--bg-card-hover);
    }

    .gov-card:hover {
      border-color: var(--border-strong);
      transform: translateY(-2px);
    }

    .tool-card.hidden-card {
      display: none;
    }

    .tool-card-top,
    .gov-card-head,
    .blog-card-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 14px;
    }

    .tool-card h3,
    .gov-card h3,
    .blog-card h3 {
      font-size: 1.08rem;
      font-weight: 700;
      margin-bottom: 8px;
      line-height: 1.35;
    }

    .tool-card p,
    .gov-card p,
    .blog-card p {
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.55;
      margin-bottom: 18px;
      flex-grow: 1;
    }

    .card-foot {
      padding-top: 12px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .card-link-cta {
      color: var(--primary);
      font-size: 0.86rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .tool-card:hover .card-link-cta span,
    .blog-card:hover .card-link-cta span {
      transform: translateX(3px);
      transition: transform 0.18s ease;
    }

    .more-tools-banner {
      margin-top: 20px;
      padding: 18px 22px;
      border-radius: 16px;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
    }

    .more-tools-banner p {
      font-size: 0.9rem;
      color: var(--text-body);
    }

    /* Governance Grid */
    .gov-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 310px), 1fr));
      gap: 18px;
    }

    .gov-card-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--border);
    }

    .gov-link {
      text-decoration: none;
      color: var(--primary);
      font-weight: 600;
      font-size: 0.86rem;
    }

    .gov-link:hover {
      text-decoration: underline;
    }

    .gov-link-muted {
      text-decoration: none;
      color: var(--text-muted);
      font-size: 0.82rem;
      font-weight: 500;
    }

    .gov-link-muted:hover {
      color: var(--text-heading);
      text-decoration: underline;
    }

    /* Blogs Grid */
    .blog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
      gap: 18px;
    }

    .read-time {
      font-size: 0.76rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* FAQ + Support Strip */
    .faq-support-grid {
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 20px;
      align-items: start;
    }

    .faq-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .faq-item {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
    }

    .faq-q {
      width: 100%;
      background: transparent;
      border: none;
      padding: 16px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      text-align: left;
      font-family: 'Outfit', sans-serif;
      font-size: 0.98rem;
      font-weight: 700;
      color: var(--text-heading);
      cursor: pointer;
    }

    .faq-chevron {
      color: var(--text-muted);
      transition: transform 0.2s ease;
      flex-shrink: 0;
    }

    .faq-item.open .faq-chevron {
      transform: rotate(180deg);
      color: var(--primary);
    }

    .faq-a {
      display: none;
      padding: 0 18px 16px;
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.6;
    }

    .faq-item.open .faq-a {
      display: block;
    }

    .support-panel {
      background: linear-gradient(155deg, rgba(37, 99, 235, 0.12), rgba(139, 92, 246, 0.08));
      border: 1px solid rgba(59, 130, 246, 0.28);
      border-radius: 18px;
      padding: 24px;
    }

    .support-panel h3 {
      font-size: 1.16rem;
      margin-bottom: 8px;
    }

    .support-panel p {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 16px;
      line-height: 1.6;
    }

    .support-links {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .support-btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 11px 14px;
      border-radius: 12px;
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      text-decoration: none;
      color: var(--text-heading);
      font-size: 0.88rem;
      font-weight: 600;
      transition: all 0.18s ease;
    }

    .support-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }

    /* Footer */
    .footer {
      border-top: 1px solid var(--border);
      background: var(--nav-bg);
      padding: 48px 20px 28px;
    }

    .footer-inner {
      max-width: 1160px;
      margin: 0 auto;
    }

    .footer-grid {
      display: grid;
      grid-template-columns: 1.6fr repeat(3, 1fr);
      gap: 32px;
      margin-bottom: 34px;
    }

    .footer-brand p {
      font-size: 0.86rem;
      color: var(--text-muted);
      margin-top: 10px;
      max-width: 300px;
      line-height: 1.6;
    }

    .footer-col h4 {
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      margin-bottom: 14px;
    }

    .footer-col ul {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 9px;
    }

    .footer-col a {
      text-decoration: none;
      font-size: 0.86rem;
      color: var(--text-muted);
      transition: color 0.15s ease;
    }

    .footer-col a:hover {
      color: var(--primary);
    }

    .footer-bottom {
      border-top: 1px solid var(--border);
      padding-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.82rem;
      color: var(--text-muted);
    }

    .footer-bottom-links {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }

    .footer-bottom-links a {
      color: var(--text-muted);
      text-decoration: none;
    }

    .footer-bottom-links a:hover {
      color: var(--primary);
    }

    /* Responsive Breakpoints */
    @media (max-width: 960px) {
      .nav-links { display: none; }
      .hamburger-btn { display: inline-flex; }
      .telemetry-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .reasons-grid,
      .lifecycle-bar,
      .next-actions-grid,
      .faq-support-grid { grid-template-columns: 1fr; }
      .footer-grid { grid-template-columns: 1fr 1fr; }
    }

    @media (max-width: 600px) {
      .nav-inner { padding: 0 14px; height: 62px; }
      .brand-pill { display: none; }
      .nav-cta { padding: 7px 11px; font-size: 0.8rem; }
      .container { padding: 20px 14px 54px; }
      .hero-card { padding: 26px 16px; border-radius: 18px; }
      .status-badge { font-size: 0.64rem; padding: 5px 11px; gap: 6px; letter-spacing: 0.02em; justify-content: center; text-align: center; }
      .hero-actions { flex-direction: column; width: 100%; }
      .hero-actions .btn { width: 100%; }
      .recovery-form { flex-direction: column; }
      .recovery-form .btn { width: 100%; }
      .telemetry-strip { grid-template-columns: 1fr 1fr; gap: 8px; }
      .telemetry-item { padding: 10px 11px; }
      .footer-grid { grid-template-columns: 1fr; gap: 24px; }
      .mobile-menu-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
      .mobile-menu a { font-size: 0.81rem; padding: 10px 8px; }
    }
  </style>
</head>
<body>
  <div class="bg-backdrop" aria-hidden="true"></div>

  <header class="navbar">
    <div class="nav-inner">
      <a href="/" class="brand">
        <img src="/logo.jpg?v=5" alt="PixelCraft AI Logo" />
        <span class="brand-name">PixelCraft AI</span>
        <span class="brand-pill">Ephemeral PDF</span>
      </a>

      <ul class="nav-links">
        <li><a href="/#tools">All Tools</a></li>
        <li><a href="/tools/pdf-to-link.html">PDF to Link</a></li>
        <li><a href="/blog/index.html">Blogs</a></li>
        <li><a href="/security-whitepaper.html">Security Whitepaper</a></li>
        <li><a href="/data-practices.html">Data Practices</a></li>
      </ul>

      <div class="nav-actions">
        <button type="button" id="theme-toggle" class="icon-btn" title="Toggle Dark / Light Theme" aria-label="Toggle Theme">☀️</button>
        <a href="/tools/pdf-to-link.html" class="nav-cta">+ New PDF Link</a>
        <button type="button" id="menu-toggle" class="icon-btn hamburger-btn" title="Open Menu" aria-label="Open Navigation Menu" aria-expanded="false">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
      </div>
    </div>

    <div class="mobile-menu" id="mobile-menu">
      <div class="mobile-menu-grid">
        <a href="/tools/pdf-to-link.html">Upload New PDF</a>
        <a href="/#tools">All 15+ Tools</a>
        <a href="/blog/index.html">Research Blogs</a>
        <a href="/security-whitepaper.html">Security Whitepaper</a>
        <a href="/data-practices.html">Data Practices</a>
        <a href="/privacy-policy.html">Privacy Policy</a>
        <a href="/terms-conditions.html">Terms &amp; Conditions</a>
        <a href="/contact-us.html">Contact Support</a>
      </div>
    </div>
  </header>

  <main class="container">
    <!-- Hero Diagnostic Section -->
    <section class="hero-card" aria-labelledby="pdf-status-heading">
      <div class="hero-top">
        <div class="status-badge">
          <span class="pulse-dot"></span>
          <span>${escapeHtml(statusPillText)}</span>
        </div>

        <div class="hero-emblem" aria-hidden="true">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <circle cx="12" cy="14" r="3"></circle>
            <path d="M12 12.8V14l.8.8"></path>
          </svg>
        </div>

        <h1 id="pdf-status-heading">${escapeHtml(headline)}</h1>
        <p class="hero-primary-msg">${escapeHtml(message)}</p>
        <p class="hero-sub-msg">
          PixelCraft AI enforces strict <strong>24-hour ephemeral document hosting</strong>. Once the 24-hour retention threshold passes, our automated hourly cleanup daemon permanently unlinks the PDF from server storage with zero MongoDB persistence and zero search indexing.
        </p>

        <div class="telemetry-strip">
          <div class="telemetry-item">
            <div class="telemetry-label">Requested Link</div>
            <div class="telemetry-val">${safeIdDisplay}</div>
          </div>
          <div class="telemetry-item">
            <div class="telemetry-label">HTTP Status</div>
            <div class="telemetry-val accent-rose">${escapeHtml(statusValueText)}</div>
          </div>
          <div class="telemetry-item">
            <div class="telemetry-label">Retention Policy</div>
            <div class="telemetry-val accent-cyan">24h Auto-Purge</div>
          </div>
          <div class="telemetry-item">
            <div class="telemetry-label">Database Footprint</div>
            <div class="telemetry-val accent-emerald">0 Bytes Stored</div>
          </div>
        </div>

        <div class="hero-actions">
          <a href="/tools/pdf-to-link.html" class="btn btn-primary">
            <span>Upload &amp; Create New PDF Link</span>
            <span>&rarr;</span>
          </a>
          <a href="/#tools" class="btn btn-secondary">Explore All 15+ Free Tools</a>
          <a href="/" class="btn btn-secondary">Go to Homepage</a>
        </div>
      </div>

      <div class="recovery-box">
        <div class="recovery-label">
          <span>Have another PDF link or broken URL?</span>
          <span class="recovery-hint">Paste full URL or 6-character code (e.g. a1b2c3)</span>
        </div>
        <form class="recovery-form" id="link-recovery-form">
          <input
            type="text"
            id="link-recovery-input"
            class="recovery-input"
            placeholder="e.g. https://pixelcraftaitools.com/p/a1b2c3 or a1b2c3"
            autocomplete="off"
            aria-label="Enter PDF link ID or URL"
          />
          <button type="submit" class="btn btn-primary">Open Link</button>
        </form>
        <div class="recovery-feedback" id="link-recovery-feedback"></div>
      </div>
    </section>

    <!-- Why Did This Happen + Ephemeral Lifecycle -->
    <section class="section" aria-labelledby="why-heading">
      <div class="section-head">
        <div>
          <div class="section-kicker">Ephemeral Architecture &amp; Diagnostics</div>
          <h2 class="section-title" id="why-heading">Why Is This PDF Unavailable?</h2>
          <p class="section-subtitle">Temporary PDF links are intentionally short-lived to protect sensitive documents from lingering indefinitely online.</p>
        </div>
      </div>

      <div class="reasons-grid">
        <article class="info-card">
          <div class="info-card-step" style="color: var(--rose);">01 &bull; Auto-Destruction</div>
          <h3>24-Hour Retention Expired</h3>
          <p>All PDFs shared via PixelCraft AI are purged automatically after 24 hours by our hourly server cleanup task (<code>cleanupExpiredPdfs</code>). Expired files cannot be recovered.</p>
        </article>

        <article class="info-card">
          <div class="info-card-step" style="color: var(--amber);">02 &bull; Link Formatting</div>
          <h3>Truncated or Broken URL</h3>
          <p>Messaging apps, email wrappers, or parentheses like <code>/p/(</code> can cut off characters. Check the full token sent to you or paste it in the recovery box above.</p>
        </article>

        <article class="info-card">
          <div class="info-card-step" style="color: var(--cyan);">03 &bull; Privacy Isolation</div>
          <h3>No Cached Backups</h3>
          <p>Responses include <code>Cache-Control: private, no-cache, no-store</code> and <code>X-Robots-Tag: noindex</code>, ensuring search engines and CDNs do not archive expired files.</p>
        </article>
      </div>

      <div class="lifecycle-bar" aria-label="24-Hour Ephemeral Lifecycle">
        <div class="life-step">
          <div class="life-num tone-blue">00h</div>
          <div>
            <h4>Instant Upload &amp; QR</h4>
            <p>PDF uploaded to isolated ephemeral disk via <code>POST /api/upload-pdf</code> with zero MongoDB database entries.</p>
          </div>
        </div>
        <div class="life-step">
          <div class="life-num tone-emerald">24h</div>
          <div>
            <h4>Private No-Index Viewing</h4>
            <p>Recipients view or download via <code>/p/:id</code> without login, protected by strict no-cache and no-index headers.</p>
          </div>
        </div>
        <div class="life-step">
          <div class="life-num tone-rose">24h+</div>
          <div>
            <h4>Permanent Auto-Purge</h4>
            <p>Hourly cron verifies file modification timestamps and permanently unlinks expired PDFs from server storage.</p>
          </div>
        </div>
      </div>

      <div class="next-actions-grid">
        <div class="next-action-card">
          <h4>Opened a shared link from WhatsApp, Telegram, or Email?</h4>
          <p>Because expired links cannot be restored, reply to the sender and ask them to re-upload the PDF using PixelCraft PDF-to-Link (takes under 3 seconds with zero login).</p>
        </div>
        <div class="next-action-card sender">
          <h4>Are you the document sender?</h4>
          <p>Tap <a href="/tools/pdf-to-link.html" style="color: var(--emerald); font-weight: 600; text-decoration: none;">Upload &amp; Create New PDF Link &rarr;</a> to generate a fresh 24-hour URL and QR code, or merge photos into a PDF first using <a href="/tools/images-to-pdf.html" style="color: var(--primary); font-weight: 600; text-decoration: none;">Images to PDF</a>.</p>
        </div>
      </div>
    </section>

    <!-- Suggested Tools Hub -->
    <section class="section" id="suggested-tools" aria-labelledby="tools-heading">
      <div class="section-head">
        <div>
          <div class="section-kicker">Recommended Utilities</div>
          <h2 class="section-title" id="tools-heading">Suggested PixelCraft AI Tools</h2>
          <p class="section-subtitle">Create a new PDF link, merge images into PDF, verify suspicious links, or sanitize hidden metadata in your browser.</p>
        </div>
        <a href="/#tools" class="section-more-link">All 15+ Tools &rarr;</a>
      </div>

      <div class="filter-tabs" role="tablist" aria-label="Filter suggested tools">
        <button type="button" class="filter-tab active" data-filter="all">All Recommended (8)</button>
        <button type="button" class="filter-tab" data-filter="pdf">PDF &amp; Sharing (3)</button>
        <button type="button" class="filter-tab" data-filter="privacy">Privacy &amp; Security (3)</button>
        <button type="button" class="filter-tab" data-filter="media">Image &amp; Media (2)</button>
      </div>

      <div class="tools-grid" id="suggested-tools-grid">
        ${renderToolCards()}
      </div>

      <div class="more-tools-banner">
        <p><strong>More tools available:</strong> EXIF Data Viewer, Watermark Adder, Smart Social Resize, Color Palette Extractor, Audio Steganography &amp; AI Voice Dubbing.</p>
        <a href="/#tools" class="btn btn-secondary">Browse Complete Tool Suite &rarr;</a>
      </div>
    </section>

    <!-- Governance, Security Whitepaper, Data Practices, Terms & Privacy -->
    <section class="section" aria-labelledby="trust-heading">
      <div class="section-head">
        <div>
          <div class="section-kicker">Transparency &amp; Governance</div>
          <h2 class="section-title" id="trust-heading">Security Whitepaper, Data Practices &amp; Legal Policies</h2>
          <p class="section-subtitle">Inspect our architecture, retention disclosures, terms of service, and privacy commitments.</p>
        </div>
        <a href="/about-us.html" class="section-more-link">About PixelCraft AI &rarr;</a>
      </div>

      <div class="gov-grid">
        ${renderGovernanceCards()}
      </div>
    </section>

    <!-- Research Blogs -->
    <section class="section" aria-labelledby="blogs-heading">
      <div class="section-head">
        <div>
          <div class="section-kicker">Cybersecurity &amp; Document Research</div>
          <h2 class="section-title" id="blogs-heading">Recommended Research Blogs &amp; Guides</h2>
          <p class="section-subtitle">Technical deep-dives on PDF redaction, zero-knowledge processing, and link safety.</p>
        </div>
        <a href="/blog/index.html" class="section-more-link">Explore All Blogs &rarr;</a>
      </div>

      <div class="blog-grid">
        ${renderBlogCards()}
      </div>
    </section>

    <!-- FAQ & Support / PWA -->
    <section class="section" aria-labelledby="faq-heading">
      <div class="section-head">
        <div>
          <div class="section-kicker">Quick Answers &amp; Support</div>
          <h2 class="section-title" id="faq-heading">Frequently Asked Questions</h2>
        </div>
      </div>

      <div class="faq-support-grid">
        <div class="faq-list">
          <div class="faq-item open">
            <button type="button" class="faq-q">
              <span>Can PixelCraft AI recover an expired PDF after 24 hours?</span>
              <span class="faq-chevron">&#9662;</span>
            </button>
            <div class="faq-a">
              No. Once the 24-hour TTL threshold passes and the hourly cleanup worker removes the file, it is permanently unlinked from disk. PDFs are never backed up to MongoDB or long-term cloud archives. Ask the sender to re-upload the document for a fresh link.
            </div>
          </div>

          <div class="faq-item">
            <button type="button" class="faq-q">
              <span>What should I do if the sender says the link was just created?</span>
              <span class="faq-chevron">&#9662;</span>
            </button>
            <div class="faq-a">
              Check if your chat app truncated the URL or attached punctuation (like <code>)</code> or <code>.</code>) at the end of <code>/p/xxxxxx</code>. Paste the full message link into the quick recovery box at the top of this page to sanitize and open the exact document ID.
            </div>
          </div>

          <div class="faq-item">
            <button type="button" class="faq-q">
              <span>Is my PDF uploaded when I use other PixelCraft tools like Images to PDF?</span>
              <span class="faq-chevron">&#9662;</span>
            </button>
            <div class="faq-a">
              No. Tools such as Images to PDF, Image Compressor, Format Converter, and Custom QR Studio run 100% locally in your browser memory (0 bytes uploaded). Full details for every tool are published in our <a href="/data-practices.html" style="color: var(--primary);">Data Practices Inventory</a>.
            </div>
          </div>
        </div>

        <aside class="support-panel">
          <h3>Need Assistance or Offline Access?</h3>
          <p>
            If you received this link from someone else, request a fresh upload via PDF to Link. To report misuse, request technical support, or install our client-side tools for offline use:
          </p>
          <div class="support-links">
            <a href="/tools/pdf-to-link.html" class="support-btn">
              <span>Re-upload &amp; Share PDF</span>
              <span>&rarr;</span>
            </a>
            <a href="/download-app.html" class="support-btn">
              <span>Install Offline App (PWA)</span>
              <span>&rarr;</span>
            </a>
            <a href="/contact-us.html" class="support-btn">
              <span>Contact &amp; Abuse Report</span>
              <span>&rarr;</span>
            </a>
            <a href="mailto:support.pixelcraft205@gmail.com" class="support-btn">
              <span>support.pixelcraft205@gmail.com</span>
              <span>&#9993;</span>
            </a>
          </div>
        </aside>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="brand">
            <img src="/logo.jpg?v=5" alt="PixelCraft AI Logo" />
            <span class="brand-name">PixelCraft AI</span>
          </a>
          <p>Privacy-first browser utilities, ephemeral PDF sharing with 24-hour auto-purge, and transparent security engineering.</p>
        </div>

        <div class="footer-col">
          <h4>Document &amp; Media Tools</h4>
          <ul>
            <li><a href="/tools/pdf-to-link.html">PDF to Link Converter</a></li>
            <li><a href="/tools/images-to-pdf.html">Images to PDF</a></li>
            <li><a href="/tools/qr-generator.html">Custom QR Code Studio</a></li>
            <li><a href="/tools/image-compressor.html">Image Compressor</a></li>
            <li><a href="/tools/format-converter.html">Format Converter</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Security &amp; Research</h4>
          <ul>
            <li><a href="/tools/phishing-scanner.html">Phishing Link Scanner</a></li>
            <li><a href="/tools/forensic-sanitizer.html">Forensic Sanitizer</a></li>
            <li><a href="/tools/digital-fingerprint-wiper.html">Digital Fingerprint Wiper</a></li>
            <li><a href="/security-whitepaper.html">Security Whitepaper</a></li>
            <li><a href="/blog/index.html">Research Blogs</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Trust &amp; Legal</h4>
          <ul>
            <li><a href="/data-practices.html">Data Practices</a></li>
            <li><a href="/privacy-policy.html">Privacy Policy</a></li>
            <li><a href="/terms-conditions.html">Terms &amp; Conditions</a></li>
            <li><a href="/cookies-policy.html">Cookies Policy</a></li>
            <li><a href="/disclaimer.html">Disclaimer</a></li>
            <li><a href="/about-us.html">About Us</a></li>
            <li><a href="/contact-us.html">Contact Support</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <span>&copy; 2026 PixelCraft AI. All rights reserved.</span>
        <div class="footer-bottom-links">
          <a href="/terms-conditions.html">Terms</a>
          <a href="/privacy-policy.html">Privacy</a>
          <a href="/data-practices.html">Data Practices</a>
          <a href="/security-whitepaper.html">Security Whitepaper</a>
          <a href="/blog/index.html">Blogs</a>
          <a href="/contact-us.html">Support</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    (function () {
      // Theme Switcher
      var themeBtn = document.getElementById('theme-toggle');
      function syncThemeBtn() {
        var current = document.documentElement.getAttribute('data-theme') || 'dark';
        if (themeBtn) {
          themeBtn.textContent = current === 'dark' ? '☀️' : '🌙';
          themeBtn.title = current === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        }
      }
      syncThemeBtn();

      if (themeBtn) {
        themeBtn.addEventListener('click', function () {
          var current = document.documentElement.getAttribute('data-theme') || 'dark';
          var next = current === 'dark' ? 'light' : 'dark';
          document.documentElement.setAttribute('data-theme', next);
          try { localStorage.setItem('pixelcraft-theme', next); } catch (e) {}
          syncThemeBtn();
        });
      }

      // Mobile Navigation Toggle
      var menuBtn = document.getElementById('menu-toggle');
      var mobileMenu = document.getElementById('mobile-menu');
      if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          var isOpen = mobileMenu.classList.toggle('open');
          menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
        document.addEventListener('click', function (e) {
          if (mobileMenu.classList.contains('open') && !mobileMenu.contains(e.target) && e.target !== menuBtn) {
            mobileMenu.classList.remove('open');
            menuBtn.setAttribute('aria-expanded', 'false');
          }
        });
      }

      // Tool Category Filtering
      var filterTabs = document.querySelectorAll('.filter-tab');
      var toolCards = document.querySelectorAll('#suggested-tools-grid .tool-card');
      filterTabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          var target = tab.getAttribute('data-filter');
          filterTabs.forEach(function (t) { t.classList.remove('active'); });
          tab.classList.add('active');
          toolCards.forEach(function (card) {
            var cat = card.getAttribute('data-cat');
            if (target === 'all' || cat === target) {
              card.classList.remove('hidden-card');
            } else {
              card.classList.add('hidden-card');
            }
          });
        });
      });

      // FAQ Accordion
      document.querySelectorAll('.faq-q').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var item = btn.closest('.faq-item');
          if (!item) return;
          var wasOpen = item.classList.contains('open');
          document.querySelectorAll('.faq-item').forEach(function (i) { i.classList.remove('open'); });
          if (!wasOpen) item.classList.add('open');
        });
      });

      // Quick PDF Link Recovery / Sanitizer
      var form = document.getElementById('link-recovery-form');
      var input = document.getElementById('link-recovery-input');
      var feedback = document.getElementById('link-recovery-feedback');

      if (form && input && feedback) {
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          var raw = (input.value || '').trim();
          feedback.style.display = 'none';

          if (!raw) {
            feedback.textContent = 'Please paste a PixelCraft PDF URL or enter the document ID (e.g. a1b2c3).';
            feedback.style.display = 'block';
            return;
          }

          var extracted = raw;
          var match = raw.match(/\\/p\\/([a-zA-Z0-9_-]+)/);
          if (match && match[1]) {
            extracted = match[1];
          } else {
            extracted = raw.replace(/^.*\\/p\\//i, '').replace(/^[^a-zA-Z0-9_-]+|[^a-zA-Z0-9_-]+$/g, '');
          }

          if (!/^[a-zA-Z0-9_-]{2,64}$/.test(extracted)) {
            feedback.textContent = 'Invalid link ID format. A valid PDF link ID contains only letters, numbers, hyphens, or underscores (e.g. a1b2c3).';
            feedback.style.display = 'block';
            return;
          }

          window.location.href = '/p/' + encodeURIComponent(extracted);
        });
      }
    })();
  </script>
</body>
</html>`;
}

module.exports = {
  escapeHtml,
  renderPdfUnavailablePage
};
