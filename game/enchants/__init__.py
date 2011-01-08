# -*- coding: utf-8 -*-
"""
Enchants
 - SpellItemEnchantment.dbc
"""

from .. import Model


class Enchant(Model):
	pass

class EnchantProxy(object):
	"""
	WDBC proxy for enchants
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("SpellItemEnchantment.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getName(self, row):
		return row.name_enus

Enchant.initProxy(EnchantProxy)
