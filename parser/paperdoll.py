#!/usr/bin/python
# -*- coding: utf-8 -*-


default = {
	"ATTACK_POWER": "[Attack Power]",
	"ARMOR": "[Armor]",
	"BONUS_HEALING": "[Bonus Healing]",
	"MAIN_WPN_HANDS": "[Main Weapon Hands]",
	"MAIN_WPN_DMG": "[Main Weapon Damage]",
	"MAIN_WPN_BASEDMG": "[Main Weapon Base Damage]",
	"MAIN_WPN_SPEED": "[Main Weapon Speed]",
	"PLAYER_LVL": "[Level]",
	"RANGED_ATTACK_POWER": "[Ranged Attack Power]",
	"RANGED_WPN_BASEDMG": "[Ranged Weapon Base Damage]",
	"PERCENT_ARCANE": "[Percent Arcane]",
	"PERCENT_FIRE": "[Percent Fire]",
	"PERCENT_FROST": "[Percent Frost]",
	"PERCENT_HOLY": "[Percent Holy]",
	"PERCENT_NATURE": "[Percent Nature]",
	"PERCENT_SHADOW": "[Percent Shadow]",
	"PERCENT_BONUS_HEALING": "[Percent Healing]",
	"PERCENT_BONUS_HEALING_DAMAGE": "[Percent Healing Damage]",
	"PERCENT_BC2": "[Percent BC2]",
	"SPELL_POWER": "[Spell Power]",
	"SPELL_POWER_ARCANE": "[Arcane Spell Power]",
	"SPELL_POWER_FIRE": "[Fire Spell Power]",
	"SPELL_POWER_FROST": "[Frost Spell Power]",
	"SPELL_POWER_HOLY": "[Holy Spell Power]",
	"SPELL_POWER_NATURE": "[Nature Spell Power]",
	"SPELL_POWER_SHADOW": "[Shadow Spell Power]",
	"SPIRIT": "[Spirit]",
	"HOME": "[Home]",
	"GENDER": "[Gender]",
}

class Paperdoll(dict):
	def __init__(self, d={}):
		self.update(dict((k, default[k]) for k in default if k not in d))
