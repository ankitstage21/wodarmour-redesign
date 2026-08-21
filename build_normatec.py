#!/usr/bin/env python3
"""Generates normatec.html — single-product landing page, real data from the live store."""
import json, re, html

BASE = "https://wodarmour.in"
HANDLE = "hyperice-normatec-3-legs-compression-recovery-boots-india-buy-with-2-yr-warranty"

d = json.load(open('col-normatec.json'))['products']
p = [x for x in d if 'Normatec 3 Legs' in x['title']][0]
HANDLE = p['handle']
v = p['variants'][0]
PRICE, WAS = float(v['price']), float(v['compare_at_price'])
IN_STOCK = v['available']

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
img = lambda i, w=1200: re.sub(r'(\.(jpg|jpeg|png|webp))', rf'_{w}x\1', p['images'][i]['src'].split('?')[0])

SAVE = int(WAS - PRICE)
EMI  = int(PRICE / 12)

# ── the pulse: sequential compression, foot → thigh ──────────────────────
ZONES = [
    ("Foot",  "The cycle starts at the foot and never starts anywhere else."),
    ("Ankle", "Pressure holds below while the next zone engages above it."),
    ("Calf",  "Overlapping chambers stop fluid falling back down the leg."),
    ("Knee",  "The wave keeps climbing; nothing below it has released yet."),
    ("Thigh", "The last zone fires, the whole leg releases, and it begins again."),
]
steps = "\n".join(
    f'''<div class="step" data-step="{i}"><span class="n">Zone {i+1:02d}</span>
      <b>{esc(n)}</b><span>{esc(t)}</span></div>''' for i, (n, t) in enumerate(ZONES))

# leg SVG — five stacked chambers, lit in sequence
zh, gap, top = 74, 9, 26
bands = []
for i, (n, _) in enumerate(ZONES):
    y = top + (len(ZONES) - 1 - i) * (zh + gap)          # foot at the bottom
    w = 108 + i * 9                                       # widens toward the thigh
    x = 178 - w / 2   # nudged right so labels + bars read centred as a group
    bands.append(
        f'<rect class="zone" data-zone="{i}" x="{x:.0f}" y="{y}" width="{w}" height="{zh}" rx="16"/>'
        f'<text class="zone-label" data-zone="{i}" x="{x - 14:.0f}" y="{y + zh/2 + 4:.0f}" text-anchor="end">{n.upper()}</text>')
leg_svg = f'''<svg class="leg" viewBox="0 0 300 {top*2 + len(ZONES)*(zh+gap)}" xmlns="http://www.w3.org/2000/svg" aria-label="Compression sequence, foot to thigh">
    {''.join(bands)}
  </svg>'''

SPECS = [
    ("7", "Compression levels", "From a light flush to deep therapeutic pressure."),
    ("30–110", "mmHg pressure range", "The clinical range compression therapy is studied at."),
    ("3+ hrs", "Battery per charge", "Several full sessions before it needs the wall."),
    ("20–45", "Minutes per session", "Start short if you're new to compression, build up."),
    ("1.54 kg", "Control unit", "Roughly 4 × 4.5 × 8.5 in. It goes in a kit bag."),
    ("Bluetooth", "App control", "Set pressure and time from the unit or the Hyperice app."),
]
specs = "\n".join(f'<div class="spec rv"><b>{esc(a)}</b><span>{esc(b)}</span><small>{esc(c)}</small></div>'
                  for a, b, c in SPECS)

WHO = [
    ("Cyclists", "Back-to-back long rides where the legs never fully clear between sessions."),
    ("Hyrox &amp; CrossFit", "The particular kind of wrecked that comes from sled work and burpee broad jumps."),
    ("Runners", "Marathon blocks where weekly volume outpaces what passive rest can absorb."),
    ("On your feet all day", "Surgeons, chefs, nurses, retail. You don't have to be an athlete to have heavy legs."),
]
who = "\n".join(f'<div class="who-c rv"><b>{a}</b><p>{b}</p></div>' for a, b in WHO)

AUTH = [
 ("m12 3 8 3.4v5.2c0 4.6-3.2 8.2-8 9.4-4.8-1.2-8-4.8-8-9.4V6.4Z M9 12l2 2 4-4",
  "2-year India warranty", "Authorised Hyperice partner. Warranty honoured here, not voided by a grey import."),
 ("M3 8h11v8H3z M14 11h4l3 3v2h-7z M7 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z M17 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z",
  "Ships from Gurugram", "Held in stock in India. No customs, no six-week wait, no import paperwork."),
 ("M3 7h18v11H3z M3 11h18 M7 15h4",
  "GST invoice included", "Priced GST-inclusive, invoiced properly. Claim it if you're buying through a business."),
 ("M21 12a9 9 0 1 1-3.2-6.9L21 4 M12 8v4l3 2",
  "Indian technical support", "A real team that knows the device, in your timezone, after you've bought it."),
]
auth = "\n".join(f'''<div class="auth-i rv"><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="{p_}"/></svg>
   <b>{esc(t)}</b><p>{esc(b)}</p></div>''' for p_, t, b in AUTH)

FAQ = [
 ("What does ZoneBoost actually do?",
  "It raises compression in one chosen zone — usually the calves or thighs — instead of treating the whole leg identically. Useful when one area is doing the complaining."),
 ("How long should a session be?",
  "Most people run 20–45 minutes. If you've never used compression before, start shorter and build up rather than going straight to the top setting."),
 ("Is this the same unit sold internationally?",
  "Yes. It's the current Normatec 3 hardware, supplied through Hyperice's authorised channel, with a 2-year warranty valid in India."),
 ("Can I use it while travelling?",
  "It runs on an internal battery for 3+ hours per charge and the control unit is about 1.54 kg, so it travels. That's much of the point of the 3 over older wired systems."),
 ("How is this different from cheaper compression boots?",
  "Pressure accuracy and the sequence. Budget units inflate zones roughly and often all at once. Normatec's patented pulse holds each zone while the next engages, which is what keeps fluid moving one direction."),
]
faq = "\n".join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)

# The live product page sells this as a PREORDER with a stated ship date —
# not "out of stock". Confirmed on wodarmour.in/products/normatec-3.
PREORDER_DATE = "30 August 2026"
STOCK_NOTE = "" if IN_STOCK else (
  f'\n<!-- Variant reads available:false, but the live page takes PREORDERS '
  f'shipping {PREORDER_DATE}. CTAs reflect that. -->')
CTA = "Add to cart" if IN_STOCK else "Pre-order now"
SHIP_LINE = "In stock · ships within 48 working hours" if IN_STOCK else f"Pre-order · ships {PREORDER_DATE}"

# Judge.me, read off the live product page
RATING, NREV = "4.6", 178
stars = ('<div class="stars"><span aria-hidden="true">★★★★★</span>'
         f'<b>{RATING}</b><span class="sr">out of 5</span>'
         f'<a href="{BASE}/products/{HANDLE}#judgeme_product_reviews">{NREV} reviews</a></div>')

HTML = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Normatec 3 Legs — Compression Recovery Boots India | WOD Armour</title>
<meta name="description" content="Hyperice Normatec 3 Legs in India — 7 compression levels, 30–110 mmHg, ZoneBoost, app control. Authorised Hyperice partner, 2-year warranty, ships from Gurugram.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="normatec.css">
</head><body>{STOCK_NOTE}

<header class="hdr" id="hdr"><div class="hdr-in">
  <a href="index.html" class="logo"><img class="lg-light" src="assets/logo-light.png" alt="WOD Armour"><img class="lg-dark" src="assets/logo.png" alt=""></a>
  <div class="hdr-right">
    <a class="hdr-back" href="{BASE}/collections/normatec">All Normatec →</a>
  </div>
</div></header>

<!-- 01 · HERO -->
<section class="hero" id="hero"><div class="hero-stick">
  <div class="hero-fb" id="nmFb"></div>
  <canvas id="nmScrub"></canvas>
  <div class="hero-scrim"></div><div class="hero-scrim2"></div>
  <div class="hero-copy">
    <div class="hbeat on" data-beat="0">
      <div class="eyebrow">Hyperice · Normatec 3</div>
      <h1>Twenty minutes<br>and your legs<br><em>start again.</em></h1>
      <p>Clinic-grade dynamic air compression. The recovery system professional sport actually uses.</p>
    </div>
    <div class="hbeat" data-beat="1">
      <div class="eyebrow">How it works</div>
      <h1>Pressure that<br>only moves<br><em>one way.</em></h1>
      <p>Overlapping chambers pulse in sequence from foot to thigh, so nothing falls back down the leg.</p>
    </div>
    <div class="hbeat" data-beat="2">
      <div class="eyebrow">Authorised Hyperice partner · 2-year India warranty</div>
      <h1>Normatec 3<br><em>Legs.</em></h1>
      {stars}
      <div class="hero-buy">
        <span class="hero-price">{inr(PRICE)}<s>{inr(WAS)}</s></span>
        <a class="btn btn-primary" href="{BASE}/products/{esc(HANDLE)}">{CTA}</a>
        <a class="btn btn-ghost" href="#how">See how it works</a>
      </div>
      <p class="ship-line">{SHIP_LINE} · free shipping pan-India · GST invoice</p>
    </div>
  </div>
  <div class="cue">Scroll <i></i></div>
</div></section>

<!-- 02 · STATEMENT -->
<section class="sec stmt"><div class="wrap"><div class="stmt-grid">
  <h2 class="rv">Your legs don't get lighter because you sat down. They get lighter because <span>something moved the fluid out.</span></h2>
  <p class="lede rv">That's the whole argument for compression. Passive rest waits. Dynamic compression does the work — pneumatic chambers pushing in a fixed direction, ankle to hip, for as long as you set it.</p>
</div></div></section>

<!-- 03 · THE PULSE -->
<section class="sec pulse" id="how"><div class="wrap">
  <div class="eyebrow rv">The mechanism</div>
  <h2 class="h-sec rv">Five zones,<br>in order, every time</h2>
  <p class="lede rv" style="margin-top:18px">Normatec's patented Pulse technology holds each zone under pressure while the next one engages above it. Cheap boots inflate everything at once — which lets fluid slide straight back where it came from.</p>
  <div class="pulse-grid">
    <div class="leg-wrap rv">{leg_svg}</div>
    <div class="steps rv">{steps}</div>
  </div>
</div></section>

<!-- 04 · SPECS -->
<section class="sec"><div class="wrap">
  <div class="eyebrow rv">The numbers</div>
  <h2 class="h-sec rv" style="margin-bottom:clamp(28px,4vw,48px)">What you're<br>actually buying</h2>
  <div class="specs">{specs}</div>
</div></section>

<!-- 05 · ZONEBOOST -->
<section class="sec zb"><div class="wrap"><div class="zb-grid">
  <div class="zb-img rv"><img src="{esc(img(0))}" alt="Normatec 3 Legs in use" loading="lazy"></div>
  <div class="rv">
    <div class="eyebrow">ZoneBoost™</div>
    <h2 class="h-sec" style="margin:10px 0 16px">Treat the leg<br>that's complaining</h2>
    <p class="lede">Most sessions don't need uniform pressure. ZoneBoost raises compression in one specific zone — the calves after a long ride, the thighs after squats — while the rest of the leg runs normally.</p>
    <p class="lede" style="margin-top:16px">Set it on the unit, or from the Hyperice app over Bluetooth without getting up.</p>
  </div>
</div></div></section>

<!-- 06 · WHO -->
<section class="sec"><div class="wrap">
  <div class="eyebrow rv">Who buys one</div>
  <h2 class="h-sec rv" style="margin-bottom:clamp(28px,4vw,48px)">Not only<br>athletes</h2>
  <div class="who">{who}</div>
</div></section>

<!-- 07 · AUTHORISED -->
<section class="sec auth"><div class="wrap">
  <div class="eyebrow rv">Buying it here</div>
  <h2 class="h-sec rv" style="margin-bottom:clamp(28px,4vw,48px)">Authorised,<br>not imported</h2>
  <div class="auth-grid">{auth}</div>
</div></section>

<!-- 08 · FAQ -->
<section class="sec"><div class="wrap">
  <div class="eyebrow rv">Before you buy</div>
  <h2 class="h-sec rv" style="margin-bottom:clamp(24px,3vw,40px)">Questions<br>worth asking</h2>
  <div class="faq">{faq}</div>
</div></section>

<!-- 09 · CLOSE -->
<section class="sec close"><div class="wrap">
  <div class="eyebrow rv">Normatec 3 Legs</div>
  <h2 class="rv">Stop waiting<br>for your legs</h2>
  <p class="rv">Authorised Hyperice partner. Two-year India warranty. Ships from Gurugram.</p>
  <div class="rv" style="display:flex;justify-content:center;margin-top:22px">{stars}</div>
  <div class="close-price rv">{inr(PRICE)}<s>{inr(WAS)}</s></div>
  <a class="btn btn-primary rv" href="{BASE}/products/{esc(HANDLE)}">{CTA}</a>
  <!-- VERIFY: confirm no-cost EMI is offered before this line ships -->
  <small class="rv">{SHIP_LINE} · Save {inr(SAVE)} · GST invoice included</small>
</div></section>

<div class="buybar" id="buybar">
  <div class="bb-p">{inr(PRICE)}<s>{inr(WAS)}</s></div>
  <a class="btn btn-primary" href="{BASE}/products/{esc(HANDLE)}">{CTA}</a>
</div>

<footer class="ftr"><div class="wrap">
  <img src="assets/logo.png" alt="WOD Armour">
  <p>India's authorised store for recovery technology · <a href="tel:+918448866514">+91 84488 66514</a> · <a href="mailto:Sales@wodarmour.in">Sales@wodarmour.in</a></p>
</div></footer>

<script src="nm-frames.js"></script>
<script src="normatec.js"></script>
</body></html>'''

open('normatec.html', 'w').write(HTML)
print(f"normatec.html written — {len(HTML):,} bytes | in_stock={IN_STOCK} | {inr(PRICE)} was {inr(WAS)}")
