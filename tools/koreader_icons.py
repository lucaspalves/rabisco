"""Write Rabisco's hand-drawn icons under KOReader's own icon names.

KOReader looks in koreader/icons/ before its built-in icon set, so an SVG there
with the same name as a built-in one replaces it everywhere.

Usage: python3 tools/koreader_icons.py koreader/icons
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from wobble import Pen  # noqa: E402
import rabisco_icons as R  # noqa: E402

T = math.pi

# ---- extra drawings KOReader needs that the design system didn't have --------

def chevron_left(p):
    p.poly([(15.2, 4.6), (8.2, 12.1), (15.4, 19.6)])

def chevron_right(p):
    p.poly([(8.8, 4.6), (15.8, 12.1), (8.6, 19.6)])

def chevron_first(p):
    p.poly([(17.4, 4.8), (10.6, 12.1), (17.6, 19.4)])
    p.line(6.4, 4.8, 6.6, 19.4, bow=0.2)

def chevron_last(p):
    p.poly([(6.6, 4.8), (13.4, 12.1), (6.4, 19.4)])
    p.line(17.6, 4.8, 17.4, 19.4, bow=-0.2)

def chevron_up(p):
    p.poly([(4.6, 15.6), (12.1, 8.4), (19.6, 15.4)])

def check(p):
    p.curve([(4.2, 12.6), (8, 17.8), (10.2, 17.2), (15.4, 9.8), (20.6, 4.2)])

def plus(p):
    p.line(12, 4, 12.2, 20, bow=0.3).line(4, 12.1, 20, 11.9, bow=-0.3)

def info(p):
    p.circle(12, 12, 9)
    p.dot(12, 7.4)
    p.line(12, 10.8, 12.1, 17, bow=0.15)

def question(p):
    p.circle(12, 12, 9)
    p.curve([(9, 9.6), (10.2, 7.2), (13.4, 7), (15, 9), (13.8, 11.4), (12.1, 12.6), (12, 14.2)])
    p.dot(12, 17.2)

def warning(p):
    p.poly([(12, 3.6), (21, 19.8), (3, 20)], closed=True)
    p.line(12, 9.4, 12.1, 14.4, bow=0.1)
    p.dot(12, 17.2)

def exit_(p):
    p.poly([(13.6, 4), (4.4, 4.2), (4.6, 19.8), (13.4, 20)])
    p.line(9.4, 12, 20.4, 12.1, bow=0.3)
    p.poly([(16.6, 8.2), (20.6, 12.1), (16.4, 16)])

def edit(p):
    p.poly([(15.6, 4.2), (19.8, 8.4), (8.6, 19.6), (3.8, 20.2), (4.4, 15.4)], closed=True)
    p.line(13.6, 6.4, 17.6, 10.6, bow=0)

def star_full(p):
    R.star(p)


# KOReader name -> (drawing, filled?)
MAP = {
    "appbar.menu": (R.menu, False),
    "appbar.search": (R.search, False),
    "appbar.navigation": (R.toc, False),
    "appbar.typeset": (R.page, False),
    "appbar.textsize": (R.textsize, False),
    "appbar.settings": (R.settings, False),
    "appbar.tools": (R.tools, False),
    "appbar.filebrowser": (R.folder, False),
    "home": (R.home, False),
    "bookmark": (R.bookmark, False),
    "book.opened": (R.book, False),
    "close": (R.close, False),
    "cancel": (R.close, False),
    "star.empty": (R.star, False),
    "star.full": (star_full, True),
    "wifi": (R.wifi, False),
    "chevron.left": (chevron_left, False),
    "chevron.right": (chevron_right, False),
    "chevron.first": (chevron_first, False),
    "chevron.last": (chevron_last, False),
    "chevron.up": (chevron_up, False),
    "check": (check, False),
    "plus": (plus, False),
    "info": (info, False),
    "notice-info": (info, False),
    "notice-question": (question, False),
    "notice-warning": (warning, False),
    "exit": (exit_, False),
    "edit": (edit, False),
}


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    for i, (name, (fn, filled)) in enumerate(sorted(MAP.items())):
        # same seed for the same drawing, so "close" and "cancel" match
        p = Pen(seed=3000 + sum(map(ord, fn.__name__)))
        fn(p)
        svg = p.svg(24, 2.0, name)
        if filled:
            svg = svg.replace('fill="none"', 'fill="#111111"', 1)
        with open(os.path.join(outdir, name + ".svg"), "w") as f:
            f.write(svg)
    print("wrote %d icons to %s" % (len(MAP), outdir))


if __name__ == "__main__":
    build(sys.argv[1])
