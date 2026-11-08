-- Runs the patches against small stand-ins for KOReader modules.
-- Usage: texlua tests/patch_harness.lua koreader/patches present|missing
-- (any Lua 5.1+ works; texlua ships with TeX Live)
-- minimal stand-ins for the KOReader modules the patches touch
local fontsdir = arg[1]
local files_present = arg[2] == "present"
local log = {}
local stubs = {
  ["logger"] = { info=function(...) table.insert(log, table.concat({...}," ")) end, warn=function(...) table.insert(log, "WARN "..table.concat({...}," ")) end },
  ["libs/libkoreader-lfs"] = { attributes=function(p, m) if files_present and p:match("rabisco/") then return "file" end return nil end },
  ["fontlist"] = { fontdir = "./fonts" },
  ["ui/font"] = { fontmap = { cfont="NotoSans-Regular.ttf", tfont="NotoSans-Bold.ttf", smalltfont="NotoSans-Bold.ttf", x_smalltfont="NotoSans-Bold.ttf", ffont="NotoSans-Regular.ttf", smallffont="NotoSans-Regular.ttf", largeffont="NotoSans-Regular.ttf", rifont="NotoSans-Regular.ttf", pgfont="NotoSans-Regular.ttf", scfont="DroidSansMono.ttf", hfont="NotoSans-Regular.ttf", infofont="NotoSans-Regular.ttf", smallinfofont="NotoSans-Regular.ttf", smallinfofontbold="NotoSans-Bold.ttf", x_smallinfofont="NotoSans-Regular.ttf", xx_smallinfofont="NotoSans-Regular.ttf" },
    sizemap = { cfont=24, tfont=26, smalltfont=24, x_smalltfont=22, ffont=20, smallffont=15, largeffont=25, scfont=20, infofont=24, smallinfofont=22, smallinfofontbold=22, x_smallinfofont=20, xx_smallinfofont=18 },
    bold_font_variant = {}, regular_font_variant = {},
    getFace = function(self, k) return { name = self.fontmap[k], size = self.sizemap[k] } end },
  ["ui/widget/touchmenu"] = { bordersize = 1.5 },
  ["device"] = { screen = { scaleBySize = function(_, v) return math.floor(v * 2 + 0.5) end } },
  ["ui/size"] = { border = { default=2, thin=1, button=3, window=3, thick=4, inputtext=4 }, radius = { default=4, window=14, button=14 }, line = { thin=1, medium=2, thick=3, progress=14 } },
  ["ui/widget/container/framecontainer"] = { bordersize = 3 },
  ["ui/widget/button"] = { bordersize = 3 },
}
for name, mod in pairs(stubs) do package.preload[name] = function() return mod end end
local function run(path) local chunk = assert(loadfile(path)); chunk() end
run(fontsdir .. "/2-rabisco-fonts.lua")
run(fontsdir .. "/2-rabisco-frames.lua")
local F = stubs["ui/font"]
print("cfont", F.fontmap.cfont, F.sizemap.cfont)
print("tfont", F.fontmap.tfont, F.sizemap.tfont)
print("scfont", F.fontmap.scfont)
print("bold map", F.bold_font_variant["rabisco/RabiscoHand-Regular.ttf"])
print("touchmenu", stubs["ui/widget/touchmenu"].fface and stubs["ui/widget/touchmenu"].fface.name, stubs["ui/widget/touchmenu"].bordersize, stubs["ui/widget/touchmenu"].split_height)
print("size window", stubs["ui/size"].border.window, "radius", stubs["ui/size"].radius.window, "frame", stubs["ui/widget/container/framecontainer"].bordersize)
for _, l in ipairs(log) do print("log:", l) end
