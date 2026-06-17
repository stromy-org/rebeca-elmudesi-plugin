# Rebeca Elmúdesi — Brand Guidelines

> Visual artist — Madrid. *Quiet, editorial, gallery-neutral. Work rooted in looking.*
>
> Derived view of `charter.json` + `tokens.css`. The charter is the machine-readable
> source of truth; this document is the human-readable companion. Tier 1 (producer).

---

## 1. Foundation

| | |
|---|---|
| **Name** | Rebeca Elmúdesi *(always with the accent)* |
| **Practice** | Visual artist — contemporary painting (oil pastel, acrylic, mixed media) |
| **Based** | Madrid, Spain · b. Dominican Republic, 2003 |
| **Audience** | Collectors, galleries, curators, commission clients |
| **Archetype** | Creator / Sage |
| **Positioning** | Madrid-based visual artist presenting contemporary painting with curatorial restraint. |

**The brand in one line:** the work leads, the layout recedes. Everything here exists
to present paintings faithfully and get out of their way.

---

## 2. Logo system

Per the artist: *"No logo — it's just my name for now."* The identity is therefore a
**name wordmark** plus a compact **`r.` mark** derived from the website favicon.

| Asset | File | Use |
|---|---|---|
| **Primary wordmark** | `logos/wordmark.svg` | Helvetica regular, black on white. The main identity carrier — headers, mastheads, covers. |
| White wordmark | `logos/wordmark-white.svg` | For black / dark grounds only. |
| Accent wordmark | `logos/wordmark-accent.svg` | Wordmark with a single red period — for rare emphasis moments. |
| **Compact mark** | `logos/mark.svg` | `r.` — white on a **sharp** black square, period in red `#fe0200`. Avatars, stamps, document corners, watermark. |
| Mark (all black) | `logos/mark-black.svg` | When the red spark is unwanted. |
| Mark on dark | `logos/mark-on-dark.svg` | White square / black `r.` for placing on black. |
| Bare mark | `logos/mark-bare.svg` | Glyph only, no container. |
| PNG rasters | `logos/*.png` | For DOCX / PDF embedding (SVG not supported there). |

**Rules**
- Corners on the brand mark are **sharp**. (The rounded `rx=6` favicon in the website
  is kept *only* as the browser-tab icon — it is not part of this system, because
  rounded corners are an anti-pattern for this brand.)
- Give the wordmark generous clear space — at least the height of the cap "R" on every side.
- Never recolor the mark outside black / white / the red dot. Never add effects.
- Outlined paths — the SVGs carry no font dependency.

---

## 3. Color

A monochrome brand. Black and white do the work; red is a single, rare spark.

| Token | Hex | Role |
|---|---|---|
| Ink / primary | `#000000` | Text, rules, the wordmark |
| Ground | `#ffffff` | Every background — pure white, no alternates |
| Accent red | `#fe0200` | Used **sparingly** — the mark's period, a hairline, a link, one emphasis |
| Caption grey | `#b4b4b4` | Small text, measurements, dimensions, overlines |

- The red is an accent, not a theme. If a layout has more than one red element, it is
  probably one too many.
- No gradients, no tints, no second background. White ground, everywhere.

---

## 4. Typography

**Helvetica** throughout, shipped as the embeddable **TeX Gyre Heros** (`fonts/`,
regular + bold). One family for headings, body, and data.

- **Headings** — Helvetica, left-aligned. Regular weight is the default voice; bold only
  where hierarchy genuinely needs it.
- **Body** — Helvetica regular, **justified** (`--text-align-body: justify`), generous
  line-height (1.6).
- **Captions / measurements** — caption grey `#b4b4b4`, 12px, for titles, media, dimensions.
- Type scale runs 11px overline → 48px display; see `tokens.css` `--text-*`.

---

## 5. Layout principles

These are the brand. They come directly from the artist's brief.

1. **Spacious and curated.** Generous white space on a pure white ground; let air carry the emphasis.
2. **Thin, even margins on every side.** Page margin ≈ 18mm. **Nothing bleeds to the edge.**
3. **Justify body text.** Headings left-aligned.
4. **Hairline rules only.** 1px (0.5px thin) black rules to divide — never boxes, fills, or shadows.
5. **Mirror a professional art portfolio.** The website's sections define a document's sections.
6. **Square corners, no shadows.** `--radius: 0`, `--shadow: none` everywhere.

---

## 6. Imagery

The images **are** the brand — every one is Rebeca's own artwork (`images/`, catalogued
in `images/manifest.json` with verbatim title / medium / dimensions / year).

- **Reproduce faithfully** at true aspect ratio. `--image-fit: contain`. **Never crop,
  stretch, or distort** a work.
- **Never overlay** text, color, or the logo on an artwork.
- **Never bleed** an image to the page edge — it sits within the thin margins, room to breathe.
- **Attribute every image** to its correct title and caption. Never let a caption drift.
- No stock photography, no clip art, ever. Only her work.

---

## 7. Voice

Curatorial, not promotional — a wall label, not a sales pitch. Full profile in
`voice/voice-profile.md`; reference passages in `voice/voice-anchors.md`.

- **Source only from the artist's own input and website. Never invent copy** — no
  biography, interpretation, prices, or history that isn't on record.
- Preserve Spanish titles verbatim; English gloss only where she already gives one.
- No art-market hype ("stunning", "must-see", "visionary", "masterpiece").

---

## 8. Anti-patterns — never do these

- Full-bleed images, or any bleed to the page edge.
- Stretched or distorted images (any change to true aspect ratio).
- Drop shadows · rounded corners · clip art · stock photography.
- A second background color, gradients, or tints.
- Invented or unsourced titles, descriptions, or copy.
- Red used as anything more than a rare accent.
