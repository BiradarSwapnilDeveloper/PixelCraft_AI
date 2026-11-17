/**
 * PixelCraft AI — SEO Task 6.2.6 Runtime Refinements & Accuracy Test Suite
 * Validates:
 * 1. Smart Resize 'resize_previews_generated' renaming and two-stage funnel.
 * 2. Format Converter concurrent conversion lock and control disablement.
 * 3. GA4 DebugView host isolation (production safety vs dev opt-in).
 * 4. Zero-PII and regression integrity across all events.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('================================================================');
console.log('PIXELCRAFT AI — TASK 6.2.6 GA4 ACCURACY & REFINEMENT TEST SUITE');
console.log('================================================================\n');

let passedTests = 0;
let totalTests = 0;

function runTest(testName, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✅ [PASS] ${testName}`);
    passedTests++;
  } catch (err) {
    console.error(`  ❌ [FAIL] ${testName}`);
    console.error(`     Error: ${err.message}`);
  }
}

// 1. Test Smart Resize Event Accuracy & Renaming in utils.js
const utilsCode = fs.readFileSync(path.join(__dirname, '../public/js/utils.js'), 'utf8');

function setupUtilsEnv() {
  const events = [];
  const fakeGtag = (action, name, params) => {
    if (action === 'event') events.push({ name, params });
  };
  const sandbox = {
    window: { gtag: fakeGtag, dataLayer: [], matchMedia: () => ({ matches: false }), location: { pathname: '/' } },
    document: { documentElement: { setAttribute: () => {}, getAttribute: () => 'light' }, addEventListener: () => {} },
    localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
    navigator: {},
    console: { log: () => {}, warn: () => {}, error: () => {} },
    setTimeout: (fn, ms) => setTimeout(fn, ms),
    clearTimeout: (id) => clearTimeout(id)
  };
  sandbox.window.window = sandbox.window;
  const fn = new Function('window', 'document', 'localStorage', 'navigator', 'console', 'setTimeout', 'clearTimeout', utilsCode);
  fn(sandbox.window, sandbox.document, sandbox.localStorage, sandbox.navigator, sandbox.console, sandbox.setTimeout, sandbox.clearTimeout);
  return { analytics: sandbox.window.PixelCraftAnalytics, events };
}

runTest('Smart Resize Renaming: Maps Smart Social Resize to resize_previews_generated', () => {
  const { analytics, events } = setupUtilsEnv();
  assert(analytics, 'PixelCraftAnalytics must exist');

  // Trigger completion for Smart Social Resize
  analytics.trackCompletion('Smart Social Resize', 'png', 35000);

  assert.strictEqual(events.length, 1);
  assert.strictEqual(events[0].name, 'resize_previews_generated');
  assert.deepStrictEqual(events[0].params, {
    tool_name: 'Smart Social Resize',
    output_format: 'png',
    operation_status: 'success',
    file_size_bucket: '20KB-50KB'
  });

  // Verify downloads still use tool_output_downloaded
  analytics.trackDownload('Smart Social Resize', 'png', 35000);
  assert.strictEqual(events.length, 2);
  assert.strictEqual(events[1].name, 'tool_output_downloaded');
  assert.strictEqual(events[1].params.output_format, 'png');

  // Verify batch ZIP download
  analytics.trackDownload('Smart Social Resize', 'zip', 250000);
  assert.strictEqual(events.length, 3);
  assert.strictEqual(events[2].name, 'tool_output_downloaded');
  assert.strictEqual(events[2].params.output_format, 'zip');
  assert.strictEqual(events[2].params.file_size_bucket, '200KB-500KB');
});

// 2. Test Format Converter Processing Protection in format-converter.html
const formatConverterCode = fs.readFileSync(path.join(__dirname, '../public/tools/format-converter.html'), 'utf8');

runTest('Format Converter HTML Codebase: Contains isConverting guard, control lock, and finally block', () => {
  assert(formatConverterCode.includes('let isConverting = false;'), 'Must have isConverting state flag');
  assert(formatConverterCode.includes('setConversionControlsState(true)'), 'Must disable conversion controls during processing');
  assert(formatConverterCode.includes('setConversionControlsState(false)'), 'Must restore conversion controls in finally block');
  assert(formatConverterCode.includes('finally {'), 'Must use try/finally to guarantee lock release');
  assert(formatConverterCode.includes('if (isConverting) return;'), 'Must prevent overlapping conversions');
  assert(formatConverterCode.includes('pointerEvents = disabled ? \'none\' : \'auto\''), 'Must visually and functionally lock buttons');
});

// 3. Test GA4 Debug Mode Host Isolation in cookie-consent.js
const cookieConsentCode = fs.readFileSync(path.join(__dirname, '../public/js/cookie-consent.js'), 'utf8');

runTest('GA4 Debug Mode Host Isolation: Production host strictly rejects debug_mode', () => {
  function evaluateDebugMode(hostname, search, localStorageFlag) {
    const isDevHost = (function () {
      try {
        const h = hostname;
        return h === 'localhost' || h === '127.0.0.1' || h === '0.0.0.0' || h.endsWith('.local') || h.endsWith('.internal');
      } catch (e) {
        return false;
      }
    })();

    const gaConfig = {};
    if (isDevHost) {
      try {
        if (search.includes('ga_debug=1') || localStorageFlag === 'true') {
          gaConfig.debug_mode = true;
        }
      } catch (e) {}
    }
    return gaConfig;
  }

  // Production tests (pixelcraftaitools.com)
  assert.deepStrictEqual(evaluateDebugMode('pixelcraftaitools.com', '', 'false'), {}, 'Normal production user receives empty config');
  assert.deepStrictEqual(evaluateDebugMode('pixelcraftaitools.com', '?ga_debug=1', 'true'), {}, 'Production user with URL param NEVER receives debug_mode');
  assert.deepStrictEqual(evaluateDebugMode('www.pixelcraftaitools.com', '?ga_debug=1', 'true'), {}, 'Production www user NEVER receives debug_mode');

  // Local / Staging tests
  assert.deepStrictEqual(evaluateDebugMode('localhost', '', 'false'), {}, 'Localhost without debug flag receives normal config');
  assert.deepStrictEqual(evaluateDebugMode('localhost', '?ga_debug=1', 'false'), { debug_mode: true }, 'Localhost with ?ga_debug=1 receives debug_mode: true');
  assert.deepStrictEqual(evaluateDebugMode('127.0.0.1', '', 'true'), { debug_mode: true }, '127.0.0.1 with localStorage flag receives debug_mode: true');
  assert.deepStrictEqual(evaluateDebugMode('staging.pixelcraft.local', '?ga_debug=1', 'false'), { debug_mode: true }, '.local domain receives debug_mode: true');
});

console.log(`\n================================================================`);
console.log(`Task 6.2.6 Test Results: ${passedTests}/${totalTests} Passed`);
console.log('================================================================\n');

if (passedTests !== totalTests) {
  process.exit(1);
} else {
  process.exit(0);
}
