--[[
TODO:
1. Animations
2. Spell effects need to repeat
3. Side-by-side comparison option
4. (minor) UI could use nice borders
]]--

-- Namespace
local addonname, internal = ...

_G.MMOCAddon = internal

-- Localized
local GetTime, format, math, pi, pihalf = _G.GetTime, format, math, math.pi, math.pi / 2

-- Locals
local i
local firstGetTime = 0
internal.rotateFrequency = 0.01
internal.defaultAnimation = 0
internal.repeatFrequency = 0

-- Constants
local STARTUPMODEL = "Character\\Human\\Male\\HumanMale.m2"
local BACKGROUNDTEXTURE = "Interface\\AddOns\\MMOCViewer\\background.tga"
local FACING = {
	["front"] = 0, ["back"] = math.pi,
	["left-side"] = -(math.pi / 2), ["right-side"] = math.pi / 2,
	["right-semiside"] = 0.75, ["left-semiside"] = -0.75,
}
local ITEMFACINGS = {
	["front"] = {"INVTYPE_HEAD", "INVTYPE_BODY", "INVTYPE_CHEST", "INVTYPE_ROBE", "INVTYPE_LEGS", "INVTYPE_WAIST", "INVTYPE_TABARD", "INVTYPE_SHOULDER"},
	["back"] = {"INVTYPE_CLOAK"},
	["right-side"] = {"INVTYPE_WRIST", "INVTYPE_WEAPON", "INVTYPE_SHIELD", "INVTYPE_2HWEAPON", "INVTYPE_WEAPONMAINHAND", "INVTYPE_RANGED", "INVTYPE_THROWN", "INVTYPE_RANGEDRIGHT", "INVTYPE_RELIC"},
	["left-side"] = {"INVTYPE_WEAPONOFFHAND", "INVTYPE_HOLDABLE"},
	["right-semiside"] = {"INVTYPE_HAND", "INVTYPE_FEET"},
}

-- Set up fullscreen, logo-tiled frame
local function MMOC_FullscreenFrame(frame, frameIsModel)
    frame:ClearAllPoints()
    if not frameIsModel then
        texture = frame:CreateTexture("MMOC_Logo", "BACKGROUND")
        texture:SetPoint("TOPLEFT", UIParent, "TOPLEFT")
        texture:SetPoint("BOTTOMRIGHT", UIParent, "BOTTOMRIGHT")
        texture:SetTexture(BACKGROUNDTEXTURE, true)
        texture:SetTexCoord(0, 3, 0, 2)
        frame:EnableMouse(true)
        frame:EnableMouseWheel(true)
        frame:SetMovable(true)
        frame:EnableMouse(true)
        frame:SetClampedToScreen(false)
        frame:RegisterForDrag("LeftButton")
        frame:SetSize(UIParent:GetWidth(), UIParent:GetHeight())
        frame:SetPoint("TOP", UIParent, "TOP")
        frame:SetPoint("LEFT", UIParent, "LEFT")
        frame:SetPoint("RIGHT", UIParent, "RIGHT")
        frame:SetPoint("BOTTOM", UIParent, "BOTTOM", 0, 80)
    else
        frame:SetSize(1920, 1080)
        frame:SetPoint("CENTER", UIParent, "CENTER")
    end
    frame:Hide()
end

-- Create frame
local MMOC = CreateFrame("Frame", "MMOCViewer_Frame", UIParent)
MMOC_FullscreenFrame(MMOC, false)
internal.MMOC = MMOC

-- Create models
local MMOC_DressUp = CreateFrame("DressUpModel", "MMOC_DressUpModel", MMOC)
MMOC_FullscreenFrame(MMOC_DressUp, true)
local MMOC_Player = CreateFrame("PlayerModel", "MMOC_PlayerModel", MMOC)
MMOC_FullscreenFrame(MMOC_Player, true)
local MMOC_Cinematic = CreateFrame("CinematicModel", "MMOC_CinematicModel", MMOC)
MMOC_FullscreenFrame(MMOC_Cinematic, true)

-- Primary camera functions
local function MMOC_SetOrientation(model, distance, yaw, pitch)
	if model:HasCustomCamera() then
		model.distance, model.yaw, model.pitch = distance, yaw, pitch
		local x = distance * math.cos(yaw) * math.cos(pitch)
		local y = distance * math.sin(- yaw) * math.cos(pitch)
		local z = (distance * math.sin(- pitch))
		model:SetCameraPosition(x, y, z)
	end
end
local function MMOC_ResetCamera(model)
    model.mx, model.my, model.mz, model.rotate = 0, 0, 0, 0
	model:SetPosition(model.mx, model.my, model.mz)
    model:SetRotation(math.rad(model.rotate))
	model:RefreshCamera()
    model:SetCustomCamera(1)
	if model:HasCustomCamera() then
		local x, y, z = model:GetCameraPosition()
		model.baseX, model.baseY, model.baseZ = model:GetCameraTarget()
		model:SetCameraTarget(0, model.baseY, model.baseZ)
		local distance = math.sqrt(x * x + y * y + z * z)
		local yaw = - math.atan(y / x)
		local pitch = - math.atan(z / x)
		MMOC_SetOrientation(internal.aModel, distance, yaw, pitch)
    end
end
local function MMOC_MagicRotate(model, ...)
    if internal.rotateFrequency == 0 then return end
    if firstGetTime > 0 then
        local timeSinceRun = GetTime() - firstGetTime
        if timeSinceRun > internal.rotateFrequency then
            firstGetTime = GetTime()
            model:SetFacing(model:GetFacing()+0.005)
        end
    else
        firstGetTime = GetTime()
    end
end
local function MMOC_MagicRepeat(model, ...)
    --[[if internal.rotateFrequency == 0 then return end
    if firstGetTime > 0 then
        local timeSinceRun = GetTime() - firstGetTime
        if timeSinceRun > internal.rotateFrequency then
            firstGetTime = GetTime()
            model:SetFacing(model:GetFacing()+0.005)
        end
    else
        firstGetTime = GetTime()
    end]]--
end

-- Insecurely hook DressUpItemLink
_G.DressUpItemLink = function(item, ...) if (internal.aModel) and (internal.aModel == MMOC_DressUp) then internal.aModel:TryOn(item) else internal.MMOC_ActivateDressUp(item) end end

-- Player Models and Items: Activate DressUpModel
function internal.MMOC_ProcessItems(msg)
    -- Remove spaces
    local tempString = gsub(strtrim(msg), " ", "")
    
    -- Check for comma-separated list
    if strfind(tempString, ",") then
        -- Split input on commas, and put into an array
        local itemList = { strsplit(",", tempString) }
        
        -- Run through list and try on each item
        for i = 1, #itemList do
            -- If DressUpModel is not active, make it active first
            if (i > 1) and (internal.aModel) and (internal.aModel == MMOC_DressUp) then
                internal.aModel:TryOn(itemList[i])
            else
                internal.MMOC_ActivateDressUp(itemList[i])
            end
        end
    else
        internal.MMOC_ActivateDressUp(tempString)
    end
end
function internal.MMOC_ActivateDressUp(link)
    if internal.aModel then internal.aModel:SetScript("OnUpdate", nil) end
    
    -- Show UI
    internal.MMOCUI_Toggle("show")
    
    -- Set active model and show it
    internal.aModel = MMOC_DressUp
    
    -- Clear model, set new model, then reset camera
    internal.aModel:Show()
    internal.aModel:ClearModel()
    internal.aModel:SetUnit("player")
    internal.aModel:TryOn(link)
    MMOC_ResetCamera(internal.aModel)
    internal.aModel:SetScript("OnUpdate", MMOC_MagicRotate)

	-- Figure out the position of the model based on equip type
	local itemSlot = select(9, GetItemInfo(link))
	local facingType = "front"

	for type, list in pairs(ITEMFACINGS) do
		for _, slot in pairs(list) do
			if( itemSlot == slot ) then
				facingType = type
				break
			end
		end
	end
    
	MMOC_DressUp.facingType = facingType
	MMOC_DressUp.rotation = FACING[MMOC_DressUp.facingType] or FACING.front
	MMOC_DressUp:SetFacing(MMOC_DressUp.rotation)
end

-- Items: Hook CTRL+Clicked links
hooksecurefunc(DressUpModel, "TryOn", function(self, link)
    -- This is required because the 4.3.x models have a ControlFrame which auto-shows on mouseover - we don't want this.
    DressUpModel:HookScript("OnEnter", function(self)
        self.controlFrame:Hide()
    end)
    
    internal.MMOC_ActivateDressUp(link)
end)

-- Creatures: Activate PlayerModel
function internal.MMOC_ActivatePlayer(creatureID)
    if internal.aModel then internal.aModel:SetScript("OnUpdate", nil) end
    
    -- Show UI
    internal.MMOCUI_Toggle("show")
    
    -- Set active model
    internal.aModel = MMOC_Player
    
    -- Clear model, set new model, then reset camera
    internal.aModel:Show()
    internal.aModel:ClearModel()
    if strfind(creatureID, ".m2") or strfind(creatureID, ".M2") then
        internal.aModel:SetModel(creatureID)
    else
        internal.aModel:SetDisplayInfo(tonumber(creatureID))
    end
    MMOC_ResetCamera(internal.aModel)
    internal.aModel:SetScript("OnUpdate", MMOC_MagicRotate)
end

-- Spells: Activate CinematicModel
function internal.MMOC_ProcessSpellVisualKits(msg)
    -- Remove spaces, split input on commas, and put into an array
    local tempString = gsub(strtrim(msg), " ", "")
    local kitIDList = { strsplit(",", tempString) }
    
    -- Run through list and try on each item
    for i = 1, #kitIDList do
        -- If CinematicModel is not active, make it active first
        if internal.aModel == MMOC_Cinematic then
            internal.aModel:SetSpellVisualKit(kitIDList[i])
        else
            internal.MMOC_ActivateCinematic(kitIDList[i])
        end
    end
end
function internal.MMOC_ActivateCinematic(kitID)
    if internal.aModel then internal.aModel:SetScript("OnUpdate", nil) end
    
    -- Show UI
    internal.MMOCUI_Toggle("show")
    
    -- Set active model
    internal.aModel = MMOC_Cinematic
    
    -- Clear model, set new model, then reset camera
    internal.aModel:Show()
    internal.aModel:ClearModel()
    internal.aModel:SetUnit("player")
    internal.aModel:SetSpellVisualKit(kitID)
    MMOC_ResetCamera(internal.aModel)
    internal.aModel:SetScript("OnUpdate", MMOC_MagicRotate)
end

-- Script-triggered camera functions
--[[local function LeftButtonOnUpdate(frame, elapsed)
end]]--
local function RightButtonOnUpdate(frame, elapsed)
	if not IsMouseButtonDown("RightButton") then
		return
	end
    local x, y = GetCursorPosition()
    if IsControlKeyDown() then
        local px, py, pz = internal.aModel:GetPosition()
        internal.aModel.mx = format("%.2f", (px + (y - frame.y) / 64))
		if format("%.2f", px) ~= internal.aModel.mx then
			internal.aModel:SetPosition(tonumber(internal.aModel.mx), py, pz)
        end
    elseif IsAltKeyDown() then
		local px, py, pz = internal.aModel:GetPosition()
		internal.aModel.my = format("%.2f", (py + (x - frame.x) / 64))
		internal.aModel.mz = format("%.2f", (pz + (y - frame.y) / 64))
		if format("%.2f", py) ~= internal.aModel.my or format("%.2f", pz) ~= internal.aModel.mz then
			internal.aModel:SetPosition(px, tonumber(internal.aModel.my), tonumber(internal.aModel.mz))
        end
    else
		if not internal.aModel.distance or not internal.aModel.yaw or not internal.aModel.pitch then
			return
		end
		local pitch = internal.aModel.pitch + (y - frame.y) * pi / 256
		local limit = false
		if pitch > pihalf - 0.05 or pitch < - pihalf + 0.05 then
			limit = true
		end
		if limit then
			internal.aModel.rotate = format("%.0f", math.abs(math.deg(((x - frame.x) / 64 + internal.aModel:GetFacing())) % 360))
			if internal.aModel.rotate ~= format("%.0f", math.abs(math.deg(internal.aModel:GetFacing()) % 360)) then
				internal.aModel:SetRotation(math.rad(internal.aModel.rotate))
			end
		else
			local yaw = internal.aModel.yaw + (x - frame.x) * pi / 256
			MMOC_SetOrientation(internal.aModel, internal.aModel.distance, yaw, pitch)
		end
    end
    frame.x, frame.y = x, y
end
local function MiddleButtonOnUpdate(frame, elapsed)
	if not IsMouseButtonDown("MiddleButton") then
		return
	end
    local x, y = GetCursorPosition()
    internal.aModel.rotate = format("%.0f", math.abs(math.deg(((x - frame.x) / 84 + internal.aModel:GetFacing())) % 360))
    if internal.aModel.rotate ~= format("%.0f", math.abs(math.deg(internal.aModel:GetFacing()) % 360)) then
        internal.aModel:SetRotation(math.rad(internal.aModel.rotate))
    end
    frame.x, frame.y = x, y
end
local function OnMouseDown(frame, button)
    frame.x, frame.y = GetCursorPosition()
    --[[if button == "LeftButton" then
        frame.x, frame.y = GetCursorPosition()
        frame:SetScript("OnUpdate", LeftButtonOnUpdate)
    else]]--
    if button == "RightButton" then
        frame:SetScript("OnUpdate", RightButtonOnUpdate)
    elseif button == "MiddleButton" then
        if IsAltKeyDown() then
            MMOC_ResetCamera(internal.aModel)
        else
            frame:SetScript("OnUpdate", MiddleButtonOnUpdate)
        end
    end
end
local function OnMouseUp(frame, button)
    --[[if button == "LeftButton" then
        frame:SetScript("OnUpdate", nil)
    else]]--
    if button == "RightButton" then
        frame:SetScript("OnUpdate", nil)
    elseif button == "MiddleButton" then
        frame:SetScript("OnUpdate", nil)
    end
end
local function OnMouseWheel(frame, delta)
	if not internal.aModel.distance or not internal.aModel.yaw or not internal.aModel.pitch then
		return
	end
    local zoom = 0.15
    if IsControlKeyDown() then
        zoom = 0.01
    elseif IsAltKeyDown() then
        zoom = 0.5
    end
    local distance = internal.aModel.distance - delta * zoom
    if distance > 40 then
        distance = 40
    elseif distance < zoom then
        distance = zoom
    end
    MMOC_SetOrientation(internal.aModel, distance, internal.aModel.yaw, internal.aModel.pitch)
end
local function OnEnter(frame)
	frame:EnableMouseWheel(true)
	frame:SetScript("OnKeyUp", OnKeyUp)
	frame:SetScript("OnDragStart", OnDragStart)
	frame:SetScript("OnDragStop", OnDragStop)
	frame:SetScript("OnMouseDown", OnMouseDown)
	frame:SetScript("OnMouseUp", OnMouseUp)
	frame:SetScript("OnMouseWheel", OnMouseWheel)
    internal.MMOCUI.Hide()
end
local function OnLeave(frame)
	frame:EnableMouseWheel(false)
	frame:SetScript("OnKeyUp", nil)
	frame:SetScript("OnDragStart", nil)
	frame:SetScript("OnDragStop", nil)
	frame:SetScript("OnMouseDown", nil)
	frame:SetScript("OnMouseUp", nil)
	frame:SetScript("OnMouseWheel", nil)
end
MMOC:EnableMouseWheel(true)
MMOC:SetScript("OnKeyUp", OnKeyUp)
MMOC:SetScript("OnDragStart", OnDragStart)
MMOC:SetScript("OnDragStop", OnDragStop)
MMOC:SetScript("OnMouseDown", OnMouseDown)
MMOC:SetScript("OnMouseUp", OnMouseUp)
MMOC:SetScript("OnMouseWheel", OnMouseWheel)

--[[-- Message Processing
local funcion MMOC_DisplayItem(msg)
    -- Sanitize input and get a true itemLink based on the itemID or itemLink given to us
    local tempString = strtrim(msg)
    local _, itemLink
    if strfind(tempString, "item") then
        _, itemLink = GetItemInfo(tempString)
    else
        _, itemLink = GetItemInfo(tonumber(tempString))
    end
    
    MMOC_ActivateDressUp(itemLink)
end
local function MMOC_DisplayCreature(msg)
    MMOC_ActivatePlayer(tonumber(strtrim(msg)))
end
local function MMOC_DisplaySpell(msg)
    MMOC_ActivateCinematic(spellKitID1, spellKitID2, spellKitID3, spellKitID4, spellKitID5)
end
local function MMOC_Exit(msg)
    if rIMV_Icon then rIMV_Icon:Show() end
    if rISV_Icon then rISV_Icon:Show() end
    MainMenuBar:Show()
    MMOC:Hide()
    MMOC_DressUp:Hide()
    MMOC_Player:Hide()
    MMOC_Cinematic:Hide()
end

-- Enable slash command functionality
SlashCmdList["MMOCDRESSUP"] = MMOC_DisplayItem;
SlashCmdList["MMOCPLAYER"] = MMOC_DisplayCreature;
SlashCmdList["MMOCCINEMATIC"] = MMOC_DisplaySpell;
SlashCmdList["MMOCEXIT"] = MMOC_Exit;
SLASH_MMOCDRESSUP1 = "/mmoitem"
SLASH_MMOCDRESSUP2 = "/mmoi"
SLASH_MMOCDRESSUP3 = "/item"
SLASH_MMOCPLAYER1 = "/mmocreature"
SLASH_MMOCPLAYER2 = "/mmoc"
SLASH_MMOCPLAYER3 = "/creature"
SLASH_MMOCCINEMATIC1 = "/mmospell"
SLASH_MMOCCINEMATIC2 = "/mmos"
SLASH_MMOCCINEMATIC3 = "/spell"
SLASH_MMOCEXIT1 = "/mmoexit"
SLASH_MMOCEXIT2 = "/mexit"
SLASH_MMOCEXIT3 = "/me"]]--