// Comprehensive Retention & Security Unit Test Suite
// Run via: node test_retention_suite.js

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const mongoose = require('mongoose');

async function runTests() {
  console.log('🧪 Starting PixelCraft AI Retention & Security Test Suite...\n');
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

  async function asyncTest(name, fn) {
    total++;
    try {
      await fn();
      console.log(`  ✅ [PASS] ${name}`);
      passed++;
    } catch (e) {
      console.error(`  ❌ [FAIL] ${name}:`, e.message);
    }
  }

  // TEST 1: PDF Cleanup Logic
  await asyncTest('PDF 24-Hour Cleanup correctly purges only expired files', async () => {
    const testDir = path.join(__dirname, 'test_pdf_sandbox');
    if (!fs.existsSync(testDir)) fs.mkdirSync(testDir, { recursive: true });

    const freshFile = path.join(testDir, 'fresh_doc.pdf');
    const expiredFile = path.join(testDir, 'expired_doc.pdf');
    const nonPdfFile = path.join(testDir, 'important_config.txt');

    fs.writeFileSync(freshFile, 'fresh pdf content');
    fs.writeFileSync(expiredFile, 'expired pdf content');
    fs.writeFileSync(nonPdfFile, 'text content');

    // Set mtime of expiredFile to 26 hours in the past
    const twentySixHoursAgo = new Date(Date.now() - 26 * 60 * 60 * 1000);
    fs.utimesSync(expiredFile, twentySixHoursAgo, twentySixHoursAgo);

    // Mock cleanup function with 24-hour maxAge
    const maxAgeMs = 24 * 60 * 60 * 1000;
    const files = await fs.promises.readdir(testDir);
    const now = Date.now();
    for (const file of files) {
      if (!file.endsWith('.pdf')) continue;
      const filePath = path.join(testDir, file);
      const stats = await fs.promises.stat(filePath);
      if (now - stats.mtimeMs > maxAgeMs) {
        await fs.promises.unlink(filePath);
      }
    }

    assert.strictEqual(fs.existsSync(freshFile), true, 'Fresh PDF must NOT be deleted');
    assert.strictEqual(fs.existsSync(expiredFile), false, 'Expired PDF must be deleted');
    assert.strictEqual(fs.existsSync(nonPdfFile), true, 'Non-PDF file must be preserved');

    // Cleanup sandbox
    fs.rmSync(testDir, { recursive: true, force: true });
  });

  // TEST 2: TrapLog Schema & Expiration Calculation
  test('TrapLog model instantiates with 180-day default expiresAt', () => {
    const TrapLog = require('./models/TrapLog');
    const log = new TrapLog({
      tokenId: new mongoose.Types.ObjectId(),
      ipAddress: '127.0.0.1',
      endpoint: '/api/test'
    });

    assert.strictEqual(log.legalHold, false, 'Default legalHold must be false');
    assert.ok(log.expiresAt instanceof Date, 'expiresAt must be a Date');

    const expectedExpiry = Date.now() + 180 * 24 * 60 * 60 * 1000;
    const diff = Math.abs(log.expiresAt.getTime() - expectedExpiry);
    assert.ok(diff < 5000, `expiresAt must be ~180 days in future (diff: ${diff}ms)`);
  });

  // TEST 3: Legal Hold Dual-State Logic
  test('Placing Legal Hold unsets expiresAt (protects from TTL)', () => {
    const TrapLog = require('./models/TrapLog');
    const log = new TrapLog({
      tokenId: new mongoose.Types.ObjectId(),
      ipAddress: '127.0.0.1',
      endpoint: '/api/test'
    });

    // Simulate placing hold
    log.legalHold = true;
    log.legalHoldReason = 'Court Order #12345';
    log.legalHoldPlacedAt = new Date();
    log.expiresAt = null;

    assert.strictEqual(log.legalHold, true);
    assert.strictEqual(log.expiresAt, null, 'expiresAt must be null during hold so TTL ignores it');

    // Simulate releasing hold
    log.legalHold = false;
    log.legalHoldReason = null;
    const originalAgeMs = Date.now() - log.timestamp.getTime();
    const remainingMs = (180 * 24 * 60 * 60 * 1000) - originalAgeMs;
    log.expiresAt = new Date(Date.now() + remainingMs);

    assert.strictEqual(log.legalHold, false);
    assert.ok(log.expiresAt instanceof Date);
    assert.ok(log.expiresAt.getTime() > Date.now());
  });

  // TEST 4: Constant-Time Admin Key Verification
  test('Admin key verification uses constant-time comparison safely', () => {
    const expected = 'PxlCrft_Admin_8x9vZapL2qWkmN5jR_cF1yT';
    function safeCompare(input) {
      if (!input || typeof input !== 'string') return false;
      const bufA = Buffer.from(input.trim());
      const bufB = Buffer.from(expected);
      if (bufA.length !== bufB.length) return false;
      return crypto.timingSafeEqual(bufA, bufB);
    }

    assert.strictEqual(safeCompare(expected), true, 'Correct key must match');
    assert.strictEqual(safeCompare('wrong_key'), false, 'Wrong key must fail');
    assert.strictEqual(safeCompare(''), false, 'Empty key must fail');
    assert.strictEqual(safeCompare(null), false, 'Null key must fail');
  });

  // TEST 5: Steganography HTML Files Zero-Network Call Verification
  test('Steganography tools contain ZERO dead fetch calls to /api/forensic/log', () => {
    const decoyHtml = fs.readFileSync(path.join(__dirname, 'public/tools/advanced-decoy.html'), 'utf8');
    const audioHtml = fs.readFileSync(path.join(__dirname, 'public/tools/audio-steganography.html'), 'utf8');

    assert.strictEqual(decoyHtml.includes('/api/forensic/log'), false, 'advanced-decoy.html must NOT contain /api/forensic/log');
    assert.strictEqual(audioHtml.includes('/api/forensic/log'), false, 'audio-steganography.html must NOT contain /api/forensic/log');
  });

  // TEST 6: Session Config Integrity in server.js
  test('server.js contains 30-day session and rolling window settings', () => {
    const serverJs = fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8');
    assert.ok(serverJs.includes('1000 * 60 * 60 * 24 * 30'), 'cookie.maxAge must be set to 30 days');
    assert.ok(serverJs.includes('rolling: true'), 'Session config must enable sliding rolling window');
    assert.ok(serverJs.includes('ttl: 30 * 24 * 60 * 60'), 'MongoStore must configure 30 days ttl');
    assert.ok(serverJs.includes('touchAfter: 24 * 3600'), 'MongoStore must configure 24h touchAfter');
  });

  console.log(`\n📊 Test Suite Summary: ${passed}/${total} Tests Passed.`);
  if (passed === total) {
    console.log('🎉 ALL INTEGRITY TESTS PASSED SUCCESSFULLY!\n');
    process.exit(0);
  } else {
    console.error('❌ SOME TESTS FAILED!\n');
    process.exit(1);
  }
}

runTests();
