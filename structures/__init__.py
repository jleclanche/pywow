#!/usr/bin/python
# -*- coding: utf-8 -*-

from .base import Structure, _Generated
from .files.main import *
from .files.custom import *
from ..locales import L

class UnknownStructure(Exception):
	pass

class StructureLoader():
	wowfiles = None
	
	@classmethod
	def setup(cls):
		if cls.wowfiles is None:
			cls.wowfiles = {}
			for name in globals():
				try:
					if not issubclass(globals()[name], Structure):
						continue
				except TypeError:
					continue
				cls.wowfiles[name.lower()] = globals()[name]
	
	@classmethod
	def getstructure(cls, name, build=0, parent=None):
		if name in cls.wowfiles:
			return cls.wowfiles[name](build, parent)
		raise UnknownStructure("Structure not found for file %r" % (name))

StructureLoader.setup()
getstructure = StructureLoader.getstructure
