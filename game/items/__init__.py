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
ITEM_SIGNABLE = "<Right Click for Details>"

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
		}.get(self.binding, "")


class ItemTooltip(Tooltip):
	def __init__(self, obj, renderer):
		self.obj = obj
		self.renderer = renderer
		self.render()
	
	def render(self):
		self.values = []
		
		self.append("name", self.obj.name, self.obj.getQualityColor())
		
		#if self.obj.quality and env.colorblind:
		#	self.append("quality", self.obj.getQuality())
		
		if self.obj.isHeroic():
			self.append("heroic", HEROIC, GREEN)
		
		if self.obj.isChart():
			self.append("chart", ITEM_SIGNABLE, GREEN)
		
		if self.obj.isConjured():
			self.append("conjured", ITEM_CONJURED)
		
		self.append("binding", self.obj.getBinding())


class ItemProxy(object):
	"""
	WDBC proxy for items
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("Item-sparse.db2", build=12803)
	
	def get(self, id):
		return self.__file[id]
	
	def isHeroic(self):
		return self.flags.heroic
	
	def isChart(self):
		return self.flags.chart
	
	def isConjured(self):
		return self.flags.conjured
	
	def isAccountBound(self):
		return self.flags.account_bound
