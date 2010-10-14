# -*- coding: utf-8 -*-
"""
Classes
 - ChrClasses.dbc
"""

from .. import Model


class ChrClass(Model):
	@classmethod
	def getClassesFromMask(cls, mask):
		from pywow import wdbc
		f = wdbc.get("ChrClasses.dbc", build=-1)
		ret = []
		for id, row in f.items():
			if mask & (2**(id-1)):
				ret.append(ChrClass(id))
		
		if len(ret) < len(f):
			return ret

class ChrClassProxy(object):
	"""
	WDBC proxy for classes
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("ChrClasses.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getInternalName(self, row):
		return row.internal_name
	
	def getName(self, row):
		return row.name_male_enus

ChrClass.initProxy(ChrClassProxy)
