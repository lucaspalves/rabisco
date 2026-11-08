-- Runs the Rabisco installer plugin end to end against stand-ins for KOReader.
-- "Downloads" come from this repo's koreader/ folder instead of GitHub.
-- Usage: texlua tests/installer_harness.lua <repo>/koreader <empty temp dir> [fail-at-file]

local repo, data, fail_at = arg[1], arg[2], arg[3]
local said, restarts, settings = {}, {}, {}

local function sh(cmd) return os.execute(cmd) end
local function exists(p) local f = io.open(p, "rb"); if f then f:close(); return true end; return false end

local stubs = {}
stubs["gettext"] = function(s) return s end
stubs["ffi/util"] = { template = function(s, ...)
    local a = { ... }
    return (s:gsub("%%(%d)", function(i) return tostring(a[tonumber(i)]) end))
end }
stubs["logger"] = { warn = function(...) table.insert(said, "LOG " .. table.concat({ ... }, " ")) end,
                    info = function() end, dbg = function() end }
stubs["datastorage"] = { getDataDir = function() return data end, getSettingsDir = function() return data .. "/settings" end }
stubs["fontlist"] = { fontdir = data .. "/fonts" }
stubs["util"] = { makePath = function(p) sh("mkdir -p '" .. p .. "'") end }
stubs["ui/widget/infomessage"] = { new = function(_, o) o.kind = "info"; return o end }
stubs["ui/widget/confirmbox"] = { new = function(_, o) o.kind = "confirm"; return o end }
stubs["ui/network/manager"] = { runWhenOnline = function(_, cb) cb() end }
stubs["ui/uimanager"] = {
    show = function(_, w)
        table.insert(said, (w.kind or "?") .. ": " .. (w.text or ""))
        if w.kind == "confirm" then w.ok_callback() end
    end,
    close = function() end, forceRePaint = function() end,
    nextTick = function(_, f) f() end,
    askForRestart = function(_, t) table.insert(restarts, t) end,
}
stubs["ui/widget/container/widgetcontainer"] = { extend = function(_, o) return o end }
stubs["device"] = { screen = { getWidth = function() return 1236 end, getHeight = function() return 1648 end } }
-- networking: copy files out of the repo
stubs["ltn12"] = { sink = { table = function(t) return function(chunk) if chunk then table.insert(t, chunk) end return 1 end end } }
stubs["socket"] = { skip = function(n, ...) return select(n + 1, ...) end }
stubs["socketutil"] = {
    FILE_BLOCK_TIMEOUT = 15, LARGE_BLOCK_TIMEOUT = 10, LARGE_TOTAL_TIMEOUT = 30,
    set_timeout = function() end, reset_timeout = function() end,
    file_sink = function(handle) return function(chunk) if chunk then handle:write(chunk) else handle:close() end return 1 end end,
}
local base = "https://raw.githubusercontent.com/lucaspalves/rabisco/main/koreader/"
stubs["socket.http"] = { request = function(req)
    local rel = req.url:sub(#base + 1)
    if fail_at and rel == fail_at then req.sink(nil); return 1, 404, {}, "HTTP/1.1 404 Not Found" end
    local f = io.open(repo .. "/" .. rel, "rb")
    if not f then req.sink(nil); return 1, 404, {}, "HTTP/1.1 404 Not Found" end
    local body = f:read("*a"); f:close()
    req.sink(body); req.sink(nil)
    return 1, 200, {}, "HTTP/1.1 200 OK"
end }
for name, mod in pairs(stubs) do package.loaded[name] = mod end
G_reader_settings = {
    readSetting = function(_, k) return settings[k] end,
    saveSetting = function(_, k, v) settings[k] = v end,
}

local Rabisco = assert(loadfile(repo .. "/plugins/rabisco.koplugin/main.lua"))()
local menu = {}
Rabisco.ui = { menu = { registerToMainMenu = function(_, p) p:addToMainMenu(menu) end } }
Rabisco:init()
assert(menu.rabisco and #menu.rabisco.sub_item_table == 4, "menu not built")
print("menu:", menu.rabisco.sub_item_table[3].text_func())

menu.rabisco.sub_item_table[1].callback() -- install or update
for _, s in ipairs(said) do print("  " .. s:gsub("\n", " | ")) end
print("restart asked:", restarts[1] or "no")

local checks = {
    data .. "/fonts/rabisco/RabiscoHand-Regular.ttf",
    data .. "/icons/appbar.menu.svg",
    data .. "/patches/2-rabisco-fonts.lua",
    data .. "/plugins/rabisco.koplugin/main.lua",
    data .. "/screensaver/1236x1648/rabisco-sleeping.png",
    data .. "/settings/rabisco-manifest.txt",
}
for _, p in ipairs(checks) do print(exists(p) and "  ok  " or "  MISSING", p:sub(#data + 2)) end
print("menu after:", menu.rabisco.sub_item_table[3].text_func())

said = {}
menu.rabisco.sub_item_table[2].callback() -- sleep screens
print("sleep screen setting:", settings.screensaver_type, settings.screensaver_dir and settings.screensaver_dir:sub(#data + 2))
print("checked:", menu.rabisco.sub_item_table[2].checked_func())
