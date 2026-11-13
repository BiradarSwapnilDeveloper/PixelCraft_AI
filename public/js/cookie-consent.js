/**
 * PixelCraft AI - Unified GDPR, ePrivacy & Google Consent Mode v2 Manager
 * Ensures zero non-essential tracking scripts execute before explicit user consent.
 */
(function () {
  'use strict';

  const GA_ID = 'G-9EK2GY31YP';
  const ADSENSE_ID = 'ca-pub-3788374704176398';

  let trackingInjected = false;

  // Initialize dataLayer and Google Consent Mode v2 baseline synchronously
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  // Read saved consent status
  function getSavedConsent() {
    const consent = localStorage.getItem('cookieConsent');
    const legacy = localStorage.getItem('pc_consent_v1');
    if (consent === 'accepted' || legacy === 'true') return 'accepted';
    if (consent === 'rejected' || legacy === 'false') return 'rejected';
    return null;
  }

  const initialConsent = getSavedConsent();

  // Apply default Google Consent Mode v2 configuration before any tag loads
  if (initialConsent === 'accepted') {
    gtag('consent', 'default', {
      'ad_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'analytics_storage': 'granted'
    });
  } else {
    gtag('consent', 'default', {
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'analytics_storage': 'denied'
    });
  }

  function loadTracking() {
    if (trackingInjected) return;
    trackingInjected = true;

    // Update Consent Mode v2 to granted
    gtag('consent', 'update', {
      'ad_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'analytics_storage': 'granted'
    });

    // 1. Google Analytics 4 Script Injection
    if (!document.getElementById('ga-script') && !document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
      const gaScript = document.createElement('script');
      gaScript.id = 'ga-script';
      gaScript.async = true;
      gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
      document.head.appendChild(gaScript);

      gtag('js', new Date());
      gtag('config', GA_ID);
    }

    // 2. Google AdSense Script Injection
    if (!document.getElementById('adsense-script') && !document.querySelector('script[src*="pagead2.googlesyndication.com"]')) {
      const adScript = document.createElement('script');
      adScript.id = 'adsense-script';
      adScript.async = true;
      adScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_ID;
      adScript.crossOrigin = 'anonymous';
      document.head.appendChild(adScript);
    }
  }

  function removeTracking() {
    const wasActive = trackingInjected || !!document.getElementById('ga-script') || !!document.getElementById('adsense-script');
    trackingInjected = false;

    // Update Consent Mode v2 to denied immediately
    gtag('consent', 'update', {
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'analytics_storage': 'denied'
    });

    // Remove script elements from DOM where present
    const gaScript = document.getElementById('ga-script') || document.querySelector('script[src*="googletagmanager.com/gtag/js"]');
    if (gaScript && gaScript.parentNode) {
      gaScript.parentNode.removeChild(gaScript);
    }

    const adScript = document.getElementById('adsense-script') || document.querySelector('script[src*="pagead2.googlesyndication.com"]');
    if (adScript && adScript.parentNode) {
      adScript.parentNode.removeChild(adScript);
    }

    // Clear tracking cookies across path and domain scopes
    clearTrackingCookies();

    return wasActive;
  }

  function clearTrackingCookies() {
    const trackingCookies = ['_ga', '_gid', '_gat', '__gads', '__gpi', '_gac_', '_gat_gtag_'];
    const cookies = document.cookie.split(';');
    const hostname = window.location.hostname;
    const domainParts = hostname.split('.');
    const domains = ['', hostname];
    if (domainParts.length >= 2) {
      domains.push('.' + domainParts.slice(-2).join('.'));
    }
    const currentPath = (window.location && window.location.pathname) ? window.location.pathname : '/';
    const paths = ['/', currentPath];

    cookies.forEach(c => {
      const name = c.split('=')[0].trim();
      const isTracking = trackingCookies.some(tc => name === tc || name.startsWith(tc));
      if (isTracking) {
        paths.forEach(p => {
          domains.forEach(d => {
            const domainAttr = d ? '; domain=' + d : '';
            document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=' + p + domainAttr + ';';
          });
        });
      }
    });
  }

  // Detect whether the user is actively working on content or using an interactive tool
  function isUserWorkingOnContent() {
    // 1. Tool pages are sensitive to unsaved user work
    const pathStr = (window.location && window.location.pathname) ? window.location.pathname : '';
    const isToolPage = pathStr.includes('/tools/');

    // 2. Check for active files in file inputs
    const fileInputs = document.querySelectorAll('input[type="file"]');
    for (let i = 0; i < fileInputs.length; i++) {
      if (fileInputs[i].files && fileInputs[i].files.length > 0) return true;
    }

    // 3. Check for text entered into textareas
    const textareas = document.querySelectorAll('textarea');
    for (let i = 0; i < textareas.length; i++) {
      if (textareas[i].value && textareas[i].value.trim().length > 10) return true;
    }

    // 4. Check for active canvas buffers
    const canvases = document.querySelectorAll('canvas');
    for (let i = 0; i < canvases.length; i++) {
      if (canvases[i].width > 100 && canvases[i].height > 100) return true;
    }

    return isToolPage;
  }

  function unblurTools() {
    const toolsSec = document.getElementById('tools');
    if (toolsSec) {
      toolsSec.style.filter = 'none';
      toolsSec.style.pointerEvents = 'auto';
      toolsSec.style.userSelect = 'auto';
    }
  }

  function createBanner() {
    if (document.getElementById('cookie-consent-banner')) return;

    // Close settings drawer if open to keep banner accessible
    const drawer = document.getElementById('settings-drawer');
    if (drawer && drawer.classList.contains('active')) {
      drawer.classList.remove('active');
      const overlay = document.getElementById('settings-drawer-overlay');
      if (overlay) overlay.classList.remove('active');
    }

    // Inject styles if not present
    if (!document.getElementById('cookie-consent-styles')) {
      const style = document.createElement('style');
      style.id = 'cookie-consent-styles';
      style.textContent = `
        @keyframes pcSlideUp {
          from { transform: translate(-50%, 30px); opacity: 0; }
          to { transform: translate(-50%, 0); opacity: 1; }
        }
        @keyframes pcFadeOut {
          from { opacity: 1; transform: translate(-50%, 0); }
          to { opacity: 0; transform: translate(-50%, 20px); }
        }
        #cookie-consent-banner {
          position: fixed;
          bottom: 24px;
          left: 50%;
          transform: translate(-50%, 0);
          width: calc(100% - 32px);
          max-width: 660px;
          background: rgba(15, 23, 42, 0.96);
          backdrop-filter: blur(18px);
          -webkit-backdrop-filter: blur(18px);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 18px;
          padding: 22px 24px;
          z-index: 999999;
          box-shadow: 0 20px 45px rgba(0, 0, 0, 0.55), 0 0 1px rgba(255, 255, 255, 0.2);
          animation: pcSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          color: #e2e8f0;
          box-sizing: border-box;
        }
        #cookie-consent-banner h3 {
          margin: 0 0 8px 0;
          font-size: 1.15rem;
          font-weight: 700;
          color: #ffffff;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        #cookie-consent-banner p {
          margin: 0 0 18px 0;
          font-size: 0.9rem;
          line-height: 1.55;
          color: #94a3b8;
        }
        #cookie-consent-banner p a {
          color: #60a5fa;
          text-decoration: underline;
          text-underline-offset: 3px;
          transition: color 0.2s;
        }
        #cookie-consent-banner p a:hover {
          color: #93c5fd;
        }
        .pc-consent-actions {
          display: flex;
          justify-content: flex-end;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
        }
        .pc-btn-reject {
          background: rgba(255, 255, 255, 0.08);
          color: #cbd5e1;
          border: 1px solid rgba(255, 255, 255, 0.15);
          padding: 10px 20px;
          border-radius: 10px;
          font-weight: 600;
          font-size: 0.9rem;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .pc-btn-reject:hover {
          background: rgba(255, 255, 255, 0.15);
          color: #ffffff;
          border-color: rgba(255, 255, 255, 0.25);
        }
        .pc-btn-accept {
          background: linear-gradient(135deg, #2563eb, #1d4ed8);
          color: #ffffff;
          border: none;
          padding: 10px 24px;
          border-radius: 10px;
          font-weight: 600;
          font-size: 0.9rem;
          cursor: pointer;
          box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
          transition: all 0.2s ease;
        }
        .pc-btn-accept:hover {
          background: linear-gradient(135deg, #1d4ed8, #1e40af);
          box-shadow: 0 6px 20px rgba(37, 99, 235, 0.55);
          transform: translateY(-1px);
        }
        @media (max-width: 540px) {
          #cookie-consent-banner {
            bottom: 14px;
            padding: 18px 18px;
            border-radius: 14px;
          }
          .pc-consent-actions {
            flex-direction: column-reverse;
            width: 100%;
          }
          .pc-consent-actions button {
            width: 100%;
            text-align: center;
          }
        }
      `;
      document.head.appendChild(style);
    }

    const currentStatus = getSavedConsent();
    const statusNote = currentStatus ? ` (Currently: ${currentStatus === 'accepted' ? 'Accepted' : 'Rejected'})` : '';

    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Privacy and Cookie Consent');
    banner.innerHTML = `
      <h3>🍪 We Value Your Privacy${statusNote}</h3>
      <p>
        We use cookies to enhance your browsing experience, analyze site traffic, and serve relevant ads. By clicking <strong>"Accept All"</strong>, you consent to our use of cookies and acknowledge our 
        <a href="/terms-conditions.html" target="_blank">Terms</a>, 
        <a href="/privacy-policy.html" target="_blank">Privacy Policy</a>, and 
        <a href="/cookies-policy.html" target="_blank">Cookies Policy</a>.
      </p>
      <div class="pc-consent-actions">
        <button id="btn-reject-cookies" class="pc-btn-reject" type="button">Reject All</button>
        <button id="btn-accept-cookies" class="pc-btn-accept" type="button">Accept All</button>
      </div>
    `;

    document.body.appendChild(banner);

    function closeBanner() {
      banner.style.animation = 'pcFadeOut 0.3s ease forwards';
      setTimeout(() => {
        if (banner.parentNode) banner.remove();
      }, 300);
      unblurTools();
    }

    document.getElementById('btn-accept-cookies').onclick = () => {
      localStorage.setItem('cookieConsent', 'accepted');
      localStorage.setItem('pc_consent_v1', 'true');
      sessionStorage.setItem('tc_accepted', 'true');
      closeBanner();
      loadTracking();
      if (typeof showToast === 'function') {
        showToast('Cookie preferences updated: All cookies accepted.', 'success');
      }
    };

    document.getElementById('btn-reject-cookies').onclick = () => {
      const currentStored = getSavedConsent();
      const wasTrackingActive = trackingInjected || !!document.getElementById('ga-script') || !!document.getElementById('adsense-script') || (currentStored === 'accepted');

      localStorage.setItem('cookieConsent', 'rejected');
      localStorage.setItem('pc_consent_v1', 'false');
      sessionStorage.setItem('tc_accepted', 'true');
      closeBanner();
      removeTracking();

      if (wasTrackingActive) {
        if (isUserWorkingOnContent()) {
          if (typeof showToast === 'function') {
            showToast('Cookie preferences updated: Tracking disabled. Please refresh when your work is finished to completely unload scripts from memory.', 'default', 6000);
          }
        } else {
          if (typeof showToast === 'function') {
            showToast('Cookie preferences revoked. Refreshing page to cleanly purge in-memory tracking...', 'default', 2000);
          }
          setTimeout(() => {
            if (window.location && typeof window.location.reload === 'function') {
              window.location.reload();
            }
          }, 1200);
        }
      } else {
        if (typeof showToast === 'function') {
          showToast('Cookie preferences updated: Non-essential cookies rejected.', 'default');
        }
      }
    };
  }

  window.openCookieConsentBanner = createBanner;
  window.loadTrackingScripts = loadTracking;
  window.revokeCookieConsent = function () {
    const btn = document.getElementById('btn-reject-cookies');
    if (btn) btn.click();
    else {
      localStorage.setItem('cookieConsent', 'rejected');
      localStorage.setItem('pc_consent_v1', 'false');
      removeTracking();
    }
  };

  function init() {
    const current = getSavedConsent();

    if (current === 'accepted') {
      unblurTools();
      loadTracking();
    } else if (current === 'rejected') {
      unblurTools();
    } else {
      createBanner();
    }

    // Attach to any manual "Cookie Preferences" triggers
    document.querySelectorAll('.manage-consent-btn, [data-manage-consent]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        createBanner();
      });
    });

    // Global event delegation for any dynamically created triggers
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest && e.target.closest('.manage-consent-btn, [data-manage-consent], #cookie-preferences-btn, a[href="#cookie-preferences"], a[href="#manage-cookies"]');
      if (trigger) {
        e.preventDefault();
        createBanner();
      }
    });

    // Reopen banner if URL contains #manage-cookies or #cookie-preferences or manage-consent parameter
    if (window.location.hash === '#manage-cookies' || window.location.hash === '#cookie-preferences' || (window.location.search && window.location.search.includes('manage-consent=1'))) {
      createBanner();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();