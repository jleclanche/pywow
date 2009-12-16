#!/usr/bin/python
# -*- coding: utf-8 -*-

from .base import DBStructure, _Generated
from .files.main import *
from .files.custom import *
from ..locales import L

class StructureError(Exception):
	pass

class StructureLoader():
	wowfiles = None
	
	@classmethod
	def setup(cls):
		if cls.wowfiles is None:
			cls.wowfiles = {}
			for name in globals():
				try:
					if not issubclass(globals()[name], DBStructure):
						continue
				except TypeError:
					continue
				cls.wowfiles[name.lower()] = globals()[name]
			
	@classmethod
	def getstructure(cls, name, build=0, parent=None):
		if name in cls.wowfiles:
			return cls.wowfiles[name](build, parent)
		raise StructureError(L["NO_STRUCTURE_FOUND"] % name)

StructureLoader.setup()
getstructure = StructureLoader.getstructure
