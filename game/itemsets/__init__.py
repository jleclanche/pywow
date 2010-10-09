# -*- coding: utf-8 -*-
"""
Item Sets
 - ItemSet.dbc
"""

from .. import *
from ..globalstrings import *


class ItemSet(Model):
	pass

class ItemSetTooltip(Tooltip):
	def tooltip(self):
		
		self.append("name", ITEM_SET_NAME % (self.obj.getName(), 0, 0), color=YELLOW)
		
		items = self.obj.getItems()
		for item in items:
			self.append("item", item.getName())
		
		ret = self.values
		self.values = []
		return ret

class ItemSetProxy(object):
	"""
	WDBC proxy for item sets
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("ItemSet.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getItems(self, row):
		from ..items import Item, ItemProxy
		Item.initProxy(ItemProxy)
		ret = []
		for i in range(1, 11):
			id = row._raw("item_%i" % (i))
			if id:
				print id, Item(id)
				ret.append(Item(id))
		
		return ret
	
	def getName(self, row):
		return row.name_enus
