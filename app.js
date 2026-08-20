/* WOD Armour redesign — hero scrub, beats, reveals */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── header ─────────────────────────────────────────── */
  const hdr = document.getElementById('hdr');
  // stay transparent over the dark hero; go solid-paper only once past it
  const onScroll = () => {
    const h = document.getElementById('hero');
    const limit = h ? h.offsetHeight - 90 : 40;
    hdr.classList.toggle('solid', scrollY > limit);
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  onScroll();

  /* ── reveals ────────────────────────────────────────── */
  const io = new IntersectionObserver((es) => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -12% 0px' });
  document.querySelectorAll('.rv').forEach((el, i) => {
    el.style.transitionDelay = (i % 6) * 55 + 'ms';
    io.observe(el);
  });

  /* ── hero: canvas frame scrub ───────────────────────── */
  const hero = document.getElementById('hero');
  const cv = document.getElementById('scrub');
  const fallback = document.getElementById('heroFallback');
  const beats = [...document.querySelectorAll('.beat')];
  const ctx = cv.getContext('2d', { alpha: false });

  // Phones get a portrait 9:16 crop of the same take: cover-cropping the 16:9
  // master into a tall viewport would upscale it ~2.3x and look blocky.
  const conn = navigator.connection || {};
  const SAVER = conn.saveData === true || /2g|slow-2g/.test(conn.effectiveType || '');
  const PORTRAIT = innerWidth < 760 && innerHeight > innerWidth;
  const dir = PORTRAIT ? 'frames-mb' : SAVER ? 'frames-sm' : 'frames';
  const FRAMES = (PORTRAIT ? window.HERO_FRAMES_MB : window.HERO_FRAMES) || 0;
  const POSTER = PORTRAIT ? 'assets/hero-poster-mb.jpg' : 'assets/hero-poster.jpg';
  const src = i => `assets/${dir}/f_${String(i).padStart(4, '0')}.jpg`;
  const imgs = []; let ready = 0, current = -1;

  function fit() {
    const d = Math.min(devicePixelRatio || 1, 2);
    cv.width = innerWidth * d; cv.height = innerHeight * d;
    draw(current < 0 ? 0 : current, true);
  }

  function draw(i, force) {
    if (!FRAMES) return;
    if (i === current && !force) return;
    const im = imgs[i];
    if (!im || !im.complete || !im.naturalWidth) return;
    current = i;
    const cw = cv.width, ch = cv.height;
    const s = Math.max(cw / im.naturalWidth, ch / im.naturalHeight);
    const w = im.naturalWidth * s, h = im.naturalHeight * s;
    ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
  }

  if (FRAMES && !reduce) {
    fallback.style.display = 'none';
    for (let i = 1; i <= FRAMES; i++) {
      const im = new Image();
      im.decoding = 'async';
      im.onload = () => { if (++ready === 1) { fit(); } };
      im.src = src(i);
      imgs[i - 1] = im;
    }
    addEventListener('resize', fit, { passive: true });
  } else if (FRAMES && reduce) {
    // reduced motion: one still frame, no scrub, no preloading
    cv.style.display = 'none';
    fallback.style.background = `#08080A url('${POSTER}') center/cover no-repeat`;
  } else {
    cv.style.display = 'none';                          // graceful: gradient stands in
  }

  /* progress → frame + beat */
  let ticking = false;
  function update() {
    ticking = false;
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;

    if (FRAMES) draw(Math.min(FRAMES - 1, Math.floor(p * (FRAMES - 1) + 0.0001)));

    // three beats across the scrub, with a hold at each end
    const idx = p < 0.33 ? 0 : p < 0.66 ? 1 : 2;
    beats.forEach((b, i) => b.classList.toggle('on', i === idx));
  }
  const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  window.__heroUpdate = update;   // debug hook (rAF is frozen in hidden preview panes)
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req, { passive: true });
  update();

  /* ── Lenis smooth scroll (optional, CDN) ────────────── */
  if (!reduce) {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js';
    s.onload = () => {
      if (!window.Lenis) return;
      const lenis = new Lenis({ duration: 1.05, smoothWheel: true });
      const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      lenis.on('scroll', () => { req(); onScroll(); });
    };
    s.onerror = () => {};                               // native scroll is a fine fallback
    document.head.appendChild(s);
  }
})();
