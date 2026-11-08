# Rabisco

A naive, hand-drawn skin for [KOReader](https://koreader.rocks) on Kindle. Marker lines, doodled icons, a scribbly interface font, and sleep screens that look like notes stuck to the page. Built for e-ink first: 16 gray levels, no animation, big touch targets.

*Rabisco* is Portuguese for "scribble".

## Screens

The full Rabisco look, as designed. Stage 1 (below) already brings the fonts, icons, marker lines and sleep screens; the wobbly frames, hatching and stickers arrive in later stages ([roadmap](docs/ROADMAP.md)).

<table>
  <tr>
    <td align="center"><img src="docs/screens/main.png" width="200" alt="Library: book list with hatched covers, squiggle progress and new stickers"><br><sub>library</sub></td>
    <td align="center"><img src="docs/screens/reading.png" width="200" alt="Reading page in Literata with a hand-drawn status bar"><br><sub>reading</sub></td>
    <td align="center"><img src="docs/screens/topmenu.png" width="200" alt="Top menu with hand-drawn tab icons and the font and text page"><br><sub>top menu</sub></td>
    <td align="center"><img src="docs/screens/fontmenu.png" width="200" alt="Bottom menu with font size, line spacing, margins and light"><br><sub>bottom menu</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/screens/settings.png" width="200" alt="Settings with wobbly toggles and scribbled checkboxes"><br><sub>settings</sub></td>
    <td align="center"><img src="docs/screens/feeds.png" width="200" alt="News feeds list with unread stickers"><br><sub>news feeds</sub></td>
    <td align="center"><img src="docs/screens/dialog.png" width="200" alt="Wi-fi dialog over a hatched screen"><br><sub>dialog</sub></td>
    <td align="center"><img src="docs/screens/sleep.png" width="200" alt="Sleep screen: shh… sleeping, with the current book"><br><sub>sleep screen</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/screens/main-night.png" width="200" alt="Library in night mode"><br><sub>library · night</sub></td>
    <td align="center"><img src="docs/screens/reading-night.png" width="200" alt="Reading page in night mode"><br><sub>reading · night</sub></td>
    <td align="center"><img src="docs/screens/topmenu-night.png" width="200" alt="Top menu in night mode"><br><sub>top menu · night</sub></td>
    <td align="center"><img src="docs/screens/settings-night.png" width="200" alt="Settings in night mode"><br><sub>settings · night</sub></td>
  </tr>
</table>

Night mode is an exact inversion, the same thing KOReader's own night mode does, so the palette is built to survive it.

## What's in this version

| Part | What it does | Where it goes |
| --- | --- | --- |
| **Fonts** | Rabisco Hand (a fully informal cut of Shantell Sans) for the interface, Gaegu for titles, Literata for reading | `koreader/fonts/rabisco/` |
| **Icons** | 29 hand-drawn icons that replace KOReader's own: top menu tabs, file browser, stars, chevrons, notices | `koreader/icons/` |
| **Font patch** | Switches the whole interface to Rabisco Hand, titles to Gaegu | `koreader/patches/2-rabisco-fonts.lua` |
| **Marker patch** | Thicker borders and separators, softer corners on dialogs and buttons | `koreader/patches/2-rabisco-frames.lua` |
| **Sleep screens** | Three sleep screen images for each common Kindle resolution | `koreader/screensaver/<resolution>/` |
| **Installer** | A KOReader plugin that installs and updates all of the above over Wi-Fi | `koreader/plugins/rabisco.koplugin/` |

The wobbly frames, hatching and stickers from the mockups are planned next: see [docs/ROADMAP.md](docs/ROADMAP.md).

## Install

You need a Kindle that already runs KOReader (jailbroken).

### Over Wi-Fi, from the Kindle (recommended)

The Rabisco installer downloads everything itself, and later brings updates the same way. It only has to be copied over once.

1. **Copy the installer once.** Put the `rabisco.koplugin` folder (from `koreader/plugins/` in this repo) into `koreader/plugins/` on your Kindle. Use a computer, an Android phone with a USB OTG adapter, or KOReader's Cloud storage (Dropbox, WebDAV, FTP).
2. **Restart KOReader.**
3. **Install.** Main menu (☰) → More tools → **Rabisco** → **Install or update**. KOReader turns on Wi-Fi if needed, shows the size, and asks before downloading. If the connection drops, nothing is changed.
4. **Restart when it asks.**
5. **Sleep screens:** in the same Rabisco menu, tap **Use Rabisco sleep screens**. It picks the right size for your Kindle.
6. **Reading font:** open a book, tap the bottom of the screen, choose the font (Aa) tab and pick **Literata**.

To update later, tap **Install or update** again. **Remove Rabisco** in that menu deletes everything it installed except the installer.

### By hand, with a computer

Plug the Kindle into your computer over USB.

1. **Copy the files.** Open the `koreader` folder in this repo and copy everything inside it into the `koreader` folder on your Kindle, merging folders when asked:
   - `fonts/rabisco/` → `koreader/fonts/rabisco/`
   - `icons/` → `koreader/icons/`
   - `patches/` → `koreader/patches/`
   - `screensaver/` → `koreader/screensaver/`
   - `plugins/rabisco.koplugin/` → `koreader/plugins/` (optional: the installer, for updates over Wi-Fi)
2. **Eject the Kindle and restart KOReader** (top menu → main menu → Exit → Restart KOReader). The patches and icons load on start.
3. **Pick the reading font.** Open a book, tap the bottom of the screen, choose the font (Aa) tab and pick **Literata**.
4. **Set the sleep screen.** Top menu → Settings (gear) → Screen → Sleep screen → Wallpaper → *Show random image from folder on sleep screen*. Then under *Custom images* → *Choose random image folder*, pick the folder matching your Kindle:

   | Folder | Kindle |
   | --- | --- |
   | `1072x1448` | Kindle (2022/2024), Paperwhite 10th gen |
   | `1236x1648` | Paperwhite 11th gen / Signature |
   | `1264x1680` | Paperwhite 12th gen, Oasis, Colorsoft |

5. **Night mode** works as usual (top menu → Settings → Night mode). The palette is designed to invert cleanly.

### Turning it off

- One part: rename the patch to end in `.disabled` (e.g. `2-rabisco-frames.lua.disabled`), or delete the icons from `koreader/icons/`.
- Everything: delete the files above. KOReader goes back to normal on the next restart.
- KOReader's **Patch management** menu can also switch patches off without deleting them.

### Adjusting

Each patch has a small settings block at the top. For example, in `2-rabisco-fonts.lua` set `USE_GAEGU_FOR_TITLES = false` to keep titles in Rabisco Hand, or lower `TEXT_SCALE` if menu labels get cut off. In `2-rabisco-frames.lua` you can set every border and corner size.

## Known limits

- A few labels that KOReader creates before patches run may keep the default font until you open and close their screen.
- Wi-fi signal strength icons keep KOReader's style for now, so the bars still show real signal levels.
- Works with qewer33's title bar patch, which loads its tab icons from `koreader/icons/tab_<n>.svg`: copy the Rabisco icons under those names if you use it.
- Rabisco changes looks only. If a KOReader update renames something a patch touches, that patch skips the change rather than crashing, but test after updating.

## For developers

```
design/     the design system: tokens, brand book, icons, doodles and screen mockups (screens/)
koreader/   files that go on the device
tools/      scripts that build the fonts, icons and sleep screens
tests/      a harness that runs the patches against stand-in KOReader modules
docs/       roadmap and notes
```

Rebuild everything:

```sh
python3 tools/build_fonts.py <path to google/fonts>/ofl koreader/fonts/rabisco   # needs fonttools
python3 tools/koreader_icons.py koreader/icons
python3 tools/render_sleep.py koreader/screensaver                              # needs playwright + the fonts installed
python3 tools/render_screens.py design/screens docs/screens                     # README images, same needs
python3 tools/build_manifest.py                                                 # ALWAYS last: the installer's file list
texlua tests/installer_harness.lua "$PWD/koreader" "$(mktemp -d)"               # installer end to end, offline
texlua tests/patch_harness.lua koreader/patches present                         # any Lua 5.1+
```

## Credits and licenses

- Code and artwork in this repo: MIT (see [LICENSE](LICENSE)).
- Fonts: SIL Open Font License 1.1, licenses in `koreader/fonts/rabisco/licenses/`. Rabisco Hand is built from [Shantell Sans](https://github.com/arrowtype/shantell-sans) by Arrow Type; [Gaegu](https://fonts.google.com/specimen/Gaegu) by JIKJI SOFT; [Literata](https://github.com/googlefonts/literata) by TypeTogether.
- Inspired by how [Project: Title](https://github.com/joshuacant/ProjectTitle) and [qewer33's patches](https://github.com/qewer33/koreader-patches) customize KOReader.
