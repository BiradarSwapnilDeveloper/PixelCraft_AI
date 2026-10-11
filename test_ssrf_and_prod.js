// test_ssrf_and_prod.js
// In-depth verification of SSRF protections and Production Configuration
const http = require('http');
const net = require('net');
const dns = require('dns');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const BASE_URL = 'http://localhost:8080';

async function postJson(endpoint, data) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify(data);
    const u = new URL(endpoint, BASE_URL);
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, headers: res.headers, data: JSON.parse(body) });
        } catch (e) {
          resolve({ status: res.statusCode, headers: res.headers, raw: body });
        }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function getReq(pathAndQuery) {
  return new Promise((resolve, reject) => {
    const u = new URL(pathAndQuery, BASE_URL);
    const req = http.request({
      hostname: u.hostname,
      port: u.port,
      path: u.pathname + (u.search || ''),
      method: 'GET'
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
    });
    req.on('error', reject);
    req.end();
  });
}

async function verifySSRF() {
  console.log('\n======================================================');
  console.log('🛡️ 1. TESTING LIVE SSRF PROTECTION ON /api/scan-link');
  console.log('======================================================\n');

  const attackVectors = [
    { name: 'Localhost IPv4 (127.0.0.1)', url: 'http://127.0.0.1:8080/admin' },
    { name: 'Localhost Hostname (localhost)', url: 'http://localhost:8080/metrics' },
    { name: 'Subdomain Localhost (test.localhost)', url: 'http://foo.localhost/api' },
    { name: 'Loopback Alternative (127.12.34.56)', url: 'http://127.12.34.56:8080' },
    { name: 'Cloud AWS/GCP Metadata (169.254.169.254)', url: 'http://169.254.169.254/latest/meta-data/' },
    { name: 'Google Cloud Metadata Hostname', url: 'http://metadata.google.internal/computeMetadata/v1/' },
    { name: 'Private RFC1918 Class A (10.0.0.1)', url: 'http://10.0.0.1/admin.html' },
    { name: 'Private RFC1918 Class B (172.16.0.1)', url: 'http://172.16.0.1/' },
    { name: 'Private RFC1918 Class C (192.168.1.1)', url: 'http://192.168.1.1/router' },
    { name: 'All Interfaces (0.0.0.0)', url: 'http://0.0.0.0:8080' },
    { name: 'IPv6 Localhost (::1)', url: 'http://[::1]:8080' },
    { name: 'Decimal Encoded IP (2130706433 = 127.0.0.1)', url: 'http://2130706433:8080' },
    { name: 'Octal Encoded IP (0177.0.0.1 = 127.0.0.1)', url: 'http://0177.0.0.1:8080' },
    { name: 'Hex Encoded IP (0x7f000001 = 127.0.0.1)', url: 'http://0x7f000001:8080' },
    { name: 'Carrier-Grade NAT (100.64.0.1)', url: 'http://100.64.0.1/' }
  ];

  let ssrfBlocked = 0;
  for (const v of attackVectors) {
    try {
      const res = await postJson('/api/scan-link', { url: v.url });
      const reasoning = res.data?.aiAnalysis?.reasoning || '';
      const isBlocked = res.data?.riskScore === 100 && (reasoning.includes('SSRF') || reasoning.includes('internal loopback') || res.data?.threatDbMatch === true);
      if (isBlocked) {
        ssrfBlocked++;
        console.log(`  ✅ [BLOCKED] ${v.name}: RiskScore=100 (SSRF Intercepted)`);
      } else {
        console.log(`  ❌ [FAILED TO BLOCK] ${v.name}:`, res.data);
      }
    } catch (err) {
      console.log(`  ⚠️ [ERROR] ${v.name}:`, err.message);
    }
  }

  console.log(`\nSSRF Vector Interception: ${ssrfBlocked}/${attackVectors.length} Blocked Successfully.`);

  // Test legitimate public URL
  console.log('\nTesting Legitimate Public URL: https://google.com');
  const safeRes = await postJson('/api/scan-link', { url: 'https://google.com' });
  const isSafeOk = safeRes.status === 200 && safeRes.data && safeRes.data.riskScore < 50;
  console.log(`  ${isSafeOk ? '✅ [PASS]' : '❌ [FAIL]'} Legitimate Public URL allowed with RiskScore=${safeRes.data?.riskScore}`);
}

async function verifyProductionConfig() {
  console.log('\n======================================================');
  console.log('⚙️ 2. TESTING PRODUCTION CONFIGURATION & DEFENSES');
  console.log('======================================================\n');

  // A. Check Global Security Headers on root
  const indexRes = await getReq('/');
  const h = indexRes.headers;

  console.log('A. Global Security Headers:');
  console.log(`  ${h['x-content-type-options'] === 'nosniff' ? '✅' : '❌'} X-Content-Type-Options: ${h['x-content-type-options']}`);
  console.log(`  ${h['x-frame-options'] === 'SAMEORIGIN' ? '✅' : '❌'} X-Frame-Options: ${h['x-frame-options']}`);
  console.log(`  ${h['referrer-policy'] === 'strict-origin-when-cross-origin' ? '✅' : '❌'} Referrer-Policy: ${h['referrer-policy']}`);
  console.log(`  ${h['permissions-policy'] ? '✅' : '❌'} Permissions-Policy: ${h['permissions-policy']}`);

  // B. Sensitive API Anti-Caching Headers (/api/scan-link)
  const apiRes = await postJson('/api/scan-link', { url: 'https://example.com' });
  const ah = apiRes.headers;
  console.log('\nB. API Anti-Caching Headers (/api):');
  console.log(`  ${ah['cache-control']?.includes('no-store') ? '✅' : '❌'} Cache-Control: ${ah['cache-control']}`);
  console.log(`  ${ah['pragma'] === 'no-cache' ? '✅' : '❌'} Pragma: ${ah['pragma']}`);

  // C. Server Code Production Audit
  console.log('\nC. Server Code Production Audit:');
  const serverCode = fs.readFileSync(path.join(__dirname, 'server.js'), 'utf8');

  // Check 1: Session Cookie Security (sameSite lax, httpOnly, secure)
  const hasCookieSec = serverCode.includes("sameSite: 'lax'") && serverCode.includes("httpOnly: true");
  console.log(`  ${hasCookieSec ? '✅' : '❌'} Session Cookie: HttpOnly & SameSite=Lax configured`);

  // Check 2: MongoDB Session Store in Production
  const hasMongoSession = serverCode.includes("collectionName: 'sessions'") && serverCode.includes("ttl: 30 * 24 * 60 * 60");
  console.log(`  ${hasMongoSession ? '✅' : '❌'} MongoDB Session Store with 30-day TTL configured for Production/Render`);

  // Check 3: Active Defense Honeytoken Trap
  const hasHoneytoken = serverCode.includes('honeytokenTrap') && serverCode.includes('app.use(honeytokenTrap)');
  console.log(`  ${hasHoneytoken ? '✅' : '❌'} Honeytoken Active Defense Trap active globally`);

  // Check 4: Safe File Deploy Restrictions
  const hasDeployGuards = serverCode.includes('executablePattern') && serverCode.includes('isRootScript');
  console.log(`  ${hasDeployGuards ? '✅' : '❌'} Arbitrary executable upload defense active on admin save/deploy endpoint`);

  // Check 5: Forensic Sanitizer Fail-Closed
  const hasFailClosed = serverCode.includes('Unsanitized file cannot be verified') && serverCode.includes('status(422)');
  console.log(`  ${hasFailClosed ? '✅' : '❌'} Forensic Sanitizer fail-closed (HTTP 422) on corrupt inputs`);

  // Check 6: AI Generation Rate Limiting
  const hasAiLimits = serverCode.includes('aiGenerationLimiterMiddleware') && serverCode.includes('trimmedPrompt.length > 500');
  console.log(`  ${hasAiLimits ? '✅' : '❌'} AI API endpoints rate-limited and capped at 500 characters`);
}

async function run() {
  await verifySSRF();
  await verifyProductionConfig();
  console.log('\n✅ Verification Script Completed.\n');
}

run().catch(err => {
  console.error('Test Execution Error:', err);
  process.exit(1);
});
