# WOD Armour — homepage redesign (design preview)

A working redesign of the [wodarmour.in](https://www.wodarmour.in) homepage, built as a real
browsable page rather than a flat mockup. Product names, prices and images are pulled from the
live Shopify store, so it reads as the actual shop.

**This is a design preview, not a live storefront.** All product links point back to
wodarmour.in. Nothing here takes orders.

### Positioning
India's official authorised store for recovery technology — leading with the authorised-reseller
story (Therabody, Hyperice/Normatec, Concept2, Garmin, Polar) rather than the house apparel line.

### Structure
Nine sections, each with a distinct job, ordered *claim authority → sell the flagship →
show the catalogue → help them choose → prove it*:

1. Scroll-scrubbed hero (the only dark section)
2. Authority strip — authorised partners + genuine-warranty line
3. Flagship spotlight — Normatec 3 Legs
4. Brand shelves — Therabody / Hyperice / Concept2, differentiated
5. "Or start from what hurts" — shop by need
6. Proof — real customer pull-quote
7. WOD Armour gear — house brand, visually walled off
8. Buying guides
9. Email capture + footer

The original page was 13 sections, six of which were the same product grid, still carrying the
theme's `Your collection's name` placeholders in ~18 places.

### The hero
A canvas frame-sequence scrub over ~250vh with three copy beats. Desktop plays 175 frames at
16:9; phones get an 88-frame portrait crop of the same take (cover-cropping 16:9 into a tall
viewport upscales it ~2.3× and looks blocky). `prefers-reduced-motion` gets a still poster and
skips all preloading. See [HERO-STORYBOARD.md](HERO-STORYBOARD.md).

### Files
| | |
|---|---|
| `index.html` | generated — do not hand-edit |
| `build.py` | generates `index.html` from `data.json`; sections map 1:1 onto Liquid |
| `styles.css` | design system (light, one dark hero) |
| `app.js` | hero scrub, copy beats, scroll reveals |
| `data.json` | curated product data pulled from the live store |
| `PLAN.md` | diagnosis of the current site + the redesign rationale |

Rebuild with `python3 build.py`. Run locally with `python3 -m http.server 4620`.

### Copy still to verify
Three commercial claims in the page are placeholders pending confirmation:
no-cost EMI, the free-shipping threshold, and exactly which brands WOD Armour is
contractually authorised to sell.
