#!/usr/bin/env python3
"""Generate Rebeca Elmúdesi logo SVGs (outlined paths) from TeX Gyre Heros.

Brand rules honoured: pure black/white, red (#fe0200) accent used sparingly,
sharp corners (no rounded), Helvetica letterforms. Wordmark = her name (she
said "no logo, just my name"); lettermark = the favicon `r.` mark.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))  # client root (_build/reviews -> ..-> _build -> ..-> root)
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(ROOT, "_build", "staged", "phase2-identity", "logos")
os.makedirs(OUT, exist_ok=True)

RED = "#fe0200"
BLACK = "#000000"
WHITE = "#ffffff"

_cache = {}
def load(weight):
    if weight not in _cache:
        fn = "texgyreheros-bold.otf" if weight == "bold" else "texgyreheros-regular.otf"
        f = TTFont(os.path.join(FONTS, fn))
        _cache[weight] = f
    return _cache[weight]

def shape(text, weight, upem_scale):
    """Return (paths, total_advance) at font units; one path per char with x offset."""
    font = load(weight)
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    x = 0.0
    chars = []
    for ch in text:
        gn = cmap.get(ord(ch))
        if gn is None:
            x += upem * 0.4
            continue
        pen = SVGPathPen(gs)
        gs[gn].draw(pen)
        d = pen.getCommands()
        adv = gs[gn].width
        chars.append((ch, d, x, adv))
        x += adv
    return chars, x, upem

def wordmark_svg(text, weight="regular", cap=100, color=BLACK,
                 accent_char=None, accent_color=RED, pad=40):
    """Render text as outlined paths. y-up font flipped to y-down SVG."""
    chars, total, upem = shape(text, weight, cap)
    scale = cap / 700.0  # ~cap height of Helvetica caps ≈ 700 upem units
    # Determine vertical bounds roughly: ascender ~ 1.0em above baseline
    asc = upem * 0.95
    desc = -upem * 0.30
    w = (total * scale) + pad * 2
    h = (asc - desc) * scale + pad * 2
    baseline = pad + asc * scale
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
             f'role="img" aria-label="{text}">']
    for ch, d, xoff, adv in chars:
        if not d:
            continue
        fill = accent_color if (accent_char and ch == accent_char) else color
        tx = pad + xoff * scale
        parts.append(
            f'<path transform="translate({tx:.2f} {baseline:.2f}) scale({scale:.5f} {-scale:.5f})" '
            f'fill="{fill}" d="{d}"/>')
    parts.append("</svg>")
    return "\n".join(parts)

def lettermark_svg(square=None, glyph_color=BLACK, dot_color=None, weight="bold",
                   size=240, pad_ratio=0.30):
    """`r.` lettermark. square=fill color for a sharp square container, or None for bare."""
    chars, total, upem = shape("r.", weight, size)
    # fit glyph into a centered box
    box = size
    inner = box * (1 - pad_ratio)
    scale = inner / 700.0
    gw = total * scale
    gh = 700 * scale  # cap-ish height for lowercase r ~ x-height; approximate
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}" '
             f'role="img" aria-label="r.">']
    if square:
        parts.append(f'<rect x="0" y="0" width="{box}" height="{box}" fill="{square}"/>')
    # baseline so glyph optically centers
    xstart = (box - gw) / 2
    baseline = box * 0.66
    for ch, d, xoff, adv in chars:
        if not d:
            continue
        fill = dot_color if (ch == "." and dot_color) else glyph_color
        tx = xstart + xoff * scale
        parts.append(
            f'<path transform="translate({tx:.2f} {baseline:.2f}) scale({scale:.5f} {-scale:.5f})" '
            f'fill="{fill}" d="{d}"/>')
    parts.append("</svg>")
    return "\n".join(parts)

def write(name, svg):
    p = os.path.join(OUT, name)
    with open(p, "w") as f:
        f.write(svg)
    print("wrote", name, f"({len(svg)} bytes)")

NAME = "Rebeca Elmúdesi"

# --- Wordmarks (primary identity carrier — "just my name") ---
write("wordmark-black.svg",        wordmark_svg(NAME, "regular", color=BLACK))
write("wordmark-white.svg",        wordmark_svg(NAME, "regular", color=WHITE))
write("wordmark-bold-black.svg",   wordmark_svg(NAME, "bold",    color=BLACK))
# red-accent: the final 'i' dot is impractical to isolate; use a trailing red period mark instead
write("wordmark-accent.svg",       wordmark_svg(NAME + ".", "regular", color=BLACK,
                                                accent_char=".", accent_color=RED))

# --- Lettermark `r.` (favicon-derived compact mark, SHARP corners per anti-pattern) ---
write("mark-bare-black.svg",       lettermark_svg(square=None, glyph_color=BLACK, weight="bold"))
write("mark-square-dark.svg",      lettermark_svg(square=BLACK, glyph_color=WHITE, weight="bold"))
write("mark-square-light.svg",     lettermark_svg(square=WHITE, glyph_color=BLACK, weight="bold"))
write("mark-reddot-light.svg",     lettermark_svg(square=None, glyph_color=BLACK, dot_color=RED, weight="bold"))
write("mark-square-reddot.svg",    lettermark_svg(square=BLACK, glyph_color=WHITE, dot_color=RED, weight="bold"))
print("done ->", OUT)
