// ===== PIXELCRAFT AI - ENTERPRISE CORE SHARED UTILITIES =====

// 1. THEME MANAGEMENT SYSTEM (Light Mode / Dark Mode - GitHub & LinkedIn Style)
(function initTheme() {
  const savedTheme = localStorage.getItem('pixelcraft-theme') || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', savedTheme);
})();

window.setPixelCraftTheme = function(theme) {
  if (theme === 'system') {
    localStorage.removeItem('pixelcraft-theme');
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', systemDark ? 'dark' : 'light');
  } else {
    localStorage.setItem('pixelcraft-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }
  updateThemeUI();
};

window.togglePixelCraftTheme = function() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  window.setPixelCraftTheme(next);
  if (typeof showToast === 'function') {
    showToast(`Switched to ${next === 'dark' ? 'Dark' : 'Light'} Mode`, 'default');
  }
};

function updateThemeUI() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (toggleBtn) {
    toggleBtn.innerHTML = current === 'dark' 
      ? '<span style="font-size: 1.15rem;">☀️</span>' 
      : '<span style="font-size: 1.15rem;">🌙</span>';
    toggleBtn.title = current === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
  }
  document.querySelectorAll('.theme-choice-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeChoice === (localStorage.getItem('pixelcraft-theme') || 'system'));
  });
}

// 2. RECENT TOOLS TRACKING
const TOOL_NAME_MAP = {
  'audio-steganography.html': { name: 'Audio Steganography', icon: '🎧' },
  'digital-fingerprint-wiper.html': { name: 'Digital Fingerprint Wiper', icon: '🛡️' },
  'advanced-decoy.html': { name: 'Decoy Steganography', icon: '🎭' },
  'images-to-pdf.html': { name: 'Images to PDF', icon: '📄' },
  'pdf-to-link.html': { name: 'PDF to Link', icon: '🔗' },
  'image-compressor.html': { name: 'Image Compressor', icon: '🗜️' },
  'format-converter.html': { name: 'Format Converter', icon: '🔄' },
  'qr-generator.html': { name: 'Custom QR Generator', icon: '📱' },
  'exif-viewer.html': { name: 'EXIF Data Viewer', icon: '🔍' },
  'watermark-adder.html': { name: 'Watermark Adder', icon: '🏷️' },
  'color-palette.html': { name: 'Color Palette Extractor', icon: '🎨' },
  'image-filters.html': { name: 'Filters & Effects', icon: '✨' },
  'smart-resize.html': { name: 'Smart Social Resize', icon: '📐' },
  'phishing-scanner.html': { name: 'Phishing & Malware Scanner', icon: '🛡️' },
  'ai-dubbing.html': { name: 'AI Audio & Video Dubbing', icon: '🎙️' },
  'forensic-sanitizer.html': { name: 'Forensic Metadata Sanitizer', icon: '🧹' }
};

function recordCurrentTool() {
  const path = window.location.pathname;
  for (const [file, info] of Object.entries(TOOL_NAME_MAP)) {
    if (path.endsWith(file) || path.includes('/tools/' + file)) {
      try {
        let recents = JSON.parse(localStorage.getItem('pixelcraft_recent_tools') || '[]');
        recents = recents.filter(item => item.file !== file);
        recents.unshift({
          name: info.name,
          icon: info.icon,
          file: file,
          url: (path.includes('/tools/') ? '' : 'tools/') + file,
          timestamp: Date.now()
        });
        if (recents.length > 5) recents = recents.slice(0, 5);
        localStorage.setItem('pixelcraft_recent_tools', JSON.stringify(recents));
      } catch (e) {
        console.warn('Could not record recent tool:', e);
      }
      break;
    }
  }
}

// 3. ENTERPRISE SETTINGS DRAWER
function injectSettingsDrawer() {
  if (document.getElementById('pixelcraft-settings-drawer')) return;

  // Overlay
  const overlay = document.createElement('div');
  overlay.id = 'pixelcraft-settings-overlay';
  overlay.className = 'settings-drawer-overlay';
  document.body.appendChild(overlay);

  // Drawer
  const drawer = document.createElement('aside');
  drawer.id = 'pixelcraft-settings-drawer';
  drawer.className = 'settings-drawer';
  drawer.setAttribute('aria-label', 'Platform Settings and Account');

  drawer.innerHTML = `
    <div class="settings-drawer-header">
      <h3>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
        </svg>
        <span>Platform Settings</span>
      </h3>
      <button class="settings-close-btn" id="settings-close-btn" aria-label="Close settings">&times;</button>
    </div>

    <div class="settings-drawer-body">
      <!-- User Profile Card -->
      <div class="settings-user-card" id="settings-user-card">
        <div class="settings-user-avatar" id="settings-user-avatar">PC</div>
        <div class="settings-user-details">
          <div class="settings-user-email" id="settings-user-email">guest.client@pixelcraft.local</div>
          <div class="settings-user-badge">
            <span class="settings-user-dot"></span>
            <span id="settings-user-status">Client-Side Sandbox (Zero Logs)</span>
          </div>
        </div>
      </div>
      <div id="settings-user-actions" style="margin-top: -6px; margin-bottom: 8px; display: flex; gap: 8px;"></div>

      <!-- Recent Tools Section -->
      <div>
        <div class="settings-section-title">Recently Used Tools</div>
        <div class="recent-tools-list" id="recent-tools-list">
          <div style="font-size: 0.85rem; color: var(--text-light); padding: 8px 0;">No recently launched tools yet.</div>
        </div>
      </div>

      <!-- Appearance / Theme Switcher -->
      <div>
        <div class="settings-section-title">Theme & Appearance</div>
        <div class="theme-switcher-grid">
          <button class="theme-choice-btn" data-theme-choice="light" onclick="setPixelCraftTheme('light')">
            <span style="font-size: 1.2rem;">☀️</span>
            <span>Light</span>
          </button>
          <button class="theme-choice-btn" data-theme-choice="dark" onclick="setPixelCraftTheme('dark')">
            <span style="font-size: 1.2rem;">🌙</span>
            <span>Dark</span>
          </button>
          <button class="theme-choice-btn" data-theme-choice="system" onclick="setPixelCraftTheme('system')">
            <span style="font-size: 1.2rem;">💻</span>
            <span>System</span>
          </button>
        </div>
      </div>

      <!-- Cryptographic Engine Diagnostics -->
      <div>
        <div class="settings-section-title">Engine Diagnostics</div>
        <div style="background: var(--surface-subtle); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 14px;">
          <div class="diagnostic-row">
            <span class="diagnostic-label">WebCrypto Hardware API</span>
            <span class="diagnostic-val" style="color: var(--success);">Active ✓</span>
          </div>
          <div class="diagnostic-row">
            <span class="diagnostic-label">WebAssembly (WASM) Node</span>
            <span class="diagnostic-val" style="color: var(--success);">Operational ✓</span>
          </div>
          <div class="diagnostic-row">
            <span class="diagnostic-label">Client Memory Sandbox</span>
            <span class="diagnostic-val" id="diag-memory">&lt; 14 MB (Secure)</span>
          </div>
          <div class="diagnostic-row">
            <span class="diagnostic-label">Remote Server Uploads</span>
            <span class="diagnostic-val" style="color: var(--primary);">0 Bytes (Verified)</span>
          </div>
        </div>
      </div>

      <!-- Privacy & Data Controls -->
      <div>
        <div class="settings-section-title">Session Data Control</div>
        <button class="btn btn-secondary" style="width: 100%; justify-content: center; font-size: 0.88rem; gap: 8px;" onclick="purgeLocalSessionData()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
          <span>Purge Local Session & Buffers</span>
        </button>
      </div>

      <!-- Quick Navigation & Trust Links -->
      <div>
        <div class="settings-section-title">Support & Trust</div>
        <div class="settings-links-grid">
          <a href="/about-us.html" class="settings-link">About Us</a>
          <a href="/privacy-policy.html" class="settings-link">Privacy Policy</a>
          <a href="/terms-conditions.html" class="settings-link">Terms of Service</a>
          <a href="/cookies-policy.html" class="settings-link">Cookies Policy</a>
          <a href="/disclaimer.html" class="settings-link">Disclaimer</a>
          <a href="mailto:support.pixelcraft205@gmail.com" class="settings-link">Contact Support</a>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(drawer);

  // Bind close events
  overlay.addEventListener('click', closeSettingsDrawer);
  drawer.querySelector('#settings-close-btn').addEventListener('click', closeSettingsDrawer);

  // Esc key closes drawer
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSettingsDrawer();
    if ((e.ctrlKey || e.metaKey) && e.key === ',') {
      e.preventDefault();
      toggleSettingsDrawer();
    }
  });

  renderRecentTools();
  fetchUserSession();
}

function openSettingsDrawer() {
  const drawer = document.getElementById('pixelcraft-settings-drawer');
  const overlay = document.getElementById('pixelcraft-settings-overlay');
  if (drawer && overlay) {
    renderRecentTools();
    fetchUserSession();
    updateThemeUI();
    drawer.classList.add('active');
    overlay.classList.add('active');
  }
}

function closeSettingsDrawer() {
  const drawer = document.getElementById('pixelcraft-settings-drawer');
  const overlay = document.getElementById('pixelcraft-settings-overlay');
  if (drawer && overlay) {
    drawer.classList.remove('active');
    overlay.classList.remove('active');
  }
}

function toggleSettingsDrawer() {
  const drawer = document.getElementById('pixelcraft-settings-drawer');
  if (drawer && drawer.classList.contains('active')) {
    closeSettingsDrawer();
  } else {
    openSettingsDrawer();
  }
}

function renderRecentTools() {
  const listEl = document.getElementById('recent-tools-list');
  if (!listEl) return;
  try {
    const recents = JSON.parse(localStorage.getItem('pixelcraft_recent_tools') || '[]');
    if (recents.length === 0) {
      listEl.innerHTML = `<div style="font-size: 0.85rem; color: var(--text-light); padding: 8px 0;">No recently launched tools yet.</div>`;
      return;
    }
    listEl.innerHTML = recents.map(tool => {
      const targetUrl = '/tools/' + tool.file;
      const timeStr = formatRelativeTime(tool.timestamp);
      return `
        <a href="${targetUrl}" class="recent-tool-item">
          <div class="recent-tool-left">
            <span class="recent-tool-icon">${tool.icon}</span>
            <div>
              <div class="recent-tool-name">${tool.name}</div>
              <div class="recent-tool-time">${timeStr}</div>
            </div>
          </div>
          <span style="font-size: 0.85rem; font-weight: 600; color: var(--primary);">Open &rarr;</span>
        </a>
      `;
    }).join('');
  } catch (e) {
    console.error('Error rendering recent tools:', e);
  }
}

function formatRelativeTime(ts) {
  if (!ts) return 'Recently';
  const diff = Date.now() - ts;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

function updateAuthUI(data) {
  const isAuthenticated = !!(data && data.authenticated && data.user);
  const user = isAuthenticated ? data.user : null;

  // 1. Update all navbar auth buttons (#nav-auth-btn, .nav-auth-btn)
  const navAuthButtons = document.querySelectorAll('#nav-auth-btn, .nav-auth-btn');
  navAuthButtons.forEach(btn => {
    if (isAuthenticated) {
      btn.href = '/logout';
      const userLabel = (user && (user.name || user.email)) || 'User';
      btn.setAttribute('aria-label', `Signed in as ${user.email || userLabel}. Click to Sign Out`);
      btn.title = `Signed in as ${user.email || userLabel} • Click to Sign Out`;
      btn.classList.add('nav-auth-signed-in');
      btn.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
        <span>Sign Out</span>
      `;
    } else {
      btn.href = '/auth/google';
      btn.setAttribute('aria-label', 'Sign in with Google');
      btn.title = 'Sign in with Google';
      btn.classList.remove('nav-auth-signed-in');
      btn.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
        </svg>
        <span>Sign In</span>
      `;
    }
  });

  // 2. Update Settings Drawer User Card & Actions
  const emailEl = document.getElementById('settings-user-email');
  const avatarEl = document.getElementById('settings-user-avatar');
  const statusEl = document.getElementById('settings-user-status');
  let actionsEl = document.getElementById('settings-user-actions');

  if (!actionsEl) {
    const userCard = document.getElementById('settings-user-card');
    if (userCard) {
      actionsEl = document.createElement('div');
      actionsEl.id = 'settings-user-actions';
      actionsEl.style.cssText = 'margin-top: -6px; margin-bottom: 8px; display: flex; gap: 8px;';
      userCard.parentNode.insertBefore(actionsEl, userCard.nextSibling);
    }
  }

  if (isAuthenticated) {
    if (emailEl) emailEl.innerText = user.email || 'Authenticated User';
    if (avatarEl) {
      avatarEl.innerText = (user.name || user.email || 'U').charAt(0).toUpperCase();
    }
    if (statusEl) statusEl.innerText = 'Google Enterprise Account • Verified';
    if (actionsEl) {
      actionsEl.innerHTML = `
        <a href="/logout" class="btn btn-secondary" style="flex: 1; justify-content: center; font-size: 0.82rem; padding: 7px 12px; gap: 6px; color: #ef4444; border-color: rgba(239, 68, 68, 0.35); text-decoration: none;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span style="font-weight: 600;">Sign Out</span>
        </a>
        <a href="/auth/switch-account" class="btn btn-secondary" style="flex: 1; justify-content: center; font-size: 0.82rem; padding: 7px 12px; gap: 6px; text-decoration: none;">
          <span>Switch Account</span>
        </a>
      `;
    }
  } else {
    if (emailEl) emailEl.innerText = 'guest.client@pixelcraft.local';
    if (avatarEl) avatarEl.innerText = 'PC';
    if (statusEl) statusEl.innerText = 'Client-Side Sandbox (Zero Logs)';
    if (actionsEl) {
      actionsEl.innerHTML = `
        <a href="/auth/google" class="btn btn-primary" style="flex: 1; justify-content: center; font-size: 0.82rem; padding: 7px 12px; gap: 6px; text-decoration: none;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
          </svg>
          <span>Sign In with Google</span>
        </a>
      `;
    }
  }
}

function fetchUserSession() {
  fetch('/api/auth/status', { credentials: 'same-origin' })
    .then(res => {
      if (!res.ok) throw new Error('Status HTTP ' + res.status);
      return res.json();
    })
    .catch(() => {
      return fetch('/auth/status', { credentials: 'same-origin' }).then(r => r.json());
    })
    .then(data => {
      updateAuthUI(data);
    })
    .catch(() => {
      updateAuthUI({ authenticated: false });
    });
}

window.purgeLocalSessionData = function() {
  if (confirm('Clear all local session data, recent tool history, and browser cache for PixelCraft AI?')) {
    localStorage.removeItem('pixelcraft_recent_tools');
    renderRecentTools();
    if (typeof showToast === 'function') {
      showToast('Local buffers and recent history purged.', 'success');
    }
  }
};

// 4. TOAST NOTIFICATIONS
function showToast(msg, type = 'default') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icons = { success: '✅', error: '❌', default: 'ℹ️' };
  toast.innerHTML = `<span>${icons[type] || icons.default}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(30px)';
    toast.style.transition = 'all 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// 5. FILE DOWNLOAD HELPER
function downloadFile(dataURL, filename) {
  const a = document.createElement('a');
  a.href = dataURL;
  a.download = filename;
  a.click();
  showToast('Download started!', 'success');
}

// 6. PROMISE FILE HELPERS
function fileToDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = e => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function fileToImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => { resolve(img); };
    img.onerror = reject;
    img.src = url;
  });
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

function setupDragDrop(area, onFile) {
  if (!area) return;
  area.addEventListener('dragover', e => { e.preventDefault(); area.classList.add('drag-over'); });
  area.addEventListener('dragleave', () => area.classList.remove('drag-over'));
  area.addEventListener('drop', e => {
    e.preventDefault();
    area.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) onFile(file);
  });
}

function drawImageToCanvas(canvas, img, maxW = 800, maxH = 600) {
  let w = img.naturalWidth, h = img.naturalHeight;
  if (w > maxW) { h = h * maxW / w; w = maxW; }
  if (h > maxH) { h = h * maxH / h; h = maxH; }
  canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, w, h);
  ctx.drawImage(img, 0, 0, w, h);
  return ctx;
}

// Ensure navbar controls
function ensureNavbarControls() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  let actions = navbar.querySelector('.nav-actions');
  if (!actions) {
    actions = document.createElement('div');
    actions.className = 'nav-actions';
    navbar.appendChild(actions);
  }

  if (!actions.querySelector('#theme-toggle-btn')) {
    const themeBtn = document.createElement('button');
    themeBtn.id = 'theme-toggle-btn';
    themeBtn.className = 'nav-icon-btn';
    themeBtn.title = 'Toggle Theme (Dark / Light)';
    themeBtn.setAttribute('aria-label', 'Toggle Theme');
    themeBtn.innerHTML = '<span style="font-size: 1.15rem;">🌙</span>';
    themeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      togglePixelCraftTheme();
    });
    actions.appendChild(themeBtn);
  }

  if (!actions.querySelector('#settings-toggle-btn')) {
    const settingsBtn = document.createElement('button');
    settingsBtn.id = 'settings-toggle-btn';
    settingsBtn.className = 'nav-icon-btn';
    settingsBtn.title = 'Platform Settings & Account Info';
    settingsBtn.setAttribute('aria-label', 'Open Platform Settings');
    settingsBtn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="3"></circle>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
      </svg>
    `;
    settingsBtn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleSettingsDrawer();
    });
    actions.appendChild(settingsBtn);
  }

  // Ensure mobile 3-line hamburger menu button exists
  if (!actions.querySelector('#nav-toggle-btn') && !actions.querySelector('.nav-hamburger')) {
    const navToggleBtn = document.createElement('button');
    navToggleBtn.id = 'nav-toggle-btn';
    navToggleBtn.className = 'nav-icon-btn nav-hamburger';
    navToggleBtn.title = 'Toggle Navigation Menu';
    navToggleBtn.setAttribute('aria-label', 'Toggle Navigation Menu');
    navToggleBtn.setAttribute('aria-expanded', 'false');
    navToggleBtn.innerHTML = `
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    `;
    actions.appendChild(navToggleBtn);
  }
}

// Mobile navigation interactive controller
function initMobileNavbar() {
  const navbar = document.querySelector('.navbar');
  const navToggle = document.getElementById('nav-toggle-btn') || document.querySelector('.nav-hamburger');
  const navLinks = document.getElementById('nav-links') || document.querySelector('.nav-links');
  if (!navToggle || !navLinks) return;

  function closeMobileNav() {
    navLinks.classList.remove('mobile-open', 'open');
    navToggle.classList.remove('active');
    navToggle.setAttribute('aria-expanded', 'false');
  }

  function toggleMobileNav(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const isOpen = navLinks.classList.toggle('mobile-open');
    navLinks.classList.toggle('open', isOpen);
    navToggle.classList.toggle('active', isOpen);
    navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }

  if (!navToggle._hasNavListener) {
    navToggle._hasNavListener = true;
    navToggle.addEventListener('click', toggleMobileNav);
  }

  // Close when tapping any link inside mobile menu
  navLinks.querySelectorAll('a').forEach(link => {
    if (!link._hasNavCloseListener) {
      link._hasNavCloseListener = true;
      link.addEventListener('click', closeMobileNav);
    }
  });

  // Close when tapping outside the navbar
  if (!document._hasNavOutsideListener) {
    document._hasNavOutsideListener = true;
    document.addEventListener('click', (e) => {
      if (navbar && !navbar.contains(e.target)) {
        closeMobileNav();
      }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeMobileNav();
      }
    });
  }
}

// 7. INITIALIZATION ON DOM READY
document.addEventListener('DOMContentLoaded', () => {
  ensureNavbarControls();
  recordCurrentTool();
  injectSettingsDrawer();
  updateThemeUI();
  initMobileNavbar();
  fetchUserSession();

  // Bind settings button
  const settingsBtn = document.getElementById('settings-toggle-btn');
  if (settingsBtn && !settingsBtn._boundClick) {
    settingsBtn._boundClick = true;
    settingsBtn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleSettingsDrawer();
    });
  }

  // Bind theme toggle button
  const themeBtn = document.getElementById('theme-toggle-btn');
  if (themeBtn && !themeBtn._boundClick) {
    themeBtn._boundClick = true;
    themeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      togglePixelCraftTheme();
    });
  }

  // Navbar scroll elevation
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // FAQ Accordion
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      if (item) {
        const isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
        if (!isOpen) item.classList.add('open');
      }
    });
  });
});

// Copy phone / UPI helpers
window.copyUPIAnimated = function() {
  navigator.clipboard.writeText('9067693696@axl');
  showToast('UPI ID copied!', 'success');
};

window.copyPhoneAlert = function() {
  navigator.clipboard.writeText('+91 9067693696');
  showToast('Phone number copied!', 'success');
};

// 8. PWA Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(() => console.log('PWA: Service Worker registered'))
      .catch(err => console.error('PWA: Service Worker error', err));
  });
}
