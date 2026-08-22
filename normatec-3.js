/* Concept 3 "Object" — four photoreal frames of one product, pinned for the whole
   sequence. Scroll cross-fades between angles and moves the product; never cuts. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wrap = document.getElementById('stagewrap');
  const obj  = document.getElementById('obj');
  const phs  = [...document.querySelectorAll('.ph')];
  const bar  = document.getElementById('bar');
  const acts = [...document.querySelectorAll('.act')];

  const DESKTOP = [
    { s: 0.98, x:  0.00, y: -0.04 },
    { s: 1.10, x:  0.22, y:  0.00 },
    { s: 1.26, x: -0.22, y:  0.02 },
    { s: 1.06, x:  0.26, y:  0.02 },
  ];
  const MOBILE = [
    { s: 0.92, x: 0, y: -0.08 },
    { s: 0.80, x: 0, y: -0.24 },
    { s: 0.88, x: 0, y: -0.24 },
    { s: 0.78, x: 0, y: -0.25 },
  ];
  let POSE = DESKTOP;
  const pickPose = () => { POSE = innerWidth < 900 ? MOBILE : DESKTOP; };
  pickPose();
  addEventListener('resize', pickPose, { passive: true });

  const smooth = t => t * t * (3 - 2 * t);
  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp01 = v => Math.min(1, Math.max(0, v));

  let ticking = false;
  function update(){
    ticking = false;
    const n = acts.length;
    const total = wrap.offsetHeight - innerHeight;
    const p = total > 0 ? clamp01(-wrap.getBoundingClientRect().top / total) : 0;

    const seg = p * (n - 1);
    const i = Math.min(n - 2, Math.floor(seg));
    const t = smooth(clamp01(seg - i));
    const a = POSE[i], b = POSE[i + 1];

    const s = lerp(a.s, b.s, t);
    const x = lerp(a.x, b.x, t) * innerWidth;
    const y = lerp(a.y, b.y, t) * innerHeight;
    obj.style.transform =
      `translate(-50%,-50%) translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) scale(${s.toFixed(3)})`;

    /* each frame owns its act and fades out as the next takes over */
    phs.forEach(el => {
      const k = +el.dataset.k;
      el.style.opacity = smooth(clamp01(1 - Math.abs(seg - k))).toFixed(3);
    });

    acts.forEach((el, k) => el.classList.toggle('in', Math.abs(seg - k) < 0.62));
    bar.classList.toggle('on', -wrap.getBoundingClientRect().top > total * 0.94);
  }
  const req = () => { if (!ticking){ ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req, { passive: true });
  window.__objUpdate = update;
  update();
  acts[0] && acts[0].classList.add('in');

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
