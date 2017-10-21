from enum import _EnumDict
from collections import OrderedDict
from .fields import Field

_magic_register = {}
_name_register = {}


class StructureNotFound(Exception):
	pass

class StructureMeta(type):
	"""
	Metaclass for Structure
	"""
	@classmethod
	def __prepare__(metacls, cls, bases):
		return OrderedDict()

	def __new__(cls, name, bases, clsdict):
		c = type.__new__(cls, name, bases, clsdict)
		c._orderedKeys = clsdict.keys()
		return c

class Structure(metaclass=StructureMeta):
	def __init__(self):
		self.skeleton = []
		for attr in self.__dict__:
			if isinstance(attr, Field):
				self.skeleton.append()

	def __iter__(self):
		for key in self._orderedKeys:
			if not key.startswith("__"):
				yield key

	def items(self):
		for key in self._orderedKeys:
			if not key.startswith("__"):
				yield key, getattr(self, key)

	def values(self):
		for key in self._orderedKeys:
			if not key.startswith("__"):
				yield getattr(self, key)


def register(name, magic=None):
	def dec(cls):
		if magic:
			_magic_register[magic] = cls
		_name_register[name] = cls
	return dec


def get_structure(name=None, magic=None):
	ret = None
	if magic:
		if magic != "WDBC":
			from . import wdb
		ret = _magic_register.get(magic)
	if name and not ret:
		ret = _name_register.get(name)
	if not ret:
		raise StructureNotFound

	return ret
