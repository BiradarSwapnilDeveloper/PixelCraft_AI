// Regression Test Suite: Privacy Transparency, Retention & Disclosure Consistency
// Run via: node test_privacy_compliance.js

const assert = require('assert');
const fs = require('fs');
const path = require('path');

function runPrivacyTests() {
  console.log('🔒 Starting PixelCraft AI Privacy & Disclosure Compliance Test Suite...\n');
  let passed = 0;
  let total = 0;

  function test(name, fn) {
    total++;
    try {
      fn();
      console.log(`  ✅ [PASS] ${name}`);
      passed++;
    } catch (e) {
      console.error(`  ❌ [FAIL] ${name}:`, e.message);
    }
  }

  // 1. Source of Truth Documentation
  test('Stage 1 Source of Truth inventory docs/privacy-data-inventory.md exists and covers all core tools', () => {
    const invPath = path.join(__dirname, 'docs', 'privacy-data-inventory.md');
    assert.ok(fs.existsSync(invPath), 'docs/privacy-data-inventory.md must exist');
    const content = fs.readFileSync(invPath, 'utf8');
    assert.ok(content.includes('Forensic Image Sanitizer'), 'Must document Forensic Sanitizer');
    assert.ok(content.includes('AI Audio & Video Dubbing'), 'Must document AI Dubbing');
    assert.ok(content.includes('Phishing & Threat Link Scanner'), 'Must document Phishing Scanner');
    assert.ok(content.includes('PDF to Link'), 'Must document PDF to Link');
    assert.ok(content.includes('Digital Fingerprint Wiper'), 'Must document Digital Fingerprint Wiper');
    assert.ok(content.includes('connect.sid'), 'Must document connect.sid session cookie');
    assert.ok(content.includes('CERT-In Direction 2(iv)'), 'Must document 180-day security log basis');
    assert.ok(content.includes('[VERIFIED IN CODE]'), 'Must establish verification tiers');
  });

  // 2. Forensic Sanitizer Disclosures
  test('Forensic Sanitizer discloses server-assisted in-memory upload and purges misleading local-only claims', () => {
    const htmlPath = path.join(__dirname, 'public', 'tools', 'forensic-sanitizer.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    // Notice must appear before submission button
    const noticeIdx = html.indexOf('Server-Assisted Processing Notice');
    const submitBtnIdx = html.indexOf('id="btnProcess"');
    assert.ok(noticeIdx !== -1, 'Must display server processing badge notice');
    assert.ok(submitBtnIdx !== -1, 'Submit button must exist');
    assert.ok(noticeIdx < submitBtnIdx, 'Notice must appear prior to submission trigger');
    assert.ok(html.includes('/api/tools/forensic-sanitize'), 'Must disclose POST /api/tools/forensic-sanitize endpoint');
    assert.ok(html.includes('volatile RAM'), 'Must disclose in-memory volatile RAM processing without disk storage');
    assert.strictEqual(html.includes('Our Forensic Sanitizer runs locally within your browser'), false, 'Must not claim it runs locally in browser');
  });

  // 3. AI Dubbing Transparency Notice
  test('AI Dubbing displays pre-submission notice disclosing Groq and Google TTS transmission', () => {
    const htmlPath = path.join(__dirname, 'public', 'tools', 'ai-dubbing.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    // Notice must appear before the processDubbing trigger
    const noticeIdx = html.indexOf('Third-Party AI Data Processing Notice');
    const processBtnIdx = html.indexOf('processDubbing()');
    assert.ok(noticeIdx !== -1, 'Must display pre-submission notice');
    assert.ok(processBtnIdx !== -1, 'Processing button must exist');
    assert.ok(noticeIdx < processBtnIdx, 'Notice must appear prior to processing trigger');
    assert.ok(html.includes('/api/dub-media'), 'Must disclose POST /api/dub-media endpoint');
    assert.ok(html.includes('Groq Inc. (USA)'), 'Must disclose Groq Whisper');
    assert.ok(html.includes('Google TTS'), 'Must disclose Google TTS');
    assert.ok(html.includes('erased immediately upon processing completion') || html.includes('deleted immediately'), 'Must disclose ephemeral cleanup lifecycle');
    assert.strictEqual(html.includes('No data is sent to external servers'), false, 'Must not claim no external data transmission');
  });

  // 4. Phishing Scanner Disclosures & Clean FAQ
  test('Phishing Scanner discloses backend URL inspection and replaces image editor boilerplate', () => {
    const htmlPath = path.join(__dirname, 'public', 'tools', 'phishing-scanner.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    // Notice must appear before the scan trigger
    const noticeIdx = html.indexOf('Server-Side URL Inspection Notice');
    const scanBtnIdx = html.indexOf('id="scan-btn"');
    assert.ok(noticeIdx !== -1, 'Must display backend inspection badge');
    assert.ok(scanBtnIdx !== -1, 'Scan button must exist');
    assert.ok(noticeIdx < scanBtnIdx, 'Notice must appear prior to scan trigger');
    assert.ok(html.includes('/api/scan-link'), 'Must disclose /api/scan-link endpoint');
    assert.ok(html.includes('How does the URL Phishing Scanner detect threats?') || html.includes('How the Scanner Inspects URLs'), 'Must have authentic URL scanner threat detection FAQ/guide');
    assert.strictEqual(html.includes('Is there a file size limit for image editing?'), false, 'Boilerplate image FAQ must be removed');
  });

  // 5. QR Generator Distinguishes Local Standard vs AI 3D
  test('QR Generator distinguishes 100% client-side standard QR from optional AI 3D cloud generation', () => {
    const htmlPath = path.join(__dirname, 'public', 'tools', 'qr-generator.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.ok(html.includes('Standard QR codes remain 100% local in your browser'), 'Must disclose standard QR local execution');
    assert.ok(html.includes('AI Notice:'), 'Must disclose 3D AI cloud processing');
    assert.ok(html.includes('Hugging Face (Stable Diffusion XL)'), 'Must disclose Hugging Face API transmission');
  });

  // 6. PDF-to-Link Retention & Public Link Transparency
  test('PDF-to-Link discloses public accessibility and 24-hour lifecycle with hourly cron cleanup', () => {
    const htmlPath = path.join(__dirname, 'public', 'tools', 'pdf-to-link.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.ok(html.includes('Public Link Notice'), 'Must display upload notice badge');
    assert.ok(html.includes('exceed the 24-hour retention threshold'), 'Must disclose 24 hour deletion threshold');
    assert.ok(html.includes('hourly cleanup process'), 'Must disclose hourly cron execution');
  });

  // 7. Cookies Policy Alignment
  test('Cookies Policy specifies 30-day rolling connect.sid session cookie and localStorage consent keys', () => {
    const htmlPath = path.join(__dirname, 'public', 'cookies-policy.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.ok(html.includes('30 Days (Rolling session window)'), 'Must declare 30 days rolling for connect.sid');
    assert.ok(html.includes('cookieConsent'), 'Must declare cookieConsent key');
    assert.ok(html.includes('pc_consent_v1'), 'Must declare pc_consent_v1 key');
    assert.ok(html.includes('Browser LocalStorage'), 'Must declare LocalStorage mechanism');
  });

  // 8. Digital Fingerprint Wiper Login Removal & Claim Tempering
  test('Digital Fingerprint Wiper removes false login alert and tempers absolute anonymity claims', () => {
    const htmlPath = path.join(__dirname, 'public', 'tools', 'digital-fingerprint-wiper.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.strictEqual(html.includes('Google Login Required'), false, 'Obsolete Google Login Required alert must be removed');
    assert.strictEqual(html.includes('100% anonymity'), false, 'Unsupported "100% anonymity" claim must be removed');
    assert.strictEqual(html.includes('This guarantees that your original, un-wiped photos are never intercepted'), false, 'Unsupported guarantee claim must be removed');
    assert.ok(html.includes('100% Client-Side Processing'), 'Must highlight client-side browser execution');
  });

  // 9. Homepage FAQ & Retention Alignment
  test('Homepage index.html accurately describes ephemeral AI Dubbing RAM cleanup vs 24h PDF retention', () => {
    const htmlPath = path.join(__dirname, 'public', 'index.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.ok(html.includes('PDF-to-Link</strong> temporarily stores files on disk for up to 24 hours'), 'Must disclose PDF-to-Link 24h retention');
    assert.ok(html.includes('AI Dubbing</strong> processes media ephemerally in server RAM/temp directories'), 'Must disclose AI Dubbing ephemeral RAM lifecycle');
    assert.ok(html.includes('data-practices.html'), 'Must link to data-practices.html in FAQ or footer');
  });

  // 10. Terms and Conditions Retention Alignment
  test('Terms & Conditions accurately differentiates local, PDF-to-Link, and AI Dubbing lifetimes', () => {
    const htmlPath = path.join(__dirname, 'public', 'terms-conditions.html');
    const html = fs.readFileSync(htmlPath, 'utf8');
    assert.ok(html.includes('PDF-to-Link temporarily stores files on disk for up to 24 hours'), 'Must disclose PDF-to-Link 24h retention');
    assert.ok(html.includes('AI Dubbing processes media ephemerally in server RAM/temporary scratch space and unlinks all temporary files immediately'), 'Must disclose AI Dubbing immediate deletion');
    assert.ok(html.includes('data-practices.html'), 'Must link to data-practices.html');
  });

  // 11. Public Transparency Page Exists
  test('Public Data Practices page public/data-practices.html exists and contains comprehensive inventory table', () => {
    const dpPath = path.join(__dirname, 'public', 'data-practices.html');
    assert.ok(fs.existsSync(dpPath), 'public/data-practices.html must exist');
    const html = fs.readFileSync(dpPath, 'utf8');
    assert.ok(html.includes('Privacy & Data Practices Inventory'), 'Must have correct title');
    assert.ok(html.includes('Complete Tool Processing & Data Inventory'), 'Must contain inventory table');
    assert.ok(html.includes('VERIFIED IN CODE'), 'Must show verification tiers');
    assert.ok(html.includes('CERT-In Direction 2(iv)'), 'Must explain 180-day log retention');
    assert.ok(html.includes('Third-Party AI Services (Groq, Google Cloud, Hugging Face)'), 'Must disclose third-party limitations');
  });

  console.log(`\n📊 Privacy Compliance Test Suite Summary: ${passed}/${total} Tests Passed.`);
  if (passed === total) {
    console.log('🎉 ALL PRIVACY COMPLIANCE & DISCLOSURE TESTS PASSED!\n');
    process.exit(0);
  } else {
    console.error('❌ SOME TESTS FAILED!\n');
    process.exit(1);
  }
}

runPrivacyTests();
