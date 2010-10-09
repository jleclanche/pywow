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
	
	def getName(self, row):
		return row.name_enus
