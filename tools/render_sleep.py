"""Render Rabisco sleep screens as grayscale PNGs at Kindle resolutions.

Needs Playwright (Chromium) and the Rabisco fonts installed on this computer
(copy koreader/fonts/rabisco/*.ttf to your system fonts first).

Usage: python3 tools/render_sleep.py koreader/screensaver
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from wobble import Pen  # noqa: E402
import rabisco_icons as R  # noqa: E402

# Kindle screens (portrait, px). Add yours if it's missing.
SIZES = {
    "1072x1448": "Kindle (2022/2024), Paperwhite 10th gen",
    "1236x1648": "Paperwhite 11th gen / Signature",
    "1264x1680": "Paperwhite 12th gen, Oasis, Colorsoft",
}


def icon(name, size, sw=1.6):
    names = [n for n, _, _ in R.ICONS]
    i = names.index(name)
    p = Pen(seed=1000 + i)
    R.ICONS[i][1](p)
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="#111111" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>') % (size, size, sw, p.inner())


def doodle(name, size):
    names = [n for n, _ in R.DOODLES]
    i = names.index(name)
    p = Pen(seed=2000 + i, amp=0.6)
    R.DOODLES[i][1](p)
    return ('<svg width="%d" height="%d" viewBox="0 0 48 48" fill="none" stroke="#111111" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>') % (size, size, p.inner())


WOB_A = "255px 15px 225px 15px / 15px 225px 15px 255px"
WOB_B = "15px 225px 15px 255px / 225px 15px 255px 15px"
HAND = "'Rabisco Hand', 'Shantell Sans', cursive"
TITLE = "Gaegu, cursive"

VARIANTS = {
    "sleeping": lambda: f"""
      <div class="sticker" style="transform: rotate(-2deg); border-radius: {WOB_A};">
        {icon('night', 112)}
        <h1>shh… sleeping</h1>
      </div>
      <p class="note">press the power button to wake me up</p>""",
    "back-soon": lambda: f"""
      <div style="display:flex; align-items:flex-end; gap:10px; transform: rotate(1.5deg);">
        <div class="sticker" style="border-radius: {WOB_B};"><h1>back soon</h1></div>
        <div style="margin-bottom:-14px">{doodle('loop-arrow', 96)}</div>
      </div>
      <div style="display:flex; gap:28px; align-items:center;">
        {icon('book', 64)} {doodle('scribble', 72)} {icon('bookmark', 56)}
      </div>
      <p class="note">i’m just resting my pages</p>""",
    "dreaming": lambda: f"""
      <div style="position:relative;">
        <div class="sticker" style="border-radius: {WOB_A}; transform: rotate(-1.5deg);">
          {icon('book', 104)}
          <h1>dreaming of books</h1>
        </div>
        <div style="position:absolute; top:-30px; right:-26px; background:#fff; border-radius:999px; padding:4px; line-height:0;">{doodle('sparkle', 64)}</div>
      </div>
      <div>{doodle('squiggle', 120)}</div>""",
}

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0}
body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#fff;}
.screen{width:600px;height:%(bh)dpx;transform:scale(%(k)s);transform-origin:0 0;box-sizing:border-box;
  background-color:#fff;background-image:repeating-linear-gradient(-45deg,#dddddd 0 1.5px,transparent 1.5px 14px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;padding:40px;color:#111;font-family:%(hand)s;}
.sticker{display:flex;flex-direction:column;align-items:center;gap:6px;background:#fff;padding:18px 34px 14px;
  border:3.5px solid #111;box-shadow:3px 3px 0 #111;}
h1{margin:0;text-align:center;font-family:%(title)s;font-weight:700;font-size:64px;line-height:60px;}
.note{margin:0;background:#fff;padding:4px 12px;border-radius:6px;font-size:17px;line-height:22px;color:#555;}
</style></head><body><div class="screen">%(body)s</div></body></html>"""


def render(outdir):
    from playwright.sync_api import sync_playwright
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        browser = pw.chromium.launch()
        for size in SIZES:
            w, h = map(int, size.split("x"))
            k = w / 600.0
            for name, body in VARIANTS.items():
                html = PAGE % {"w": w, "h": h, "bh": round(h / k), "k": k, "body": body(), "hand": HAND, "title": TITLE}
                src = os.path.join(tmp, "p.html")
                open(src, "w").write(html)
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto("file://" + src)
                page.wait_for_timeout(200)
                rgb = os.path.join(tmp, "s.png")
                page.screenshot(path=rgb)
                page.close()
                out = os.path.join(outdir, size, "rabisco-%s.png" % name)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                # 8-bit grayscale snapped to the panel's 16 levels
                subprocess.run(["convert", rgb, "-colorspace", "Gray", "-posterize", "16", "-depth", "8",
                                "-define", "png:color-type=0", out], check=True)
                print("rendered", out)
        browser.close()


if __name__ == "__main__":
    render(sys.argv[1])
