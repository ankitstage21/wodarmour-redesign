/* Concept 3 "Object" — a real GLB, pinned for the whole sequence.
   Scroll orbits the camera and moves the product; it never cuts.        */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const wrap = document.getElementById('stagewrap');
  const mv   = document.getElementById('obj');
  const fb   = document.getElementById('objfb');
  const bar  = document.getElementById('bar');
  const acts = [...document.querySelectorAll('.act')];

  /* Orbit is clamped to the front hemisphere on purpose: the mesh was built
     from two front-facing references, so its reverse side is mirrored.     */
  const FRONT = 90;          // the mesh's front faces +90deg in model-viewer's frame
  const DESKTOP = [
    { fov: 34, x:  0.00, y: -0.06, th: FRONT      },
    { fov: 27, x:  0.24, y:  0.00, th: FRONT - 24 },
    { fov: 27, x: -0.24, y:  0.00, th: FRONT + 24 },
    { fov: 21, x:  0.28, y:  0.06, th: FRONT -  9 },
  ];
  const MOBILE = [
    { fov: 36, x: 0, y: -0.07, th: FRONT      },
    { fov: 40, x: 0, y: -0.24, th: FRONT - 20 },
    { fov: 40, x: 0, y: -0.24, th: FRONT + 20 },
    { fov: 34, x: 0, y: -0.26, th: FRONT -  8 },
  ];
  let POSE = DESKTOP;
  const pickPose = () => { POSE = innerWidth < 900 ? MOBILE : DESKTOP; };
  pickPose();
  addEventListener('resize', pickPose, { passive: true });

  const smooth = t => t * t * (3 - 2 * t);
  const lerp = (a, b, t) => a + (b - a) * t;

  /* let a drag win for a moment, then hand the camera back to scroll */
  let userUntil = 0;
  mv && mv.addEventListener('camera-change', e => {
    if (e.detail && e.detail.source === 'user-interaction') userUntil = performance.now() + 2600;
  });

  let ticking = false;
  function update(){
    ticking = false;
    const n = acts.length;
    const total = wrap.offsetHeight - innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -wrap.getBoundingClientRect().top / total)) : 0;

    const seg = p * (n - 1);
    const i = Math.min(n - 2, Math.floor(seg));
    const t = smooth(Math.min(1, Math.max(0, seg - i)));
    const a = POSE[i], b = POSE[i + 1];

    const x = lerp(a.x, b.x, t) * innerWidth;
    const y = lerp(a.y, b.y, t) * innerHeight;
    mv.style.transform = `translate(-50%,-50%) translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;

    if (performance.now() > userUntil) {
      mv.fieldOfView = lerp(a.fov, b.fov, t).toFixed(2) + 'deg';
      mv.cameraOrbit = `${lerp(a.th, b.th, t).toFixed(2)}deg 82deg auto`;
    }

    acts.forEach((el, k) => el.classList.toggle('in', Math.abs(seg - k) < 0.62));
    bar.classList.toggle('on', -wrap.getBoundingClientRect().top > total * 0.94);
  }
  const req = () => { if (!ticking){ ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req, { passive: true });
  window.__objUpdate = update;
  update();
  acts[0] && acts[0].classList.add('in');

  /* no WebGL, or reduced motion: fall back to the photoreal still */
  const noGL = (() => { try { return !document.createElement('canvas').getContext('webgl'); }
                        catch(e){ return true; } })();
  if (noGL || reduce){
    mv.style.display = 'none';
    fb.style.backgroundImage = "url('assets/inf-poster.jpg')";
    fb.style.backgroundSize = '52% auto';
  }

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
