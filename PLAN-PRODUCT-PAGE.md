# Normatec 3 Legs — 3D product landing page, integrated into Shopify

**Brief (from WOD Armour):** a mobile-friendly 3D landing page for one product, integrated into Shopify.
**Product:** Hyperice Normatec 3 Legs — ₹99,980 (was ₹1,20,999)
**Approach:** rotatable 3D model + AR, opened by a scroll-scrubbed cinematic hero.

---

## Short answer: yes, and Shopify supports most of it natively

Verified against Shopify's own docs, not assumed:

| Capability | Status |
|---|---|
| 3D model as product media | Native — `Model3d`, **GLB + USDZ, up to 500 MB** |
| Rotatable viewer | Native — `model_viewer_tag` Liquid filter, `camera-controls` on by default |
| AR "view in your room" | Native — Shopify-XR library → **AR Quick Look (iOS) / Scene Viewer (Android)** |
| Device support | iOS 13+, Android 9+ |
| Custom page structure | JSON templates, up to 25 sections each |

That last row matters: **AR is the thing a flat page can't do.** Someone deciding on a ₹99,980 pair of
boots can stand them on their own floor at true scale. That is a materially better mobile experience
than any scroll animation, and it costs less to load.

---

## How it plugs into Shopify

Build on a **duplicate of the live District theme** (District 7.1.1, theme id 159497322712):

1. Duplicate the theme — the live store is never touched
2. Add a custom page template (`page.normatec.json`) plus purpose-built sections
3. Upload the GLB as product media on the Normatec 3 Legs product
4. Hero frames go to **Shopify Files** (the content CDN), not theme assets
5. Share the theme preview URL for approval
6. Publish — one click, instantly revertible

### One constraint worth knowing up front
The theme `assets/` directory **does not support subdirectories** — every file sits flat. So the
homepage's `assets/frames/f_0001.jpg …` pattern can't move across as-is. Frames go to Shopify Files,
or get bundled into a handful of sprite sheets. Decided now rather than discovered late.

---

## Page structure

1. **Scroll-scrub hero** — 3s of cinematic, resolving on the product
2. **The model** — rotatable, pinch-zoom, with a prominent *View in your room* button on supported devices
3. **How it works** — the pulse sequence, zone by zone
4. **What it's for** — cyclists, Hyrox, marathon, standing all day
5. **Authorised** — warranty, service, GST invoice, genuine-vs-grey
6. **Specs + what's in the box**
7. **Proof** — the Hyrox review, reviews
8. **Buy** — price, EMI, add to cart, sticky on mobile

---

## Mobile-first engineering rules

- Poster image is the LCP element — never the model, never the scrub
- 3D loads **after** first paint, and only on viewport entry
- Honour `save-data` and `prefers-reduced-motion`: static hero, model on tap only
- Target: interactive well before the GLB finishes downloading
- Test target is a mid-range Android on 4G, not a MacBook

---

## The one real dependency: the GLB

Ranked by preference:

1. **Ask Hyperice for the official model.** They supply asset kits to authorised resellers and
   already ship AR on their own storefront. Free, accurate, zero risk. **Ask this first.**
2. **Photogrammetry from real photos** — 20–30 shots around the product, if WOD Armour has a unit
   in Gurgaon. Slow but accurate.
3. **AI image-to-3D — TESTED, FAILED.** Tripo H3.1, 9 credits. Result in `models/normatec-test.glb`,
   four rendered views in `models/normatec-test-views.jpg`. It is not usable:
   - **The human is baked into the geometry.** The model fused the person's forearm and hand from the
     source photo into the mesh as solid geometry.
   - **The branding is mirrored.** With only one view, the model mirrors the front texture onto the
     back — "Normatec" reads backwards from two of four angles.
   - **There is no back.** Rotating 180° reveals a formless hollow shell; the mesh is a relief lifted
     from the photograph, not a solid object.
   - **55 MB, 1.97 million triangles** — roughly 40x too heavy for mobile even if the shape were right.

   The failure is the source imagery, not the model choice. Single-image 3D needs one isolated object
   on a plain background; every Normatec photo the store has is a lifestyle shot with a person in it.
   Multi-view generation would improve it, but that needs the photos that don't exist yet.

With option 3 now ruled out by testing, this comes down to **option 1 or 2 — both of which need
WOD Armour or Hyperice to supply something.** There is no route to an accurate model from the assets
that exist today.

If neither lands, the honest fallback is a **360° turntable** — 36 real photos of the actual product,
scrubbed on drag. It rotates, it is genuinely accurate, it needs no geometry, and it works on any
phone. It just can't do AR. For an authorised reseller, an accurate turntable beats an invented mesh
every time.

---

## Open questions for WOD Armour

- Does Hyperice supply a GLB to authorised resellers?
- Is there a Normatec 3 unit in Gurgaon we could photograph?
- Shopify collaborator access, or do they paste what we hand over?
- Same three claims still unconfirmed: **no-cost EMI**, **free-shipping threshold**,
  **which brands are contractually authorised**.
