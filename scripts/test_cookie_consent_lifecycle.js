const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('🧪 Running PixelCraft AI Cookie Consent Automated Verification Suite...\n');

const cookieConsentPath = path.join(__dirname, '..', 'public', 'js', 'cookie-consent.js');
const cookieConsentCode = fs.readFileSync(cookieConsentPath, 'utf8');

// Helper to create a realistic mock browser environment
function createMockDOM(initialStorage = {}) {
  const storage = { ...initialStorage };
  const cookies = {};
  
  const mockLocalStorage = {
    getItem: (k) => (k in storage ? storage[k] : null),
    setItem: (k, v) => { storage[k] = String(v); },
    removeItem: (k) => { delete storage[k]; },
    clear: () => { Object.keys(storage).forEach(k => delete storage[k]); }
  };

  const mockSessionStorage = {
    getItem: (k) => (k in storage ? storage[k] : null),
    setItem: (k, v) => { storage[k] = String(v); },
    removeItem: (k) => { delete storage[k]; }
  };

  const elements = new Map();
  const listeners = {};

  class MockElement {
    constructor(tag) {
      this.tagName = tag.toUpperCase();
      this.id = '';
      this.className = '';
      this.attributes = {};
      this.children = [];
      this.parentNode = null;
      this._innerHTML = '';
      this.textContent = '';
      this.style = {};
      this._onclick = null;
    }

    get innerHTML() {
      return this._innerHTML || '';
    }

    set innerHTML(val) {
      this._innerHTML = val;
      const regex = /<([a-z0-9]+)[^>]*id=["']([^"']+)["'][^>]*>/gi;
      let match;
      while ((match = regex.exec(val)) !== null) {
        const tag = match[1];
        const id = match[2];
        const child = new MockElement(tag);
        child.id = id;
        child.parentNode = this;
        this.children.push(child);
        elements.set(id, child);
      }
    }

    setAttribute(k, v) { this.attributes[k] = String(v); }
    getAttribute(k) { return this.attributes[k] || null; }
    hasAttribute(k) { return k in this.attributes; }

    appendChild(child) {
      child.parentNode = this;
      this.children.push(child);
      if (child.id) elements.set(child.id, child);
      return child;
    }

    removeChild(child) {
      const idx = this.children.indexOf(child);
      if (idx !== -1) {
        this.children.splice(idx, 1);
        child.parentNode = null;
        if (child.id) elements.delete(child.id);
      }
      return child;
    }

    remove() {
      if (this.parentNode) {
        this.parentNode.removeChild(this);
      }
    }

    addEventListener(event, fn) {
      listeners[event] = listeners[event] || [];
      listeners[event].push({ target: this, fn });
    }

    set onclick(fn) { this._onclick = fn; }
    get onclick() { return this._onclick; }

    click() {
      if (this._onclick) this._onclick({ target: this, preventDefault: () => {} });
      if (listeners['click']) {
        listeners['click'].forEach(l => {
          if (l.target === this) l.fn({ target: this, preventDefault: () => {} });
        });
      }
    }

    closest(sel) {
      if (sel.includes('.manage-consent-btn') && this.className.includes('manage-consent-btn')) return this;
      return null;
    }
  }

  const documentHead = new MockElement('head');
  const documentBody = new MockElement('body');

  const mockDocument = {
    head: documentHead,
    body: documentBody,
    readyState: 'complete',
    createElement: (tag) => new MockElement(tag),
    getElementById: (id) => elements.get(id) || null,
    querySelector: (sel) => {
      for (const el of elements.values()) {
        if (sel.startsWith('#') && el.id === sel.slice(1)) return el;
        if (sel.includes('googletagmanager') && el.src && el.src.includes('googletagmanager')) return el;
        if (sel.includes('pagead2') && el.src && el.src.includes('pagead2')) return el;
      }
      return null;
    },
    querySelectorAll: (sel) => {
      const found = [];
      for (const el of elements.values()) {
        if (sel.includes('.manage-consent-btn') && el.className.includes('manage-consent-btn')) {
          found.push(el);
        }
      }
      return found;
    },
    addEventListener: (event, fn) => {
      listeners[event] = listeners[event] || [];
      listeners[event].push({ target: 'document', fn });
    },
    dispatchEvent: (event, data = {}) => {
      if (listeners[event]) {
        listeners[event].forEach(l => l.fn(data));
      }
    },
    get cookie() {
      return Object.entries(cookies).map(([k, v]) => `${k}=${v}`).join('; ');
    },
    set cookie(val) {
      const parts = val.split(';')[0].split('=');
      const k = parts[0].trim();
      const v = parts.slice(1).join('=').trim();
      if (val.includes('expires=Thu, 01 Jan 1970')) {
        delete cookies[k];
      } else {
        cookies[k] = v;
      }
    }
  };

  const mockWindow = {
    dataLayer: [],
    location: { hostname: 'pixelcraftaitools.com', hash: '', search: '' },
    localStorage: mockLocalStorage,
    sessionStorage: mockSessionStorage,
    document: mockDocument
  };

  return { mockWindow, mockDocument, mockLocalStorage, elements, listeners };
}

function runScript(mockEnv) {
  const fn = new Function('window', 'document', 'localStorage', 'sessionStorage', cookieConsentCode);
  fn(mockEnv.mockWindow, mockEnv.mockDocument, mockEnv.mockLocalStorage, mockEnv.mockWindow.sessionStorage);
}

let passed = 0;
let total = 0;

function runTest(name, fn) {
  total++;
  try {
    fn();
    console.log(`  ✅ [PASS] ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ❌ [FAIL] ${name}:`, err.message);
  }
}

// -------------------------------------------------------------
// TEST 1: First-time visitor (no tracking scripts before consent)
// -------------------------------------------------------------
runTest('Scenario 1: First-time visitor - Zero tracking scripts load before consent choice', () => {
  const env = createMockDOM();
  runScript(env);

  // Assert banner is rendered
  const banner = env.elements.get('cookie-consent-banner');
  assert.ok(banner, 'Banner must be rendered for first-time visitor');

  // Assert zero tracking scripts loaded
  const gaScript = env.elements.get('ga-script');
  const adsScript = env.elements.get('adsense-script');
  assert.strictEqual(gaScript, undefined, 'GA script must NOT be loaded for first-time visitor');
  assert.strictEqual(adsScript, undefined, 'AdSense script must NOT be loaded for first-time visitor');

  // Assert default Consent Mode v2 denies storage
  const consentCall = env.mockWindow.dataLayer.find(args => args[0] === 'consent' && args[1] === 'default');
  assert.ok(consentCall, 'Default consent state must be configured');
  assert.strictEqual(consentCall[2].analytics_storage, 'denied', 'analytics_storage must default to denied');
  assert.strictEqual(consentCall[2].ad_storage, 'denied', 'ad_storage must default to denied');
});

// -------------------------------------------------------------
// TEST 2: Accept All action
// -------------------------------------------------------------
runTest('Scenario 2: Accept All - Appropriate tracking scripts load and consent updates to granted', () => {
  const env = createMockDOM();
  runScript(env);

  const acceptBtn = env.elements.get('btn-accept-cookies');
  assert.ok(acceptBtn, 'Accept All button must exist in banner');

  // Click accept
  acceptBtn.click();

  // Assert localStorage
  assert.strictEqual(env.mockLocalStorage.getItem('cookieConsent'), 'accepted', 'cookieConsent must be saved as accepted');
  assert.strictEqual(env.mockLocalStorage.getItem('pc_consent_v1'), 'true', 'pc_consent_v1 must be saved as true');

  // Assert tracking scripts injected
  const gaScript = env.elements.get('ga-script');
  const adsScript = env.elements.get('adsense-script');
  assert.ok(gaScript, 'GA script must be injected after acceptance');
  assert.ok(adsScript, 'AdSense script must be injected after acceptance');
  assert.ok(gaScript.src.includes('G-9EK2GY31YP'), 'GA script must contain correct GA ID');
  assert.ok(adsScript.src.includes('ca-pub-3788374704176398'), 'AdSense script must contain correct publisher ID');

  // Assert Consent Mode update
  const updateCall = env.mockWindow.dataLayer.find(args => args[0] === 'consent' && args[1] === 'update');
  assert.ok(updateCall, 'Consent update must be dispatched');
  assert.strictEqual(updateCall[2].analytics_storage, 'granted', 'analytics_storage must be granted');
  assert.strictEqual(updateCall[2].ad_storage, 'granted', 'ad_storage must be granted');
});

// -------------------------------------------------------------
// TEST 3: Reject All action
// -------------------------------------------------------------
runTest('Scenario 3: Reject All - Non-essential scripts remain strictly blocked', () => {
  const env = createMockDOM();
  runScript(env);

  const rejectBtn = env.elements.get('btn-reject-cookies');
  assert.ok(rejectBtn, 'Reject All button must exist in banner');

  // Click reject
  rejectBtn.click();

  // Assert localStorage
  assert.strictEqual(env.mockLocalStorage.getItem('cookieConsent'), 'rejected', 'cookieConsent must be saved as rejected');
  assert.strictEqual(env.mockLocalStorage.getItem('pc_consent_v1'), 'false', 'pc_consent_v1 must be saved as false');

  // Assert tracking scripts remain blocked
  const gaScript = env.elements.get('ga-script');
  const adsScript = env.elements.get('adsense-script');
  assert.strictEqual(gaScript, undefined, 'GA script must NOT be injected on rejection');
  assert.strictEqual(adsScript, undefined, 'AdSense script must NOT be injected on rejection');

  // Assert Consent Mode update
  const updateCall = env.mockWindow.dataLayer.find(args => args[0] === 'consent' && args[1] === 'update');
  assert.ok(updateCall, 'Consent update must be dispatched');
  assert.strictEqual(updateCall[2].analytics_storage, 'denied', 'analytics_storage must be denied');
  assert.strictEqual(updateCall[2].ad_storage, 'denied', 'ad_storage must be denied');
});

// -------------------------------------------------------------
// TEST 4: Refresh after accepting
// -------------------------------------------------------------
runTest('Scenario 4: Refresh after accepting - Saved preference automatically loads scripts with zero banner', () => {
  const env = createMockDOM({ cookieConsent: 'accepted', pc_consent_v1: 'true' });
  runScript(env);

  // Assert banner is NOT rendered
  const banner = env.elements.get('cookie-consent-banner');
  assert.strictEqual(banner, undefined, 'Banner must NOT be rendered when user has already accepted');

  // Assert scripts automatically loaded
  const gaScript = env.elements.get('ga-script');
  const adsScript = env.elements.get('adsense-script');
  assert.ok(gaScript, 'GA script must load on refresh for accepted user');
  assert.ok(adsScript, 'AdSense script must load on refresh for accepted user');

  // Assert default consent was initialized as granted
  const consentCall = env.mockWindow.dataLayer.find(args => args[0] === 'consent' && args[1] === 'default');
  assert.strictEqual(consentCall[2].analytics_storage, 'granted');
});

// -------------------------------------------------------------
// TEST 5: Refresh after rejecting
// -------------------------------------------------------------
runTest('Scenario 5: Refresh after rejecting - Saved preference blocks scripts with zero banner', () => {
  const env = createMockDOM({ cookieConsent: 'rejected', pc_consent_v1: 'false' });
  runScript(env);

  // Assert banner is NOT rendered
  const banner = env.elements.get('cookie-consent-banner');
  assert.strictEqual(banner, undefined, 'Banner must NOT be rendered when user has already rejected');

  // Assert scripts remain blocked
  const gaScript = env.elements.get('ga-script');
  const adsScript = env.elements.get('adsense-script');
  assert.strictEqual(gaScript, undefined, 'GA script must NOT load for rejected user');
  assert.strictEqual(adsScript, undefined, 'AdSense script must NOT load for rejected user');
});

// -------------------------------------------------------------
// TEST 6: Multi-page navigation (idempotency & no duplicate scripts)
// -------------------------------------------------------------
runTest('Scenario 6: Navigation & Idempotency - Calling loadTracking multiple times never injects duplicate scripts', () => {
  const env = createMockDOM({ cookieConsent: 'accepted', pc_consent_v1: 'true' });
  runScript(env);

  // Count scripts in head
  const scriptsBefore = env.mockDocument.head.children.filter(c => c.tagName === 'SCRIPT');
  assert.strictEqual(scriptsBefore.length, 2, 'Exactly 2 scripts in head (GA + AdSense)');

  // Try calling loadTracking again
  env.mockWindow.loadTrackingScripts();
  env.mockWindow.loadTrackingScripts();

  const scriptsAfter = env.mockDocument.head.children.filter(c => c.tagName === 'SCRIPT');
  assert.strictEqual(scriptsAfter.length, 2, 'Still exactly 2 scripts in head (no duplicates injected)');
});

// -------------------------------------------------------------
// TEST 7: Cookie Preferences Reopen & Revocation Flow
// -------------------------------------------------------------
runTest('Scenario 7: Cookie Preferences Reopen & Revocation Flow', () => {
  const env = createMockDOM({ cookieConsent: 'accepted', pc_consent_v1: 'true' });
  runScript(env);

  // Add dummy tracking cookies
  env.mockDocument.cookie = '_ga=GA1.1.12345';
  env.mockDocument.cookie = '__gads=ID=67890';
  assert.ok(env.mockDocument.cookie.includes('_ga'), 'Tracking cookie should exist');

  // Assert banner is closed initially
  assert.strictEqual(env.elements.get('cookie-consent-banner'), undefined);

  // Simulate user clicking Cookie Preferences trigger (.manage-consent-btn)
  const prefBtn = env.mockDocument.createElement('button');
  prefBtn.className = 'manage-consent-btn';
  env.mockDocument.body.appendChild(prefBtn);

  // Trigger click via event delegation
  if (env.listeners['click']) {
    env.listeners['click'].forEach(l => {
      l.fn({ target: prefBtn, preventDefault: () => {} });
    });
  }

  // Assert banner reopens
  const banner = env.elements.get('cookie-consent-banner');
  assert.ok(banner, 'Banner must reopen when Cookie Preferences is clicked');

  // Now simulate user choosing "Reject All" to revoke consent
  const rejectBtn = env.elements.get('btn-reject-cookies');
  rejectBtn.click();

  // Assert preference updated to rejected
  assert.strictEqual(env.mockLocalStorage.getItem('cookieConsent'), 'rejected');
  assert.strictEqual(env.mockLocalStorage.getItem('pc_consent_v1'), 'false');

  // Assert tracking scripts were purged from DOM
  assert.strictEqual(env.elements.get('ga-script'), undefined, 'GA script should be purged upon revocation');
  assert.strictEqual(env.elements.get('adsense-script'), undefined, 'AdSense script should be purged upon revocation');

  // Assert tracking cookies cleared
  assert.ok(!env.mockDocument.cookie.includes('_ga'), 'Google Analytics cookie must be deleted');
  assert.ok(!env.mockDocument.cookie.includes('__gads'), 'Google AdSense cookie must be deleted');
});

// -------------------------------------------------------------
// TEST 8: Codebase HTML Audit (All public HTML files)
// -------------------------------------------------------------
runTest('Scenario 8: HTML Codebase Audit - All public HTML files contain zero premature tracking scripts', () => {
  const publicDir = path.join(__dirname, '..', 'public');
  function scanDir(dir) {
    let files = [];
    fs.readdirSync(dir).forEach(f => {
      const p = path.join(dir, f);
      if (fs.statSync(p).isDirectory()) files = files.concat(scanDir(p));
      else if (f.endsWith('.html') && !f.endsWith('.bak')) files.push(p);
    });
    return files;
  }

  const htmlFiles = scanDir(publicDir);
  assert.ok(htmlFiles.length >= 38, `Must find at least 38 public HTML files, found ${htmlFiles.length}`);

  htmlFiles.forEach(file => {
    const content = fs.readFileSync(file, 'utf8');
    const rel = path.relative(publicDir, file);
    assert.ok(!content.includes('googletagmanager.com/gtag/js'), `${rel} must not contain direct GA script tag`);
    assert.ok(!content.includes('pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'), `${rel} must not contain direct AdSense script tag`);
  });
});

console.log(`\n================================================================`);
console.log(`📊 Test Summary: ${passed}/${total} Scenarios Passed.`);
console.log(`================================================================\n`);

if (passed === total) {
  process.exit(0);
} else {
  process.exit(1);
}
