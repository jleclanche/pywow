# -*- coding: utf-8 -*-

from .. import globalstrings

## Possibly useful
#ITEM_MOD_DAMAGE_PER_SECOND_SHORT = "Damage Per Second"
#ITEM_MOD_MASTERY_RATING_SPELL = "(%s)"
#ITEM_MOD_MASTERY_RATING_TWO_SPELLS = "(%s/%s)"
#ITEM_MOD_POWER_REGEN0_SHORT = "Mana Per 5 Sec."
#ITEM_MOD_POWER_REGEN1_SHORT = "Rage Per 5 Sec."
#ITEM_MOD_POWER_REGEN2_SHORT = "Focus Per 5 Sec."
#ITEM_MOD_POWER_REGEN3_SHORT = "Energy Per 5 Sec."
#ITEM_MOD_POWER_REGEN4_SHORT = "Happiness Per 5 Sec."
#ITEM_MOD_POWER_REGEN5_SHORT = "Runes Per 5 Sec."
#ITEM_MOD_POWER_REGEN6_SHORT = "Runic Power Per 5 Sec."


class Stat(object):
	EXTRA_ARMOR       = 50
	FIRE_RESISTANCE   = 51
	FROST_RESISTANCE  = 52
	SHADOW_RESISTANCE = 54
	NATURE_RESISTANCE = 55
	ARCANE_RESISTANCE = 56
	
	TABLE = {
		1: "HEALTH",
		3: "AGILITY",
		4: "STRENGTH",
		5: "INTELLECT",
		6: "SPIRIT",
		7: "STAMINA",
		12: "DEFENSE_SKILL_RATING",
		13: "DODGE_RATING",
		14: "PARRY_RATING",
		15: "BLOCK_RATING",
		16: "HIT_MELEE_RATING",
		17: "HIT_RANGED_RATING",
		18: "HIT_SPELL_RATING",
		19: "CRIT_MELEE_RATING",
		20: "CRIT_RANGED_RATING",
		21: "CRIT_SPELL_RATING",
		22: "HIT_MELEE_TAKEN_RATING",
		23: "HIT_RANGED_TAKEN_RATING",
		24: "HIT_SPELL_TAKEN_RATING",
		25: "CRIT_MELEE_TAKEN_RATING",
		26: "CRIT_RANGED_TAKEN_RATING",
		27: "CRIT_SPELL_TAKEN_RATING",
		28: "HASTE_MELEE_RATING",
		29: "HASTE_RANGED_RATING",
		30: "HASTE_SPELL_RATING",
		31: "HIT_RATING",
		32: "CRIT_RATING",
		33: "HIT_TAKEN_RATING",
		34: "CRIT_TAKEN_RATING",
		35: "RESILIENCE_RATING",
		36: "HASTE_RATING",
		37: "EXPERTISE_RATING",
		38: "ATTACK_POWER",
		39: "RANGED_ATTACK_POWER",
		40: "FERAL_ATTACK_POWER",
		41: "SPELL_HEALING_DONE",
		42: "SPELL_DAMAGE_DONE",
		43: "MANA_REGENERATION",
		44: "ARMOR_PENETRATION_RATING",
		45: "SPELL_POWER",
		46: "HEALTH_REGENERATION",
		47: "SPELL_PENETRATION",
		48: "BLOCK_VALUE",
		49: "MASTERY_RATING",
		50: "EXTRA_ARMOR",
		51: "FIRE_RESISTANCE",
		52: "FROST_RESISTANCE",
		54: "SHADOW_RESISTANCE",
		55: "NATURE_RESISTANCE",
		56: "ARCANE_RESISTANCE",
	}
	
	RESISTANCES = {
		FIRE_RESISTANCE  : globalstrings.DAMAGE_SCHOOL3,
		FROST_RESISTANCE : globalstrings.DAMAGE_SCHOOL5,
		SHADOW_RESISTANCE: globalstrings.DAMAGE_SCHOOL6,
		NATURE_RESISTANCE: globalstrings.DAMAGE_SCHOOL4,
		ARCANE_RESISTANCE: globalstrings.DAMAGE_SCHOOL7,
	}
	
	def __init__(self, id):
		if id not in self.TABLE:
			raise ValueError("Unknown stat: %r" % (id))
		
		self.id = id
		
		if not self.isResistance() and not self.isExtraArmor():
			name = "ITEM_MOD_" + self.TABLE[id]
			self.text = getattr(globalstrings, name)
			self.name = getattr(globalstrings, name + "_SHORT")
	
	def getResistanceText(self):
		return self.RESISTANCES.get(self.id, "")
	
	def getText(self, amount):
		if not self.isExtraArmor():
			if self.isResistance():
				return globalstrings.ITEM_RESIST_SINGLE % (amount, self.getResistanceText())
			return self.text % (amount)
	
	def isExtraArmor(self):
		return self.id == self.EXTRA_ARMOR
	
	def isResistance(self):
		return self.id in self.RESISTANCES
	
	def isSpecial(self):
		return self.id > 10 and not self.isResistance()
