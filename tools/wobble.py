"""Rabisco: deterministic hand-drawn ("naive") SVG strokes.

Every shape is sampled into points, jittered with a seeded RNG, then drawn as a
smooth Catmull-Rom curve. Closed shapes overshoot their start a little, the way a
marker does when you draw a circle by hand.
"""
import math, random

INK = "#111111"


class Pen:
    def __init__(self, seed, amp=0.32):
        self.r = random.Random(seed)
        self.amp = amp
        self.paths = []

    def j(self, a=None):
        a = self.amp if a is None else a
        return self.r.uniform(-a, a)

    # ---- curve core -------------------------------------------------------
    @staticmethod
    def _cr(points):
        """Catmull-Rom through points -> SVG cubic path string (open)."""
        if len(points) < 2:
            return ""
        pts = [points[0]] + points + [points[-1]]
        d = "M%.2f %.2f" % points[0]
        for i in range(1, len(pts) - 2):
            p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += " C%.2f %.2f %.2f %.2f %.2f %.2f" % (c1 + c2 + p2)
        return d

    def curve(self, pts, jitter=True):
        if jitter:
            pts = [(x + self.j(), y + self.j()) for x, y in pts]
        self.paths.append(self._cr(pts))
        return self

    # ---- primitives -------------------------------------------------------
    def line(self, x1, y1, x2, y2, bow=None, over=0.25):
        """A slightly bowed line with a tiny overshoot at both ends."""
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        bow = self.j(self.amp * 1.4) if bow is None else bow
        o1, o2 = self.r.uniform(0, over), self.r.uniform(0, over)
        a = (x1 - ux * o1, y1 - uy * o1)
        b = (x2 + ux * o2, y2 + uy * o2)
        n = max(2, int(L / 6))
        pts = [a]
        for k in range(1, n):
            t = k / n
            s = math.sin(math.pi * t) * bow
            pts.append((x1 + dx * t + nx * s, y1 + dy * t + ny * s))
        pts.append(b)
        self.paths.append(self._cr([(p[0] + self.j(0.08), p[1] + self.j(0.08)) for p in pts]))
        return self

    def poly(self, pts, closed=False, over=0.6):
        """Polyline whose corners stay sharp-ish; closed ones overshoot."""
        seq = list(pts)
        if closed:
            seq = seq + [seq[0]]
        out = []
        for i in range(len(seq) - 1):
            (x1, y1), (x2, y2) = seq[i], seq[i + 1]
            L = math.hypot(x2 - x1, y2 - y1)
            n = max(1, int(L / 5))
            for k in range(n):
                t = k / n
                out.append((x1 + (x2 - x1) * t + self.j(0.12), y1 + (y2 - y1) * t + self.j(0.12)))
        # corners: snap a sample exactly to each corner (+ jitter) to keep them crisp
        last = seq[-1]
        if closed:
            # overshoot past the start along the first edge
            (x1, y1), (x2, y2) = seq[0], seq[1]
            L = math.hypot(x2 - x1, y2 - y1) or 1
            out.append((x1 + self.j(0.15), y1 + self.j(0.15)))
            out.append((x1 + (x2 - x1) / L * over, y1 + (y2 - y1) / L * over))
        else:
            out.append((last[0] + self.j(0.15), last[1] + self.j(0.15)))
        # draw corners as separate segments so they don't round off too much
        self.paths.append(self._poly_path(out))
        return self

    @staticmethod
    def _poly_path(pts):
        d = "M%.2f %.2f" % pts[0]
        for p in pts[1:]:
            d += " L%.2f %.2f" % p
        return d

    def circle(self, cx, cy, r, over=0.45, start=None, wob=0.05, n=None):
        start = self.r.uniform(0, 2 * math.pi) if start is None else start
        n = n or max(8, int(r * 2.2))
        total = 2 * math.pi + over
        pts = []
        for k in range(n + 1):
            a = start + total * k / n
            rr = r * (1 + self.r.uniform(-wob, wob))
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.paths.append(self._cr(pts))
        return self

    def arc(self, cx, cy, r, a0, a1, wob=0.04, n=None):
        n = n or max(4, int(abs(a1 - a0) * r / 2.2))
        pts = []
        for k in range(n + 1):
            a = a0 + (a1 - a0) * k / n
            rr = r * (1 + self.r.uniform(-wob, wob))
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.paths.append(self._cr(pts))
        return self

    def dot(self, x, y):
        self.paths.append("M%.2f %.2f l0.15 0.05" % (x + self.j(0.15), y + self.j(0.15)))
        return self

    def svg(self, size=24, sw=2.0, title=None, extra=""):
        body = "".join('<path d="%s"/>' % p for p in self.paths)
        t = "<title>%s</title>" % title if title else ""
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s}" height="{s}" '
            'fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            "{t}{b}{x}</svg>"
        ).format(s=size, ink=INK, sw=sw, t=t, b=body, x=extra)

    def inner(self):
        return "".join('<path d="%s"/>' % p for p in self.paths)
