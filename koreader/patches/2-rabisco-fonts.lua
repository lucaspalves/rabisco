--[[
Rabisco · interface fonts

Swaps KOReader's interface font (Noto Sans) for Rabisco Hand, a fully informal
cut of Shantell Sans, and sets titles in Gaegu. Book text is not touched: pick
Literata yourself in the reading menu.

Needs the font files in koreader/fonts/rabisco/. If they're missing, this patch
does nothing and logs a message, so KOReader still starts normally.

Remove this file (or rename it to end in .disabled) to go back to the default font.
--]]

local lfs = require("libs/libkoreader-lfs")
local logger = require("logger")
local Font = require("ui/font")
local FontList = require("fontlist")

-- ---- settings you can change ------------------------------------------------
local REGULAR = "rabisco/RabiscoHand-Regular.ttf"
local BOLD    = "rabisco/RabiscoHand-Bold.ttf"
local TITLE   = "rabisco/Gaegu-Bold.ttf"
local USE_GAEGU_FOR_TITLES = true
local TEXT_SCALE  = 0.95 -- Rabisco Hand runs wider than Noto Sans
local TITLE_SCALE = 1.15 -- Gaegu runs smaller than Noto Sans
-- -----------------------------------------------------------------------------

local function exists(name)
    return lfs.attributes(FontList.fontdir .. "/" .. name, "mode") == "file"
end

if not (exists(REGULAR) and exists(BOLD)) then
    logger.warn("Rabisco: font files not found in koreader/fonts/rabisco, keeping the default interface font")
    return
end
local titles = USE_GAEGU_FOR_TITLES and exists(TITLE)

-- Let KOReader use our real bold instead of faking it.
Font.bold_font_variant[REGULAR] = BOLD
Font.regular_font_variant[BOLD] = REGULAR

local text_keys = {
    "cfont", "ffont", "smallffont", "largeffont", "rifont", "pgfont", "hfont",
    "infofont", "smallinfofont", "x_smallinfofont", "xx_smallinfofont",
}
local bold_keys = { "smallinfofontbold" }
local title_keys = { "tfont", "smalltfont", "x_smalltfont" }

local function scale(key, factor)
    local size = Font.sizemap[key]
    if size then Font.sizemap[key] = math.floor(size * factor + 0.5) end
end

for _, key in ipairs(text_keys) do
    if Font.fontmap[key] then
        Font.fontmap[key] = REGULAR
        scale(key, TEXT_SCALE)
    end
end
for _, key in ipairs(bold_keys) do
    if Font.fontmap[key] then
        Font.fontmap[key] = BOLD
        scale(key, TEXT_SCALE)
    end
end
for _, key in ipairs(title_keys) do
    if Font.fontmap[key] then
        Font.fontmap[key] = titles and TITLE or BOLD
        scale(key, titles and TITLE_SCALE or TEXT_SCALE)
    end
end

-- The top menu caches its font when it's first loaded: refresh it.
local ok, TouchMenu = pcall(require, "ui/widget/touchmenu")
if ok and TouchMenu then
    TouchMenu.fface = Font:getFace("ffont")
end

logger.info("Rabisco: interface fonts applied")
