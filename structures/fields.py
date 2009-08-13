#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Database fields"""

from datetime import timedelta
from ..parser.bitmask import BitMask
from ..parser.spellstrings import SpellString


##########
## Core ##
##########

OLD_LOCALES = ("enus", "kokr", "frfr", "dede", "zhcn", "zhtw", "eses", "esmx")
LOCALES = ("enus", "kokr", "frfr", "dede", "zhcn", "zhtw", "eses", "esmx",
	"ruru", "unk1", "unk2", "unk3", "unk4", "unk5", "unk6", "unk7")

class DBField(object):
	"""A database field."""
	def __init__(self, name="", dynamic=0, group=None, **kwargs):
		self.name = name or "unknown"
		self.dyn = dynamic
		self.group = group
		if "value" in kwargs:
			self.real_value = kwargs["value"]
			self.parent = kwargs["parent"]
			del kwargs["value"], kwargs["parent"]
		self.kwargs = kwargs.copy()
	
	def __repr__(self):
		if hasattr(self, "real_value"):
			return self.value.__repr__()
		return "<%s: %s>" % (self.__class__.__name__, self.name)
	
	def new(self, value, parent):
		return self.__class__(value=value, parent=parent, name=self.name, dynamic=self.dyn, **self.kwargs)
	
	def from_python(self, value):
		return value
	
	def to_python(self):
		return self.value
	
	@property
	def value(self):
		return self.real_value
	
	@value.setter
	def _set_value(self, value):
		self.real_value = value


################
## Base types ##
################

class ByteField(DBField):
	"""1-byte field."""
	char = "b"

class ShortField(DBField):
	"""2-byte field."""
	char = "h"

class IntegerField(DBField):
	"""An int32 field."""
	char = "i"

class UnsignedIntegerField(DBField):
	"""An uint32 field."""
	char = "I"

class StringField(DBField):
	"""A string field."""
	char = "s"

class FloatField(DBField):
	"""A float32 field."""
	char = "f"


#######################
## Core custom types ##
#######################

class IDField(IntegerField):
	def __init__(self, name="_id", **kwargs):
		IntegerField.__init__(self, name=name, **kwargs)

class DynamicMaster(IntegerField):
	"""Masterfield for dynamic columns, determining how many will be present."""
	char = "A"

class StringIDField(IDField):
	"""String field as pkey (see GameTables.dbc)"""
	char = "s"


###################
## Dynamic types ##
###################

class DynamicFields(list):
	"""
	A dynamic column master, followed by the full list of dynamic columns.
	Usage:
	DynamicFields("name", [((Field, "x"), (Field, "y"), ...), 10])
	"""
	
	def __init__(self, name, columns, **kwargs):
		self.name = name
		self.master = DynamicMaster(name, group=self)
		self.append(self.master)
		cols, amt = columns
		for i in range(amt):
			self.append([v[0](name="%s_%s_dyn%i" % (name, v[1], i+1), dynamic=i+1, group=self, **kwargs) for v in cols])

class LocalizedFields(list):
	"""
	Localized StringField.
	16 StringField, 1 BitMaskField
	"""
	
	def __init__(self, name, field_type=StringField, locales=LOCALES, **kwargs):
		self.name = name
		for loc in locales:
			self.append(field_type(name="%s_%s" % (name, loc), group=self, **kwargs))
		
		self.append(BitMaskField("%s_locflags" % name, group=self))


##################
## Custom types ##
##################

class RecLenField(IntegerField):
	def __init__(self, name="_reclen", **kwargs):
		IntegerField.__init__(self, name=name, **kwargs)

class ForeignKey(IntegerField):
	"""Integer link to another table's primary key. Relation required."""
	def __init__(self, name, relation, **kwargs):
		IntegerField.__init__(self, name=name, relation=relation, **kwargs)
		self.relation = relation
	
	def to_python(self):
		f = self.parent.parent.environment[self.relation]
		return f[self.value]

class GenericForeignKey(IntegerField):
	def __init__(self, name="", get_relation=None, get_value=lambda x: x.value, **kwargs):
		IntegerField.__init__(self, name, get_relation=get_relation, get_value=get_value, **kwargs)
		if not callable(get_relation):
			raise TypeError
		self._get_relation = get_relation
		self._get_value = get_value
	
	def get_relation(self):
		return self._get_relation(self)
	
	def get_value(self):
		return self._get_value(self)
	
	def to_python(self):
		f = self.parent.parent.environment[self.get_relation()]
		return f[self.get_value()]

class BitMaskField(IntegerField):
	def __init__(self, name="", flags=[], **kwargs):
		IntegerField.__init__(self, name, flags=flags, **kwargs)
		self.flags = flags
		if hasattr(self, "real_value"):
			self.bitmask = BitMask(self.real_value)
	
	def from_python(self, value):
		if isinstance(value, dict):
			return sum([2**(self.flags.index(i)+1) for i in value if value[i]])
		return value
	
	def to_python(self):
		return self.bitmask.expand(self.flags)
	
	def explode(self):
		try:
			val = self.bitmask.explode()
		except ValueError:
			val = []
		return val
	
	def set(self, key, val):
		i = self.flags.index(key)
		self.bitmask[i] = val
		self.parent[self.name] = self.value
	
	@property
	def value(self):
		return int(self.bitmask)

class BooleanField(IntegerField):
	pass

class DurationField(IntegerField):
	units = {
		# "years": 31556925993600, # 52.177457 * (7*24*60*60*1000*1000)
		# "months": 2629743828768, # 4.34812141 * (7*24*60*60*1000*1000)
		"weeks": 604800000000, # 7*24*60*60*1000*1000
		"days": 86400000000, # 24*60*60*1000*1000
		"hours": 3600000000, # 60*60*1000*1000
		"minutes": 60000000, # 60*1000*1000
		"seconds": 1000000, # 1000*1000
		"milliseconds": 1000,
		"microseconds": 1,
	}
	def __init__(self, name="", unit="seconds", **kwargs):
		IntegerField.__init__(self, name, unit=unit, **kwargs)
		if unit not in self.units:
			raise ValueError
		self.unit = unit
		if hasattr(self, "real_value"):
			self.duration = self.timedelta(self.real_value)
	
	def timedelta(self, value):
		return timedelta(microseconds=value*self.units[self.unit])
	
	def to_python(self):
		return self.duration

class MoneyField(UnsignedIntegerField):
	pass

class UnknownField(IntegerField):
	pass

class FilePathField(StringField):
	pass

class SpellMacroField(StringField):
	def to_python(self):
		val = SpellString(self.value)
		return val.format(self.parent)

class CoordField(FloatField):
	"""X/Y/Z coordinate field (floating point)"""
	pass

