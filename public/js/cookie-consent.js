(function() {
  const GA_ID = 'G-V78ZLHJLR8';
  const ADSENSE_ID = 'ca-pub-3788374704176398';

  function loadTracking() {
    const gaScript = document.createElement('script');
    gaScript.async = true;
    gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(gaScript);
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', GA_ID);

    const adScript = document.createElement('script');
    adScript.async = true;
    adScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_ID;
    adScript.crossOrigin = 'anonymous';
    document.head.appendChild(adScript);
  }

  function createBanner() {
    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.style.cssText = 'position:fixed; bottom:0; left:0; width:100%; background:rgba(15, 23, 42, 0.95); backdrop-filter:blur(10px); color:#e2e8f0; padding:20px; z-index:99999; display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.1); flex-wrap:wrap; gap:15px; font-family:sans-serif;';
    banner.innerHTML = `
      <div style="flex:1; min-width:300px; font-size:0.9rem; line-height:1.5;">
        <strong>We value your privacy.</strong> We use cookies to enhance your browsing experience, serve personalized ads, and analyze our traffic. By clicking "Accept All", you consent to our use of cookies. <a href="/privacy-policy.html" style="color:#38bdf8; text-decoration:underline;">Read more</a>.
      </div>
      <div style="display:flex; gap:10px;">
        <button id="btn-reject-cookies" style="background:transparent; border:1px solid #64748b; color:#cbd5e1; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:600;">Reject All</button>
        <button id="btn-accept-cookies" style="background:#3b82f6; border:none; color:#fff; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:600;">Accept All</button>
      </div>
    `;
    document.body.appendChild(banner);

    document.getElementById('btn-accept-cookies').onclick = () => {
      localStorage.setItem('cookieConsent', 'accepted');
      banner.remove();
      loadTracking();
    };

    document.getElementById('btn-reject-cookies').onclick = () => {
      localStorage.setItem('cookieConsent', 'rejected');
      banner.remove();
    };
  }

  const consent = localStorage.getItem('cookieConsent');
  if (consent === 'accepted') {
    loadTracking();
  } else if (!consent) {
    if(document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', createBanner);
    } else {
      createBanner();
    }
  }
})();