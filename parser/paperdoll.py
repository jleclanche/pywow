#!/usr/bin/python
# -*- coding: utf-8 -*-


default = {
	"ATTACK_POWER": "<Attack Power>",
	"ARMOR": "<Armor>",
	"MAIN_WPN_HANDS": "<Main Weapon Hands>",
	"MAX_MAIN_WPN_DMG": "<Max Main Weapon Damage>",
	"MIN_MAIN_WPN_DMG": "<Min Main Weapon Damage",
	"MAX_MAIN_WPN_BASEDMG": "<Max Main Weapon Base Damage>",
	"MIN_MAIN_WPN_BASEDMG": "<Min Main Weapon Base Damage>",
	"MAIN_WPN_SPEED": "<Main Weapon Speed>",
	"PLAYER_LVL": "<Level>",
	"RANGED_ATTACK_POWER": "<Ranged Attack Power>",
	"MAX_RANGED_WPN_BASEDMG": "<Max Ranged Weapon Base Damage>",
	"MIN_RANGED_WPN_BASEDMG": "<Min Ranged Weapon Base Damage>",
	"SPELL_POWER_HOLY": "<Holy Spell Power>",
	"SPIRIT": "<Spirit>",
	"HOME": "<Home>",
	"GENDER": "<Gender>",
}

class Paperdoll(dict):
	def __init__(self, d={}):
		self.update(dict((k, default[k]) for k in default if k not in d))
