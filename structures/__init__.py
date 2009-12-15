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
					issubclass(globals()[name], DBStructure)
				except TypeError:
					continue
				cls.wowfiles[name.lower()] = globals()[name]
			
	@classmethod
	def getstructure(cls, name, build=0):
		if name in cls.wowfiles:
			return cls.wowfiles[name](build)
		raise StructureError(L["NO_STRUCTURE_FOUND"] % name)

StructureLoader.setup()
getstructure = StructureLoader.getstructure
