import math, os, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from wobble import Pen

T = math.pi


def menu(p):
    p.line(4, 7, 19.5, 6.6).line(4.5, 12.2, 17, 12).line(4, 17.3, 20, 17.6)

def search(p):
    p.circle(10.3, 10.2, 5.6).line(14.6, 14.6, 20, 20.2, bow=0.2)

def book(p):
    # open book: two pages meeting at a spine
    p.curve([(12, 6.5), (8.5, 5.2), (4.5, 5.4), (3.2, 6)], ).line(3.2, 6, 3.4, 18.4, bow=0.15)
    p.curve([(3.4, 18.4), (7.5, 17.6), (10.5, 18.2), (12, 19.2)])
    p.curve([(12, 6.5), (15.5, 5.2), (19.5, 5.4), (20.8, 6)]).line(20.8, 6, 20.6, 18.4, bow=-0.15)
    p.curve([(20.6, 18.4), (16.5, 17.6), (13.5, 18.2), (12, 19.2)])
    p.line(12, 6.5, 12, 19.2, bow=0.1)

def bookmark(p):
    p.poly([(6.5, 3.8), (17.5, 4.1), (17.2, 20.3), (12.1, 15.6), (6.8, 20.1)], closed=True)

def toc(p):
    for i, y in enumerate((6.5, 12, 17.5)):
        p.dot(4.6, y)
        p.line(8.5, y + p.j(0.3), [19.5, 16.5, 18.6][i], y + p.j(0.3))

def page(p):
    # document with folded corner
    p.poly([(5.5, 3.5), (14.5, 3.6), (18.8, 7.9), (18.6, 20.5), (5.6, 20.3)], closed=True)
    p.poly([(14.4, 3.8), (14.3, 8.2), (18.6, 8.1)])
    p.line(8.4, 12, 15.6, 12.2).line(8.4, 15.6, 13.8, 15.5)

def textsize(p):
    # big A + little a
    p.poly([(2.8, 19.5), (8, 4.8), (13.2, 19.4)])
    p.line(5, 14.2, 11.1, 14.1)
    p.circle(17.6, 16.4, 2.9, over=0.3, start=-0.4)
    p.line(20.6, 12.4, 20.7, 19.6, bow=0.1)

def settings(p):
    # three slider rails, each with a knob somewhere different
    for y, kx in ((6, 15.5), (12, 8), (18, 13.5)):
        p.line(3.5, y, kx - 2.6, y + p.j(0.2), bow=0)
        p.line(kx + 2.6, y + p.j(0.2), 20.5, y, bow=0)
        p.circle(kx, y, 2.3, n=9)

def tools(p):
    # wrench: an open jaw and a long handle
    p.arc(15.4, 8.6, 4.8, -0.785 + 0.75, -0.785 + 2 * T - 0.75, wob=0.05)
    p.line(12.3, 11.6, 4.3, 19.6, bow=0.25)
    p.line(14.6, 13.8, 6.4, 21.4, bow=0.25)

def sun(p):
    p.circle(12, 12, 4)
    for k in range(8):
        a = k * T / 4 + p.j(0.1)
        p.line(12 + 6.6 * math.cos(a), 12 + 6.6 * math.sin(a), 12 + (9 + p.j(0.6)) * math.cos(a), 12 + (9 + p.j(0.6)) * math.sin(a), bow=0)

def moon(p):
    a0, a1 = 0.95, 2 * T - 0.95
    p.arc(12, 12, 8, a0, a1, wob=0.03)
    e = (12 + 8 * math.cos(a1), 12 + 8 * math.sin(a1))
    s = (12 + 8 * math.cos(a0), 12 + 8 * math.sin(a0))
    p.curve([e, (12.6, 8.4), (11.4, 12.2), (12.8, 15.8), s])
    p.dot(19.6, 9.4)
    p.dot(17.8, 4.2)

def wifi(p):
    for r in (3.6, 7.4, 11.2):
        p.arc(12, 20, r, -T + 0.75, -0.75, wob=0.04)
    p.dot(12, 19.8)

def battery(p):
    p.poly([(2.8, 7.4), (18.6, 7.2), (18.8, 17), (3, 17.2)], closed=True)
    p.line(21, 10.4, 21.1, 13.8, bow=0)
    for x in (6, 8.8, 11.6):
        p.line(x, 15, x + 2.2, 9.6, bow=0)

def home(p):
    p.poly([(3, 11.6), (12, 3.8), (21, 11.4)])
    p.poly([(5.6, 9.6), (5.8, 20.2), (18.4, 20.4), (18.3, 9.4)])
    p.poly([(10, 20.2), (10.1, 14.6), (14, 14.5), (14.1, 20.3)])

def back(p):
    p.line(20, 12.4, 4.6, 12, bow=0.6)
    p.poly([(10.2, 6), (4.2, 12), (10.6, 18.2)])

def close(p):
    p.line(5.5, 5.5, 18.5, 18.6, bow=0.4).line(18.2, 5.2, 5.6, 18.6, bow=-0.4)

def star(p):
    pts = []
    for k in range(10):
        a = -T / 2 + k * T / 5
        r = 9 if k % 2 == 0 else 3.9
        pts.append((12 + r * math.cos(a), 12.6 + r * math.sin(a)))
    p.poly(pts, closed=True)

def folder(p):
    p.poly([(3, 6), (9.2, 5.8), (11, 8.2), (20.8, 8), (20.6, 19), (3.2, 19.2)], closed=True)
    p.line(3.2, 10.6, 20.6, 10.8)


ICONS = [
    ("menu", menu, "main menu"), ("search", search, "search"), ("book", book, "library / open book"),
    ("bookmark", bookmark, "bookmarks"), ("toc", toc, "table of contents"), ("page", page, "page & layout"),
    ("text-size", textsize, "font & text size"), ("settings", settings, "settings"), ("tools", tools, "tools"),
    ("frontlight", sun, "frontlight"), ("night", moon, "night mode"), ("wifi", wifi, "wi-fi"),
    ("battery", battery, "battery"), ("home", home, "home folder"), ("back", back, "go back"),
    ("close", close, "close"), ("star", star, "favorite / finished"), ("folder", folder, "folder"),
]

# ---- doodles (48 grid) -----------------------------------------------------

def squiggle(p):
    pts = [(4 + i * 5, 24 + (7 if i % 2 else -7) + p.j(1.5)) for i in range(9)]
    p.curve(pts, jitter=False)

def sparkle(p):
    c = 24
    p.curve([(c, 4), (c + 3, c - 3), (44, c), (c + 3, c + 3), (c, 44), (c - 3, c + 3), (4, c), (c - 3, c - 3), (c + 0.4, 5.2)])
    p.line(39, 7, 39, 13, bow=0).line(36, 10, 42, 10, bow=0)

def underline(p):
    pts, x, y, d = [], 4, 22, 1
    for i in range(5):
        pts += [(x, y + p.j(1.2)), (44 - (i * 1.5) if d > 0 else 6 + i, y - 2 + p.j(1))]
        d *= -1
        y += 3.6
    p.curve(pts, jitter=False)

def loop_arrow(p):
    p.curve([(4, 36), (14, 30), (24, 14), (16, 9), (12, 17), (22, 24), (34, 24), (43, 17)])
    p.poly([(36, 14.5), (43.4, 16.8), (40.5, 23.8)])

def heart(p):
    p.curve([(24, 41), (12, 31), (5, 21), (8, 11), (17, 9), (24, 17), (31, 9), (40, 11), (43, 21), (36, 31), (24.6, 40.4)])

def scribble(p):
    pts = []
    for k in range(15):
        a = k * 1.25
        pts.append((9 + k * 2.1 + 6 * math.cos(a), 24 + 11 * math.sin(a)))
    p.curve(pts)

DOODLES = [("squiggle", squiggle), ("sparkle", sparkle), ("underline", underline),
           ("loop-arrow", loop_arrow), ("heart", heart), ("scribble", scribble)]


def build(outdir):
    os.makedirs(os.path.join(outdir, "Icons"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "Doodles"), exist_ok=True)
    inner = {}
    for i, (name, fn, label) in enumerate(ICONS):
        p = Pen(seed=1000 + i)
        fn(p)
        open(os.path.join(outdir, "Icons", name + ".svg"), "w").write(p.svg(24, 2.0, label))
        inner[name] = p.inner()
    for i, (name, fn) in enumerate(DOODLES):
        p = Pen(seed=2000 + i, amp=0.6)
        fn(p)
        open(os.path.join(outdir, "Doodles", name + ".svg"), "w").write(p.svg(48, 3.0, name))
        inner["d-" + name] = p.inner()
    return inner


if __name__ == "__main__":
    build(sys.argv[1])
