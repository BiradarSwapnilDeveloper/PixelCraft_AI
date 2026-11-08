/**
 * ============================================================================
 * PIXELCRAFT AI — CELESTIAL FANTASY DIWALI ENGINE (ANOTHER DIMENSION EDITION)
 * ============================================================================
 * Features:
 * - Hyperspace Cosmic Starfield & Nebula Glow
 * - Supernova Multi-Stage Fireworks with Volumetric Shockwaves & Willow Trails
 * - Ethereal Floating Sacred Diya Relic with 4-Layer Plasma Flame & Rising Sparks
 * - Cinematic Symphonic Web Audio Synthesis (Temple Bells, Drone, Chimes, Boom)
 * - Interactive Celestial Particle Trail & Tap-to-Detonate Supernova
 * - Dimensional Stargate Warp Exit Transition (~3.2s)
 */

(function () {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCelestialDiwali);
  } else {
    initCelestialDiwali();
  }

  function initCelestialDiwali() {
    if (document.getElementById('diwali-splash')) return;

    // Create Cosmic Overlay Element
    const splash = document.createElement('div');
    splash.id = 'diwali-splash';
    splash.innerHTML = `
      <canvas id="diwali-canvas"></canvas>

      <!-- Sacred Astral Geometry & Dimensional Portal Rings -->
      <div class="diwali-portal-wrap">
        <div class="portal-nebula-pulse"></div>
        <div class="portal-ring-outer"></div>
        <div class="portal-ring-mid"></div>
        <div class="god-rays"></div>
      </div>

      <!-- Audio Indicator Pill -->
      <div class="diwali-sound-pill" id="diwali-sound-btn" title="Toggle Festive Sound">
        <span>✨</span> Celestial Symphony Active
      </div>

      <!-- Central Floating Divine Sanctum -->
      <div class="diwali-content-card">
        <!-- Floating Divine Sacred Diya Relic -->
        <div class="diya-container">
          <div class="diya-sacred-aura"></div>
          <svg class="diya-svg" viewBox="0 0 200 160" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="astralGold" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#fff8db"/>
                <stop offset="25%" stop-color="#ffd700"/>
                <stop offset="50%" stop-color="#f59e0b"/>
                <stop offset="75%" stop-color="#b45309"/>
                <stop offset="100%" stop-color="#451a03"/>
              </linearGradient>
              <linearGradient id="divineFlameOuter" x1="50%" y1="0%" x2="50%" y2="100%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="15%" stop-color="#fde047"/>
                <stop offset="45%" stop-color="#ff6b00"/>
                <stop offset="80%" stop-color="#dc2626"/>
                <stop offset="100%" stop-color="#991b1b"/>
              </linearGradient>
              <radialGradient id="plasmaStarCore" cx="50%" cy="75%" r="50%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="40%" stop-color="#38bdf8"/>
                <stop offset="75%" stop-color="#818cf8"/>
                <stop offset="100%" stop-color="transparent"/>
              </radialGradient>
              <linearGradient id="gemRuby" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ff758f"/>
                <stop offset="100%" stop-color="#be123c"/>
              </linearGradient>
              <linearGradient id="gemEmerald" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#6ee7b7"/>
                <stop offset="100%" stop-color="#047857"/>
              </linearGradient>
            </defs>

            <!-- Multidimensional Divine Flame -->
            <g class="flame-divine-group">
              <!-- Radiant Outer Solar Flare -->
              <path d="M100 8 C84 32 68 55 70 82 C72 110 88 120 100 120 C112 120 128 110 130 82 C132 55 116 32 100 8 Z" fill="url(#divineFlameOuter)" filter="drop-shadow(0 0 16px rgba(255, 140, 0, 0.95))"/>
              <!-- Golden Mid-Mantle -->
              <path d="M100 28 C90 46 80 62 82 85 C84 104 92 112 100 112 C108 112 116 104 118 85 C120 62 110 46 100 28 Z" fill="#fff9c4"/>
              <!-- White-Hot Plasma Core -->
              <ellipse cx="100" cy="102" rx="9" ry="14" fill="url(#plasmaStarCore)"/>
              <!-- Sacred Wick -->
              <line x1="100" y1="106" x2="100" y2="122" stroke="#1f0902" stroke-width="3" stroke-linecap="round"/>
            </g>

            <!-- Ornate Sacred Brass / Celestial Gold Diya Body -->
            <path d="M26 112 C38 98 62 96 100 96 C138 96 162 98 174 112 C184 122 174 142 146 149 C122 155 78 155 54 149 C26 142 16 122 26 112 Z" fill="url(#astralGold)" stroke="#fef08a" stroke-width="1.6"/>
            <!-- Filigree Rim Engraving -->
            <path d="M34 112 Q100 124 166 112" stroke="#fffbeb" stroke-width="2.5" stroke-linecap="round" fill="none" opacity="0.9"/>
            
            <!-- Inset Cosmic Gemstones -->
            <circle cx="60" cy="122" r="3" fill="url(#gemRuby)" stroke="#ffd700" stroke-width="0.8"/>
            <circle cx="100" cy="128" r="4.5" fill="url(#gemEmerald)" stroke="#ffd700" stroke-width="1"/>
            <circle cx="140" cy="122" r="3" fill="url(#gemRuby)" stroke="#ffd700" stroke-width="0.8"/>

            <!-- Ornate Lotus Base Petals -->
            <ellipse cx="100" cy="151" rx="35" ry="6.5" fill="#451a03" stroke="#b45309" stroke-width="1.2"/>
            <path d="M80 151 Q100 157 120 151" stroke="#f59e0b" stroke-width="1.5" fill="none"/>
          </svg>
        </div>

        <!-- Sacred Sanskrit/Hindi Inscription -->
        <div class="diwali-sanskrit-title">॥ दिव्य शुभ दीपावली ॥</div>

        <!-- 3D Liquid Gold Cinematic Headline -->
        <h1 class="diwali-main-title">Happy Diwali</h1>

        <!-- Celestial Blessing -->
        <div class="diwali-tagline">
          Enter the dimension of eternal light, divine abundance, and boundless cosmic joy.
        </div>

        <!-- Iridescent Badge -->
        <div class="diwali-badge">
          <span>✨</span> PIXELCRAFT AI • CELESTIAL CELEBRATION <span>✨</span>
        </div>
      </div>

      <!-- Action Hints & Skip Portal -->
      <div class="diwali-actions">
        <div class="diwali-hint">
          <span>🌌</span> Move cursor or tap to summon supernovas
        </div>
        <button class="diwali-skip-btn" id="diwali-skip-btn">Skip Portal ✕</button>
      </div>
    `;

    document.body.prepend(splash);

    const canvas = document.getElementById('diwali-canvas');
    const ctx = canvas.getContext('2d');

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    });

    // ========================================================
    // CINEMATIC SYMPHONIC WEB AUDIO SYNTHESIS
    // ========================================================
    let audioCtx = null;
    let hasPlayedAudio = false;

    function playCelestialSymphony() {
      if (hasPlayedAudio) return;
      hasPlayedAudio = true;

      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        audioCtx = new AudioContext();

        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
        }

        const now = audioCtx.currentTime;

        // 1. Deep Celestial Drone / Sacred Om Resonance (108Hz)
        const droneOsc = audioCtx.createOscillator();
        const droneGain = audioCtx.createGain();
        const droneFilter = audioCtx.createBiquadFilter();

        droneOsc.type = 'sawtooth';
        droneOsc.frequency.setValueAtTime(108, now); // Sacred 108Hz harmonic
        droneFilter.type = 'lowpass';
        droneFilter.frequency.setValueAtTime(180, now);
        droneFilter.frequency.exponentialRampToValueAtTime(320, now + 1.2);

        droneGain.gain.setValueAtTime(0.0001, now);
        droneGain.gain.exponentialRampToValueAtTime(0.22, now + 0.3);
        droneGain.gain.exponentialRampToValueAtTime(0.0001, now + 3.2);

        droneOsc.connect(droneFilter);
        droneFilter.connect(droneGain);
        droneGain.connect(audioCtx.destination);
        droneOsc.start(now);
        droneOsc.stop(now + 3.4);

        // 2. Cascading Temple Bell / Crystal Harp Glissando (7 Ascending Harmonics)
        const chimeNotes = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98, 2093.00, 2637.00];
        chimeNotes.forEach((freq, idx) => {
          const osc1 = audioCtx.createOscillator();
          const osc2 = audioCtx.createOscillator(); // Harmonic Detune for lush shimmer
          const gain = audioCtx.createGain();

          osc1.type = 'sine';
          osc1.frequency.setValueAtTime(freq, now + idx * 0.12);

          osc2.type = 'triangle';
          osc2.frequency.setValueAtTime(freq * 2.01, now + idx * 0.12); // Shimmer overtone

          const startT = now + idx * 0.12;
          gain.gain.setValueAtTime(0.0001, startT);
          gain.gain.exponentialRampToValueAtTime(0.18, startT + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.0001, startT + 2.0);

          osc1.connect(gain);
          osc2.connect(gain);
          gain.connect(audioCtx.destination);

          osc1.start(startT);
          osc2.start(startT);
          osc1.stop(startT + 2.1);
          osc2.stop(startT + 2.1);
        });

        // 3. Supernova Blast Impact (Low-frequency Boom + Crackle)
        const bufferSize = audioCtx.sampleRate * 2.0;
        const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          output[i] = Math.random() * 2 - 1;
        }

        const whiteNoise = audioCtx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;

        const noiseFilter = audioCtx.createBiquadFilter();
        noiseFilter.type = 'bandpass';
        noiseFilter.frequency.setValueAtTime(1400, now + 0.25);
        noiseFilter.frequency.exponentialRampToValueAtTime(350, now + 1.2);
        noiseFilter.Q.setValueAtTime(4.0, now + 0.25);

        const noiseGain = audioCtx.createGain();
        noiseGain.gain.setValueAtTime(0.0001, now + 0.25);
        noiseGain.gain.exponentialRampToValueAtTime(0.15, now + 0.45);
        noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + 1.8);

        whiteNoise.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        noiseGain.connect(audioCtx.destination);

        whiteNoise.start(now + 0.25);
        whiteNoise.stop(now + 2.0);

      } catch (err) {}
    }

    // Interactive Tap Chime Sound
    function playTapSparkleSound() {
      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const freq = [1318.5, 1568, 2093, 2637, 3136][Math.floor(Math.random() * 5)];
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.5, now + 0.1);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.36);
      } catch (e) {}
    }

    setTimeout(playCelestialSymphony, 100);
    window.addEventListener('pointerdown', playCelestialSymphony, { once: true });

    // ========================================================
    // ASTRAL PARTICLE SYSTEMS: STARS, SUPERNOVAS & TRAILS
    // ========================================================

    // 1. Hyperspace Twinkling Starfield
    const stars = [];
    const STAR_COUNT = Math.min(220, Math.floor(width * 0.18));
    for (let i = 0; i < STAR_COUNT; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        size: Math.random() * 2 + 0.5,
        baseAlpha: Math.random() * 0.7 + 0.3,
        twinkleSpeed: Math.random() * 0.04 + 0.015,
        twinklePhase: Math.random() * Math.PI * 2,
        color: ['#ffffff', '#fff8db', '#fde047', '#93c5fd', '#f472b6'][Math.floor(Math.random() * 5)]
      });
    }

    // 2. Rising Divine Flame Sparks (Continuous Stream from Diya)
    const flameSparks = [];
    function spawnFlameSpark() {
      const diyaCenterX = width * 0.5;
      const diyaFlameTopY = height * 0.5 - 30;
      flameSparks.push({
        x: diyaCenterX + (Math.random() * 20 - 10),
        y: diyaFlameTopY,
        vx: (Math.random() - 0.5) * 1.8,
        vy: -(Math.random() * 2.8 + 1.2),
        alpha: 1,
        decay: Math.random() * 0.02 + 0.015,
        size: Math.random() * 2.5 + 1.2,
        color: ['#ffffff', '#ffd700', '#ff8c00', '#ff3300'][Math.floor(Math.random() * 4)]
      });
    }

    // 3. Supernova Fireworks & Shockwaves
    const supernovas = [];
    const shockwaves = [];
    const celestialComets = [];

    const celestialPalettes = [
      ['#ffffff', '#fff3b0', '#ffd700', '#f59e0b', '#fb923c'], // Solar Gold Supernova
      ['#ffffff', '#a5f3fc', '#06b6d4', '#8b5cf6', '#d946ef'], // Cosmic Nebula Cyan & Violet
      ['#ffffff', '#fbcfe8', '#ec4899', '#f43f5e', '#fbbf24'], // Iridescent Ruby Starlight
      ['#ffffff', '#bbf7d0', '#22c55e', '#06b6d4', '#3b82f6'], // Emerald Aurora Starglow
      ['#ffffff', '#fed7aa', '#f97316', '#ef4444', '#ffd700'], // Saffron Holy Flame
    ];

    class Shockwave {
      constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.radius = 5;
        this.maxRadius = 140 + Math.random() * 60;
        this.alpha = 0.85;
        this.lineWidth = 4;
      }
      update() {
        this.radius += (this.maxRadius - this.radius) * 0.12;
        this.alpha *= 0.91;
        this.lineWidth *= 0.94;
      }
      draw() {
        if (this.alpha <= 0.01) return;
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.strokeStyle = this.color;
        ctx.lineWidth = Math.max(0.5, this.lineWidth);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 18;
        ctx.stroke();
        ctx.restore();
      }
    }

    class SupernovaParticle {
      constructor(x, y, palette, isWillow = false) {
        this.x = x;
        this.y = y;
        this.color = palette[Math.floor(Math.random() * palette.length)];
        const angle = Math.random() * Math.PI * 2;
        const speed = isWillow ? (Math.random() * 6 + 1) : (Math.random() * 9 + 2);
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.friction = isWillow ? 0.96 : 0.93;
        this.gravity = isWillow ? 0.18 : 0.12;
        this.alpha = 1;
        this.decay = isWillow ? (Math.random() * 0.01 + 0.008) : (Math.random() * 0.02 + 0.012);
        this.size = Math.random() * 3 + 1.5;
        this.trail = [];
        this.twinkle = Math.random() > 0.3;
      }
      update() {
        this.trail.push({ x: this.x, y: this.y, alpha: this.alpha });
        if (this.trail.length > 5) this.trail.shift();

        this.vx *= this.friction;
        this.vy *= this.friction;
        this.vy += this.gravity;
        this.x += this.vx;
        this.y += this.vy;
        this.alpha -= this.decay;
      }
      draw() {
        ctx.save();
        // Tail
        for (let i = 0; i < this.trail.length; i++) {
          const pt = this.trail[i];
          ctx.globalAlpha = pt.alpha * (i / this.trail.length) * 0.6;
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, this.size * 0.7, 0, Math.PI * 2);
          ctx.fillStyle = this.color;
          ctx.fill();
        }
        // Head
        ctx.globalAlpha = Math.max(0, this.alpha);
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        if (this.twinkle && Math.random() > 0.25) {
          ctx.shadowColor = this.color;
          ctx.shadowBlur = 12;
        }
        ctx.fill();
        ctx.restore();
      }
    }

    class CelestialComet {
      constructor(targetX, targetY) {
        this.x = width * 0.15 + Math.random() * (width * 0.7);
        this.y = height + 20;
        this.targetX = targetX !== undefined ? targetX : (width * 0.15 + Math.random() * (width * 0.7));
        this.targetY = targetY !== undefined ? targetY : (height * 0.12 + Math.random() * (height * 0.4));
        this.speed = 15 + Math.random() * 6;
        const angle = Math.atan2(this.targetY - this.y, this.targetX - this.x);
        this.vx = Math.cos(angle) * this.speed;
        this.vy = Math.sin(angle) * this.speed;
        this.palette = celestialPalettes[Math.floor(Math.random() * celestialPalettes.length)];
        this.dead = false;
        this.tail = [];
      }
      update() {
        this.tail.push({ x: this.x, y: this.y });
        if (this.tail.length > 8) this.tail.shift();
        this.x += this.vx;
        this.y += this.vy;
        if (this.vy < 0 && this.y <= this.targetY) {
          this.detonate();
          this.dead = true;
        }
      }
      detonate() {
        shockwaves.push(new Shockwave(this.x, this.y, this.palette[1]));
        const particleCount = 75 + Math.floor(Math.random() * 50);
        for (let i = 0; i < particleCount; i++) {
          supernovas.push(new SupernovaParticle(this.x, this.y, this.palette, i % 2 === 0));
        }
      }
      draw() {
        ctx.save();
        for (let i = 0; i < this.tail.length; i++) {
          const pt = this.tail[i];
          ctx.globalAlpha = (i / this.tail.length) * 0.75;
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 2.5, 0, Math.PI * 2);
          ctx.fillStyle = '#ffd700';
          ctx.shadowColor = '#ff8c00';
          ctx.shadowBlur = 10;
          ctx.fill();
        }
        ctx.globalAlpha = 1;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = '#ffffff';
        ctx.shadowBlur = 16;
        ctx.fill();
        ctx.restore();
      }
    }

    // Launch initial celebratory barrage
    setTimeout(() => {
      celestialComets.push(new CelestialComet(width * 0.22, height * 0.22));
      celestialComets.push(new CelestialComet(width * 0.78, height * 0.20));
    }, 80);

    setTimeout(() => {
      celestialComets.push(new CelestialComet(width * 0.5, height * 0.16));
      celestialComets.push(new CelestialComet(width * 0.15, height * 0.36));
      celestialComets.push(new CelestialComet(width * 0.85, height * 0.34));
    }, 550);

    setTimeout(() => {
      celestialComets.push(new CelestialComet(width * 0.35, height * 0.22));
      celestialComets.push(new CelestialComet(width * 0.65, height * 0.24));
    }, 1100);

    // Interactive Tap / Click: Detonate Supernova & Shockwave
    splash.addEventListener('click', (e) => {
      playCelestialSymphony();
      playTapSparkleSound();
      shockwaves.push(new Shockwave(e.clientX, e.clientY, '#ffd700'));
      const pal = celestialPalettes[Math.floor(Math.random() * celestialPalettes.length)];
      for (let i = 0; i < 60; i++) {
        supernovas.push(new SupernovaParticle(e.clientX, e.clientY, pal, i % 2 === 0));
      }
    });

    // Pointer Move: Floating Magic Stardust Trail
    splash.addEventListener('pointermove', (e) => {
      for (let i = 0; i < 2; i++) {
        flameSparks.push({
          x: e.clientX + (Math.random() * 12 - 6),
          y: e.clientY + (Math.random() * 12 - 6),
          vx: (Math.random() - 0.5) * 1.5,
          vy: -(Math.random() * 1.5 + 0.5),
          alpha: 0.9,
          decay: 0.03,
          size: Math.random() * 2.5 + 1,
          color: ['#ffd700', '#00f5ff', '#ff007f', '#ffffff'][Math.floor(Math.random() * 4)]
        });
      }
    });

    const skipBtn = document.getElementById('diwali-skip-btn');
    if (skipBtn) {
      skipBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dismissDiwaliPortal();
      });
    }

    // ========================================================
    // MAIN RENDER LOOP
    // ========================================================
    let isRunning = true;
    function render() {
      if (!isRunning) return;
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Twinkling Starfield
      stars.forEach(star => {
        star.twinklePhase += star.twinkleSpeed;
        const currentAlpha = Math.max(0.1, Math.min(1, star.baseAlpha + Math.sin(star.twinklePhase) * 0.35));
        ctx.globalAlpha = currentAlpha;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fillStyle = star.color;
        ctx.fill();
      });

      // 2. Spawn & Draw Flame Sparks from Diya
      if (Math.random() > 0.4) spawnFlameSpark();
      for (let i = flameSparks.length - 1; i >= 0; i--) {
        const s = flameSparks[i];
        s.x += s.vx;
        s.y += s.vy;
        s.alpha -= s.decay;
        if (s.alpha <= 0) {
          flameSparks.splice(i, 1);
          continue;
        }
        ctx.save();
        ctx.globalAlpha = s.alpha;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        ctx.fillStyle = s.color;
        ctx.shadowColor = s.color;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.restore();
      }

      // 3. Draw Comets
      for (let i = celestialComets.length - 1; i >= 0; i--) {
        const c = celestialComets[i];
        c.update();
        c.draw();
        if (c.dead) celestialComets.splice(i, 1);
      }

      // 4. Draw Shockwaves
      for (let i = shockwaves.length - 1; i >= 0; i--) {
        const sw = shockwaves[i];
        sw.update();
        sw.draw();
        if (sw.alpha <= 0.01) shockwaves.splice(i, 1);
      }

      // 5. Draw Supernova Particles
      for (let i = supernovas.length - 1; i >= 0; i--) {
        const p = supernovas[i];
        p.update();
        p.draw();
        if (p.alpha <= 0) supernovas.splice(i, 1);
      }

      requestAnimationFrame(render);
    }
    render();

    // ========================================================
    // AUTO-DISMISS: STARGATE WARP TRANSITION (~3.2s)
    // ========================================================
    let autoTimer = setTimeout(() => {
      dismissDiwaliPortal();
    }, 3200);

    function dismissDiwaliPortal() {
      clearTimeout(autoTimer);
      splash.classList.add('fade-out');
      setTimeout(() => {
        splash.style.display = 'none';
        isRunning = false;
      }, 900);
    }

    // Global Replay Method
    window.replayDiwaliIntro = function () {
      splash.style.display = 'flex';
      splash.classList.remove('fade-out');
      isRunning = true;
      hasPlayedAudio = false;
      playCelestialSymphony();
      render();
      celestialComets.push(new CelestialComet(width * 0.28, height * 0.2));
      celestialComets.push(new CelestialComet(width * 0.72, height * 0.2));
      autoTimer = setTimeout(() => {
        dismissDiwaliPortal();
      }, 3200);
    };
  }
})();
