# -*- coding: utf-8 -*-

from pywow.structures import Structure, Skeleton
from .fields import *
from .main import *
from .custom import *
from .generated import GeneratedStructure

class StructureNotFound(Exception):
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
		raise StructureNotFound("Structure not found for file %r" % (name))

StructureLoader.setup()
getstructure = StructureLoader.getstructure
