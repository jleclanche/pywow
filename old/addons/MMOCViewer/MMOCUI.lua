-- Namespace
local _, internal = ...

-- Localized
internal.MMOCUI = CreateFrame("Frame", "MMOC_UI", MMOCViewer_Frame)
local MMOCUI = internal.MMOCUI

-- Locals
local lastFontstring
local lastEditbox

-- Constants
local COLOR_R, COLOR_G, COLOR_B, COLOR_A = 0.2, 0.2, 0.2, 1
local SND_SWAP    = "INTERFACESOUND_LOSTTARGETUNIT"
local SND_SELECT  = "igMainMenuOption"
local SND_CLOSE   = "igMainMenuLogout"

-- Set UI panel appearance
MMOCUI:SetPoint("LEFT", UIParent, "LEFT")
MMOCUI:SetPoint("BOTTOM", UIParent, "BOTTOM")
MMOCUI:SetPoint("RIGHT", UIParent, "RIGHT")
MMOCUI:SetPoint("TOP", UIParent, "BOTTOM", 0, 80)
local texture = MMOCUI:CreateTexture(nil, "BACKGROUND", nil, -8)
texture:SetAllPoints(MMOCUI)
texture:SetTexture(COLOR_R * 0.5, COLOR_G * 0.5, COLOR_B * 0.5, COLOR_A)
MMOCUI.tex = texture
MMOCUI.tex:Hide()
MMOCUI:Show()

-- Batch creation functions for fontstrings and editboxes
local function CreateFontstring(text, width, height, anchorPoint, relativeTo, relativePoint, xoff, yoff, font)
	local realfont = font or "GameFontNormal"
	local fontstring = MMOCUI:CreateFontString(nil, "BACKGROUND", realfont)
	fontstring:SetJustifyH("CENTER")
	fontstring:SetJustifyV("MIDDLE")
	fontstring:SetPoint(anchorPoint, relativeTo, relativePoint, xoff, yoff)
	fontstring:SetSize(width, height)
	fontstring:SetText(" " .. text)
    fontstring:Hide()
	lastFontstring = fontstring
	return fontstring
end
local function CreateEditbox(name, width, height, anchorPoint, relativeTo, relativePoint, xoff, yoff, font)
	local editbox = CreateFrame("EditBox", "MMOC_Editbox_" .. name, MMOCUI, "InputBoxTemplate")
	editbox:SetPoint(anchorPoint, relativeTo, relativePoint, xoff, yoff)
	editbox:SetSize(width, height)
	if font then editbox.text:SetFontObject(font) end
    editbox:Hide()
	lastEditbox = editbox
	return editbox
end

-- Rotate Frequency
MMOCUI.NameRotateFrequency = CreateFontstring("Rotate Frequency", 140, 16, "CENTER", MMOCUI, "BOTTOM", -500, 60)
MMOCUI.OptRotateFrequency = CreateEditbox("RotateFrequency", 100, 20, "CENTER", MMOCUI, "BOTTOM", -500, 40)
MMOCUI.OptRotateFrequency:SetText(tostring(internal.rotateFrequency))
MMOCUI.OptRotateFrequency:SetScript("OnEnterPressed", function(self, ...)
    PlaySound(SND_SWAP)
    internal.rotateFrequency = tonumber(self:GetText())
end)

-- Set Item
MMOCUI.NameSetItem = CreateFontstring("Set Item(s)", 140, 16, "CENTER", MMOCUI, "BOTTOM", -300, 60)
MMOCUI.OptSetItem = CreateEditbox("SetItem", 100, 20, "CENTER", MMOCUI, "BOTTOM", -300, 40)
MMOCUI.OptSetItem:SetScript("OnEnterPressed", function(self, ...)
    PlaySound(SND_SWAP)
    print(self:GetText())
    internal.MMOC_ProcessItems(self:GetText())
end)

-- Set Creature
MMOCUI.NameSetCreature = CreateFontstring("Set Creature/M2", 140, 16, "CENTER", MMOCUI, "BOTTOM", -100, 60)
MMOCUI.OptSetCreature = CreateEditbox("SetCreature", 100, 20, "CENTER", MMOCUI, "BOTTOM", -100, 40)
MMOCUI.OptSetCreature:SetScript("OnEnterPressed", function(self, ...)
    PlaySound(SND_SWAP)
    internal.MMOC_ActivatePlayer(strtrim(self:GetText()))
end)

-- Set Spell Visual Kit
MMOCUI.NameSetSpellVisualKit = CreateFontstring("Set Spell Visual Kit(s)", 140, 16, "CENTER", MMOCUI, "BOTTOM", 100, 60)
MMOCUI.OptSetSpellVisualKit = CreateEditbox("SetSpellVisualKit", 100, 20, "CENTER", MMOCUI, "BOTTOM", 100, 40)
MMOCUI.OptSetSpellVisualKit:SetScript("OnEnterPressed", function(self, ...)
    PlaySound(SND_SWAP)
    internal.MMOC_ProcessSpellVisualKits(self:GetText())
end)

-- Set Animation
MMOCUI.NameSetAnimation = CreateFontstring("Set Animation", 140, 16, "CENTER", MMOCUI, "BOTTOM", 300, 60)
MMOCUI.OptSetAnimation = CreateEditbox("SetAnimation", 100, 20, "CENTER", MMOCUI, "BOTTOM", 300, 40)
MMOCUI.OptSetAnimation:SetText(tostring(internal.defaultAnimation))
MMOCUI.TextSetAnimation = CreateFontstring(" ", 140, 16, "CENTER", MMOCUI, "BOTTOM", 300, 20)
if internal.AnimationList[internal.defaultAnimation] and MMOCUI.TextSetAnimation then
    MMOCUI.TextSetAnimation:SetText(internal.defaultAnimation .. ". " .. internal.AnimationList[internal.defaultAnimation])
elseif MMOCUI.TextSetAnimation then
    MMOCUI.TextSetAnimation:SetText("Unknown Animation #" .. internal.defaultAnimation)
end
MMOCUI.OptSetAnimation:SetScript("OnEnterPressed", function(self, ...)
    PlaySound(SND_SWAP)
    local selectedAnimation = tonumber(self:GetText())
    if internal.AnimationList[selectedAnimation] and MMOCUI.TextSetAnimation then
        MMOCUI.TextSetAnimation:SetText(selectedAnimation .. ". " .. internal.AnimationList[selectedAnimation])
    elseif MMOCUI.TextSetAnimation then
        MMOCUI.TextSetAnimation:SetText("Unknown Animation #" .. selectedAnimation)
    end
    if internal.aModel then
        internal.aModel:SetAnimation(internal.defaultAnimation)
        internal.aModel:SetAnimation(selectedAnimation)
    end
end)

-- Set Repeat Frequency
MMOCUI.NameRepeatFrequency = CreateFontstring("Repeat Frequency", 140, 16, "CENTER", MMOCUI, "BOTTOM", 500, 60)
MMOCUI.OptRepeatFrequency = CreateEditbox("RepeatFrequency", 100, 20, "CENTER", MMOCUI, "BOTTOM", 500, 40)
MMOCUI.OptRepeatFrequency:SetText(tostring(internal.repeatFrequency))
MMOCUI.OptRepeatFrequency:SetScript("OnEnterPressed", function(self, ...)
    PlaySound(SND_SWAP)
    internal.repeatFrequency = tonumber(self:GetText())
end)

-- Enter and Leave scripts for UI Panel
function MMOCUI.Show(frame)
    if not MMOCViewer_Frame:IsMouseOver() then
        MMOCUI.tex:Show()
        MMOCUI.NameRotateFrequency:Show()
        MMOCUI.OptRotateFrequency:Show()
        MMOCUI.NameSetItem:Show()
        MMOCUI.OptSetItem:Show()
        MMOCUI.NameSetCreature:Show()
        MMOCUI.OptSetCreature:Show()
        MMOCUI.NameSetSpellVisualKit:Show()
        MMOCUI.OptSetSpellVisualKit:Show()
        MMOCUI.NameSetAnimation:Show()
        MMOCUI.OptSetAnimation:Show()
        MMOCUI.TextSetAnimation:Show()
        MMOCUI.NameRepeatFrequency:Show()
        MMOCUI.OptRepeatFrequency:Show()
    end
end
function MMOCUI.Hide(frame)
    if MMOCViewer_Frame:IsMouseOver() then
        MMOCUI.tex:Hide()
        MMOCUI.NameRotateFrequency:Hide()
        MMOCUI.OptRotateFrequency:Hide()
        MMOCUI.NameSetItem:Hide()
        MMOCUI.OptSetItem:Hide()
        MMOCUI.NameSetCreature:Hide()
        MMOCUI.OptSetCreature:Hide()
        MMOCUI.NameSetSpellVisualKit:Hide()
        MMOCUI.OptSetSpellVisualKit:Hide()
        MMOCUI.NameSetAnimation:Hide()
        MMOCUI.OptSetAnimation:Hide()
        MMOCUI.TextSetAnimation:Hide()
        MMOCUI.NameRepeatFrequency:Hide()
        MMOCUI.OptRepeatFrequency:Hide()
    end
end
MMOCUI:SetScript("OnEnter", MMOCUI.Show)
MMOCUI:SetScript("OnLeave", MMOCUI.Hide)

-- Toggle UI
function internal.MMOCUI_ModelToggle()
    MMOC_DressUpModel:Hide()
    MMOC_PlayerModel:Hide()
    MMOC_CinematicModel:Hide()
    internal.aModel = nil
end
function internal.MMOCUI_Toggle(forceState)
    if (MMOCViewer_Frame:IsVisible() and ((not forceState) or (forceState ~= "show"))) or (forceState and forceState == "hide") then
        if rIMV_Icon then rIMV_Icon:Show() end
        if rISV_Icon then rISV_Icon:Show() end
        MainMenuBar:Show()
        MMOCViewer_Frame:Hide()
        MMOCUI.Hide()
    else
        if rIMV_Icon then rIMV_Icon:Hide() end
        if rISV_Icon then rISV_Icon:Hide() end
        MainMenuBar:Hide()
        MMOCViewer_Frame:Show()
        MMOCUI.Show()
    end
    internal.MMOCUI_ModelToggle()
end

-- Enable slash command functionality
SlashCmdList["MMOCUITOGGLE"] = internal.MMOCUI_Toggle;
SLASH_MMOCUITOGGLE1 = "/mmo"
SLASH_MMOCUITOGGLE2 = "/mmoc"