"""Render the screen mockups in design/screens/ to PNG images for the README.

The mockups are Design canvas components (.dc.html). This script fills in their
templates itself ({{holes}}, <sc-for>, <sc-if>) so they can be rendered with a
plain headless browser, without the canvas editor.

Needs Playwright (Chromium) and the Rabisco fonts installed on this computer.

Usage: python3 tools/render_screens.py design/screens docs/screens
"""
import json
import os
import re
import sys
import tempfile

ORDER = ["Main", "Reading", "TopMenu", "FontMenu", "Settings", "Feeds", "Dialog", "Sleep"]

SHIM = r"""
<script>
class DCLogic { constructor(props) { this.props = props || {}; this.state = {}; } setState(s) { Object.assign(this.state, s); } }
function lookup(scope, path) {
  path = path.trim();
  if (path === 'true') return true; if (path === 'false') return false;
  if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
  return path.split('.').reduce((o, k) => (o == null ? undefined : o[k]), scope);
}
function fill(text, scope) {
  return text.replace(/\{\{\s*([^}]+?)\s*\}\}/g, (_, p) => { const v = lookup(scope, p); return v == null ? '' : String(v); });
}
function render(node, scope) {
  for (const child of Array.from(node.childNodes)) {
    if (child.nodeType === 3) { if (child.nodeValue.includes('{{')) child.nodeValue = fill(child.nodeValue, scope); continue; }
    if (child.nodeType !== 1) continue;
    const tag = child.tagName.toLowerCase();
    if (tag === 'sc-for') {
      const list = lookup(scope, child.getAttribute('list').replace(/[{}]/g, '')) || [];
      const as = child.getAttribute('as') || 'item';
      const frag = document.createDocumentFragment();
      list.forEach((item, i) => {
        const holder = document.createElement('div');
        holder.innerHTML = child.innerHTML;
        render(holder, Object.assign({}, scope, { [as]: item, $index: i }));
        while (holder.firstChild) frag.appendChild(holder.firstChild);
      });
      child.replaceWith(frag);
      continue;
    }
    if (tag === 'sc-if') {
      if (lookup(scope, child.getAttribute('value').replace(/[{}]/g, ''))) {
        render(child, scope);
        child.replaceWith(...Array.from(child.childNodes));
      } else child.remove();
      continue;
    }
    for (const attr of Array.from(child.attributes)) {
      if (attr.value.includes('{{')) child.setAttribute(attr.name, fill(attr.value, scope));
    }
    render(child, scope);
  }
}
</script>
"""

FONT_ALIAS = """<style>
@font-face { font-family: 'Shantell Sans'; src: local('Rabisco Hand Regular'), local('RabiscoHand-Regular'), local('Rabisco Hand'); font-weight: 300 500; }
@font-face { font-family: 'Shantell Sans'; src: local('Rabisco Hand Bold'), local('RabiscoHand-Bold'); font-weight: 600 800; }
</style>"""


def page_for(src, night):
    html = open(src, encoding="utf-8").read()
    body = re.search(r"<x-dc>(.*)</x-dc>", html, re.S).group(1)
    body = re.sub(r"<link[^>]+fonts\.googleapis[^>]*>", "", body)  # fonts come from this computer
    body = body.replace("<helmet>", "").replace("</helmet>", "")
    script = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', html, re.S).group(1)
    props = json.dumps({"night": night})
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">{FONT_ALIAS}{SHIM}</head>
<body style="margin:0"><template id="t">{body}</template>
<script>{script}
const vals = new Component({props}).renderVals();
const root = document.createElement('div');
root.innerHTML = document.getElementById('t').innerHTML;
render(root, vals);
document.body.appendChild(root);
</script></body></html>"""


def main(src_dir, out_dir):
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        browser = pw.chromium.launch()
        for name in ORDER:
            for night in (False, True):
                path = os.path.join(tmp, "s.html")
                open(path, "w", encoding="utf-8").write(page_for(os.path.join(src_dir, name + ".dc.html"), night))
                page = browser.new_page(viewport={"width": 600, "height": 800}, device_scale_factor=1.5)
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto("file://" + path)
                page.wait_for_timeout(300)
                out = os.path.join(out_dir, "%s%s.png" % (name.lower(), "-night" if night else ""))
                page.screenshot(path=out, clip={"x": 0, "y": 0, "width": 600, "height": 800})
                page.close()
                print("rendered", out, "ERRORS: " + "; ".join(errors) if errors else "")
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
