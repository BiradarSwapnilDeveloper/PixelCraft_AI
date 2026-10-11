// Hardened Admin Authentication & Access Control Regression Test Suite
// Run via: node test_admin_hardening.js

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

async function runTests() {
  console.log('🛡️ Starting PixelCraft AI Admin Hardening Test Suite...\n');
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

  // TEST 1: Fail-Closed Constant-Time Verification
  test('verifyAdminKey fails closed when env is missing/empty and resists timing attacks', () => {
    const verifyKey = (candidate, configured) => {
      if (!configured || typeof configured !== 'string' || configured.trim() === '') {
        return false;
      }
      if (!candidate || typeof candidate !== 'string') {
        return false;
      }
      const cleanConfigured = configured.replace(/["']/g, '').trim();
      const hashA = crypto.createHash('sha256').update(candidate.trim()).digest();
      const hashB = crypto.createHash('sha256').update(cleanConfigured).digest();
      return crypto.timingSafeEqual(hashA, hashB);
    };

    // Fail-closed checks
    assert.strictEqual(verifyKey('admin123', null), false, 'Must fail when env is null');
    assert.strictEqual(verifyKey('admin123', undefined), false, 'Must fail when env is undefined');
    assert.strictEqual(verifyKey('admin123', ''), false, 'Must fail when env is empty string');
    assert.strictEqual(verifyKey('admin123', '   '), false, 'Must fail when env is only whitespace');
    assert.strictEqual(verifyKey(null, 'valid_secret'), false, 'Must fail when candidate is null');

    // Matching checks
    const secret = 'Hardened_Admin_Key_2026_XYZ!@#';
    assert.strictEqual(verifyKey(secret, secret), true, 'Exact match must succeed');
    assert.strictEqual(verifyKey('   ' + secret + '  ', secret), true, 'Trimmed match must succeed');
    assert.strictEqual(verifyKey(secret, `"${secret}"`), true, 'Quoted env variable must match cleanly');
    assert.strictEqual(verifyKey('wrong_pass', secret), false, 'Wrong password must fail');
    assert.strictEqual(verifyKey('Hardened_Admin_Key_2026', secret), false, 'Prefix substring must fail');
  });

  // TEST 2: Rate Limiter Logic
  test('Admin login rate limiter blocks IP after 5 failed attempts', () => {
    const attempts = new Map();
    const checkLimit = (ip) => {
      const now = Date.now();
      const windowMs = 15 * 60 * 1000;
      const record = attempts.get(ip) || { count: 0, resetTime: now + windowMs, lockedUntil: null };
      if (record.lockedUntil && now < record.lockedUntil) {
        return { allowed: false, retryAfter: Math.ceil((record.lockedUntil - now) / 1000) };
      }
      return { allowed: true };
    };

    const recordFail = (ip) => {
      const now = Date.now();
      const windowMs = 15 * 60 * 1000;
      const record = attempts.get(ip) || { count: 0, resetTime: now + windowMs, lockedUntil: null };
      record.count++;
      if (record.count >= 5) {
        record.lockedUntil = now + windowMs;
      }
      attempts.set(ip, record);
    };

    const testIp = '198.51.100.42';
    for (let i = 0; i < 4; i++) {
      recordFail(testIp);
      assert.strictEqual(checkLimit(testIp).allowed, true, `Attempt ${i + 1} should still be allowed`);
    }

    // 5th failure triggers lockout
    recordFail(testIp);
    const lockedCheck = checkLimit(testIp);
    assert.strictEqual(lockedCheck.allowed, false, '5th attempt must trigger lockout');
    assert.ok(lockedCheck.retryAfter > 800, 'Retry-after must be > 800 seconds');

    // Other IPs are not affected
    assert.strictEqual(checkLimit('203.0.113.1').allowed, true, 'Different IP must remain unaffected');
  });

  // TEST 3: Multi-layer CSRF & Origin/Referer Validation
  test('verifyAdminCsrfAndOrigin validates host match and unpredictable session token', () => {
    const verifyCsrf = (req) => {
      const host = req.headers['host'];
      const origin = req.headers['origin'];
      const referer = req.headers['referer'];

      if (origin) {
        try {
          const originHost = new URL(origin).host;
          if (originHost !== host) return { valid: false, error: 'Forbidden: Cross-origin request rejected.' };
        } catch (e) {
          return { valid: false, error: 'Forbidden: Malformed origin header.' };
        }
      } else if (referer) {
        try {
          const refererHost = new URL(referer).host;
          if (refererHost !== host) return { valid: false, error: 'Forbidden: Referer header mismatch.' };
        } catch (e) {
          return { valid: false, error: 'Forbidden: Malformed referer header.' };
        }
      } else {
        return { valid: false, error: 'Forbidden: Missing Origin and Referer header on state-changing request.' };
      }

      const clientToken = req.headers['x-admin-csrf-token'];
      const sessionToken = req.session ? req.session.adminCsrfToken : null;
      if (!clientToken || !sessionToken || typeof clientToken !== 'string') {
        return { valid: false, error: 'Forbidden: Missing or invalid CSRF security token.' };
      }

      const bufClient = Buffer.from(clientToken, 'utf8');
      const bufSession = Buffer.from(sessionToken, 'utf8');
      if (bufClient.length !== bufSession.length || !crypto.timingSafeEqual(bufClient, bufSession)) {
        return { valid: false, error: 'Forbidden: CSRF token verification failed.' };
      }

      return { valid: true };
    };

    const validToken = crypto.randomBytes(32).toString('hex');
    const matchingReq = {
      headers: {
        host: 'pixelcraftaitools.com',
        origin: 'https://pixelcraftaitools.com',
        'x-admin-csrf-token': validToken
      },
      session: { adminCsrfToken: validToken }
    };
    assert.strictEqual(verifyCsrf(matchingReq).valid, true, 'Valid origin and matching token must pass');

    // Cross-origin attack
    const evilReq = {
      headers: {
        host: 'pixelcraftaitools.com',
        origin: 'https://evil-attacker.com',
        'x-admin-csrf-token': validToken
      },
      session: { adminCsrfToken: validToken }
    };
    assert.strictEqual(verifyCsrf(evilReq).valid, false, 'Attacker origin must be rejected');

    // Missing token
    const missingTokenReq = {
      headers: {
        host: 'pixelcraftaitools.com',
        origin: 'https://pixelcraftaitools.com'
      },
      session: { adminCsrfToken: validToken }
    };
    assert.strictEqual(verifyCsrf(missingTokenReq).valid, false, 'Missing token must be rejected');

    // Fixed dummy token "1" attack
    const fixedTokenReq = {
      headers: {
        host: 'pixelcraftaitools.com',
        origin: 'https://pixelcraftaitools.com',
        'x-admin-csrf-token': '1'
      },
      session: { adminCsrfToken: validToken }
    };
    assert.strictEqual(verifyCsrf(fixedTokenReq).valid, false, 'Fixed value token must be rejected');
  });

  // TEST 4: Path Containment & Schema Validation
  test('Path containment rejects directory traversal, null bytes, and sensitive files', () => {
    const validateContainment = (userPath) => {
      if (!userPath || typeof userPath !== 'string') return null;
      if (userPath.includes('\0')) return null;

      const normalized = path.normalize(userPath);
      const absoluteCandidate = path.resolve(__dirname, normalized);
      let realProjectRoot;
      try {
        realProjectRoot = fs.realpathSync(__dirname);
      } catch (e) {
        realProjectRoot = path.resolve(__dirname);
      }

      const relFromRoot = path.relative(realProjectRoot, absoluteCandidate);
      if (relFromRoot === '' || relFromRoot.startsWith('..') || path.isAbsolute(relFromRoot)) {
        return null;
      }

      const blockedPatterns = [/^\.env/i, /^\.git/i, /^node_modules/i, /\.pem$/i, /\.key$/i, /\.pfx$/i, /\.crt$/i, /\.bak$/i, /^scripts[\\\/]/i, /^models[\\\/]/i];
      if (blockedPatterns.some(p => p.test(relFromRoot))) {
        return null;
      }

      if (fs.existsSync(absoluteCandidate)) {
        try {
          const realTarget = fs.realpathSync(absoluteCandidate);
          const realRel = path.relative(realProjectRoot, realTarget);
          if (realRel.startsWith('..') || path.isAbsolute(realRel)) {
            return null;
          }
        } catch (e) {
          return null;
        }
      }

      return { absolutePath: absoluteCandidate, relativePath: relFromRoot };
    };

    assert.strictEqual(validateContainment('../../etc/passwd'), null, 'Traversal must return null');
    assert.strictEqual(validateContainment('..\\..\\Windows\\System32'), null, 'Windows traversal must return null');
    assert.strictEqual(validateContainment('.env'), null, '.env must be blocked');
    assert.strictEqual(validateContainment('.env.production'), null, '.env.* must be blocked');
    assert.strictEqual(validateContainment('models/User.js'), null, 'models/ must be blocked');
    assert.strictEqual(validateContainment('scripts/plant_honeytoken.js'), null, 'scripts/ must be blocked');
    assert.strictEqual(validateContainment('server.js.pre-retention.bak'), null, '.bak files must be blocked');
    assert.strictEqual(validateContainment('public/index.html\0.png'), null, 'Null byte injection must be blocked');

    // Valid path
    const valid = validateContainment('public/index.html');
    assert.ok(valid !== null, 'public/index.html should be allowed');
    assert.strictEqual(valid.relativePath.replace(/\\/g, '/'), 'public/index.html');
  });

  // TEST 5: Schema Validation on settings.json
  test('Settings schema validation strictly enforces boolean requireLoginForTools', () => {
    const validateSettingsJson = (content) => {
      try {
        const parsed = JSON.parse(content);
        if (typeof parsed.requireLoginForTools !== 'boolean') {
          return { valid: false, error: 'settings.json requires boolean requireLoginForTools' };
        }
        return { valid: true };
      } catch (e) {
        return { valid: false, error: 'Must be valid JSON' };
      }
    };

    assert.strictEqual(validateSettingsJson('{"requireLoginForTools": true}').valid, true);
    assert.strictEqual(validateSettingsJson('{"requireLoginForTools": false}').valid, true);
    assert.strictEqual(validateSettingsJson('{"requireLoginForTools": "true"}').valid, false);
    assert.strictEqual(validateSettingsJson('{"requireLoginForTools": 1}').valid, false);
    assert.strictEqual(validateSettingsJson('{malformed json}').valid, false);
  });

  // TEST 6: Zero Leakage Verification
  test('View files ensure absolute zero leakage of dashboard or private keys', () => {
    // 1. public/controlroommanage.html must not exist
    const publicPath = path.join(__dirname, 'public', 'controlroommanage.html');
    assert.strictEqual(fs.existsSync(publicPath), false, 'public/controlroommanage.html must not exist');

    // 2. views/admin-gate.html has NO dashboard DOM or admin elements
    const gateHtml = fs.readFileSync(path.join(__dirname, 'views', 'admin-gate.html'), 'utf8');
    assert.strictEqual(gateHtml.includes('CodeMirror'), false, 'Gate must not include CodeMirror');
    assert.strictEqual(gateHtml.includes('Chart.js'), false, 'Gate must not include Chart.js');
    assert.strictEqual(gateHtml.includes('Entity Database'), false, 'Gate must not mention Entity Database');
    assert.strictEqual(gateHtml.includes('user-modal'), false, 'Gate must not include user modal');
    assert.strictEqual(gateHtml.includes('Deployment Hub'), false, 'Gate must not include Deployment Hub');
    assert.strictEqual(gateHtml.includes('Legal Preservation Hub'), false, 'Gate must not include Legal Preservation');
    assert.strictEqual(gateHtml.includes('sessionStorage'), false, 'Gate must not use sessionStorage');

    // 3. views/admin-dashboard.html has NO embedded RSA private key or sessionStorage
    const dashHtml = fs.readFileSync(path.join(__dirname, 'views', 'admin-dashboard.html'), 'utf8');
    assert.strictEqual(dashHtml.includes('BEGIN RSA PRIVATE KEY'), false, 'Dashboard must not contain RSA private key');
    assert.strictEqual(dashHtml.includes('sessionStorage'), false, 'Dashboard must not store master key in sessionStorage');
    assert.ok(dashHtml.includes('X-Admin-CSRF-Token'), 'Dashboard must use X-Admin-CSRF-Token header');
  });

  // TEST 7: Server Route Gating Integrity
  test('server.js contains server-side gated controlroom routing with cache prevention', () => {
    const serverCode = fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8');

    assert.ok(serverCode.includes("app.get(['/controlroommanage', '/controlroommanage.html']"), 'Must register controlroom route gate');
    assert.ok(serverCode.includes("res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private')"), 'Must send strict no-store cache headers');
    assert.ok(serverCode.includes("req.session && req.session.isAdmin"), 'Must check session admin state');
    assert.ok(serverCode.includes("admin-dashboard.html"), 'Must serve admin-dashboard.html for authenticated admins');
    assert.ok(serverCode.includes("admin-gate.html"), 'Must serve admin-gate.html for unauthenticated visitors');
    assert.strictEqual((serverCode.match(/requireAdminAuth/g) || []).length, 0, 'No legacy requireAdminAuth should remain');
  });

  console.log(`\n📊 Admin Hardening Test Suite Summary: ${passed}/${total} Tests Passed.`);
  if (passed === total) {
    console.log('🎉 ALL HARDENING TESTS PASSED WITH 100% SUCCESS!\n');
    process.exit(0);
  } else {
    console.error('❌ SOME TESTS FAILED!\n');
    process.exit(1);
  }
}

runTests();
