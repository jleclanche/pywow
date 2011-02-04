# -*- coding: utf-8 -*-
"""
Enchants
 - CurrencyTypes.dbc
"""

from .. import *


class Currency(Model):
	
	def getTooltip(self):
		return CurrencyTooltip(self)


class CurrencyTooltip(Tooltip):
	def tooltip(self):
		self.append("name", self.obj.getName())
		self.append("description", self.obj.getDescription(), color=YELLOW)
		
		return self.flush()


class CurrencyProxy(object):
	"""
	WDBC proxy for currencies
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("CurrencyTypes.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getDescription(self, row):
		return row.description_enus
	
	def getName(self, row):
		return row.name_enus

Currency.initProxy(CurrencyProxy)
