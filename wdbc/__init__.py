# -*- coding: utf-8 -*-

import os, os.path
from cStringIO import StringIO
from struct import pack, unpack, error as StructError
from .log import log
from .structures import fields, StructureNotFound, getstructure
from .utils import getfilename, generate_structure


class DBHeader(object):
	"""
	Base DBFile header class
	"""
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, self.__dict__[k]) for k in self.__dict__))


class DBFile(object):
	"""
	Base class for WDB and DBC files
	"""
	
	def __init__(self, file, build, structure, environment):
		self.file = file
		self._addresses = {}
		self._values = {}
		self.environment = environment
		
		self.__row_dynfields = 0 # Dynamic fields index, used when parsing a row
	
	def __repr__(self):
		return "%s(file=%r, build=%r)" % (self.__class__.__name__, self.file, self.build)
	
	def __contains__(self, id):
		return id in self._addresses
	
	def __getitem__(self, item):
		if isinstance(item, slice):
			keys = sorted(self._addresses.keys())[item]
			return [self[k] for k in keys]
		
		if item not in self._values:
			self._parse_row(item)
		
		return self._values[item]
	
	def __setitem__(self, item, value):
		if not isinstance(item, int):
			raise TypeError("DBFile indices must be integers, not %s" % type(item))
		
		if value and type(value) in (list, dict):
			value = DBRow(self, columns=value)
		
		if isinstance(value, DBRow):
			self._values[item] = value
			self._addresses[item] = -1
			#self[key].pk = item
		else: # FIXME technically we should allow DBRow, but this is untested and will need resetting parent
			raise TypeError("Unsupported type for DBFile.__setitem__: %s" % type(value))
	
	def __delitem__(self, item):
		if item in self._values:
			del self._values[item]
		del self._addresses[item]
	
	def __iter__(self):
		return self._addresses.__iter__()
	
	def __len__(self):
		return len(self._addresses)
	
	def _add_row(self, id, address, reclen):
		if id in self._addresses: # Something's wrong here
			log.warning("Multiple instances of row %r found" % (id))
		self._addresses[id] = (address, reclen)
	
	def _parse_field(self, data, field, row=None):
		"""
		Parse a single field in stream.
		"""
		if field.dyn > self.__row_dynfields:
			return None # The column doesn't exist in this row, we set it to None
		
		ret = None
		
		try:
			if isinstance(field, fields.StringField):
				ret = self._parse_string(data)
			
			elif isinstance(field, fields.DataField): # wowcache.wdb
				length = getattr(row, field.master)
				ret = data.read(length)
			
			elif isinstance(field, fields.DynamicMaster):
				ret, = unpack("<I", data.read(4))
				self.__row_dynfields = ret
			
			else:
				ret, = unpack("<%s" % (field.char), data.read(field.size))
		except StructError:
			log.warning("Field %s could not be parsed properly" % (field))
			ret = None
		finally:
			return ret
	
	def append(self, row):
		"""
		Append a row at the end of the file.
		If the row does not have an id, one is automatically assigned.
		"""
		i = len(self) + 1 # FIXME this wont work properly in incomplete files
		if "_id" not in row:
			row["_id"] = i
		self[i] = row
	
	def clear(self):
		"""
		Delete every row in the file
		"""
		for k in self.keys(): # Use key, otherwise we get RuntimeError: dictionary changed size during iteration
			del self[k]
	
	def keys(self):
		return self._addresses.keys()
	
	def items(self):
		return [(k, self[k]) for k in self]
	
	def rows(self):
		"""
		Return a list of each row in the file
		"""
		return [self[id] for id in self]
	
	def write(self, filename=""):
		"""
		Write the file data on disk. If filename is not given, use currently opened file.
		"""
		_filename = filename or self.file.name
		
		data = self.header.data() + self.data() + self.eof()
		
		f = open(_filename, "wb") # Don't open before calling data() as uncached rows would be empty
		f.write(data)
		f.close()
		log.info("Written %i bytes at %s" % (os.path.getsize(f.name), f.name))
		
		if not filename: # Reopen self.file, we modified it
			# XXX do we need to wipe self._values here?
			self.file.close()
			self.file = open(f.name, "rb")


class DBRow(list):
	"""
	A database row.
	Names of the variables of that class should not be used in field names of structures
	"""
	initialized = False
	
	def __init__(self, parent, data=None, columns=None, reclen=0):
		self._parent = parent 
		self._values = {} # Columns values storage
		self.structure = parent.structure
		
		self.initialized = True # needed for __setattr__
		
		if columns:
			if type(columns) == list:
				self.extend(columns)
			
			elif type(columns) == dict:
				self._default()
				_cols = [k.name for k in self.structure]
				for k in columns:
					try:
						self[_cols.index(k)] = columns[k]
					except ValueError:
						log.warning("Column %r not found" % (k))
		
		elif data:
			dynfields = 0
			data = StringIO(data)
			for field in self.structure:
				_data = parent._parse_field(data, field, self)
				self.append(_data)
			
			if reclen:
				real_reclen = reclen + self._parent.row_header_size
				if data.tell() != real_reclen:
					log.warning("Reclen not respected for row %r. Expected %i, read %i. (%+i)" % (self._id, real_reclen, data.tell(), real_reclen-data.tell()))
	
	def __int__(self):
		return self._id
	
	def __getattr__(self, attr):
		if attr in self.structure:
			return self._get_value(attr)
		
		if attr in self.structure._abstractions: # Union abstractions etc
			field, func = self.structure._abstractions[attr]
			return func(field, self)
		
		if "__" in attr:
			return self.__get_deep_relation(attr)
		
		return super(DBRow, self).__getattribute__(attr)
	
	def __setattr__(self, attr, value):
		"""
		Do not preserve the value in DBRow!
		Use the save method to save.
		"""
		if self.initialized and attr in self.structure:
			self._set_value(attr, value)
		return super(DBRow, self).__setattr__(attr, value)
	
	def __setitem__(self, index, value):
		if not isinstance(index, int):
			raise TypeError("Expected int instance, got %s instead (%r)" % (type(index), index))
		list.__setitem__(self, index, value)
		col = self.structure[index]
		try:
			self._values[col.name] = col.to_python(value, row=self)
		except fields.UnresolvedRelation:
			self._values[col.name] = value
	
	def __dir__(self):
		result = self.__dict__.keys()
		result.extend(self.structure.column_names)
		return result
	
	
	def __get_reverse_relation(self, table, field):
		""" Return a list of rows matching the reverse relation """
		if not hasattr(self._parent, "_reverse_relation_cache"):
			self._parent._reverse_relation_cache = {}
		cache = self._parent._reverse_relation_cache
		
		tfield = table + "__" + field
		if tfield not in cache:
			cache[tfield] = {}
			# First time lookup, let's build the cache
			table = self._parent.environment[table]
			for row in table:
				row = table[row]
				id = row._raw(field)
				if id not in cache[tfield]:
					cache[tfield][id] = []
				cache[tfield][id].append(row)
		
		return cache[tfield].get(self._id, None)
	
	def __get_deep_relation(self, rel):
		""" Parse a django-like multilevel relationship """
		rels = rel.split("__")
		if "" in rels: # empty string
			raise ValueError("Invalid relation string")
		
		first = rels[0]
		if not hasattr(self, first):
			if first in self._parent.environment:
				remainder = rel[len(first + "__"):]
				return self.__get_reverse_relation(first, remainder)
			raise ValueError("Invalid relation string")
		
		ret = self
		rels = rels[::-1]
		while rels:
			ret = getattr(ret, rels.pop())
		
		return ret
	
	
	def _set_value(self, name, value):
		col = self.structure[self.structure.index(name)]
		try:
			self._values[name] = col.to_python(value, self)
		except fields.UnresolvedRelation:
			self._values[name] = value
	
	def _get_value(self, name):
		if name not in self._values:
			raw_value = self[self.structure.index(name)]
			try:
				self._set_value(name, raw_value)
			except fields.UnresolvedRelation, e:
				return fields.UnresolvedObjectRef(e.reference)
			except fields.RelationError:
				return None # Key doesn't exist, or equals 0
		return self._values[name]
	
	def _save(self):
		for name in self._values:
			index = self.structure.index(name)
			col = self.structure[index]
			self[index] = col.from_python(self._values[name])
	
	def _raw(self, name):
		""" Returns the raw value from field 'name' """
		index = self.structure.index(name)
		return self[index]
	
	def _field(self, name):
		""" Returns the field 'name' """
		index = self.structure.index(name)
		return self.structure[index]
	
	def _default(self):
		""" Change all fields to their default values """
		del self[:]
		self._values = {}
		for col in self.structure:
			char = col.char
			if col.dyn: self.append(None)
			elif char == "s": self.append("")
			elif char == "f": self.append(0.0)
			else: self.append(0)
	
	def dict(self):
		"Return a dict of the row as colname: value"
		return dict(zip(self.structure.column_names, self))
	
	def update(self, other):
		for k in other:
			self[k] = other[k]
	
	@property
	def id(self):
		"Temporary hack to transition between _id and id"
		return self._id


def fopen(name, build=0, structure=None, environment={}):
	file = open(name, "rb")
	signature = file.read(4)
	if signature == "WDB2" or signature == "WCH2":
		cls = DB2File
		try:
			_structure = structure or getstructure(getfilename(file.name))
		except StructureNotFound:
			pass
		
	
	elif signature == "WDBC":
		cls = DBCFile
		try:
			_structure = structure or getstructure(getfilename(file.name))
		except StructureNotFound:
			pass
		else:
			cls = DBCFile
			if len(_structure.primary_keys) > 1:
				cls = ComplexDBCFile
			elif getattr(_structure, "implicit_id", None):
				cls = InferredDBCFile
	
	elif not signature:
		raise IOError()
	
	elif name.endswith(".wcf"):
		cls = WCFFile
		structure = structure or getstructure(getfilename(file.name))
	
	else:
		cls = WDBFile
	
	file = cls(file, build=build, structure=structure, environment=environment)
	file.preload()
	return file


def new(name, build=0, structure=None, environment={}):
	filename = getfilename(name)
	if not structure:
		structure = getstructure(filename, build=build)
	
	file = open(name, "wb")
	
	if structure.signature == "WDBC":
		return DBCFile(file, build=build, structure=structure, environment=environment)
	return WDBFile(file, build=build, structure=structure, environment=environment)


__envcache = {}

def get(name, build):
	from .environment import Environment
	if build not in __envcache:
		__envcache[build] = Environment(build)
	return __envcache[build][name]
