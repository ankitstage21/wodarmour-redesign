# Hero Storyboard — "The Chamber"

**Status: LIVE = the empty-studio cut** (`assets/hero.mp4`).
A Normatec product cut was also generated and is kept at `assets/hero-normatec.mp4` — not currently wired in. Notes on it are at the bottom.

## Concept
Slow forward dolly through a dark recovery studio at night. Volumetric shafts cut low drifting haze; empty black treatment benches pass on both sides. Ahead, a lone athlete lies reclined in a pool of cool light, completely still, in near-silhouette with the face not readable. One warm red practical glows deep in the background, tying to the WOD Armour red.

## Beat map

| Scroll | Image | Copy overlay |
|---|---|---|
| 0–33% | Wide, deep, empty hall | "Recovery is the training you're not doing." |
| 33–66% | Mid-push, benches passing, shafts strongest | "Normatec / Theragun / Concept2 / Garmin" |
| 66–100% | Athlete resolves in light, camera settles | "Officially authorised in India." + CTA |

## Constraints it solves for
One unbroken take (a cut reads as a glitch when scrubbed), constant camera speed, a dark frame so white copy stays legible throughout, reserved negative space, and a stable final frame for the CTA. The face stays unreadable on purpose — it dodges AI-face uncanny valley. No recognisable branded device appears, which keeps the "authorised reseller" claim clear of any mangled-logo risk.

## Delivered sequences

| Variant | Frames | Size | Notes |
|---|---|---|---|
| `assets/frames/` | 175 @ 1152px | 3.4 MB | desktop 16:9 |
| `assets/frames-sm/` | 175 @ 640px | 1.5 MB | save-data / slow connections |
| `assets/frames-mb/` | 88 @ 540×960 | 1.0 MB | phones: portrait 9:16 centre crop |
| `assets/hero-poster*.jpg` | 1 each | 44 / 28 KB | `prefers-reduced-motion` still |

**The first 16 frames are trimmed** (`-ss 0.70`). The generation opens with hard black side-masking that clears around frame 16; starting there gives a clean full-bleed first frame.

Phones get a portrait crop rather than the 16:9 master — cover-cropping 16:9 into a tall viewport upscales it ~2.3× and looks blocky.

## Generation record
- Model: `gemini_omni` (Gemini Omni Flash) · 8s · 720p · 16:9 · 24 credits
- Text-only, no reference image
- Declined the suggested "IN THE DARK" preset — presets impose their own camera move, and the constant-speed dolly is what makes the scrub work.

---

## Unused alternate: the Normatec product cut

`assets/hero-normatec.mp4` — same studio, but the camera resolves on a pair of Normatec boots with the chambers pulsing, wordmark and Hyperice H mark legible. Generated with the store's own product photo as an `image_references` input, which is what kept the branding accurate. 24 credits, already spent. To wire it in, copy it over `assets/hero.mp4` and re-run the extraction (see git-free notes below).

Two things learned generating it, worth keeping:
1. Using the **lifestyle shot** (person reclining in a sheer jacket) as the reference returned **`nsfw`** — the filter reads reclining figures as suggestive; the prompt was not the problem. A **product-only reference** plus "No people" cleared it immediately.
2. On mobile the full push ends up *inside* one boot, clipping the wordmark. That cut had to stop at frame 130.
