#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Database fields
"""

from datetime import timedelta
from ..parser.spellstrings import SpellString
from ..parser.bitflags import BitFlags


##
# Core
#

OLD_LOCALES = ("enus", "kokr", "frfr", "dede", "zhcn", "zhtw", "eses", "esmx")
LOCALES = ("enus", "kokr", "frfr", "dede", "zhcn", "zhtw", "eses", "esmx",
	"ruru", "unk1", "unk2", "unk3", "unk4", "unk5", "unk6", "unk7")

class DBField(object):
	"""
	A database field.
	"""
	def __init__(self, name="", dynamic=0, group=None, dead=False):
		self.name = name or "unknown"
		self.dyn = dynamic
		self.group = group
	
	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.name)
	
	def __str__(self):
		return self.name
	
	def from_python(self, value):
		return value
	
	def to_python(self, value, row):
		return value


##
# Base types
#

class ByteField(DBField):
	"""A 1-byte field."""
	char = "b"
	size = 1

class SmallIntegerField(DBField):
	"""An int16 field."""
	char = "h"
	size = 2

class IntegerField(DBField):
	"""An int32 field."""
	char = "i"
	size = 4

class UnsignedIntegerField(DBField):
	"""An uint32 field."""
	char = "I"
	size = 4

class BigIntegerField(DBField):
	"""An int64 field."""
	char = "l"
	size = 8

class FloatField(DBField):
	"""A float32 field."""
	char = "f"
	size = 4

class StringField(DBField):
	"""A string field."""
	char = "s"
	size = 4


##
# Core custom types
#

class IDField(IntegerField):
	"""
	Integer field containing the row's ID
	"""
	def __init__(self, name="_id"):
		IntegerField.__init__(self, name=name)

class RecLenField(IntegerField):
	"""
	Integer field containing the length of the row from itself
	"""
	def __init__(self, name="_reclen"):
		IntegerField.__init__(self, name=name)

class StringIDField(IDField):
	"""
	String field as pkey (see GameTables.dbc)
	"""
	char = "s"

class ImplicitIDField(DBField):
	"""
	IDField used when there isn't one. Always equal to
	the row's position in the dbc.
	"""
	char = ""
	size = 0
	def __init__(self, name="_id"):
		DBField.__init__(self, name=name)


##
# Dynamic types
#

class DynamicFieldsBase(list):
	def get_fields(self):
		return self

class DynamicMaster(IntegerField):
	"""
	Master field for dynamic columns, determining how many will be present.
	"""
	char = "A"

class DynamicFields(DynamicFieldsBase):
	"""
	A dynamic column master, followed by the full list of dynamic columns.
	Used in itemcache.wdb
	DynamicFields("name", [((Field, "x"), (Field, "y"), ...), 10])
	"""
	
	def __init__(self, name, columns):
		self.name = name
		self.master = DynamicMaster(name, group=self)
		self.append(self.master)
		cols, amt = columns
		for i in xrange(amt):
			self.append([v[0](name="%s_%s_dyn%i" % (name, v[1], i+1), dynamic=i+1, group=self) for v in cols])
			
	def get_fields(self):
		yield self.master
		for v in self[1:]:
			for f in v:
				yield f

class LocalizedFields(DynamicFieldsBase):
	"""
	Localized StringField.
	16 StringField, 1 BitMaskField
	"""
	
	def __init__(self, name, field_type=StringField, locales=LOCALES):
		self.name = name
		self.field_type = field_type
		self.__regenerate(locales)
	
	def __regenerate(self, locales):
		for loc in locales:
			self.append(self.field_type(name="%s_%s" % (self.name, loc), group=self))
		
		self.append(BitMaskField("%s_locflags" % (self.name), group=self))
	
	def update_locales(self, locales):
		del self[:]
		self.__regenerate(locales)

class ListField(DynamicFieldsBase):
	"""
	Helpful on unknown fields
	"""
	
	def __init__(self, name, length, field_type=IntegerField, **kwargs):
		self.name = name
		for i in xrange(length):
			self.append(field_type(name="%s_%d" % (name, i), group=self, **kwargs))


##
# Relations
#

class UnresolvedObjectRef(int):
	def __repr__(self):
		return "<%s: %d>" % (self.__class__.__name__, int(self))

class RelationError(Exception):
	pass

class UnresolvedRelation(RelationError):
	def __init__(self, message, reference):
		self.reference = reference
		super(UnresolvedRelation, self).__init__(message)

class ForeignKeyBase(IntegerField):
	"""
	Base class for ForeignKeys
	"""
	def from_python(self, value): # FIXME use isinstance(DBFile) instead
		if isinstance(value, int) or isinstance(value, long):
			return value
		pkey = value.structure.pkeys[0] # TODO: what about multiple pkeys ?
		index = value.structure.index(pkey.name)
		return value[index]
	
	def to_python(self, value, row):
		if isinstance(value, int):
			self.raw_value = value
			env = self.parent.parent.environment
			rel = self.get_relation(value)
			try:
				f = env[rel]
			except KeyError:
				raise UnresolvedRelation("Relation %r does not exist in the current environment" % (rel), value)
			relation_key = self.get_relation_key(value, row)
			try:
				value = f[relation_key]
			except KeyError:
				raise RelationError("Key %r does not exist in %s" % (relation_key, rel))
			return self.get_final_value(value, row)
		return value
	
	def get_final_value(self, value, row):
		return value
	
	def get_relation(self, value):
		raise NotImplementedError("Subclasses must implement this method")
	
	def get_relation_key(self, value, row):
		raise NotImplementedError("Subclasses must implement this method")

class ForeignKey(ForeignKeyBase):
	"""
	Integer link to another table's primary key.
	Relation required.
	"""
	def __init__(self, name, relation):
		IntegerField.__init__(self, name)
		self.relation = relation
		
	def get_relation(self, value):
		return self.relation.lower()
	
	def get_relation_key(self, value, row):
		return value

class ForeignMask(ForeignKey):
	"""
	Integer field containing a bitmask relation to
	multiple rows in another file.
	TODO
	"""
	pass

class ForeignByte(ForeignKey):
	"""
	This is a HACK
	"""
	char = "b"
	size = 2

class GenericForeignKey(ForeignKeyBase):
	def __init__ (self, name="", get_relation=None, get_value=lambda x, value: value):
		IntegerField.__init__(self, name)
		if not callable(get_relation):
			raise TypeError("%s._get_relation must be a callable type" % (self.__class__.__name__))
		self._get_relation = get_relation
		self._get_value = get_value
	
	def get_relation(self, value):
		return self._get_relation(self, value)
	
	def get_relation_key(self, value, row):
		return self._get_value(self, value)


class ForeignCell(ForeignKeyBase):
	"""
	Like a ForeignKey, but returns a specific cell
	from the relation. Requires both a get_column
	and a get_row method.
	"""
	def __init__(self, name, relation, get_column, get_row):
		IntegerField.__init__(self, name)
		self.relation = relation
		self.get_column = get_column
		self.get_row = get_row
	
	def get_final_value(self, value, row):
		column = self.get_column(row, self.raw_value)
		if column:
			return getattr(value, column)
		return self.raw_value
	
	def get_relation_key(self, value, row):
		return self.get_row(row, self.raw_value)
		
	def get_relation(self, value):
		return self.relation.lower()


##
# Custom types
#

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
		IntegerField.__init__(self, name, **kwargs)
		if unit not in self.units:
			raise ValueError("%r is not a valid duration unit (choices are: %s)" % (unit, ", ".join(self.units.keys())))
		self.unit = unit
	
	def timedelta(self, value):
		return timedelta(microseconds=value * self.units[self.unit])
	
	def to_python(self, value, row):
		return self.timedelta(value)

class MoneyField(UnsignedIntegerField):
	pass

class UnknownField(IntegerField):
	pass

class FilePathField(StringField):
	pass

class SpellMacroField(StringField):
	def to_python(self, value, row):
		val = SpellString(value)
		return val.format(row)
