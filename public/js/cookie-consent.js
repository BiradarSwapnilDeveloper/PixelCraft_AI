/**
 * PixelCraft AI - Unified GDPR & AdSense Cookie & Privacy Consent Manager
 * Consolidates all consent modals into a single, polished, non-intrusive component.
 */
(function () {
  const GA_ID = 'G-V78ZLHJLR8';
  const ADSENSE_ID = 'ca-pub-3788374704176398';

  function loadTracking() {
    // Prevent duplicate injections
    if (!document.getElementById('ga-script')) {
      const gaScript = document.createElement('script');
      gaScript.id = 'ga-script';
      gaScript.async = true;
      gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
      document.head.appendChild(gaScript);

      window.dataLayer = window.dataLayer || [];
      function gtag() { window.dataLayer.push(arguments); }
      gtag('js', new Date());
      gtag('config', GA_ID);
    }

    if (!document.getElementById('adsense-script')) {
      const adScript = document.createElement('script');
      adScript.id = 'adsense-script';
      adScript.async = true;
      adScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_ID;
      adScript.crossOrigin = 'anonymous';
      document.head.appendChild(adScript);
    }
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

    // Inject styles
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

    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Privacy and Cookie Consent');
    banner.innerHTML = `
      <h3>🍪 We Value Your Privacy</h3>
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
    };

    document.getElementById('btn-reject-cookies').onclick = () => {
      localStorage.setItem('cookieConsent', 'rejected');
      localStorage.setItem('pc_consent_v1', 'false');
      sessionStorage.setItem('tc_accepted', 'true');
      closeBanner();
    };
  }

  window.openCookieConsentBanner = createBanner;
  window.loadTrackingScripts = loadTracking;

  function init() {
    const hasAccepted = localStorage.getItem('cookieConsent') === 'accepted' || localStorage.getItem('pc_consent_v1') === 'true';
    const hasRejected = localStorage.getItem('cookieConsent') === 'rejected' || localStorage.getItem('pc_consent_v1') === 'false';

    if (hasAccepted) {
      unblurTools();
      loadTracking();
    } else if (hasRejected) {
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
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();