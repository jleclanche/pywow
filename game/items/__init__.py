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
		
		if self.obj.slot:
			self.append("slot", str(self.obj.slot))
		
		# damage
		
		# armor
		
		# block
		
		# stats
		
		# enchant
		
		# sockets
		
		if self.obj.gem_properties:
			self.append("gemProperties", self.obj.gem_properties.enchant.name_enus)
		
		# random ench
		
		# duration
		
		self.append("requiredHoliday", self.obj.getRequiredHoliday())
		
		# race/class reqs
		
		self.append("durability", self.obj.durability)
		
		if self.obj.required_level:
			self.append("requiredLevel", ITEM_MIN_LEVEL % (self.obj.required_level))
		
		if self.obj.slot:
			self.append("level", ITEM_LEVEL % (self.obj.level))
		
		# (required arena rating)
		
		requiredSkill, requiredSkillLevel = self.obj.getRequiredSkill()
		if requiredSkill and requiredSkillLevel:
			self.append("requiredSkill", ITEM_MIN_SKILL % (requiredSkill, requiredSkillLevel))
		
		# required spell
		
		# required faction
		
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
	
	def getRequiredZone(self, row):
		if row.required_zone:
			return row.required_zone.name_enus
		return ""
