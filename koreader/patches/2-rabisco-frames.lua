--[[
Rabisco · marker lines

Makes borders, buttons and separators look drawn with a marker instead of a
fine pen: thicker lines everywhere, softer corners on dialogs and buttons.

KOReader can only draw straight or evenly rounded boxes, so the truly wobbly
frames from the Rabisco mockups come in a later patch (see docs/ROADMAP.md).

Remove this file (or rename it to end in .disabled) to go back to the default look.
--]]

local logger = require("logger")
local Screen = require("device").screen
local Size = require("ui/size")

local function px(v) return Screen:scaleBySize(v) end

-- ---- settings you can change (KOReader size units, before screen scaling) ---
local BORDER = {
    default   = 1.5, -- KOReader: 1
    thin      = 1.5, -- KOReader: 0.5 (toggle switches in the bottom menu)
    button    = 2.5, -- KOReader: 1.5
    window    = 3,   -- KOReader: 1.5 (dialogs, menus)
    thick     = 3,   -- KOReader: 2
    inputtext = 2.5, -- KOReader: 2
}
local RADIUS = {
    default = 4,  -- KOReader: 2
    window  = 14, -- KOReader: 7
    button  = 12, -- KOReader: 7
}
local LINE = {
    thin   = 1,   -- KOReader: 0.5
    medium = 1.5, -- KOReader: 1   (separators between menu rows)
    thick  = 2.5, -- KOReader: 1.5
}
-- -----------------------------------------------------------------------------

for k, v in pairs(BORDER) do if Size.border[k] then Size.border[k] = px(v) end end
for k, v in pairs(RADIUS) do if Size.radius[k] then Size.radius[k] = px(v) end end
for k, v in pairs(LINE)   do if Size.line[k]   then Size.line[k]   = px(v) end end

-- Some widgets copied the old sizes when they were first loaded: update them.
local function set_default(module, field, value)
    local ok, widget = pcall(require, module)
    if ok and type(widget) == "table" then widget[field] = value end
end
set_default("ui/widget/container/framecontainer", "bordersize", Size.border.window)
set_default("ui/widget/button", "bordersize", Size.border.button)
set_default("ui/widget/touchmenu", "bordersize", Size.border.window)
set_default("ui/widget/touchmenu", "split_height", Size.line.medium)

logger.info("Rabisco: marker lines applied")
