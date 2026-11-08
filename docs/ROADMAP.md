# Roadmap

Rabisco is built in stages, from safe look changes to deeper drawing changes. Each stage ships as separate patch files you can switch off on their own.

## Stage 1 — done

- Static fonts: Rabisco Hand (Shantell Sans, informal), Gaegu, Literata
- Interface font patch (`2-rabisco-fonts.lua`)
- Marker lines patch: thicker borders, separators and corners (`2-rabisco-frames.lua`)
- 29 hand-drawn icon overrides under KOReader's own icon names
- Sleep screens for three Kindle resolutions
- Test harness for patches

## Stage 2 — drawing

- **Paper-cut shadows** on dialogs and the top menu: a hard 3px offset block. Needs care so the shadow is inside the area KOReader refreshes, or e-ink leaves ghosts.
- **Hatching** behind dialogs and on covers without art. KOReader's frame widget already supports striped fills (`stripe_color`, `stripe_width`), so this can reuse it.
- **Wobbly frames**: draw dialog, menu and button borders from pre-drawn, stretchable images (9-slice) instead of straight lines. The biggest job here.
- **Hand-drawn separators** between menu rows instead of straight gray lines.
- **Active tab ring** in the top menu, like the mockups (or pair with qewer33's title bar patch).

## Stage 3 — library and reading

- Library rows with hatched cover placeholders, squiggle progress and "new" / "done" states, as a plugin or on top of Project: Title.
- Tilted stickers as pre-drawn images (KOReader can only rotate in 90° steps).
- A sleep screen patch that shows the book you were reading in the Rabisco layout.
- More icon overrides: frontlight, page modes, wi-fi signal levels in the same style.

## Design references

- Design system (tokens, components, brand book): `design/`
- Screen mockups: `design/screens/` (sources) and `docs/screens/` (images, shown in the README)
