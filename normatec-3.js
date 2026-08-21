/* Concept 3 "Object" — the product is pinned for the whole sequence and never cuts.
   Scroll moves the page past it; the product only scales and drifts.            */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wrap = document.getElementById('stagewrap');
  const cv   = document.getElementById('obj');
  const fb   = document.getElementById('objfb');
  const bar  = document.getElementById('bar');
  const acts = [...document.querySelectorAll('.act')];
  const ctx  = cv.getContext('2d', { alpha: true });

  const N   = window.INF_FRAMES || 0;
  const src = i => `assets/inf-frames/f_${String(i).padStart(4,'0')}.jpg`;
  const imgs = [];
  let current = -1, ready = false;

  /* Per-act product pose. x/y are fractions of the viewport.
     The product travels: centre → right → left → right-and-close.        */
  const DESKTOP = [
    { s: 0.62, x:  0.00, y: -0.06 },
    { s: 0.86, x:  0.24, y:  0.00 },
    { s: 0.86, x: -0.24, y:  0.00 },
    { s: 1.30, x:  0.28, y:  0.06 },
  ];
  /* On a phone there is no room beside the product — it sits above the copy,
     never behind it. Same journey, stacked instead of side-by-side.        */
  const MOBILE = [
    { s: 0.60, x: 0, y: -0.07 },
    { s: 0.52, x: 0, y: -0.24 },
    { s: 0.52, x: 0, y: -0.24 },
    { s: 0.60, x: 0, y: -0.26 },
  ];
  let POSE = DESKTOP;
  const pickPose = () => { POSE = innerWidth < 900 ? MOBILE : DESKTOP; };
  pickPose();
  addEventListener('resize', pickPose, { passive: true });

  const smooth = t => t * t * (3 - 2 * t);           // smoothstep
  const lerp = (a, b, t) => a + (b - a) * t;

  function sizeCanvas(){
    const d = Math.min(devicePixelRatio || 1, 2);
    cv.width  = innerWidth  * d;
    cv.height = innerHeight * d;
    cv.style.width  = innerWidth  + 'px';
    cv.style.height = innerHeight + 'px';
    draw(current < 0 ? 0 : current, true);
  }

  function draw(i, force){
    if (!N || !ready || (i === current && !force)) return;
    const im = imgs[i];
    if (!im || !im.complete || !im.naturalWidth) return;
    current = i;
    const cw = cv.width, ch = cv.height;
    ctx.clearRect(0, 0, cw, ch);
    const s = Math.min(cw / im.naturalWidth, ch / im.naturalHeight) * 0.78;
    const w = im.naturalWidth * s, h = im.naturalHeight * s;
    ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
  }

  if (N && !reduce) {
    let loaded = 0;
    for (let i = 1; i <= N; i++){
      const im = new Image();
      im.decoding = 'async';
      im.onload = () => { if (++loaded === 1){ ready = true; sizeCanvas(); } };
      im.src = src(i);
      imgs[i-1] = im;
    }
    addEventListener('resize', sizeCanvas, { passive: true });
  } else {
    cv.style.display = 'none';
    fb.style.backgroundImage = "url('assets/inf-poster.jpg')";
    fb.style.backgroundSize = '58% auto';
  }

  let ticking = false;
  function update(){
    ticking = false;
    const n = acts.length;
    const total = wrap.offsetHeight - innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -wrap.getBoundingClientRect().top / total)) : 0;

    /* which act, and how far through the handoff */
    const seg = p * (n - 1);
    const i   = Math.min(n - 2, Math.floor(seg));
    const t   = smooth(Math.min(1, Math.max(0, seg - i)));
    const a = POSE[i], b = POSE[i + 1];
    const s = lerp(a.s, b.s, t);
    const x = lerp(a.x, b.x, t) * innerWidth;
    const y = lerp(a.y, b.y, t) * innerHeight;
    cv.style.transform = `translate(-50%,-50%) translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) scale(${s.toFixed(3)})`;

    /* the sleeves fill only through act 03 — a detail, not the concept */
    if (N){
      const f = seg < 1.6 ? 0
              : seg > 2.6 ? 1
              : (seg - 1.6);
      draw(Math.min(N - 1, Math.round(smooth(f) * (N - 1))));
    }

    /* reveal the act whose text is on screen */
    acts.forEach((el, k) => el.classList.toggle('in', Math.abs(seg - k) < 0.62));

    bar.classList.toggle('on', -wrap.getBoundingClientRect().top > total * 0.94);
  }
  const req = () => { if (!ticking){ ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req, { passive: true });
  window.__objUpdate = update;
  update();
  acts[0] && acts[0].classList.add('in');

  /* smooth scroll — the motion only reads as expensive if the scroll does */
  if (!reduce){
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js';
    s.onload = () => {
      if (!window.Lenis) return;
      const l = new Lenis({ duration: 1.25, smoothWheel: true });
      const raf = t => { l.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      l.on('scroll', req);
    };
    s.onerror = () => {};
    document.head.appendChild(s);
  }
})();
