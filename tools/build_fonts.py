"""Build Rabisco's static fonts from the variable Google Fonts sources.

KOReader picks font files by name and can't choose an instance of a variable
font, so we bake the exact looks Rabisco wants into static files:

  Rabisco Hand  <- Shantell Sans, fully informal (INFM 100) with a little bounce
  Literata      <- static Regular / Italic / Bold / Bold Italic for reading
  Gaegu         <- already static, copied as-is

Usage: python3 tools/build_fonts.py <google-fonts-ofl-dir> <out-dir>
"""
import os, shutil, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)


def rename(font, family, style, ps):
    name = font["name"]
    full = f"{family} {style}"
    for rec in list(name.names):
        if rec.nameID in (16, 17, 25):  # typographic family/subfamily, var prefix
            name.removeNames(nameID=rec.nameID)
    name.setName(family if style in ("Regular", "Bold", "Italic", "Bold Italic") else f"{family} {style}", 1, 3, 1, 0x409)
    name.setName(style if style in ("Regular", "Bold", "Italic", "Bold Italic") else "Regular", 2, 3, 1, 0x409)
    name.setName(full, 4, 3, 1, 0x409)
    name.setName(ps, 6, 3, 1, 0x409)
    name.setName(f"{ps};rabisco", 3, 3, 1, 0x409)
    bold = "Bold" in style
    italic = "Italic" in style
    font["OS/2"].usWeightClass = 700 if bold else 400
    fs = 0
    if bold: fs |= 1 << 5
    if italic: fs |= 1 << 0
    if not bold and not italic: fs |= 1 << 6
    font["OS/2"].fsSelection = (font["OS/2"].fsSelection & ~0b1100001) | fs
    font["head"].macStyle = (1 if bold else 0) | (2 if italic else 0)
    for t in ("STAT", "fvar", "avar", "gvar", "HVAR", "MVAR"):
        if t in font: del font[t]


def instance(path, coords, family, style, fname):
    f = TTFont(path)
    inst = instantiateVariableFont(f, coords, updateFontNames=False)
    rename(inst, family, style, fname.rsplit(".", 1)[0])
    inst.save(os.path.join(out, fname))
    print("built", fname)


shantell = os.path.join(src, "shantellsans", "ShantellSans[BNCE,INFM,SPAC,wght].ttf")
shantell_i = os.path.join(src, "shantellsans", "ShantellSans-Italic[BNCE,INFM,SPAC,wght].ttf")
hand = {"INFM": 100, "BNCE": 30, "SPAC": 0}
instance(shantell, dict(hand, wght=430), "Rabisco Hand", "Regular", "RabiscoHand-Regular.ttf")
instance(shantell, dict(hand, wght=700), "Rabisco Hand", "Bold", "RabiscoHand-Bold.ttf")
instance(shantell_i, dict(hand, wght=430), "Rabisco Hand", "Italic", "RabiscoHand-Italic.ttf")

lit = os.path.join(src, "literata", "Literata[opsz,wght].ttf")
lit_i = os.path.join(src, "literata", "Literata-Italic[opsz,wght].ttf")
instance(lit, {"opsz": 12, "wght": 400}, "Literata", "Regular", "Literata-Regular.ttf")
instance(lit, {"opsz": 12, "wght": 700}, "Literata", "Bold", "Literata-Bold.ttf")
instance(lit_i, {"opsz": 12, "wght": 400}, "Literata", "Italic", "Literata-Italic.ttf")
instance(lit_i, {"opsz": 12, "wght": 700}, "Literata", "Bold Italic", "Literata-BoldItalic.ttf")

for w in ("Regular", "Bold"):
    shutil.copy(os.path.join(src, "gaegu", f"Gaegu-{w}.ttf"), out)
    print("copied", f"Gaegu-{w}.ttf")

lic = os.path.join(out, "licenses")
os.makedirs(lic, exist_ok=True)
for fam in ("shantellsans", "literata", "gaegu"):
    shutil.copy(os.path.join(src, fam, "OFL.txt"), os.path.join(lic, f"OFL-{fam}.txt"))
