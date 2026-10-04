#!/usr/bin/env python3
"""Generate Marin skincare placeholder packshots (800x800 SVG)."""
import os, sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif"


def shade(hex_, f):
    h = hex_.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 0:
        r, g, b = (round(c + (255 - c) * f) for c in (r, g, b))
    else:
        r, g, b = (round(c * (1 + f)) for c in (r, g, b))
    return '#%02X%02X%02X' % (r, g, b)


def label(cx, y, w, h, name, sub, ink, paper, small=False):
    """Centered label panel with brand, name (1-2 lines) and subtitle."""
    lines = name.split('\n')
    fs = 26 if not small else 20
    out = [f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="6" fill="{paper}" opacity=".94"/>']
    ty = y + (h * 0.26)
    out.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-family="{FONT}" font-size="{12 if not small else 10}" '
               f'letter-spacing="4" font-weight="700" fill="{ink}" opacity=".7">MARIN</text>')
    out.append(f'<line x1="{cx - 14}" y1="{ty + 10}" x2="{cx + 14}" y2="{ty + 10}" stroke="{ink}" opacity=".35"/>')
    ny = ty + 14 + fs
    for ln in lines:
        out.append(f'<text x="{cx}" y="{ny}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" '
                   f'font-weight="500" fill="{ink}">{escape(ln)}</text>')
        ny += fs + 4
    out.append(f'<text x="{cx}" y="{y + h - 14}" text-anchor="middle" font-family="{FONT}" font-size="{11 if not small else 9}" '
               f'letter-spacing="2" fill="{ink}" opacity=".6">{escape(sub)}</text>')
    return '\n'.join(out)


def jar(c, name, sub, scale=1.0, cx=400, base=630, small=False):
    body, lid, ink, paper = c['body'], c['lid'], c['ink'], c['paper']
    return f'''<g transform="translate({cx} {base}) scale({scale}) translate(-400 -630)">
<ellipse cx="400" cy="634" rx="190" ry="20" fill="#000" opacity=".16" filter="url(#blur)"/>
<rect x="268" y="398" width="264" height="232" rx="30" fill="{body}"/>
<rect x="268" y="398" width="264" height="232" rx="30" fill="url(#glassL)"/>
<rect x="250" y="322" width="300" height="88" rx="16" fill="{lid}"/>
<rect x="250" y="322" width="300" height="88" rx="16" fill="url(#glassL)"/>
<rect x="250" y="398" width="300" height="12" fill="#000" opacity=".12"/>
<g stroke="#000" opacity=".1" stroke-width="2">{''.join(f'<line x1="{x}" y1="334" x2="{x}" y2="398"/>' for x in range(270, 540, 14))}</g>
{label(400, 440, 200, 150, name, sub, ink, paper, small)}
</g>'''


def tube(c, name, sub, scale=1.0, cx=400, base=630):
    body, lid, ink, paper = c['body'], c['lid'], c['ink'], c['paper']
    return f'''<g transform="translate({cx} {base}) scale({scale}) translate(-400 -630)">
<ellipse cx="400" cy="634" rx="120" ry="16" fill="#000" opacity=".16" filter="url(#blur)"/>
<path d="M312 140 H488 L492 500 Q492 566 460 566 H340 Q308 566 308 500 Z" fill="{body}"/>
<path d="M312 140 H488 L492 500 Q492 566 460 566 H340 Q308 566 308 500 Z" fill="url(#glassL)"/>
<rect x="312" y="124" width="176" height="28" rx="4" fill="{shade(body, -.14)}"/>
<g stroke="#000" opacity=".16" stroke-width="2">{''.join(f'<line x1="{x}" y1="128" x2="{x}" y2="150"/>' for x in range(322, 484, 10))}</g>
<rect x="334" y="562" width="132" height="70" rx="12" fill="{lid}"/>
<rect x="334" y="562" width="132" height="70" rx="12" fill="url(#glassL)"/>
{label(400, 230, 150, 250, name, sub, ink, paper)}
</g>'''


def dropper(c, name, sub, scale=1.0, cx=400, base=630):
    body, lid, ink, paper = c['body'], c['lid'], c['ink'], c['paper']
    return f'''<g transform="translate({cx} {base}) scale({scale}) translate(-400 -630)">
<ellipse cx="400" cy="634" rx="130" ry="17" fill="#000" opacity=".16" filter="url(#blur)"/>
<rect x="296" y="352" width="208" height="278" rx="34" fill="{body}"/>
<rect x="296" y="352" width="208" height="278" rx="34" fill="url(#glassL)"/>
<rect x="352" y="318" width="96" height="40" rx="6" fill="{body}"/>
<rect x="338" y="262" width="124" height="64" rx="10" fill="{lid}"/>
<rect x="338" y="262" width="124" height="64" rx="10" fill="url(#glassL)"/>
<path d="M368 266 V196 Q368 130 400 130 Q432 130 432 196 V266 Z" fill="{shade(lid, -.1)}"/>
<path d="M368 266 V196 Q368 130 400 130 Q432 130 432 196 V266 Z" fill="url(#glassL)"/>
{label(400, 410, 170, 190, name, sub, ink, paper, small=True)}
</g>'''


def pump(c, name, sub, scale=1.0, cx=400, base=630):
    body, lid, ink, paper = c['body'], c['lid'], c['ink'], c['paper']
    return f'''<g transform="translate({cx} {base}) scale({scale}) translate(-400 -630)">
<ellipse cx="400" cy="634" rx="150" ry="18" fill="#000" opacity=".16" filter="url(#blur)"/>
<rect x="286" y="318" width="228" height="312" rx="38" fill="{body}"/>
<rect x="286" y="318" width="228" height="312" rx="38" fill="url(#glassL)"/>
<rect x="356" y="286" width="88" height="40" rx="6" fill="{lid}"/>
<rect x="382" y="196" width="36" height="96" fill="{lid}"/>
<path d="M366 196 H500 Q520 196 520 214 V222 Q520 238 500 238 H366 Z" fill="{lid}"/>
<path d="M366 196 H500 Q520 196 520 214 V222 Q520 238 500 238 H366 Z" fill="url(#glassL)"/>
{label(400, 380, 190, 214, name, sub, ink, paper)}
</g>'''


def toner(c, name, sub, scale=1.0, cx=400, base=630):
    body, lid, ink, paper = c['body'], c['lid'], c['ink'], c['paper']
    return f'''<g transform="translate({cx} {base}) scale({scale}) translate(-400 -630)">
<ellipse cx="400" cy="634" rx="120" ry="16" fill="#000" opacity=".16" filter="url(#blur)"/>
<path d="M326 630 V330 Q326 296 352 284 H448 Q474 296 474 330 V630 Z" fill="{body}"/>
<path d="M326 630 V330 Q326 296 352 284 H448 Q474 296 474 330 V630 Z" fill="url(#glassL)"/>
<rect x="344" y="196" width="112" height="96" rx="10" fill="{lid}"/>
<rect x="344" y="196" width="112" height="96" rx="10" fill="url(#glassL)"/>
<g stroke="#000" opacity=".1" stroke-width="2">{''.join(f'<line x1="{x}" y1="204" x2="{x}" y2="286"/>' for x in range(356, 452, 12))}</g>
{label(400, 360, 124, 236, name, sub, ink, paper, small=True)}
</g>'''


def kit(c, name, sub):
    a = dict(c)
    return (jar(a, 'Day\nCream', '50 ML', scale=.74, cx=205, base=630, small=True) +
            toner(a, 'Toner', '150 ML', scale=.84, cx=600, base=630) +
            dropper(a, 'Serum', '30 ML', scale=.92, cx=400, base=630))


FIT = {'jar': 1.45, 'tube': 1.12, 'dropper': 1.15, 'pump': 1.22, 'toner': 1.2}
SHAPES = {k: (lambda c, n, s, f=f, k=k: globals()[k](c, n, s, scale=FIT[k])) for k, f in FIT.items()}
SHAPES['kit'] = kit

# palettes: backdrop tint, container, lid, label ink, label paper
P = {
    'cream':  dict(bg='#F3EBDD', body='#F7F2E8', lid='#C9A27A', ink='#3B2F25', paper='#FFFFFF'),
    'sage':   dict(bg='#E3EADC', body='#A9BFA0', lid='#F3EFE4', ink='#2E3F2C', paper='#F6F8F1'),
    'blush':  dict(bg='#F6E3DD', body='#EBC3B8', lid='#FBF4EF', ink='#5A2F28', paper='#FFF9F6'),
    'amber':  dict(bg='#F2E4CF', body='#B9783A', lid='#2B2A28', ink='#3B2616', paper='#FBF3E6'),
    'sky':    dict(bg='#E1EAF0', body='#B6CBDA', lid='#FFFFFF', ink='#233646', paper='#F7FAFC'),
    'ink':    dict(bg='#E7E3DC', body='#2F3A38', lid='#D9C7A3', ink='#2F3A38', paper='#F4EFE5'),
    'sun':    dict(bg='#F6EACB', body='#F0C75E', lid='#FFF9EC', ink='#4A3510', paper='#FFFDF6'),
    'lilac':  dict(bg='#E9E3EF', body='#C9B8DA', lid='#FFFFFF', ink='#3C2D52', paper='#FBF9FD'),
}

PRODUCTS = [
    # slug, shape, palette, label name, sub
    ('daily-moisturiser',    'jar',     'cream', 'Daily\nMoisturiser', '50 ML'),
    ('night-repair-cream',   'jar',     'ink',   'Night\nRepair', '50 ML'),
    ('rich-body-butter',     'jar',     'blush', 'Body\nButter', '200 ML'),
    ('hydrating-cleanser',   'tube',    'sage',  'Hydrating\nCleanser', '125 ML'),
    ('mineral-sunscreen',    'tube',    'sun',   'Mineral\nSPF 50', '50 ML'),
    ('clay-mask',            'tube',    'blush', 'Clay\nMask', '75 ML'),
    ('hand-cream',           'tube',    'sky',   'Hand\nCream', '50 ML'),
    ('vitamin-c-serum',      'dropper', 'amber', 'Vitamin C\nSerum', '30 ML'),
    ('hyaluronic-serum',     'dropper', 'sky',   'Hyaluronic\nSerum', '30 ML'),
    ('retinol-serum',        'dropper', 'ink',   'Retinol\nSerum', '30 ML'),
    ('gentle-body-lotion',   'pump',    'lilac', 'Body\nLotion', '250 ML'),
    ('foaming-face-wash',    'pump',    'sage',  'Foaming\nFace Wash', '150 ML'),
    ('balancing-toner',      'toner',   'blush', 'Balancing\nToner', '150 ML'),
    ('micellar-water',       'toner',   'sky',   'Micellar\nWater', '200 ML'),
    ('essentials-kit',       'kit',     'cream', '', ''),
    ('glow-ritual-kit',      'kit',     'sage',  '', ''),
]

for slug, shape, pal, name, sub in PRODUCTS:
    c = P[pal]
    art = SHAPES[shape](c, name, sub)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800" role="img" aria-label="{escape(slug.replace('-', ' '))}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(c['bg'], .45)}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
<linearGradient id="glassL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".22" stop-color="#fff" stop-opacity=".02"/><stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient>
<filter id="blur" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<rect width="800" height="800" fill="url(#bg)"/>
<ellipse cx="400" cy="640" rx="330" ry="46" fill="#fff" opacity=".35"/>
{art}
</svg>
'''
    with open(os.path.join(OUT, slug + '.svg'), 'w') as f:
        f.write(svg)
print(len(PRODUCTS), 'written')
