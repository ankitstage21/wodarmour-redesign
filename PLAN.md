# WOD Armour — Homepage Redesign Plan

**Positioning (locked):** India's official authorised store for recovery technology.
**Scope (locked):** Homepage only, incl. header + footer. 3D scroll-scrubbed hero.
**Mode (locked):** Light throughout — the hero is the only dark section.
**Delivery (locked):** Design first as a real, viewable local page → approve → port to Shopify (District, theme id 159497322712).

---

## 1. Diagnosis of the current page

| Problem | Evidence on the live site |
|---|---|
| Default-theme placeholders shipped to production | "Your collection's name" appears ~18× ; headings read "Collection", "Featured collection" (×2), "All Collection" |
| Six near-identical grids | 6 of 13 sections are the same product/collection grid component |
| Duplicate merchandising | Therabody, Hyperice, Garmin, Blazepod appear in both the top collection list and "All Collection" |
| Positioning collision | ₹2,49,990 Concept2 Strength ERG sits in the same scroll as a ₹999 crop tee, with no separation |
| The biggest asset is invisible | "Authorised Reseller" appears only inside a collection *title*, never as a trust claim |
| No consideration path for high AOV | No EMI, warranty, shipping, returns, comparison, or "help me choose" for a ₹65k purchase |
| Social proof unused | 16 reviews on the Normatec Hips are buried; Virat Kohli + Ronaldo imagery carries no claim |
| No email capture | Zero list-building on a 9,650px page |
| Mobile hero broken | Headline overlaps the product's own NORMATEC wordmark, no scrim → unreadable; ~400px dead space below hero |

Page is 9,650px tall with 99 images and does roughly three jobs badly instead of eight jobs well.

---

## 2. New homepage architecture

Nine sections, each with a distinct job. Order: **claim authority → sell the flagship → show the catalogue → help them choose → prove it.**

**01 · Scroll-scrubbed hero** — the only dark section. Canvas frame-scrub over ~250vh, three copy beats. Desktop runs 175 frames at 16:9; phones get an 88-frame portrait crop of the same take. Poster-frame fallback on `prefers-reduced-motion`. See HERO-STORYBOARD.md.

**02 · Authority strip** — authorised-partner wordmarks + genuine-warranty line. The moat: grey-market importers cannot copy it.

**03 · Flagship spotlight — Normatec 3 Legs** — editorial treatment, real price, saving, EMI line.

**04 · Brand shelves** — Therabody / Hyperice / Concept2 as three *differentiated* rows, not three copies of one grid.

**05 · "Or start from what hurts"** — 4 goal cards (heavy legs / soreness / heat-cold / train-measure). Sits below the catalogue as a fallback path for anyone who didn't find their brand.

**06 · Proof** — real pull-quote from the Hyrox JetBoots review + three stats.

**07 · WOD Armour gear** — house brand walled off with a red rule and diagonal texture, so a ₹999 tee never competes with a ₹2.5L erg.

**08 · Buying guides** — the three existing blog posts as consideration content.

**09 · Email capture + footer.**

*Cut from the original plan on request: the "Why buy here" trust bar. Its warranty/EMI/shipping content now lives in the authority strip and the flagship block.*

## 3. Design system

- **Palette:** near-black ground, warm off-white, WOD Armour red as a single accent (sampled from the logo). Premium-clinical for the device world; the gear shelf gets a grittier variant.
- **Type:** wide/condensed display face for headlines (athletic authority) + clean sans for body. Replaces IBM Plex Sans throughout.
- **Cards:** one product card, one collection card, one goal card — three components, not six variants.
- **Motion:** Lenis smooth scroll, reveal-on-enter, canvas scrub for the hero only. Everything respects `prefers-reduced-motion`.
- **Mobile first** — India ecommerce is mobile-dominant and the current mobile hero is the worst thing on the site.

---

## 4. Build

Static HTML/CSS/JS at `~/wodarmour-redesign`, served locally via `.claude/launch.json` (no deploy — local only until approved). Real product data, prices and images pulled from the live Shopify store so the page reads as the actual shop, not lorem ipsum. Structured in section blocks that map 1:1 onto Liquid sections for the later port.

---

## 5. Open decision: hero footage

The site has **no video today** — the hero is two static JPEGs. A scroll-scrub hero needs a frame sequence. See chat for options.
