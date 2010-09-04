# -*- coding: utf-8 -*-

import os, os.path
from cStringIO import StringIO
from struct import pack, unpack, error as StructError
from .log import log
from .structures import fields, StructureNotFound, getstructure
from .utils import getfilename, generate_structure
from .wdb import WDBFile

##
# Header classes
#

class DBHeader(object):
	"""
	Base DBFile header class
	"""
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, self.__dict__[k]) for k in self.__dict__))

class DBCHeader(DBHeader):
	def __len__(self):
		return 20
	
	def load(self, file):
		file.seek(0)
		data = file.read(len(self))
		self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize = unpack("<4s4i", data)
	
	def data(self):
		return pack("<4s4i", self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize)

class DB2Header(DBHeader):
	def __len__(self):
		if self.build < 12834:
			return 32
		return 48
	
	def load(self, file):
		file.seek(0)
		self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize, self.dbhash, self.build, self.unk1 = unpack("<4s7i", file.read(32))
		if self.build >= 12834:
			self.time, self.unk2, self.locale, self.unk3 = unpack("<4i", file.read(16))
	
	def get_block_size(self):
		if self.build < 12834:
			return 0
		return self.unk3 and  self.unk3 - 2 * len(self) or len(self)


##
# File classes
#

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


class DBCFile(DBFile):
	"""
	A DBC file.
	- Each file has an arbitrary amount of columns always of the same length and
	  structure (defined in the header).
	- Each string is a 32-bit pointer to an address inside the stringblock, starting
	  from 0 as the stringblock address (defined in the header as well).
	- EOF is 1 NULL byte, followed by the stringblock if there is one.
	- The stringblock is a non-repetitive block of null-terminated strings.
	"""
	
	def __init__(self, file, build, structure, environment):
		super(DBCFile, self).__init__(file, build, structure, environment)
		self.header = DBCHeader()
		self.header.load(file)
		if not build:
			build = 0
		self.build = build
		self.__load_structure(structure)
	
	def __check_padding(self, file, field):
		"""
		In 4.0.0 DBCs, fields are padded to their own size
		within the file. Example:
		byte, int -> byte, pad, pad, pad, int
		"""
		address = file.tell()
		seek = (address % field.size)
		seek = seek and -(seek - field.size)
		file.seek(seek, os.SEEK_CUR)
	
	def __load_structure(self, structure):
		name = getfilename(self.file.name)
		try:
			self.structure = getstructure(name, self.build, parent=self)
		except StructureNotFound:
			self.structure = generate_structure(self)
		
		# Generate the Localized Fields
		fieldidx = []
		for i, field in enumerate(self.structure):
			if isinstance(field, structures.LocalizedField):
				fieldidx.append((i, field.name))
		
		if fieldidx:
			from copy import copy
			fields = structures.LocalizedStringField(build=self.build)
			for i, name in reversed(fieldidx):
				# Build a copy of the fields
				toinsert = [copy(field).rename("%s_%s" % (name, field.name)) for field in fields]
				self.structure[i:i+1] = toinsert
		
		log.info("Using %s build %i" % (self.structure, self.build))
		
		self.check_integrity()
	
	def _parse_field(self, data, field, row=None):
		if self.build in (11927, 12025): # TODO pywow.builddata
			self.__check_padding(data, field)
		return super(DBCFile, self)._parse_field(data, field, row)
	
	def _parse_row(self, id):
		address, reclen = self._addresses[id]
		self.file.seek(address)
		data = self.file.read(reclen) # We also read id and reclen columns
		row = DBRow(self, data=data)
		self._values[id] = row
	
	def _parse_string(self, data):
		address, = unpack("<I", data.read(4))
		if not address:
			return ""
		
		f = self.file
		pos = f.tell()
		f.seek(-self.header.stringblocksize, os.SEEK_END) # Go to the stringblock
		f.seek(address, os.SEEK_CUR) # seek to the address in the stringblock
		
		# Read until \0
		chars = []
		while True:
			char = f.read(1)
			if char == "\0":
				break
			if not char:
				if not chars:
					#log.warning("No string found at 0x%08x (%i), some values may be corrupt. Fix your structures!" % (address, address - self.header.stringblocksize))
					return ""
				log.warning("Unfinished string, this file may be corrupted.")
				break
			chars.append(char)
		
		f.seek(pos)
		
		return "".join(chars)
	
	def check_integrity(self):
		reclen = self.header.reclen
		struct_len = self.structure._reclen()
		if struct_len != reclen:
			log.warning("File structure does not respect DBC reclen. Expected %i, reading %i. (%+i)" % (reclen, struct_len, reclen-struct_len))
		
		field_count = self.header.field_count
		total_fields = len(self.structure)
		if field_count != total_fields:
			log.warning("File structure does not respect DBC field count. Expected %i, got %i instead." % (field_count, total_fields))
	
	def data(self):
		ret = []
		self.__stringblock = []
		address_lookup = {}
		address = 1
		for row in self:
			row = self[row]
			row._save()
			_data = []
			for field, value in zip(self.structure, row):
				if isinstance(field, fields.StringField):
					if not value:
						_value = 0
					elif value in address_lookup: # the string is already in the stringblock
						_value = address_lookup[value]
					else:
						_value = address
						address_lookup[value] = address
						self.__stringblock.append(value)
						address += len(value) + 1
					value = pack("<I", _value)
				
				else:
					value = pack("<%s" % (field.char), value)
				
				_data.append(value)
			ret.append("".join(_data))
		return "".join(ret)
	
	def eof(self):
		return "\0" + ("\0".join(self.__stringblock)) + "\0"
	
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		if isinstance(self, DB2File):
			print f.seek(self.header.get_block_size())
		
		rows = 0
		field = self.structure[0]
		row_header_size = field.size
		reclen = self.header.reclen
		while rows < self.header.row_count:
			address = f.tell() # Get the address of the full row
			id = self._parse_field(f, field)
			
			self._add_row(id, address, reclen)
			
			f.seek(reclen - row_header_size, os.SEEK_CUR) # minus length of id
			rows += 1
		
		log.info("%i rows total" % (rows))


class DB2File(DBCFile):
	"""
	New DB format introduced in build 12803
	"""
	
	def __init__(self, file, build, structure, environment):
		super(DBCFile, self).__init__(file, build, structure, environment)
		self.header = DB2Header()
		self.header.load(file)
		self.build = build or self.header.build
		self.__load_structure(structure)
	
	def __load_structure(self, structure):
		name = getfilename(self.file.name)
		try:
			self.structure = getstructure(name, self.build, parent=self)
		except StructureNotFound:
			self.structure = generate_structure(self)
		
		# Generate the Localized Fields
		fieldidx = []
		for i, field in enumerate(self.structure):
			if isinstance(field, structures.LocalizedField):
				fieldidx.append((i, field.name))
		
		if fieldidx:
			from copy import copy
			fields = structures.LocalizedStringField(build=self.build)
			for i, name in reversed(fieldidx):
				# Build a copy of the fields
				toinsert = [copy(field).rename("%s_%s" % (name, field.name)) for field in fields]
				self.structure[i:i+1] = toinsert
		
		log.info("Using %s build %i" % (self.structure, self.build))
		self.check_integrity()


class WCFFile(DBCFile):
	"""
	Pretty much a DBC file without a header.
	Currently only used with baddons.wcf.
	"""
	def preload(self):
		f = self.file
		f.seek(0)
		rows = 0
		field = self.structure[0]
		reclen = sum(k.size for k in self.structure)
		row_header_size = field.size
		while True:
			address = f.tell() # Get the address of the full row
			id = self._parse_field(f, field)
			if id is None:
				break
			
			self._add_row(id, address, reclen)
			
			f.seek(reclen - row_header_size, os.SEEK_CUR) # minus length of id
			rows += 1
		
		log.info("%i rows total" % (rows))


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


class InferredDBCFile(DBCFile):
	"""
	DBCFile with implicit ordering. These files have no IDField.
	"""
	
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		
		rows = 0
		reclen = self.header.reclen
		while rows < self.header.row_count:
			address = f.tell() # Get the address of the full row
			id = rows + 1
			
			self._addresses[id] = (address, reclen)
			
			f.seek(reclen, os.SEEK_CUR)
			rows += 1
		
		log.info("%i rows total" % (rows))


class ComplexDBCFile(DBCFile):
	"""
	Only used in ItemSubClass.dbc for now
	Two IDFields.
	"""
	
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		
		rows = 0
		reclen = self.header.reclen
		while rows < self.header.row_count:
			address = f.tell() # Get the address of the full row
			id = unpack("<ii", f.read(8)) # id is a tuple instead
			
			if id in self._addresses: # Something's wrong here
				log.warning("Multiple instances of row %s found" % (".".join(id)))
			self._addresses[id] = (address, reclen)
			
			f.seek(reclen - 8, os.SEEK_CUR) # minus 4 bytes for each id
			rows += 1
		
		log.info("%i rows total" % (rows))


class UnknownDBCFile(DBCFile):
	"""
	A DBC file with an unknown structure.
	"""
	writable = False
	def load_structure(self, filename=None, build=None):
		self.structure = self._generate_structure()
		log.info("Using generated structure for file %s, build %i" % (self.filename, self.build))


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
