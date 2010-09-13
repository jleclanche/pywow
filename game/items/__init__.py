# -*- coding: utf-8 -*-
"""
Items
 - itemcache.wdb (1.x->4.x)
 - Item.dbc + itemcache.wdb (2.x->4.x)
 - Item-sparse.db2 (4.x)
"""
from .. import *
from ..globalstrings import *

class Item(Model):
	
	def getQualityColor(self):
		return {
			0: GREY,   # Poor
			1: WHITE,  # Common
			2: GREEN,  # Uncommon
			3: BLUE,   # Rare
			4: PURPLE, # Epic
			5: ORANGE, # Legendary
			6: GOLD,   # Artifact
			7: GOLD,   # Heirloom
		}.get(self.quality, WHITE)
	
	def getBindingText(self):
		if self.isAccountBound():
			return ITEM_BIND_TO_ACCOUNT
		
		return {
			1: ITEM_BIND_ON_PICKUP,
			2: ITEM_BIND_ON_EQUIP,
			3: ITEM_BIND_ON_USE,
			4: ITEM_BIND_QUEST,
		}.get(self.bind, "")
	
	def getSlotText(self):
		return {
			#INVTYPE_WEAPONMAINHAND_PET = "Main Attack"
			 1: INVTYPE_HEAD,
			 2: INVTYPE_NECK,
			 3: INVTYPE_SHOULDER,
			 4: INVTYPE_BODY,
			 5: INVTYPE_CHEST,
			 6: INVTYPE_WAIST,
			 7: INVTYPE_LEGS,
			 8: INVTYPE_FEET,
			 9: INVTYPE_WRIST,
			10: INVTYPE_HAND,
			11: INVTYPE_FINGER,
			12: INVTYPE_TRINKET,
			13: INVTYPE_WEAPON,
			14: INVTYPE_SHIELD,
			15: INVTYPE_RANGED,
			16: INVTYPE_CLOAK, # INVTYPE_BACK ?
			17: INVTYPE_2HWEAPON,
			18: INVTYPE_BAG,
			19: INVTYPE_TABARD,
			20: INVTYPE_ROBE,
			21: INVTYPE_WEAPONMAINHAND,
			22: INVTYPE_WEAPONOFFHAND,
			23: INVTYPE_HOLDABLE,
			24: INVTYPE_AMMO,
			25: INVTYPE_THROWN,
			26: INVTYPE_RANGEDRIGHT,
			#27: INVTYPE_QUIVER,
			28: INVTYPE_RELIC,
		}.get(self.slot, "")


class ItemTooltip(Tooltip):
	def __init__(self, obj, renderer=None):
		self.obj = obj
		self.renderer = renderer
		self.keys = []
		self.values = []
	
	def render(self):
		
		self.append("name", self.obj.name, self.obj.getQualityColor())
		
		#if self.obj.quality and env.colorblind:
		#	self.append("quality", self.obj.getQuality())
		
		# glyph
		
		if self.obj.isHeroic():
			self.append("heroic", ITEM_HEROIC, GREEN)
		
		if self.obj.isChart():
			self.append("chart", ITEM_SIGNABLE, GREEN)
		
		self.append("requiredZone", self.obj.getRequiredZone())
		self.append("requiredInstance", self.obj.getRequiredInstance())
		
		if self.obj.isConjured():
			self.append("conjured", ITEM_CONJURED)
		
		self.append("binding", self.obj.getBindingText())
		
		if self.obj.isUniqueEquipped():
			self.append("unique", ITEM_UNIQUE_EQUIPPABLE)
		elif self.obj.unique:
			if self.obj.unique > 1:
				self.append("unique", ITEM_UNIQUE_MULTIPLE % (self.obj.unique))
			else:
				self.append("unique", ITEM_UNIQUE)
		elif self.obj.unique_category:
			pass
		
		if self.obj.starts_quest:
			self.append("startsQuest", ITEM_STARTS_QUEST)
		
		# lockpicking
		
		# subclass
		
		self.append("slot", self.obj.getSlotText())
		
		# damage
		
		# armor
		
		# block
		
		# stats
		
		# enchant
		
		# sockets
		
		self.append("gemProperties", self.obj.getGemProperties())
		
		# random ench
		
		# duration
		
		self.append("requiredHoliday", self.obj.getRequiredHoliday())
		
		# race/class reqs
		
		if self.obj.durability:
			self.append("durability", DURABILITY_TEMPLATE % (self.obj.getDurability()))
		
		if self.obj.required_level:
			self.append("requiredLevel", ITEM_MIN_LEVEL % (self.obj.required_level))
		
		if self.obj.slot:
			self.append("level", ITEM_LEVEL % (self.obj.level))
		
		# (required arena rating)
		
		requiredSkill, requiredSkillLevel = self.obj.getRequiredSkill()
		if requiredSkill and requiredSkillLevel:
			self.append("requiredSkill", ITEM_MIN_SKILL % (requiredSkill, requiredSkillLevel))
		
		self.formatAppend("requiredSpell", ITEM_REQ_SKILL, self.obj.getRequiredSpell())
		
		requiredFaction, requiredReputation = self.obj.getRequiredFaction()
		if requiredFaction: # and requiredReputation?
			self.append("requiredFaction", ITEM_REQ_REPUTATION % (requiredFaction, requiredReputation))
		
		# special stats
		
		# spells
		
		# charges
		
		# itemset
		
		self.append("note", self.obj.note and '"%s"' % (self.obj.note))
		
		# openable
		
		# page
		
		# disenchanting
		
		# sell price
		
		ret = self.values
		self.values = []
		return ret


class ItemProxy(object):
	"""
	WDBC proxy for items
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("Item-sparse.db2", build=12803)
	
	def get(self, id):
		return self.__file[id]
	
	def isAccountBound(self, row):
		return row.flags.account_bound
	
	def isChart(self, row):
		return row.flags.chart
	
	def isConjured(self, row):
		return row.flags.conjured
	
	def isHeroic(self, row):
		return row.flags.heroic
	
	def isUniqueEquipped(self, row):
		return row.flags.unique_equipped
	
	def getDurability(self, row):
		# return min, max
		return row.durability, row.durability
	
	def getGemProperties(self, row):
		if row.gem_properties and row.gem_properties.enchant:
			return row.gem_properties.enchant.name_enus
		return ""
	
	def getRequiredFaction(self, row):
		requiredReputation = globals().get("FACTION_STANDING_LABEL%i" % (row.required_reputation + 1), "")
		if row.required_faction:
			return row.required_faction.name_enus, requiredReputation
		return "", requiredReputation
	
	def getRequiredHoliday(self, row):
		if row.required_holiday:
			return row.required_holiday.name.name_enus
		return ""
	
	def getRequiredInstance(self, row):
		if row._raw("required_instance") and row.required_instance:
			return row.required_instance.name_enus
		return ""
	
	def getRequiredSkill(self, row):
		requiredSkillLevel = row.required_skill_level
		if row.required_skill:
			return row.required_skill.name_enus, requiredSkillLevel
		return "", requiredSkillLevel
	
	def getRequiredSpell(self, row):
		if row.required_spell:
			return row.required_spell.name_enus
		return ""
	
	def getRequiredZone(self, row):
		if row.required_zone:
			return row.required_zone.name_enus
		return ""
