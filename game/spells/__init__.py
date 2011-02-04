# -*- coding: utf-8 -*-
"""
Spells
 - Spell.dbc
"""

from .. import *
from .. import durationstring
from ..globalstrings import *

POWER_TYPE_HEALTH      = -2
POWER_TYPE_MANA        = 0
POWER_TYPE_RAGE        = 1
POWER_TYPE_FOCUS       = 2
POWER_TYPE_ENERGY      = 3
POWER_TYPE_RUNES       = 5
POWER_TYPE_RUNIC_POWER = 6
POWER_TYPE_SOUL_SHARDS = 7

class Spell(Model):
	def getCastTimeText(self):
		if self.isPassive():
			return
		
		if self.isNextMelee():
			return SPELL_ON_NEXT_SWING
		
		if self.isChanneled():
			return SPELL_CAST_CHANNELED
		
		castTime = self.getCastTime()
		if not castTime:
			if self.isOnGlobalCooldown():
				return SPELL_CAST_TIME_INSTANT
			return SPELL_CAST_TIME_INSTANT_NO_MANA
		
		if castTime < durationstring.timedelta(0):
			return SPELL_CAST_TIME_INSTANT
		
		return SPELL_CAST_TIME % (durationstring.duration(castTime, durationstring.SHORT))
	
	def getCooldownText(self):
		cooldown = self.getCooldown()
		if cooldown:
			return SPELL_RECAST_TIME % (durationstring.duration(cooldown, durationstring.SHORTCAP))
		return ""
	
	def getPowerCostText(self):
		powerType, powerAmount, powerPerLevel, powerPercent, powerPerSecond, powerDisplay = self.getPowerInfo()
		
		if powerType == POWER_TYPE_RUNES:
			bloodCost, unholyCost, frostCost = self.getRuneCostInfo()
			runes = []
			if bloodCost:
				runes.append(RUNE_COST_BLOOD % (bloodCost))
			if frostCost:
				runes.append(RUNE_COST_FROST % (frostCost))
			if unholyCost:
				runes.append(RUNE_COST_UNHOLY % (unholyCost))
			
			return " ".join(runes)
		
		if powerPercent:
			if powerType == POWER_TYPE_HEALTH:
				return "%i%% of base health" % (powerPercent)
			if powerType == POWER_TYPE_FOCUS:
				return "%i%% of base focus" % (powerPercent)
			
			#assert powerType == POWER_TYPE_MANA, "%r: %i" % (self, powerType)
			return "%i%% of base mana" % (powerPercent)
		
		if powerPerSecond:
			if powerDisplay:
				return POWER_DISPLAY_COST_PER_TIME % (powerAmount, powerDisplay, powerPerSecond)
			
			if type == POWER_TYPE_HEALTH:
				return HEALTH_COST_PER_TIME % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_MANA:
				return MANA_COST_PER_TIME % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_RAGE:
				return RAGE_COST_PER_TIME % (powerAmount / 10, powerPerSecond)
			
			if type == POWER_TYPE_ENERGY:
				return ENERGY_COST_PER_TIME % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_FOCUS:
				return FOCUS_COST_PER_TIME % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_RUNIC_POWER:
				return RUNIC_POWER_COST_PER_TIME % (powerAmount / 10, powerPerSecond)
		
		if powerAmount:
			if powerDisplay:
				return POWER_DISPLAY_COST % (powerAmount, powerDisplay, powerPerSecond)
			
			if type == POWER_TYPE_HEALTH:
				return HEALTH_COST % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_MANA:
				return MANA_COST % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_RAGE:
				return RAGE_COST % (powerAmount / 10, powerPerSecond)
			
			if type == POWER_TYPE_ENERGY:
				return ENERGY_COST % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_FOCUS:
				return FOCUS_COST % (powerAmount, powerPerSecond)
			
			if type == POWER_TYPE_RUNIC_POWER:
				return RUNIC_POWER_COST % (powerAmount / 10, powerPerSecond)
			
			if type == POWER_TYPE_SOUL_SHARDS:
				if powerAmount == 1:
					return SOUL_SHARDS_COST % (powerAmount, powerPerSecond)
				return SOUL_SHARDS_COST_PLURAL % (powerAmount, powerPerSecond)
	
	def getRangeText(self):
		rangeMin, rangeMinFriendly, rangeMax, rangeMaxFriendly, flags = self.getRangeInfo()
		
		if rangeMaxFriendly and rangeMax != rangeMaxFriendly:
			enemy = SPELL_RANGE_DUAL % (ENEMY, rangeMax)
			friendly = SPELL_RANGE_DUAL % (FRIENDLY, rangeMaxFriendly)
			return "%s\n%s" % (enemy, friendly)
		
		if rangeMax == 50000:
			return SPELL_RANGE_UNLIMITED
		
		if rangeMax:
			if rangeMin or flags & 0x2:
				range = "%i-%i" % (rangeMin or 5, rangeMax)
				return SPELL_RANGE % (range)
			
			if rangeMax == 5 and flags & 0x1:
				return MELEE_RANGE
			
			return SPELL_RANGE % (rangeMax)
		
		return ""
	
	def showCastTime(self):
		return not self.isTrade()
	
	def getTooltip(self):
		return SpellTooltip(self)

class SpellTooltip(Tooltip):
	def tooltip(self):
		name = self.obj.getName()
		if self.obj.isTrade():
			skill = self.obj.getPrimarySkill()
			if skill:
				name = "%s: %s" % (skill, name)
			color = YELLOW
		else:
			color = WHITE
		self.append("name", name, color=color)
		
		self.append("range", self.obj.getRangeText())
		
		self.append("cost", self.obj.getPowerCostText())
		
		if self.obj.showCastTime():
			self.append("castTime", self.obj.getCastTimeText())
		
		self.append("cooldown", self.obj.getCooldownText())
		# required tools
		# reagents
		# required item subclasses
		# required stances / level
		self.append("description", self.obj.getDescription(), color=YELLOW)
		
		createdItem = self.obj.getCreatedItem()
		if createdItem:
			self.appendEmptyLine()
			self.append("createdItem", createdItem.getTooltip())
		
		return self.flush()


class SpellProxy(object):
	"""
	WDBC proxy for spells
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("Spell.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getCastTime(self, row):
		if row.cast_time:
			return row.cast_time.cast_time
		return 0
	
	def getCooldown(self, row):
		return row.cooldowns and row.cooldowns.cooldown or 0
	
	def getCreatedItem(self, row):
		effects = self.getEffects(row)
		if effects and effects[0]._raw("effect") in (24, 157):
			id = effects[0].type
			if id:
				from ..items import Item
				return Item(id)
	
	def getDescription(self, row):
		from pywow.spellstrings import SpellString, WDBCProxy
		description = row.description_enus
		return SpellString(description).format(self.get(row.id), proxy=WDBCProxy)
	
	def getEffects(self, row):
		return row.spelleffect__spell
	
	def getGlyphInfo(self, row):
		return row.class_options.spell_class_set
	
	def getGlyphLearned(self, row):
		effects = self.getEffects(row)
		if effects and effects[0]._raw("effect") == 74:
			id = effects[0].misc_value_1
			if id:
				from ..glyphs import Glyph
				return Glyph(id)
	
	def getIcon(self, row):
		icon = row.icon and row.icon.path or ""
		return icon.lower().replace("\\", "/").split("/")[-1]
	
	def getLevel(self, row):
		return row.levels and row.levels.level or 0
	
	def getName(self, row):
		return row.name_enus
	
	def getPowerInfo(self, row):
		if row.power:
			powerDisplay = row.power.power_display and row.power.power_display.name
			powerDisplay = powerDisplay and globals()[powerDisplay] or ""
			return row.power_type, row.power.power_amount, row.power.power_per_level, row.power.power_percent, row.power.power_per_second, powerDisplay
		
		return 0, 0, 0, 0, 0, ""
	
	def getRangeInfo(self, row):
		return int(row.range.range_min), int(row.range.range_min_friendly), int(row.range.range_max), int(row.range.range_max_friendly), row.range.flags
	
	def getRank(self, row):
		return row.rank_enus
	
	def getReagents(self, row):
		from ..items import Item
		ret = []
		fields = ("reagents__reagent_%i", "reagents__amount_%i")
		
		for i in range(1, 9):
			reagent = getattr(row, fields[0] % (i))
			amount = getattr(row, fields[1] % (i))
			if reagent and amount:
				reagent = Item(reagent.id)
				ret.append((reagent, amount))
		
		return ret
	
	def getRequiredLevel(self, row):
		if row.levels:
			return row.levels.base_level
	
	def getRuneCostInfo(self, row):
		if row.rune_cost:
			return row.rune_cost.blood, row.rune_cost.unholy, row.rune_cost.frost
		return 0, 0, 0
	
	def getPrimarySkill(self, row):
		# TODO getPrimarySkill.getName()
		skills = row.skilllineability__spell
		if skills:
			return skills[0].skill.name_enus
	
	def isChanneled(self, row):
		return row.flags_2.channeled or row.flags_2.channeled_2
	
	def isNextMelee(self, row):
		return row.flags_1.next_melee or row.flags_1.next_melee_2
	
	def isOnGlobalCooldown(self, row):
		return row.categories and row.categories._raw("recovery_category") == 133
	
	def isPassive(self, row):
		return row.flags_1.passive
	
	def isTrade(self, row):
		return row.flags_1.tradespell

Spell.initProxy(SpellProxy)
