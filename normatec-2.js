/* Concept 2 — scroll drives one full compression cycle: inflate, then release */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stage = document.getElementById('stage');
  const cv    = document.getElementById('inf');
  const fb    = document.getElementById('fb');
  const bar   = document.getElementById('bar');
  const ctx   = cv.getContext('2d', { alpha: false });

  const N   = window.INF_FRAMES || 0;
  const src = i => `assets/inf-frames/f_${String(i).padStart(4,'0')}.jpg`;
  const imgs = [];
  let current = -1;

  const GROUND = '#EBEBE9';

  function fit(){
    const d = Math.min(devicePixelRatio || 1, 2);
    cv.width  = cv.clientWidth  * d;
    cv.height = cv.clientHeight * d;
    draw(current < 0 ? 0 : current, true);
  }
  function draw(i, force){
    if (!N || (i === current && !force)) return;
    const im = imgs[i];
    if (!im || !im.complete || !im.naturalWidth) return;
    current = i;
    const cw = cv.width, ch = cv.height;
    ctx.fillStyle = GROUND; ctx.fillRect(0, 0, cw, ch);
    // contain, not cover — the product stays whole on every screen
    const s = Math.min(cw / im.naturalWidth, ch / im.naturalHeight);
    const w = im.naturalWidth * s, h = im.naturalHeight * s;
    ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
  }

  if (N && !reduce) {
    fb.style.display = 'none';
    let loaded = 0;
    for (let i = 1; i <= N; i++){
      const im = new Image();
      im.decoding = 'async';
      im.onload = () => { if (++loaded === 1) fit(); };
      im.src = src(i);
      imgs[i-1] = im;
    }
    addEventListener('resize', fit, { passive: true });
  } else {
    cv.style.display = 'none';
    fb.style.backgroundImage = "url('assets/inf-poster.jpg')";
  }

  let ticking = false;
  function update(){
    ticking = false;
    const r = stage.getBoundingClientRect();
    const total = stage.offsetHeight - innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    // ping-pong: 0 -> full inflation -> released. One complete pulse cycle.
    const t = p < 0.5 ? p * 2 : (1 - p) * 2;
    if (N) draw(Math.min(N - 1, Math.round(t * (N - 1))));
    bar.classList.toggle('on', scrollY > stage.offsetHeight * 0.9);
  }
  const req = () => { if (!ticking){ ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req, { passive: true });
  window.__infUpdate = update;
  update();
})();
