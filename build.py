#!/usr/bin/env python3
"""Generates index.html for the WOD Armour homepage redesign from real store data."""
import json, html

D = json.load(open('data.json'))
BASE = "https://wodarmour.in"

def inr(n):
    n = int(round(n)); s = str(n)
    if len(s) <= 3: return "₹" + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return "₹" + ",".join(parts) + "," + tail

def esc(s): return html.escape(str(s))

def card(p):
    tag = ""
    if not p['available']:
        tag = '<span class="tag out">Sold out</span>'
    elif p['compare'] and p['compare'] > p['price']:
        off = round((1 - p['price']/p['compare']) * 100)
        tag = f'<span class="tag sale">−{off}%</span>'
    was = f"<s>{inr(p['compare'])}</s>" if p['compare'] and p['compare'] > p['price'] else ""
    img = f'<img src="{esc(p["img"])}" alt="{esc(p["title"])}" loading="lazy" decoding="async">' if p['img'] else ''
    return f'''<a class="card" href="{BASE}/products/{esc(p['handle'])}">
        <div class="card-img">{img}{tag}</div>
        <div class="card-body"><h4>{esc(p['title'])}</h4>
          <div class="card-price">{inr(p['price'])}{was}</div></div></a>'''

def row(items): return "\n".join(card(p) for p in items)

def shelf(title, blurb, handle, items):
    return f'''<div class="shelf rv">
      <div class="shelf-head"><div><h3>{esc(title)}</h3><p>{esc(blurb)}</p></div>
        <a class="link-more" href="{BASE}/collections/{handle}">All {esc(title)} →</a></div>
      <div class="row">{row(items)}</div></div>'''

f = D['flagship']
save = int(f['compare'] - f['price']) if f['compare'] else 0
emi = int(f['price'] / 12)

GOALS = [
    ("Heavy legs &amp; circulation", "Dynamic air compression that flushes the legs after long rides, runs and race days.",
     "Normatec · JetBoots · Flowlife", D['goals']['legs'], "normatec"),
    ("Muscle soreness &amp; knots", "Percussive therapy for the tight spots foam rolling never quite reaches.",
     "Theragun · Hypervolt · Achedaway", D['goals']['soreness'], "self-rehab-products"),
    ("Heat &amp; cold therapy", "Contrast therapy on demand — no ice bath, no tub, no plumbing.",
     "RecoveryTherm · Venom", (D['goals']['thermal'] or [D['goals']['soreness']])[0], "therabody"),
    ("Train &amp; measure", "Ergometers and wearables that tell you whether the recovery is actually working.",
     "Concept2 · Garmin · Polar", D['goals']['measure'], "equipment-1"),
]

goals_html = "\n".join(f'''<a class="goal rv" href="{BASE}/collections/{h}">
      <div class="goal-img"><img src="{esc(p['img'])}" alt="" loading="lazy" decoding="async"></div>
      <div class="goal-body"><h3>{t}</h3><p>{b}</p><div class="g-brands">{br}</div></div></a>'''
    for t, b, br, p, h in GOALS)

BLOG = [
 ("August 18, 2026", "Normatec for Cyclists: How Compression Boots Speed Up Leg Recovery",
  "Do compression boots actually work for cyclists? What the research shows, the exact 20–30 minute protocol to use after long rides, and what it costs in India.",
  "normatec-for-cyclists-how-compression-boots-speed-up-leg-recovery"),
 ("July 30, 2026", "Six Months of Hyrox Training on the Therabody JetBoots Pro Plus",
  "An honest long-term review from a Bengaluru Hyrox athlete — what the JetBoots changed, what they didn't, and who should skip them.",
  "recovering-like-an-athlete-my-honest-review-of-the-therabody-jetboots-pro-plus"),
 ("July 23, 2026", "Theragun Pro Plus in India: Price, Features & Where to Buy",
  "Everything on the Pro Plus — near-infrared, heat, breathwork — and how to tell an authorised unit from a grey import.",
  "theragun-pro-plus-india-price-features-why-wod-armour-is-the-best-place-to-buy"),
]
blog_html = "\n".join(f'''<a class="guide rv" href="{BASE}/blogs/news/{h}"><time>{d}</time><h3>{esc(t)}</h3>
      <p>{esc(b)}</p><span class="link-more">Read the guide →</span></a>''' for d, t, b, h in BLOG)

NAV = [("Recovery","self-rehab-products"),("Normatec","normatec"),("Therabody","therabody"),
       ("Hyperice","hyperice"),("Equipment","equipment-1"),("Wearables","garmin"),("Gear","gear-and-accessories")]
nav_html = "".join(f'<a href="{BASE}/collections/{h}">{esc(t)}</a>' for t, h in NAV)

MARKS = ["Therabody","Hyperice","Normatec","Concept2","Garmin","Polar","Compex","Blazepod","Achedaway","Flowlife"]

HTML = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WOD Armour — India's Authorised Recovery Technology Store</title>
<meta name="description" content="Official authorised Indian reseller of Therabody, Hyperice Normatec, Concept2, Garmin and Polar. Genuine warranty, no-cost EMI, free shipping.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head><body>

<header class="hdr" id="hdr"><div class="hdr-in">
  <a href="#" class="logo"><img class="lg-light" src="assets/logo-light.png" alt="WOD Armour"><img class="lg-dark" src="assets/logo.png" alt=""></a>
  <nav class="nav">{nav_html}</nav>
  <div class="hdr-act"><span class="pill-auth"><b>●</b> Authorised reseller</span></div>
</div></header>

<!-- 01 · HERO ─ scroll-scrubbed -->
<section class="hero" id="hero">
  <div class="hero-stick">
    <div class="hero-fallback" id="heroFallback"></div>
    <canvas id="scrub"></canvas>
    
    <div class="hero-vig"></div><div class="hero-vig2"></div>
    <div class="hero-copy">
      <div class="beat on" data-beat="0">
        <h1>Recovery is the<br>training you're<br><em>not doing.</em></h1>
        <p>The half of performance that happens after you stop.</p>
      </div>
      <div class="beat" data-beat="1">
        <div class="eyebrow">The equipment that does it</div>
        <div class="brandline" style="margin-top:18px">
          Normatec <span>/</span> Theragun <span>/</span> Concept2 <span>/</span> Garmin
        </div>
        <p>The systems used by professional teams — available in India, properly.</p>
      </div>
      <div class="beat" data-beat="2">
        <h1>Officially<br>authorised<br><em>in India.</em></h1>
        <p>Genuine warranty. Real service. No grey imports.</p>
        <a class="btn btn-primary" href="{BASE}/collections/self-rehab-products">Shop recovery</a>
      </div>
    </div>
    <div class="scroll-cue">Scroll <i></i></div>
  </div>
</section>

<!-- 02 · AUTHORITY -->
<section class="auth"><div class="wrap">
  <div class="auth-top"><span class="dot"></span><b>Officially authorised Indian reseller</b></div>
  <div class="auth-marks">{"".join(f"<span>{m}</span>" for m in MARKS)}</div>
  <p class="auth-sub"><b>Genuine India warranty</b> · <b>Official service network</b> · <b>GST invoice</b> · <b>Authorised firmware &amp; app support</b></p>
</div></section>


<!-- 03 · FLAGSHIP -->
<section class="sec"><div class="wrap"><div class="flag rv">
  <div class="flag-img"><span class="flag-badge">Most asked for</span>
    <img src="{esc(f.get('img2') or f['img'])}" alt="{esc(f['title'])}" loading="lazy"></div>
  <div>
    <div class="eyebrow">The flagship</div>
    <h2>{esc(f['title'])}</h2>
    <p class="lede">Patented precision-pulse compression that moves fluid out of tired legs the way a physio's hands would — in twenty minutes, on your sofa.</p>
    <ul>
      <li>Seven overlapping zones, pulsing in sequence from foot to hip</li>
      <li>Twenty minutes replaces an hour of passive rest between sessions</li>
      <li>The system used across pro cycling, CrossFit and Hyrox</li>
      <li>Sold, warranted and serviced in India by WOD Armour</li>
    </ul>
    <div class="price-row"><span class="price">{inr(f['price'])}</span>
      <span class="price-was">{inr(f['compare'])}</span>
      <span class="price-save">Save {inr(save)}</span></div>
    <!-- VERIFY: confirm EMI is actually offered before this ships -->
    <p class="emi">or <b>{inr(emi)}/month</b> on no-cost EMI for 12 months</p>
    <div class="flag-cta">
      <a class="btn btn-primary" href="{BASE}/products/{esc(f['handle'])}">Shop Normatec</a>
      <a class="btn btn-ghost" href="{BASE}/collections/normatec">Compare the range</a>
    </div>
  </div>
</div></div></section>

<!-- 04 · SHELVES -->
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><div><div class="eyebrow">The catalogue</div>
    <h2 class="h-sec">Brands we're<br>authorised to sell</h2></div></div>
  {shelf("Therabody", "Theragun percussive therapy, JetBoots compression and RecoveryTherm contrast — the full Therabody line, officially.", "therabody", D['therabody'])}
  {shelf("Hyperice", "Normatec compression, Hypervolt massage and Venom heat wraps. The recovery room used by professional sport.", "hyperice", D['hyperice'])}
  {shelf("Concept2", "The ergometers every gym benchmarks against. RowErg, SkiErg, BikeErg — with genuine India service.", "concept-2", D['concept2'])}
</div></section>

<!-- 05 · GOALS -->
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><div>
    <div class="eyebrow">Shop by need</div>
    <h2 class="h-sec">Or start from<br>what hurts</h2>
  </div><p class="lede">Not sure which brand you need? Pick the problem instead and we'll point at the shelf that solves it.</p></div>
  <div class="goals">{goals_html}</div>
</div></section>

<!-- 06 · PROOF -->
<section class="sec proof"><div class="wrap"><div class="proof-grid">
  <div class="rv">
    <div class="eyebrow">From the field</div>
    <blockquote class="quote" style="margin-top:20px">"I did my first Hyrox in Mumbai a little over a year ago, and if you've done one, you know <span>the particular kind of wrecked</span> your legs feel afterward."</blockquote>
    <div class="by"><b>Ankit Kataria</b>Hyrox athlete, Bengaluru — six months on the Therabody JetBoots Pro Plus</div>
  </div>
  <div class="stat-col rv">
    <div class="stat"><b>10</b><span>Global brands stocked in India</span></div>
    <div class="stat"><b>800+</b><span>Products in the catalogue</span></div>
    <div class="stat"><b>Gurgaon</b><span>Where your order actually ships from</span></div>
  </div>
</div></div></section>

<!-- 07 · HOUSE GEAR -->
<section class="sec gear"><div class="wrap">
  <div class="sec-head rv"><div><div class="eyebrow">Our own label</div>
    <h2 class="h-sec">WOD Armour gear</h2>
    <p class="gear-note">The grips, sleeves and bags we make ourselves — because the kit we wanted for the box didn't exist here.</p></div>
    <a class="link-more" href="{BASE}/collections/gear-and-accessories">All gear →</a></div>
  <div class="row rv">{row(D['gear'][:6])}</div>
</div></section>

<!-- 08 · GUIDES -->
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><div><div class="eyebrow">Before you spend</div>
    <h2 class="h-sec">Not sure which<br>one to buy?</h2></div>
    <a class="link-more" href="{BASE}/blogs/news">All guides →</a></div>
  <div class="guides">{blog_html}</div>
</div></section>

<!-- 09 · SIGNUP -->
<section class="sec signup"><div class="wrap"><div class="signup-in">
  <div class="rv"><div class="eyebrow">Free guide</div>
    <h2>How to choose a<br>recovery system</h2>
    <p>Twelve pages, no marketing: what compression actually does, when percussion beats it, and how to not overspend on your first device.</p></div>
  <form class="form rv" onsubmit="event.preventDefault();this.innerHTML='<p style=&quot;font-family:var(--display);font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--red)&quot;>Sent — check your inbox.</p>'">
    <input type="email" placeholder="your@email.com" required aria-label="Email address">
    <button class="btn btn-primary" type="submit">Send it</button>
    <small>One email. The guide, then occasional restock notes. Unsubscribe anytime.</small>
  </form>
</div></div></section>

<footer class="ftr"><div class="wrap">
  <div class="ftr-grid">
    <div><img src="assets/logo.png" alt="WOD Armour">
      <p style="max-width:34ch">India's authorised store for recovery technology. Shipped from Gurgaon.</p></div>
    <div><h5>Recovery</h5>
      <a href="{BASE}/collections/normatec">Normatec</a><br><a href="{BASE}/collections/therabody">Therabody</a><br>
      <a href="{BASE}/collections/hyperice">Hyperice</a><br><a href="{BASE}/collections/compex">Compex</a></div>
    <div><h5>Train</h5>
      <a href="{BASE}/collections/concept-2">Concept2</a><br><a href="{BASE}/collections/garmin">Garmin</a><br>
      <a href="{BASE}/collections/polar">Polar</a><br><a href="{BASE}/collections/blazepod">Blazepod</a></div>
    <div><h5>Help</h5>
      <a href="tel:+918448866514">+91 84488 66514</a><br><a href="mailto:Sales@wodarmour.in">Sales@wodarmour.in</a><br>
      <a href="{BASE}/policies/refund-policy">Returns</a><br><a href="{BASE}/policies/shipping-policy">Shipping</a></div>
  </div>
  <div class="ftr-base"><span>© 2026 WOD Armour · 222 Krishna Nagar, Basai Road, Gurgaon 122001</span>
    <span>Authorised reseller · Genuine warranty</span></div>
</div></footer>

<script src="frames.js"></script>
<script src="app.js"></script>
</body></html>'''

open('index.html', 'w').write(HTML)
print(f"index.html written — {len(HTML):,} bytes")
