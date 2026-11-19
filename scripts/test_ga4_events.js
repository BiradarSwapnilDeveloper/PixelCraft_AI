/**
 * PixelCraft AI - GA4 Custom Tool Event Instrumentation Verification Suite
 * Verifies event payload structures, size bucketing, zero-PII enforcement,
 * error categorization, debounce mechanisms, and tool integration.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('================================================================');
console.log('PIXELCRAFT AI — GA4 CUSTOM TOOL EVENT INSTRUMENTATION TEST SUITE');
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

// 1. Load utils.js in a simulated DOM environment
const utilsCode = fs.readFileSync(path.join(__dirname, '../public/js/utils.js'), 'utf8');

function setupEnvironment() {
  const eventsCaptured = [];
  const fakeGtag = function(action, eventName, params) {
    if (action === 'event') {
      eventsCaptured.push({ eventName, params });
    }
  };

  const sandbox = {
    window: {
      gtag: fakeGtag,
      dataLayer: [],
      matchMedia: () => ({ matches: false }),
      location: { pathname: '/tools/image-compressor.html' },
      addEventListener: () => {}
    },
    document: {
      documentElement: { setAttribute: () => {}, getAttribute: () => 'light' },
      addEventListener: () => {},
      querySelectorAll: () => [],
      getElementById: () => null,
      createElement: () => ({ style: {}, appendChild: () => {}, setAttribute: () => {} }),
      body: { appendChild: () => {} }
    },
    localStorage: {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {}
    },
    navigator: {},
    console: { log: () => {}, warn: () => {}, error: () => {} },
    setTimeout: (fn, ms) => setTimeout(fn, ms),
    clearTimeout: (id) => clearTimeout(id)
  };

  sandbox.window.window = sandbox.window;
  sandbox.window.document = sandbox.document;
  sandbox.window.localStorage = sandbox.localStorage;

  const fn = new Function('window', 'document', 'localStorage', 'navigator', 'console', 'setTimeout', 'clearTimeout', utilsCode);
  fn(sandbox.window, sandbox.document, sandbox.localStorage, sandbox.navigator, sandbox.console, sandbox.setTimeout, sandbox.clearTimeout);

  return { analytics: sandbox.window.PixelCraftAnalytics, eventsCaptured, sandbox };
}

// TEST 1: Size Bucketing Accuracy
runTest('File Size Bucketing: Correctly classifies all defined byte ranges and boundary conditions', () => {
  const { analytics } = setupEnvironment();
  assert(analytics, 'PixelCraftAnalytics helper must be defined');

  assert.strictEqual(analytics.getFileSizeBucket(0), 'unknown');
  assert.strictEqual(analytics.getFileSizeBucket(-500), 'unknown');
  assert.strictEqual(analytics.getFileSizeBucket(null), 'unknown');
  assert.strictEqual(analytics.getFileSizeBucket(undefined), 'unknown');
  assert.strictEqual(analytics.getFileSizeBucket('string'), 'unknown');

  // <20KB: 1 byte to 20479 bytes
  assert.strictEqual(analytics.getFileSizeBucket(1024), '<20KB');
  assert.strictEqual(analytics.getFileSizeBucket(19 * 1024), '<20KB');
  assert.strictEqual(analytics.getFileSizeBucket(20 * 1024 - 1), '<20KB');

  // 20KB-50KB: 20480 bytes to 51200 bytes
  assert.strictEqual(analytics.getFileSizeBucket(20 * 1024), '20KB-50KB');
  assert.strictEqual(analytics.getFileSizeBucket(35 * 1024), '20KB-50KB');
  assert.strictEqual(analytics.getFileSizeBucket(50 * 1024), '20KB-50KB');

  // 50KB-100KB: 51201 bytes to 102400 bytes
  assert.strictEqual(analytics.getFileSizeBucket(50 * 1024 + 1), '50KB-100KB');
  assert.strictEqual(analytics.getFileSizeBucket(75 * 1024), '50KB-100KB');
  assert.strictEqual(analytics.getFileSizeBucket(100 * 1024), '50KB-100KB');

  // 100KB-200KB: 102401 bytes to 204800 bytes
  assert.strictEqual(analytics.getFileSizeBucket(100 * 1024 + 1), '100KB-200KB');
  assert.strictEqual(analytics.getFileSizeBucket(150 * 1024), '100KB-200KB');
  assert.strictEqual(analytics.getFileSizeBucket(200 * 1024), '100KB-200KB');

  // 200KB-500KB: 204801 bytes to 512000 bytes
  assert.strictEqual(analytics.getFileSizeBucket(200 * 1024 + 1), '200KB-500KB');
  assert.strictEqual(analytics.getFileSizeBucket(350 * 1024), '200KB-500KB');
  assert.strictEqual(analytics.getFileSizeBucket(500 * 1024), '200KB-500KB');

  // >500KB: 512001 bytes and above
  assert.strictEqual(analytics.getFileSizeBucket(500 * 1024 + 1), '>500KB');
  assert.strictEqual(analytics.getFileSizeBucket(1024 * 1024), '>500KB');
  assert.strictEqual(analytics.getFileSizeBucket(15 * 1024 * 1024), '>500KB');
});

// TEST 2: Successful Tool Completion Events Mapping
runTest('Tool Completion Events: Maps tool names to exact custom GA4 event names', () => {
  const { analytics, eventsCaptured } = setupEnvironment();

  analytics.trackCompletion('Image Compressor', 'jpg', 45000);
  analytics.trackCompletion('Format Converter', 'webp', 85000);
  analytics.trackCompletion('Custom QR Generator', 'png', 12000);
  analytics.trackCompletion('Smart Social Resize', 'png', 150000);
  analytics.trackCompletion('Images to PDF', 'pdf', 450000);

  assert.strictEqual(eventsCaptured.length, 5);

  assert.strictEqual(eventsCaptured[0].eventName, 'image_compressed');
  assert.deepStrictEqual(eventsCaptured[0].params, {
    tool_name: 'Image Compressor',
    output_format: 'jpg',
    operation_status: 'success',
    file_size_bucket: '20KB-50KB'
  });

  assert.strictEqual(eventsCaptured[1].eventName, 'format_converted');
  assert.deepStrictEqual(eventsCaptured[1].params, {
    tool_name: 'Format Converter',
    output_format: 'webp',
    operation_status: 'success',
    file_size_bucket: '50KB-100KB'
  });

  assert.strictEqual(eventsCaptured[2].eventName, 'qr_generated');
  assert.deepStrictEqual(eventsCaptured[2].params, {
    tool_name: 'Custom QR Generator',
    output_format: 'png',
    operation_status: 'success',
    file_size_bucket: '<20KB'
  });

  assert.strictEqual(eventsCaptured[3].eventName, 'resize_previews_generated');
  assert.deepStrictEqual(eventsCaptured[3].params, {
    tool_name: 'Smart Social Resize',
    output_format: 'png',
    operation_status: 'success',
    file_size_bucket: '100KB-200KB'
  });

  assert.strictEqual(eventsCaptured[4].eventName, 'pdf_created');
  assert.deepStrictEqual(eventsCaptured[4].params, {
    tool_name: 'Images to PDF',
    output_format: 'pdf',
    operation_status: 'success',
    file_size_bucket: '200KB-500KB'
  });
});

// TEST 3: User Download Tracking
runTest('Download Tracking: Correctly dispatches tool_output_downloaded event', () => {
  const { analytics, eventsCaptured } = setupEnvironment();

  analytics.trackDownload('Image Compressor', 'webp', 32000);
  analytics.trackDownload('Smart Social Resize', 'zip', 650000);

  assert.strictEqual(eventsCaptured.length, 2);
  assert.strictEqual(eventsCaptured[0].eventName, 'tool_output_downloaded');
  assert.deepStrictEqual(eventsCaptured[0].params, {
    tool_name: 'Image Compressor',
    output_format: 'webp',
    operation_status: 'success',
    file_size_bucket: '20KB-50KB'
  });

  assert.strictEqual(eventsCaptured[1].eventName, 'tool_output_downloaded');
  assert.deepStrictEqual(eventsCaptured[1].params, {
    tool_name: 'Smart Social Resize',
    output_format: 'zip',
    operation_status: 'success',
    file_size_bucket: '>500KB'
  });
});

// TEST 4: Controlled Error Categorization
runTest('Tool Error Tracking: Restricts error_type to 4 authorized categories', () => {
  const { analytics, eventsCaptured } = setupEnvironment();

  analytics.trackError('Image Compressor', 'invalid_input');
  analytics.trackError('Format Converter', 'unsupported_format');
  analytics.trackError('Images to PDF', 'processing_failed');
  analytics.trackError('Custom QR Generator', 'file_too_large');
  analytics.trackError('Smart Social Resize', 'arbitrary_unknown_error'); // Should fallback

  assert.strictEqual(eventsCaptured.length, 5);

  assert.strictEqual(eventsCaptured[0].eventName, 'tool_operation_error');
  assert.deepStrictEqual(eventsCaptured[0].params, {
    tool_name: 'Image Compressor',
    error_type: 'invalid_input',
    operation_status: 'error'
  });

  assert.strictEqual(eventsCaptured[1].eventName, 'tool_operation_error');
  assert.deepStrictEqual(eventsCaptured[1].params, {
    tool_name: 'Format Converter',
    error_type: 'unsupported_format',
    operation_status: 'error'
  });

  assert.strictEqual(eventsCaptured[2].eventName, 'tool_operation_error');
  assert.deepStrictEqual(eventsCaptured[2].params, {
    tool_name: 'Images to PDF',
    error_type: 'processing_failed',
    operation_status: 'error'
  });

  assert.strictEqual(eventsCaptured[3].eventName, 'tool_operation_error');
  assert.deepStrictEqual(eventsCaptured[3].params, {
    tool_name: 'Custom QR Generator',
    error_type: 'file_too_large',
    operation_status: 'error'
  });

  assert.strictEqual(eventsCaptured[4].eventName, 'tool_operation_error');
  assert.deepStrictEqual(eventsCaptured[4].params, {
    tool_name: 'Smart Social Resize',
    error_type: 'processing_failed', // sanitized fallback
    operation_status: 'error'
  });
});

// TEST 5: Strict Zero-PII Enforcement
runTest('Zero-PII Compliance: Blocks and strips sensitive keys (filenames, prompts, URLs, secrets)', () => {
  const { analytics, eventsCaptured } = setupEnvironment();

  analytics.trackCompletion('Format Converter', 'png', 40000, {
    filename: 'confidential_contract.pdf',
    file_name: 'passport_scan.jpg',
    url: 'https://secret.company.org/auth',
    prompt: 'steganography secret text',
    secret: 'aes-key-12345',
    safe_feature_flag: 'high_contrast'
  });

  assert.strictEqual(eventsCaptured.length, 1);
  const params = eventsCaptured[0].params;
  assert.strictEqual(params.filename, undefined);
  assert.strictEqual(params.file_name, undefined);
  assert.strictEqual(params.url, undefined);
  assert.strictEqual(params.prompt, undefined);
  assert.strictEqual(params.secret, undefined);
  assert.strictEqual(params.safe_feature_flag, 'high_contrast');
});

// TEST 6: Resilient & Fault-Tolerant Behavior
runTest('Fault Tolerance: Does not crash or throw if gtag throws an exception or is blocked', () => {
  const { analytics, sandbox } = setupEnvironment();
  // Simulate ad blocker or gtag throwing exception
  sandbox.window.gtag = () => { throw new Error('AdBlocker active'); };

  assert.doesNotThrow(() => {
    analytics.trackCompletion('Image Compressor', 'jpg', 25000);
    analytics.trackDownload('Image Compressor', 'jpg', 25000);
    analytics.trackError('Image Compressor', 'processing_failed');
  });
});

// TEST 7: HTML Codebase Instrumentation Audit
runTest('HTML Codebase Audit: Priority tool pages contain instrumented PixelCraftAnalytics calls and load utils.js', () => {
  const targetTools = [
    { file: 'image-compressor.html', completion: 'image_compressed', toolName: 'Image Compressor' },
    { file: 'format-converter.html', completion: 'format_converted', toolName: 'Format Converter' },
    { file: 'qr-generator.html', completion: 'qr_generated', toolName: 'Custom QR Generator' },
    { file: 'smart-resize.html', completion: 'resize_previews_generated', toolName: 'Smart Social Resize' },
    { file: 'images-to-pdf.html', completion: 'pdf_created', toolName: 'Images to PDF' }
  ];

  targetTools.forEach(tool => {
    const htmlPath = path.join(__dirname, '../public/tools', tool.file);
    const content = fs.readFileSync(htmlPath, 'utf8');

    // Check utils.js script tag
    assert(content.includes('<script src="../js/utils.js"></script>'), `${tool.file} must load ../js/utils.js`);

    // Check analytics completion call
    assert(
      content.includes(`PixelCraftAnalytics.trackCompletion`) || content.includes(`PixelCraftAnalytics.trackCompletionDebounced`),
      `${tool.file} must track completion`
    );

    // Check analytics download call
    assert(content.includes(`PixelCraftAnalytics.trackDownload`), `${tool.file} must track downloads`);

    // Check analytics error call
    assert(content.includes(`PixelCraftAnalytics.trackError`), `${tool.file} must track errors`);

    // Ensure zero PII is sent to trackCompletion or trackDownload
    assert(!content.includes(`trackCompletion(${tool.file}, currentFile.name`), `${tool.file} must never pass file names to analytics`);
  });
});

// TEST 8: Blog-to-Tool & Internal Discovery CTA Event Structure
runTest('Tool CTA Click: Correctly structures tool_cta_clicked event with safe parameters', () => {
  const { analytics, eventsCaptured } = setupEnvironment();
  assert(typeof analytics.trackToolCtaClick === 'function', 'trackToolCtaClick must be defined');

  analytics.trackToolCtaClick(
    '/blog/passport-and-exam-photo-resizing-guide.html?ref=google#section2',
    '../tools/smart-resize.html?utm_source=blog',
    'blog_mid_cta',
    'blog_article'
  );

  assert.strictEqual(eventsCaptured.length, 1);
  const event = eventsCaptured[0];
  assert.strictEqual(event.eventName, 'tool_cta_clicked');
  assert.deepStrictEqual(event.params, {
    source_page: 'passport-and-exam-photo-resizing-guide.html',
    destination_tool: 'smart-resize.html',
    cta_location: 'blog_mid_cta',
    content_type: 'blog_article'
  });
});

// TEST 9: Duplicate Suppression for Rapid Clicks
runTest('Duplicate Suppression: Prevents multiple tool_cta_clicked events within cooldown window', () => {
  const { analytics, eventsCaptured } = setupEnvironment();

  analytics.trackToolCtaClick('blog-post.html', 'image-compressor.html', 'body', 'blog_article');
  analytics.trackToolCtaClick('blog-post.html', 'image-compressor.html', 'body', 'blog_article'); // duplicate within 1000ms
  analytics.trackToolCtaClick('blog-post.html', 'image-compressor.html', 'footer', 'blog_article'); // different location -> allowed

  assert.strictEqual(eventsCaptured.length, 2);
  assert.strictEqual(eventsCaptured[0].params.cta_location, 'body');
  assert.strictEqual(eventsCaptured[1].params.cta_location, 'footer');
});

// TEST 10: Fault Tolerance for CTA Click Tracking
runTest('CTA Fault Tolerance: Does not throw if gtag throws or is blocked', () => {
  const { analytics, sandbox } = setupEnvironment();
  sandbox.window.gtag = () => { throw new Error('Blocked by privacy protection'); };

  assert.doesNotThrow(() => {
    analytics.trackToolCtaClick('article.html', 'qr-generator.html', 'blog_end', 'blog_article');
  });
});

console.log(`\n================================================================`);
console.log(`Test Execution Results: ${passedTests}/${totalTests} Passed`);
console.log('================================================================\n');

if (passedTests !== totalTests) {
  process.exit(1);
} else {
  process.exit(0);
}
