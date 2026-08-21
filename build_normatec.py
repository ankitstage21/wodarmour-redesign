#!/usr/bin/env python3
"""normatec.html — short-form landing page with a real Shopify buy form."""
import json, re, html
import nm_data as D

BASE = "https://www.wodarmour.in"
p = json.load(open('nm3.json'))['product']
HANDLE = p['handle']
v = p['variants'][0]
VARIANT = v['id']
PRICE, WAS = float(v['price']), float(v['compare_at_price'])
IN_STOCK = v.get('available', False)   # products.json omits this; the live page sells it as pre-order

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
def img(i, w=1200):
    return re.sub(r'(\.(jpg|jpeg|png|webp))', r'_%dx\1' % w, p['images'][i]['src'].split('?')[0])

SAVE = int(WAS - PRICE)
PREORDER_DATE = "30 August 2026"
CTA        = "Add to cart" if IN_STOCK else "Pre-order now"
STOCK_LINE = "In stock · ships within 48 working hours" if IN_STOCK else f"Pre-order · ships {PREORDER_DATE}"

stars = ('<div class="stars"><span aria-hidden="true">★★★★★</span>'
         f'<b>{D.RATING}</b><span class="sr">out of 5</span>'
         f'<a href="#reviews">{D.NREV} reviews</a></div>')

def emi(mini=False):
    return (f'<div class="emi-card{" mini" if mini else ""} rv">'
      '<div class="emi-head"><b>EMI plans and Pay Later</b><i>powered by <strong>Razorpay</strong></i></div>'
      '<div class="emi-body">'
      f'<div class="emi-col"><h4>No cost EMI starting from {D.EMI_FROM}/mon</h4>'
      f'<div class="emi-banks"><i>H</i><i>A</i><i>I</i><i class="more">+{D.EMI_BANKS-3}</i></div>'
      f'<a class="emi-btn" href="{BASE}/products/{HANDLE}">View plans &rsaquo;</a></div>'
      '<div class="emi-col"><h4>Pay Later available at 0% interest</h4>'
      '<div class="emi-banks"><i>S</i></div>'
      f'<a class="emi-btn ghost" href="{BASE}/products/{HANDLE}">View options &rsaquo;</a></div>'
      '</div></div>')

# ── real Shopify add-to-cart form. Posts cross-domain to /cart/add and
#    lands the buyer in Shopify checkout. Becomes the Liquid product form on port.
def buy_form(btn_class="btn btn-primary"):
    return f'''<form class="buy-form" action="{BASE}/cart/add" method="post" enctype="multipart/form-data">
      <input type="hidden" name="id" value="{VARIANT}">
      <input type="hidden" name="return_to" value="/checkout">
      <div class="qty">
        <button type="button" data-step="-1" aria-label="Decrease quantity">−</button>
        <input type="number" name="quantity" value="1" min="1" aria-label="Quantity">
        <button type="button" data-step="1" aria-label="Increase quantity">+</button>
      </div>
      <button class="{btn_class}" type="submit">{CTA} — {inr(PRICE)}</button>
    </form>'''

TRUST = [
 ("m12 3 8 3.4v5.2c0 4.6-3.2 8.2-8 9.4-4.8-1.2-8-4.8-8-9.4V6.4Z M9 12l2 2 4-4", "Authorised Hyperice partner · 2-year India warranty"),
 ("M3 8h11v8H3z M14 11h4l3 3v2h-7z M7 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z M17 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z", "Free shipping pan-India, from Gurugram"),
 ("M3 7h18v11H3z M3 11h18 M7 15h4", "GST invoice included"),
 ("M21 12a9 9 0 1 1-3.2-6.9L21 4 M12 8v4l3 2", "Delivered in 2–6 working days"),
]
trust = "".join(f'<div><svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg><span>{esc(t)}</span></div>' for d, t in TRUST)

# ── pulse diagram ───────────────────────────────────────────────────
ZONES = [("Foot","The cycle starts at the foot, every time."),
         ("Ankle","Pressure holds below while the next zone engages."),
         ("Calf","Overlapping chambers stop fluid falling back down."),
         ("Knee","The wave keeps climbing; nothing below has released."),
         ("Thigh","The last zone fires, the leg releases, it begins again.")]
steps = "\n".join(f'<div class="step" data-step="{i}"><span class="n">Zone {i+1:02d}</span><b>{esc(n)}</b><span>{esc(t)}</span></div>'
                  for i,(n,t) in enumerate(ZONES))
zh, gap, top = 74, 9, 26
bands = []
for i,(n,_) in enumerate(ZONES):
    y = top + (len(ZONES)-1-i)*(zh+gap); w = 108 + i*9; x = 178 - w/2
    bands.append(f'<rect class="zone" data-zone="{i}" x="{x:.0f}" y="{y}" width="{w}" height="{zh}" rx="16"/>'
                 f'<text class="zone-label" data-zone="{i}" x="{x-14:.0f}" y="{y+zh/2+4:.0f}" text-anchor="end">{n.upper()}</text>')
leg_svg = (f'<svg class="leg" viewBox="0 0 300 {top*2+len(ZONES)*(zh+gap)}" xmlns="http://www.w3.org/2000/svg" '
           f'aria-label="Compression sequence, foot to thigh">{"".join(bands)}</svg>')

SPECS = [("7","Compression levels"),("30–110","mmHg range"),("3+ hrs","Battery"),
         ("20–45","Min per session"),("1.54 kg","Control unit"),("Bluetooth","App control")]
specs = "\n".join(f'<div class="spec rv"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in SPECS)
box_html = "\n".join(f'<li><span class="q">{q}&times;</span><div><b>{esc(n)}</b><span>{esc(t)}</span></div></li>'
                     for q,n,t in D.BOX)

_hdr  = "".join(f'<th class="{"me" if me else ""}">{l}</th>' for l,_,me,_ in D.COMPARE)
_price= "".join(f'<td class="{"me" if me else ""}"><span class="price">{pr}</span></td>' for _,pr,me,_ in D.COMPARE)
_rows = ""
for i,r in enumerate(D.COMPARE_ROWS):
    _rows += ('<tr><th scope="row">%s</th>%s</tr>' % (esc(r),
              "".join(f'<td class="{"me" if me else ""}">{esc(f[i])}</td>' for _,_,me,f in D.COMPARE)))
cmp_html = ('<table class="cmp"><thead><tr><th></th>'+_hdr+'</tr></thead><tbody><tr>'
            '<th scope="row">Price</th>'+_price+'</tr>'+_rows+'</tbody></table>')

hist_html = "".join(f'<div class="hist-row"><span>{s} &#9733;</span><div class="hist-bar">'
                    f'<i style="width:{n/D.NREV*100:.1f}%"></i></div><span>{n}</span></div>' for s,n in D.HIST)
rev_html = "\n".join(f'<div class="rev-c rv"><div class="st">{"&#9733;"*s}{"&#9734;"*(5-s)}</div><p>{esc(t)}</p>'
                     f'<cite>{esc(w)}<em>{esc(l)}</em></cite></div>' for s,t,w,l in D.REVIEWS)
faq = "\n".join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in D.FAQ)
strip = "".join(f'<figure class="rv"><img src="{esc(img(i))}" alt="{esc(c)}" loading="lazy"></figure>'
                for i,c in [(1,"Control unit"),(4,"Build quality"),(3,"App control"),(5,"Normatec 3")])

HTML = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Normatec 3 Legs — Compression Recovery Boots India | WOD Armour</title>
<meta name="description" content="Hyperice Normatec 3 Legs in India — 7 compression levels, 30–110 mmHg, ZoneBoost, app control. Authorised Hyperice partner, 2-year warranty, no-cost EMI from {D.EMI_FROM}/mon.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="normatec.css">
</head><body>

<header class="hdr" id="hdr"><div class="hdr-in">
  <a href="index.html" class="logo"><img class="lg-light" src="assets/logo-light.png" alt="WOD Armour"><img class="lg-dark" src="assets/logo.png" alt=""></a>
  <div class="hdr-right"><a class="hdr-back" href="{BASE}/collections/normatec">All Normatec →</a></div>
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
      <p>Clinic-grade dynamic air compression. Pressure that only moves one way — foot to thigh, never back.</p>
    </div>
    <div class="hbeat" data-beat="1">
      <div class="eyebrow">Authorised Hyperice partner · 2-year India warranty</div>
      <h1>Normatec 3<br><em>Legs.</em></h1>
      {stars}
      <div class="hero-buy">
        <span class="hero-price">{inr(PRICE)}<s>{inr(WAS)}</s></span>
        <a class="btn btn-primary" href="#buy">{CTA}</a>
      </div>
      <p class="ship-line">No-cost EMI from {D.EMI_FROM}/mon · {STOCK_LINE}</p>
    </div>
  </div>
  <div class="cue">Scroll <i></i></div>
</div></section>

<!-- 02 · BUY — real Shopify cart form -->
<section class="sec buy" id="buy"><div class="wrap"><div class="buy-grid">
  <div class="buy-media rv"><img src="{esc(img(0))}" alt="Normatec 3 Legs in use"></div>
  <div class="rv">
    <div class="eyebrow">Authorised Hyperice partner</div>
    <h1>Normatec 3 Legs</h1>
    {stars}
    <div class="price-row"><span class="price">{inr(PRICE)}</span>
      <span class="price-was">{inr(WAS)}</span><span class="price-save">Save {inr(SAVE)}</span></div>
    <div class="buy-meta"><span class="dot"></span>{esc(STOCK_LINE)}</div>
    {buy_form()}
    {emi(mini=True)}
    <div class="buy-trust">{trust}</div>
  </div>
</div>
<div class="strip rv" style="margin-top:clamp(26px,3.5vw,44px)">{strip}</div>
</div></section>

<!-- 03 · HOW IT WORKS -->
<section class="sec pulse" id="how"><div class="wrap">
  <div class="eyebrow rv">The mechanism</div>
  <h2 class="h-sec rv">Five zones,<br>in order, every time</h2>
  <p class="lede rv" style="margin-top:16px">Normatec's patented Pulse technology holds each zone under pressure while the next engages above it. Cheap boots inflate everything at once, which lets fluid slide straight back. <b style="color:#F4F2EF">ZoneBoost</b> adds extra pressure to one zone — calves after a ride, thighs after squats.</p>
  <div class="pulse-grid">
    <div class="leg-wrap rv">{leg_svg}</div>
    <div class="steps rv">{steps}</div>
  </div>
</div></section>

<!-- 04 · SPECS + BOX -->
<section class="sec"><div class="wrap">
  <div class="eyebrow rv">The detail</div>
  <h2 class="h-sec rv">Numbers, and<br>what's in the box</h2>
  <div class="sb-grid">
    <div>
      <div class="specs">{specs}</div>
      <!-- ⚠ PLACEHOLDER: box contents invented — confirm with WOD Armour -->
      <ul class="box-list rv" style="margin-top:26px">{box_html}</ul>
    </div>
    <div class="box-img rv"><img src="{esc(img(2))}" alt="Everything included in the box" loading="lazy"></div>
  </div>
</div></section>

<!-- 05 · COMPARISON — ⚠ PLACEHOLDER feature deltas; prices are real -->
<section class="sec zb"><div class="wrap">
  <div class="eyebrow rv">Honestly compared</div>
  <h2 class="h-sec rv">Is this the<br>right one?</h2>
  <p class="lede rv" style="margin-top:16px">The Elite is wireless and costs ₹29,010 more. If the hose would irritate you, buy that instead.</p>
  <div class="cmp-wrap rv" style="margin-top:clamp(24px,3vw,40px)">{cmp_html}</div>
</div></section>

<!-- 06 · REVIEWS — score + histogram REAL; ⚠ quotes are PLACEHOLDER -->
<section class="sec" id="reviews"><div class="wrap">
  <div class="eyebrow rv">What buyers say</div>
  <h2 class="h-sec rv" style="margin-bottom:clamp(26px,3.5vw,44px)">178 people<br>already own one</h2>
  <div class="rev-top">
    <div class="rev-score rv"><b>{D.RATING}</b><span class="st">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
      <span>Based on {D.NREV} verified reviews</span></div>
    <div class="hist rv">{hist_html}</div>
  </div>
  <div class="rev-grid">{rev_html}</div>
</div></section>

<!-- 07 · FAQ — ⚠ PLACEHOLDER answers incl. sizing, returns, contraindications -->
<section class="sec care"><div class="wrap">
  <div class="eyebrow rv">Before you buy</div>
  <h2 class="h-sec rv" style="margin-bottom:clamp(22px,3vw,36px)">Questions<br>worth asking</h2>
  <div class="faq">{faq}</div>
</div></section>

<!-- 08 · CLOSE -->
<section class="sec close"><div class="wrap">
  <div class="eyebrow rv">Normatec 3 Legs</div>
  <h2 class="rv">Stop waiting<br>for your legs</h2>
  <div class="rv" style="display:flex;justify-content:center;margin-top:20px">{stars}</div>
  <div class="close-price rv">{inr(PRICE)}<s>{inr(WAS)}</s></div>
  <div class="rv" style="max-width:460px;margin:22px auto 0">{buy_form()}</div>
  <small class="rv">{esc(STOCK_LINE)} · No-cost EMI from {D.EMI_FROM}/month · GST invoice included</small>
</div></section>

<div class="buybar" id="buybar">
  <div class="bb-p">{inr(PRICE)}<s>{inr(WAS)}</s></div>
  <form action="{BASE}/cart/add" method="post" enctype="multipart/form-data" style="margin-left:auto">
    <input type="hidden" name="id" value="{VARIANT}">
    <input type="hidden" name="quantity" value="1">
    <input type="hidden" name="return_to" value="/checkout">
    <button class="btn btn-primary" type="submit">{CTA}</button>
  </form>
</div>

<footer class="ftr"><div class="wrap">
  <img src="assets/logo.png" alt="WOD Armour">
  <p>India's authorised store for recovery technology · <a href="tel:+918448866514">+91 84488 66514</a> · <a href="mailto:Sales@wodarmour.in">Sales@wodarmour.in</a></p>
</div></footer>

<script src="nm-frames.js"></script>
<script src="normatec.js"></script>
</body></html>'''

open('normatec.html','w').write(HTML)
print(f"normatec.html — {len(HTML):,} bytes | variant {VARIANT} | {CTA}")
