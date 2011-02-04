# -*- coding: utf-8 -*-
"""
Talents
 - Talent.dbc
"""

from .tabs import TalentTab
from .. import Model, Tooltip

class Talent(Model):
	def getTooltip(self):
		return TalentTooltip(self)

class TalentTooltip(Tooltip):
	def tooltip(self):
		self.appendEmptyLine()
		
		return self.flush()


class TalentProxy(object):
	"""
	WDBC proxy for talents
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("Talent.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getName(self, row):
		return "pass"

Talent.initProxy(TalentProxy)
