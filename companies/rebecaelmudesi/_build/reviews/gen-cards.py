#!/usr/bin/env python3
"""Finished, on-brand business card for Rebeca Elmúdesi.
EU 85×55mm trim + 3mm bleed = 91×61mm. Content kept inside a 3mm safe margin.
Embeds the outlined wordmark / r. mark (no font dependency); contact set in Helvetica.
Épuré: white front (name + practice + contact), black back (centered r. mark)."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOGOS = os.path.join(ROOT, "logos")
OUT = os.path.join(ROOT, "business-cards", "source")
os.makedirs(OUT, exist_ok=True)

def inner(fn):
    """Return (inner_markup, vbw, vbh) of a logo SVG, stripped of its outer <svg> tag."""
    s = open(os.path.join(LOGOS, fn)).read()
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    vbw, vbh = float(m.group(1)), float(m.group(2))
    body = re.sub(r'^.*?<svg[^>]*>', '', s, count=1, flags=re.S)
    body = re.sub(r'</svg>\s*$', '', body, flags=re.S)
    return body, vbw, vbh

def nested(fn, x, y, w):
    body, vbw, vbh = inner(fn)
    h = w * vbh / vbw
    return f'<svg x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" viewBox="0 0 {vbw} {vbh}" overflow="visible">{body}</svg>', h

# canvas in mm
BLEED, TRIM_W, TRIM_H = 3, 85, 55
W, H = TRIM_W + 2*BLEED, TRIM_H + 2*BLEED  # 91 x 61
SAFE = BLEED + 4  # content margin from bleed edge ≈ inner 4mm past trim start

def card(bg, fg, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="Rebeca Elmúdesi business card">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            # trim guide (non-printing reference; remove for final print PDF/X)
            f'<rect x="{BLEED}" y="{BLEED}" width="{TRIM_W}" height="{TRIM_H}" fill="none" '
            f'stroke="{fg}" stroke-width="0.1" stroke-dasharray="0.8 0.8" opacity="0.18"/>'
            + body + '</svg>')

HEL = "Helvetica, Arial, sans-serif"

# ---- FRONT: white ground ----
wm, wmh = nested("wordmark.svg", SAFE, SAFE+2, 46)         # ~46mm wide wordmark
front_body = (
    wm
    + f'<text x="{SAFE}" y="{SAFE+2+wmh+5}" font-family="{HEL}" font-size="3.0" fill="#b4b4b4">Visual artist — Madrid</text>'
    # bottom hairline + contact
    + f'<line x1="{SAFE}" y1="{H-SAFE-6}" x2="{W-SAFE}" y2="{H-SAFE-6}" stroke="#000" stroke-width="0.2"/>'
    + f'<text x="{SAFE}" y="{H-SAFE-2}" font-family="{HEL}" font-size="2.7" fill="#000">'
      f'rebeca.elmudesi@gmail.com<tspan fill="#b4b4b4">   ·   </tspan>@elmudesi.studio</text>'
)
mk, mkh = nested("mark.svg", W-SAFE-9, H-SAFE-6-9-3, 9)    # r. mark above the rule, right
front_body += mk

# ---- BACK: black ground, centered r. mark (white square) ----
mb, mbh = nested("mark-on-dark.svg", (W-16)/2, (H-16)/2, 16)
back_body = mb

open(os.path.join(OUT, "rebeca-card-eu-front.svg"), "w").write(card("#ffffff", "#000000", front_body))
open(os.path.join(OUT, "rebeca-card-eu-back.svg"),  "w").write(card("#000000", "#ffffff", back_body))
print("wrote rebeca-card-eu-front.svg + rebeca-card-eu-back.svg ->", OUT)
