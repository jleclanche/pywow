# -*- coding: utf-8 -*-
"""
Items
 - itemcache.wdb (1.x->4.x)
 - Item.dbc + itemcache.wdb (2.x->4.x)
 - Item-sparse.db2 (4.x)
"""
from pywow.game import *

# Globalstrings
HEROIC = "Heroic"
ITEM_BIND_ON_EQUIP = "Binds when equipped"
ITEM_BIND_ON_PICKUP = "Binds when picked up"
ITEM_BIND_ON_USE = "Binds when used"
ITEM_BIND_QUEST = "Quest Item"
ITEM_BIND_TO_ACCOUNT = "Binds to account"
ITEM_CONJURED = "Conjured Item"
ITEM_LEVEL = "Level %d" # The actual level of the item
ITEM_LEVEL_AND_MIN = "Level %d (min %d)" # The level and minimum required level for an item
ITEM_LEVEL_RANGE = "Requires level %d to %d" # Item is only useable in the range of levels specified.
ITEM_LEVEL_RANGE_CURRENT = "Requires level %d to %d (%d)" # Item is only useable in the range of levels specified.
ITEM_LIMIT_CATEGORY = "Unique: %s (%d)"
ITEM_LIMIT_CATEGORY_MULTIPLE = "Unique Equipped: %s (%d)"
ITEM_MILLABLE = "Millable" # Item is millable
ITEM_MIN_LEVEL = "Requires Level %d"
ITEM_MIN_SKILL = "Requires %s (%d)" # Required skill rank to use the item
ITEM_SIGNABLE = "<Right Click for Details>"
ITEM_SPELL_TRIGGER_ONEQUIP = "Equip:"
ITEM_SPELL_TRIGGER_ONPROC = "Chance on hit:"
ITEM_SPELL_TRIGGER_ONUSE = "Use:"
ITEM_STARTS_QUEST = "This Item Begins a Quest"
ITEM_UNIQUE = "Unique"
ITEM_UNIQUE_EQUIPPABLE = "Unique-Equipped"
ITEM_UNIQUE_MULTIPLE = "Unique (%d)"

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
	
	def getBinding(self):
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
		self.render()
	
	def render(self):
		
		self.append("name", self.obj.name, self.obj.getQualityColor())
		
		#if self.obj.quality and env.colorblind:
		#	self.append("quality", self.obj.getQuality())
		
		# glyph
		
		if self.obj.isHeroic():
			self.append("heroic", HEROIC, GREEN)
		
		if self.obj.isChart():
			self.append("chart", ITEM_SIGNABLE, GREEN)
		
		# zone
		# instance
		
		if self.obj.isConjured():
			self.append("conjured", ITEM_CONJURED)
		
		self.append("binding", self.obj.getBinding())
		
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
		
		if self.obj.required_holiday:
			self.append("requiredHoliday", self.obj.required_holiday.name.name_enus)
		
		# race/class reqs
		
		self.append("durability", self.obj.durability)
		if self.obj.required_level:
			self.append("requiredLevel", ITEM_MIN_LEVEL % (self.obj.required_level))
		
		if self.obj.slot:
			self.append("level", ITEM_LEVEL % (self.obj.level))
		
		# (required arena rating)
		
		# required skill
		
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
		
		print self.values


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
