--[[--
Rabisco installer.

Downloads the Rabisco skin (fonts, icons, patches, sleep screens, and this
plugin itself) from the public GitHub repo over Wi-Fi, so it can be installed
and updated from the Kindle alone.

How it works: koreader/manifest.txt in the repo lists every file with its size
and a version. The plugin downloads each file next to its final place as
"<name>.part", and only when all of them arrived does it move them into place,
so a dropped connection never leaves a half-installed skin.

Menu: main menu (☰) → More tools → Rabisco.

@module koplugin.rabisco
--]]--

local ConfirmBox = require("ui/widget/confirmbox")
local DataStorage = require("datastorage")
local FontList = require("fontlist")
local InfoMessage = require("ui/widget/infomessage")
local NetworkMgr = require("ui/network/manager")
local UIManager = require("ui/uimanager")
local WidgetContainer = require("ui/widget/container/widgetcontainer")
local logger = require("logger")
local util = require("util")
local _ = require("gettext")
local T = require("ffi/util").template

local REPO_URL = "https://raw.githubusercontent.com/lucaspalves/rabisco/main/koreader/"
local MANIFEST_NAME = "manifest.txt"
local SELF_PREFIX = "plugins/rabisco.koplugin/"

local Rabisco = WidgetContainer:extend{
    name = "rabisco",
    is_doc_only = false,
}

-- ---- small helpers -----------------------------------------------------------

local function readFile(path)
    local f = io.open(path, "rb")
    if not f then return nil end
    local s = f:read("*a")
    f:close()
    return s
end

local function writeFile(path, s)
    local f = io.open(path, "wb")
    if not f then return false end
    f:write(s)
    f:close()
    return true
end

local function dirname(path)
    return path:match("^(.*)/[^/]*$") or "."
end

local function installedManifestPath()
    return DataStorage:getSettingsDir() .. "/rabisco-manifest.txt"
end

--- Where a manifest path lives on this device.
-- Fonts go wherever KOReader reads its fonts from; everything else goes in the
-- KOReader data folder (on a Kindle both are inside /mnt/us/koreader).
local function localPath(path)
    if path:sub(1, 6) == "fonts/" then
        return FontList.fontdir .. "/" .. path:sub(7)
    end
    return DataStorage:getDataDir() .. "/" .. path
end

--- Parse manifest text: "version <v>" and "file <size> <path>" lines.
local function parseManifest(text)
    if not text then return nil end
    local manifest = { files = {} }
    for line in text:gmatch("[^\r\n]+") do
        local key, value = line:match("^(%a+)%s+(.+)$")
        if key == "version" then
            manifest.version = value
        elseif key == "file" then
            local size, path = value:match("^(%d+)%s+(%S+)$")
            -- only plain relative paths inside the koreader folder
            if path and not path:find("%.%.") and path:sub(1, 1) ~= "/" then
                table.insert(manifest.files, { path = path, size = tonumber(size) })
            end
        end
    end
    if manifest.version and #manifest.files > 0 then return manifest end
    return nil
end

--- GET a URL. With dest, streams to that file; without, returns the body.
local function fetch(url, dest)
    local http = require("socket.http")
    local ltn12 = require("ltn12")
    local socket = require("socket")
    local socketutil = require("socketutil")
    if dest then
        local handle = io.open(dest, "wb")
        if not handle then return nil, "can't write " .. dest end
        socketutil:set_timeout(socketutil.FILE_BLOCK_TIMEOUT, 300)
        local code, _headers, status = socket.skip(1, http.request{
            url = url,
            sink = socketutil.file_sink(handle),
        })
        socketutil:reset_timeout()
        if code ~= 200 then
            os.remove(dest)
            return nil, status or tostring(code)
        end
        return true
    end
    local body = {}
    socketutil:set_timeout(socketutil.LARGE_BLOCK_TIMEOUT, socketutil.LARGE_TOTAL_TIMEOUT)
    local code, _headers, status = socket.skip(1, http.request{
        url = url,
        sink = ltn12.sink.table(body),
    })
    socketutil:reset_timeout()
    if code ~= 200 then return nil, status or tostring(code) end
    return table.concat(body)
end

local function sayInfo(text, timeout)
    UIManager:show(InfoMessage:new{ text = text, timeout = timeout })
end

-- ---- plugin ------------------------------------------------------------------

function Rabisco:init()
    self.ui.menu:registerToMainMenu(self)
end

function Rabisco:installed()
    return parseManifest(readFile(installedManifestPath()))
end

function Rabisco:addToMainMenu(menu_items)
    menu_items.rabisco = {
        text = _("Rabisco"),
        sorting_hint = "more_tools",
        sub_item_table = {
            {
                text = _("Install or update"),
                keep_menu_open = true,
                callback = function() self:checkForUpdate() end,
            },
            {
                text = _("Use Rabisco sleep screens"),
                checked_func = function()
                    local dir = G_reader_settings:readSetting("screensaver_dir") or ""
                    return G_reader_settings:readSetting("screensaver_type") == "random_image"
                        and dir:find("/screensaver/", 1, true) ~= nil
                end,
                enabled_func = function() return self:installed() ~= nil end,
                callback = function() self:useSleepScreens() end,
            },
            {
                text_func = function()
                    local m = self:installed()
                    return m and T(_("Installed version: %1"), m.version) or _("Not installed yet")
                end,
                keep_menu_open = true,
                callback = function()
                    sayInfo(_("rabisco is a hand-drawn skin for koreader.\n\nfonts, icons and patches load when koreader starts. to switch a patch off, use patch management or rename it to end in .disabled."))
                end,
            },
            {
                text = _("Remove Rabisco"),
                enabled_func = function() return self:installed() ~= nil end,
                separator = true,
                callback = function() self:confirmRemove() end,
            },
        },
    }
end

function Rabisco:checkForUpdate()
    NetworkMgr:runWhenOnline(function()
        local text, err = fetch(REPO_URL .. MANIFEST_NAME)
        local remote = parseManifest(text)
        if not remote then
            logger.warn("Rabisco: manifest fetch failed", err)
            sayInfo(T(_("couldn't reach the rabisco repo (%1). check your wi-fi and try again."), tostring(err or "bad manifest")))
            return
        end
        local total = 0
        for _i, f in ipairs(remote.files) do total = total + (f.size or 0) end
        local mb = string.format("%.1f", total / 1048576)
        local current = self:installed()
        local question
        if current and current.version == remote.version then
            question = T(_("rabisco %1 is already installed.\n\ndownload it again? (%2 MB)"), remote.version, mb)
        elseif current then
            question = T(_("rabisco %1 is ready (you have %2).\n\nupdate now? (%3 MB)"), remote.version, current.version, mb)
        else
            question = T(_("install rabisco %1?\n\nthat's %2 files, %3 MB."), remote.version, #remote.files, mb)
        end
        UIManager:show(ConfirmBox:new{
            text = question,
            ok_text = current and _("update") or _("install"),
            cancel_text = _("not now"),
            ok_callback = function()
                -- let the dialog close before the download blocks the screen
                UIManager:nextTick(function() self:install(remote) end)
            end,
        })
    end)
end

function Rabisco:install(remote)
    local busy = InfoMessage:new{ text = _("downloading rabisco…\nthis can take a minute."), dismissable = false }
    UIManager:show(busy)
    UIManager:forceRePaint()

    local parts, failed = {}, nil
    for _i, f in ipairs(remote.files) do
        local dest = localPath(f.path)
        util.makePath(dirname(dest))
        local ok, err = fetch(REPO_URL .. f.path, dest .. ".part")
        if not ok then
            failed = f.path .. " (" .. tostring(err) .. ")"
            break
        end
        table.insert(parts, dest)
    end

    if failed then
        for _i, dest in ipairs(parts) do os.remove(dest .. ".part") end
        UIManager:close(busy)
        logger.warn("Rabisco: download failed", failed)
        sayInfo(T(_("the download stopped at %1.\n\nnothing was changed. try again when the wi-fi is steadier."), failed))
        return
    end

    -- everything arrived: move it all into place
    for _i, dest in ipairs(parts) do
        os.remove(dest)
        os.rename(dest .. ".part", dest)
    end

    -- remove files an older version had that this one no longer ships
    local old = self:installed()
    if old then
        local keep = {}
        for _i, f in ipairs(remote.files) do keep[f.path] = true end
        for _i, f in ipairs(old.files) do
            if not keep[f.path] then os.remove(localPath(f.path)) end
        end
    end

    local lines = { "version " .. remote.version }
    for _i, f in ipairs(remote.files) do
        table.insert(lines, string.format("file %d %s", f.size or 0, f.path))
    end
    util.makePath(dirname(installedManifestPath()))
    if not writeFile(installedManifestPath(), table.concat(lines, "\n") .. "\n") then
        logger.warn("Rabisco: couldn't save", installedManifestPath())
    end

    UIManager:close(busy)
    UIManager:askForRestart(T(_("rabisco %1 is installed. koreader needs to restart to use it."), remote.version))
end

function Rabisco:useSleepScreens()
    local m = self:installed()
    if not m then return end
    -- the screensaver folders are named WIDTHxHEIGHT; pick the closest to this screen
    local Screen = require("device").screen
    local w, h = Screen:getWidth(), Screen:getHeight()
    if w > h then w, h = h, w end
    local best, best_d
    for _i, f in ipairs(m.files) do
        local fw, fh = f.path:match("^screensaver/(%d+)x(%d+)/")
        if fw then
            local d = math.abs(tonumber(fw) - w) + math.abs(tonumber(fh) - h)
            if not best_d or d < best_d then
                best, best_d = "screensaver/" .. fw .. "x" .. fh, d
            end
        end
    end
    if not best then
        sayInfo(_("no rabisco sleep screens found. try install or update first."))
        return
    end
    G_reader_settings:saveSetting("screensaver_type", "random_image")
    G_reader_settings:saveSetting("screensaver_dir", localPath(best))
    sayInfo(T(_("sleep screens set: %1"), best:match("[^/]+$")), 3)
end

function Rabisco:confirmRemove()
    UIManager:show(ConfirmBox:new{
        text = _("remove rabisco's fonts, icons, patches and sleep screens?\n\nthis installer stays, so you can bring it back later."),
        ok_text = _("remove"),
        cancel_text = _("keep"),
        ok_callback = function()
            local m = self:installed()
            if not m then return end
            for _i, f in ipairs(m.files) do
                if f.path:sub(1, #SELF_PREFIX) ~= SELF_PREFIX then
                    os.remove(localPath(f.path))
                end
            end
            os.remove(installedManifestPath())
            local dir = G_reader_settings:readSetting("screensaver_dir") or ""
            if dir:find("/screensaver/", 1, true) then
                G_reader_settings:saveSetting("screensaver_type", "disable")
            end
            UIManager:askForRestart(_("rabisco is removed. koreader needs to restart."))
        end,
    })
end

return Rabisco
