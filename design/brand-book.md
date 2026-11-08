Rabisco ("scribble" in Portuguese) is a naive-design skin for reading on a Kindle running KOReader. It should feel like a notebook someone doodled in: wobbly marker lines, crooked stickers, hatching instead of gray, and a voice that talks like a friend leaving you a note. Everything is drawn for an e-ink panel first: 16 gray levels, no motion, big touch targets.

## Principles

- **Drawn, not built.** Lines bow a little, corners overshoot, circles don't quite close. Use the `wobble-*` shapes and the hand-drawn icons; never a perfect rectangle or a geometric icon set.
- **Ink on paper.** The UI is `ink` on `paper`. Gray is for meaning (selected, secondary), never decoration.
- **Hatch, don't shade.** E-ink dithers soft grays into grain. When something needs tone, fill it with diagonal `hatch` lines at `space-2` pitch, or a solid `smudge`.
- **Still is fine.** No animation, no fades. A screen changes in one refresh.
- **Room for thumbs.** Every tappable row is at least `space-8` (56px) tall.

## Voice

- lowercase for every label, title and button: "open book", "turn on wi-fi?", "chapter 4".
- Talk to the reader as "you", keep it short, a little warm: "12 min left in this chapter", "nothing here yet. go find a book."
- Numbers stay numbers ("42 / 310", "78%"). No exclamation marks in system messages, no emoji. A doodle (`sparkle`, `heart`) does the job an emoji would.

## Color

Every gray is a multiple of `#111111`, so each lands exactly on one of the panel's 16 levels and never dithers.

- Screens sit on `paper`. Raised panels and pressed buttons use `paper-shade`; the selected row in any list uses `smudge`.
- Text is `ink`. Secondary text (authors, values, hints) is `pencil` — on `paper`, `paper-shade` and `smudge` only.
- `hatch` is for strokes and fills that carry no words: hatching, unread progress, disabled outlines. Never set text in it.
- Filled stickers and primary buttons are `ink` with `on-ink` text.
- Outlines and separators use `line` (an alias of `ink`).
- The **night** theme is an exact inversion of **paper**, so it matches what KOReader's own night mode produces. Never design a separate dark look.

## Type

- UI text is Shantell Sans (`font-hand`): rows and settings in `body`, tab labels and menu items in `menu`, authors and values in `meta`, the status bar in `tiny`.
- Screen titles (the library header, dialog titles) use Gaegu (`font-display`): `display` for the one title on a screen, `title` for dialogs.
- Book text stays a calm serif: `book` in Literata (`font-book`). The naive look lives in the frame around the page, never inside the text you read.
- Never tilt or hatch text.

## Shape, line and depth

- Boxes (buttons, dialogs, covers, toggles) take `wobble-a` or `wobble-b` as their border-radius. Alternate them between neighbours so no two shapes look stamped.
- Borders: `stroke-pen` for controls, `stroke-marker` for dialogs and the active tab, `stroke-hair` for separators and hatching.
- Depth is a hard paper-cut shadow, `shadow-cut` (dialogs, primary buttons) or `shadow-cut-sm` (stickers). No blur: blurred shadows turn to grain on e-ink.
- Pressed means the shadow disappears and the element shifts by its shadow's offset, as if pushed flat.
- Stickers (badges like "new") may lean by `tilt-left` or `tilt-right`. Only stickers and doodles tilt.

## Spacing

Steps are `space-1` 4, `space-2` 8, `space-3` 14, `space-4` 20, `space-6` 32 and `space-8` 56. `space-3` is 14, not 12, on purpose: the rhythm should feel hand-spaced. Use `space-4` for screen gutters, `space-3` between a row's icon and its text, `space-8` as the minimum row height.

## Iconography

- Use the **Icons** group: 24 × 24, single ink `#111111`, 2px round strokes, drawn with wobble. In code, inline the path so it can take `stroke: var(--ink)` and flip in night mode.
- Don't mix in other icon sets, and don't fill icons. An active icon gets a `wobble-a` ring around it instead of a filled state.
- The **Doodles** group (48 × 48, 3px strokes) is punctuation: `squiggle` under a heading, `sparkle` on something new, `heart` for favourites, `underline` for the active choice. At most one doodle per screen.

## Applying it in KOReader

- Fonts: copy the Shantell Sans, Gaegu and Literata `.ttf` files into `koreader/fonts`, then pick Literata as the reading font.
- Icons: the Icons SVGs are made to drop into `koreader/icons`. qewer33's custom title bar patch reads its tab icons from `tab_<n>.svg` files there, so the menu icons can be copied under those names.
- Night mode: use KOReader's built-in night mode. The palette is designed to invert cleanly.
