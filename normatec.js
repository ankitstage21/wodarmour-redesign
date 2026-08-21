/* Normatec 3 Legs landing page — hero scrub, pulse sequence, reveals */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.getElementById('hero');
  const hdr  = document.getElementById('hdr');
  const bar  = document.getElementById('buybar');

  /* header + sticky buy bar --------------------------------- */
  const onScroll = () => {
    const past = scrollY > hero.offsetHeight - 90;
    hdr.classList.toggle('solid', past);              // stay clear over the dark hero
    bar.classList.toggle('on', past);                 // buy bar appears once the hero is done
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  onScroll();

  /* reveals -------------------------------------------------- */
  const io = new IntersectionObserver((es) => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -12% 0px' });
  document.querySelectorAll('.rv').forEach((el, i) => {
    el.style.transitionDelay = (i % 5) * 60 + 'ms';
    io.observe(el);
  });

  /* hero frame scrub ---------------------------------------- */
  const cv = document.getElementById('nmScrub');
  const fb = document.getElementById('nmFb');
  const ctx = cv.getContext('2d', { alpha: false });
  const beats = [...document.querySelectorAll('.hbeat')];

  const conn = navigator.connection || {};
  const PORTRAIT = innerWidth < 760 && innerHeight > innerWidth;
  const dir    = PORTRAIT ? 'nm-frames-mb' : 'nm-frames';
  const FRAMES = (PORTRAIT ? window.NM_FRAMES_MB : window.NM_FRAMES) || 0;
  const POSTER = PORTRAIT ? 'assets/nm-poster-mb.jpg' : 'assets/nm-poster.jpg';
  const src = i => `assets/${dir}/f_${String(i).padStart(4, '0')}.jpg`;

  const imgs = []; let current = -1;

  function fit() {
    const d = Math.min(devicePixelRatio || 1, 2);
    cv.width = innerWidth * d; cv.height = innerHeight * d;
    draw(current < 0 ? 0 : current, true);
  }
  function draw(i, force) {
    if (!FRAMES || (i === current && !force)) return;
    const im = imgs[i];
    if (!im || !im.complete || !im.naturalWidth) return;
    current = i;
    const cw = cv.width, ch = cv.height;
    const s = Math.max(cw / im.naturalWidth, ch / im.naturalHeight);
    const w = im.naturalWidth * s, h = im.naturalHeight * s;
    ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
  }

  if (FRAMES && !reduce) {
    fb.style.display = 'none';
    let loaded = 0;
    for (let i = 1; i <= FRAMES; i++) {
      const im = new Image();
      im.decoding = 'async';
      im.onload = () => { if (++loaded === 1) fit(); };
      im.src = src(i);
      imgs[i - 1] = im;
    }
    addEventListener('resize', fit, { passive: true });
  } else {
    cv.style.display = 'none';
    fb.style.background = `#08080A url('${POSTER}') center/cover no-repeat`;
  }

  /* progress → frame + hero beat ----------------------------- */
  let ticking = false;
  function update() {
    ticking = false;
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    if (FRAMES) draw(Math.min(FRAMES - 1, Math.floor(p * (FRAMES - 1) + 1e-4)));
    const idx = p < 0.34 ? 0 : p < 0.68 ? 1 : 2;
    beats.forEach((b, i) => b.classList.toggle('on', i === idx));
  }
  const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req, { passive: true });
  window.__nmUpdate = update;     // debug hook (rAF is frozen in hidden preview panes)
  update();

  /* the pulse: run the zones foot → thigh, on a loop --------- */
  const zones  = [...document.querySelectorAll('.zone')];
  const labels = [...document.querySelectorAll('.zone-label')];
  const steps  = [...document.querySelectorAll('.step')];
  let pulseTimer = null, z = 0;

  function litUpTo(n) {
    zones.forEach((el, i)  => el.classList.toggle('lit', i <= n));
    labels.forEach((el, i) => el.classList.toggle('lit', i <= n));
    steps.forEach((el, i)  => el.classList.toggle('lit', i === n));
  }
  function tick() {
    litUpTo(z);
    z++;
    if (z > zones.length) { z = 0; litUpTo(-1); }   // full release, then start again
  }
  function startPulse() {
    if (pulseTimer || reduce) return;
    z = 0; tick();
    pulseTimer = setInterval(tick, 900);
  }
  function stopPulse() { clearInterval(pulseTimer); pulseTimer = null; }

  const pulseSec = document.getElementById('how');
  if (pulseSec) {
    new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? startPulse() : stopPulse()),
      { threshold: 0.25 }).observe(pulseSec);
    if (reduce) litUpTo(zones.length - 1);   // reduced motion: show the finished state
  }

  /* smooth scroll ------------------------------------------- */
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
    s.onerror = () => {};
    document.head.appendChild(s);
  }
})();
