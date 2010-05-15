# -*- coding: utf-8 -*-

from pywow.structures.fields import *

##
# Core custom types for WDB/DBC files
#

class IDField(IntegerField):
	"""
	Integer field containing the row's ID
	"""
	def __init__(self, name="_id"):
		IntegerField.__init__(self, name=name, primary_key=True)

class RecLenField(IntegerField):
	"""
	Integer field containing the length of the row from itself
	"""
	def __init__(self, name="_reclen"):
		IntegerField.__init__(self, name=name)


##
# Dynamic types
#

class DynamicFieldsBase(list):
	def get_fields(self):
		return self
	
	def delete_field(self, name):
		"""
		Delete a field, by name or by instance
		"""
		if isinstance(name, basestring):
			for index, field in enumerate(self):
				if field.name == name:
					del self[index]
					break
		else:
			for index, field in enumerate(self):
				if isinstance(field, name.__class__):
					del self[index]
					break

class DynamicMaster(IntegerField):
	"""
	Master field for dynamic columns, determining how many will be present.
	"""
	pass

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
	
	def delete_locflags(self):
		for field in self:
			if isinstance(field, BitMaskField): # XXX better way
				self.delete_field(field)

class SubRow(object):
	"""
	Used in Unions as a fake DBRow
	"""
	
	def __init__(self, field, row, structure):
		self.__field = field
		self.__row = row
		self._structure = structure(row._parent.build, row._parent)
	
	def __dir__(self):
		result = self.__dict__.keys()
		result.extend(self._structure.column_names)
		return result
	
	def __getattr__(self, name):
		if name in self._structure:
			index = self._structure.index(name)
			value = self._raw(name)
			return self._structure[index].to_python(value, self.__row)
		return super(SubRow, self).__getattribute__(name)
	
	def _raw(self, name):
		index = self._structure.index(name)
		real_name = self.__field.column_names[index]
		return getattr(self.__row, real_name)

class Union(DynamicFieldsBase):
	"""
	Imitates a C++ union.
	Takes a name argument and field_1, ... field_n fields to
	populate the default union.
	Required get_structure(x, row) callable argument that
	returns the structure corresponding to a specific row.
	"""
	
	def __init__(self, name, fields, get_structure):
		DynamicFieldsBase.__init__(self, fields)
		self.name = name
		if not callable(get_structure):
			raise StructureError("%s._get_structure must be a callable type" % (self.__class__.__name__))
		self._get_structure = get_structure
		self.column_names = [k.name for k in fields]
	
	def __build_list(self, field, row):
		"Builds a fake DBRow to allow deep attribute seeking"
		return SubRow(field, row, self._get_structure(row))
	
	def get_abstraction(self):
		return self.name, self.__build_list
	
	def get_structure(self, row):
		return self._get_structure(row)


class MultiField(DynamicFieldsBase):
	"""
	Expands a list of fields to a specific amount
	"""
	
	def __init__(self, name, fields, amount):
		super(DynamicFieldsBase, self).__init__(fields)
	
	def __build_list(self):
		pass
	
	def get_abstraction(self):
		return self.name, self.__build_list


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
		pk = value.structure.primary_keys[0] # TODO: what about multiple primary keys ?
		index = value.structure.index(pk.name)
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
	size = 1

class GenericForeignKey(ForeignKeyBase):
	def __init__ (self, name="", get_relation=None, get_value=lambda x, value: value):
		IntegerField.__init__(self, name)
		if not callable(get_relation):
			raise FieldError("%s._get_relation must be a callable type" % (self.__class__.__name__))
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
# Misc. types
#

class UnknownField(IntegerField):
	pass

class ColorField(UnsignedIntegerField):
	pass

class MoneyField(UnsignedIntegerField):
	pass

class FilePathField(StringField):
	pass

class GUIDField(BigIntegerField):
	pass

class HashField(Field):
	char = "16s"
	size = 16

class DataField(Field):
	char = "s"
	def __init__(self, name, master):
		Field.__init__(self, name=name)
		self.master = master
