#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Database fields
"""

from datetime import timedelta
from .bitflags import BitFlags


##
# Core
#

class FieldError(Exception):
	pass

OLD_LOCALES = ("enus", "kokr", "frfr", "dede", "zhcn", "zhtw", "eses", "esmx")
LOCALES = ("enus", "kokr", "frfr", "dede", "zhcn", "zhtw", "eses", "esmx",
	"ruru", "unk1", "unk2", "unk3", "unk4", "unk5", "unk6", "unk7")
LOCALES_CATACLYSM = ("enus", )

class Field(object):
	"""
	A database field.
	"""
	def __init__(self, name="", dynamic=0, group=None, primary_key=False):
		self.name = name or "unknown"
		self.dyn = dynamic
		self.group = group
		self.primary_key = primary_key
	
	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.name)
	
	def from_python(self, value):
		return value
	
	def to_python(self, value, row):
		return value


##
# Base types
#

class ByteField(Field):
	"""A byte field."""
	char = "b"
	size = 1

class UnsignedByteField(Field):
	"""An unsigned byte field."""
	char = "B"
	size = 1

class SmallIntegerField(Field):
	"""An int16 field."""
	char = "h"
	size = 2

class UnsignedSmallIntegerField(Field):
	"""An uint16 field."""
	char = "H"
	size = 2

class IntegerField(Field):
	"""An int32 field."""
	char = "i"
	size = 4

class UnsignedIntegerField(Field):
	"""An uint32 field."""
	char = "I"
	size = 4

class BigIntegerField(Field):
	"""An int64 field."""
	char = "q"
	size = 8

class UnsignedBigIntegerField(Field):
	"""An uint64 field."""
	char = "Q"
	size = 8

class FloatField(Field):
	"""A float32 field."""
	char = "f"
	size = 4

class StringField(Field):
	"""A string field."""
	char = "s"
	size = 4


##
# Misc. types
#

class BooleanField(IntegerField):
	pass

class BitMaskField(UnsignedIntegerField):
	"""
	Integer field containing a bitmask
	"""
	def __init__(self, name="", flags={}, **kwargs):
		UnsignedIntegerField.__init__(self, name, **kwargs)
		self.flags = flags
	
	def from_python(self, value):
		assert isinstance(value, BitFlags)
		return int(value)
	
	def to_python(self, value, row):
		if isinstance(value, BitFlags):
			return value
		return BitFlags(value, self.flags)

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
		IntegerField.__init__(self, name, **kwargs)
		if unit not in self.units:
			raise FieldError("%r is not a valid duration unit (choices are: %s)" % (unit, ", ".join(self.units.keys())))
		self.unit = unit
	
	def timedelta(self, value):
		return timedelta(microseconds=value * self.units[self.unit])
	
	def to_python(self, value, row):
		return self.timedelta(value)
