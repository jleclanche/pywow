# -*- coding: utf-8 -*-
"""
Talent tabs
 - TalentTab.dbc
"""

from .. import Model
from .tabs import Tab

class TalentTab(Model):
	ROLE_TANK   = 0x2
	ROLE_HEALER = 0x4
	ROLE_DAMAGE = 0x8


class TalentTabProxy(object):
	"""
	WDBC proxy for talent tabs
	"""
	
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("TalentTab.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getClasses(self, row):
		from ..classes import ChrClass
		return ChrClass.getClassesFromMask(mask)
	
	def getDescription(self, row):
		return row.description_enus
	
	def getIcon(self, row):
		icon = row.icon and row.icon.path or ""
		return icon.lower().replace("\\", "/").split("/")[-1]
	
	def getInternalName(self, row):
		return row.internal_name
	
	def getMasteries(self, row):
		from ..spells import Spell
		
		fields = ("mastery_1", "mastery_2")
		ret = []
		for field in fields:
			mastery = row._raw(field)
			if mastery:
				ret.append(Spell(mastery))
		
		return ret
	
	def getName(self, row):
		return row.name_enus
	
	def getPage(self, row):
		return row.page
	
	def getPet(self, row):
		pass
	
	def getRoles(self, row):
		return row._raw("roles")

TalentTab.initProxy(TalentTabProxy)
