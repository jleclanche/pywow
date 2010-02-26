#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, os.path
from struct import pack, unpack, error as StructError
from pywow.log import log
from pywow.structures.fields import RelationError, UnresolvedRelation, UnresolvedObjectRef, DynamicFields, RecLenField
from .structures import GeneratedStructure, StructureNotFound, getstructure


def getfilename(val):
	"Returns 'item' from /home/adys/Item.dbc"
	return os.path.splitext(os.path.basename(val))[0].lower()

def getsignature(path):
	"Attempts to find the signature of the given file"
	f = open(path, "rb")
	sig = f.read(4)
	f.close()
	return sig


##
# Header classes
#

class DBCHeader(object):
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, self.__dict__[k]) for k in self.__dict__))
	
	def __len__(self):
		return 20
	
	def load(self, file):
		file.seek(0)
		data = file.read(len(self))
		self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize = unpack("<4s4i", data)
	
	def data(self):
		return pack("<4s4i", self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize)

class WDBHeader(object):
	"""
	A WDB header, structure as follows:
	- 4 byte string signature (reversed)
	- 4 byte integer build
	- 4 byte string locale (reversed)
	- 4 byte integer unknown - maybe related to dynamic fields?
	- 4 byte integer unknown
	As of build 9438, an additional 4 byte integer indicates the data version for that build.
	"""
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, self.__dict__[k]) for k in self.__dict__))
	
	def __len__(self):
		if not hasattr(self, "build"):
			return 0
		if self.build < 9438:
			return 20
		return 24
	
	def load(self, file):
		file.seek(0)
		self.signature = file.read(4)
		self.build, = unpack("<i", file.read(4))
		self.locale = file.read(4)
		self.wdb4, self.wdb5 = unpack("<ii", file.read(8))
		if self.build >= 9438:
			self.version, = unpack("<i", file.read(4))
	
	def data(self):
		if not hasattr(self, "build"):
			return ""
		ret = pack("<4si4sii", self.signature, self.build, self.locale, self.wdb4, self.wdb5)
		if self.build >= 9438:
			ret += pack("<i", self.version)
		
		return ret


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
		self._load_structure(structure) # This should happen after self.build has been set
	
	def __repr__(self):
		return "%s(file=%r, build=%r)" % (self.__class__.__name__, self.file, self.build)
	
	def __contains__(self, id):
		return id in self._addresses
	
	def __getitem__(self, item):
		if item not in self._values:
			self._parse_row(item)
		return self._values[item]
	
	def __setitem__(self, item, value):
		if not isinstance(item, int):
			raise TypeError("DBFile indices must be integers, not %s" % type(item))
		
		if type(value) in (list, dict):
			value = DBRow(self, columns=value)
			self._values[key] = item
			self[key].pk = item
		
		# FIXME technically we should allow DBRow, but this is untested and will need resetting parent
		raise TypeError("Unsupported type for DBFile.__setitem__: %s" % type(value))
	
	def __delitem__(self, item):
		if item in self._values:
			del self._values[item]
		if item in self._addresses: # Maybe we added it later
			del self._addresses[item]
	
	def __iter__(self):
		return self._addresses.__iter__()
	
	def append(self, row):
		"Appends a row at the end of the file."
		l = len(self) + 1
		if "_id" not in row:
			row["_id"] = l
		self[l] = row
	
	def clear(self):
		"Delete every row in the file"
		for k in self.keys(): # Use key, otherwise we get RuntimeError: dictionary changed size during iteration
			del self[k]
	
	def keys(self):
		return self._addresses.keys()
	
	def rows(self):
		return [self[id] for id in self]
	
	def filter(self, args, limit=0):
		results = []
		match = len(args)
		for k in self:
			i = 0
			for arg in args:
				if self[k]._raw(arg) != args[arg]:
					break
				i += 1
			if i == match:
				results.append(k)
				if len(results) >= limit:
					return results
		
		return results
	
	def write(self, filename=""):
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


class WDBFile(DBFile):
	"""
	A WDB file.
	- The first column of every WDB file is an unique ID primary key.
	- The second column specifies the record length (reclen). The reclen is the
	  size in bytes of the following row (not counting the id and reclen itself).
	- EOF is 8 NULL bytes (corresponding to id and reclen of 0).
	"""
	
	MAGIC = {
		"BDIW": "itemcache",
		"BDNW": "itemnamecache",
		"BOMW": "creaturecache",
		"BOGW": "gameobjectcache",
		"CPNW": "npccache",
		"NDRW": "wowcache",
		"TSQW": "questcache",
		"XTIW": "itemtextcache",
		"XTPW": "pagetextcache",
	}
	
	def __init__(self, file, build, structure, environment):
		self.header = WDBHeader()
		if "w" in self.file.mode: # open for writing
			self.header.signature = structure.signature
			self.header.build = build
		else:
			self.header.load(file)
			if not build:
				build = self.header.build
		self.build = build
		
		super(WDBFile, self).__init__(file, build, structure, environment)
	
	def __setitem__(self, key, item):
		if type(item) in (list, dict) and item:
			DBFile.__setitem__(self, key, DBRow(self, columns=item))
			#if str(key).isdigit(): self[key].id = int(key)
		else:
			DBFile.__setitem__(self, key, item)
	
	def _parse_row(self, id):
		address, reclen = self._addresses[id]
		self.file.seek(address)
		data = self.file.read(reclen + 8) # We also read id and reclen columns
		row = DBRow(self, data=data, reclen=reclen)
		self._values[id] = row
	
	def _load_structure(self, structure):
		if self.header.signature in self.MAGIC:
			name = self.MAGIC[self.header.signature]
		else: # allow for custom structures
			name = getfilename(self.file.name)
		self.structure = getstructure(name, self.build, parent=self)
		log.info("Using %s structure build %i" % (self.structure.name, self.build))
	
	def eof(self):
		return "\0" * 8
	
	def data(self):
		return "".join([self[k]._data() for k in self])
	
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		
		rows = 0
		while True:
			address = f.tell() # Get the address of the full row
			id, reclen = unpack("<ii", f.read(8))
			if reclen == 0: # EOF
				break
			
			if id in self._addresses: # Something's wrong here
				log.warning("Multiple instances of row #%r found" % (id))
			self._addresses[id] = (address, reclen)
			
			f.seek(reclen, os.SEEK_CUR)
			rows += 1
		
		log.info("%i rows total" % (rows))
	
	def update_dynfields(self):
		"""Update all the dynfields in the file"""
		dyns = [k for k in self.structure.columns if isinstance(k, DynamicFields)]
		for k in self:
			for group in dyns:
				master_name = group[0].name
				amount = 0 # Amount of active fields
				for fields in group[1:]:
					values = [self[k]._raw(col.name) for col in fields]
					if set(values) == set([None]):
						continue
					elif None in values: # TODO log event
						for col in fields:
							if self[k]._raw(col.name) != None:
								setattr(self[0], col.name, 0)
					amount += 1
				setattr(self[k], master_name, amount) # set master to correct field amount
	
	def update_reclens(self):
		"""Update all the reclens in the file"""
		for k in self:
			self[k]._reclen = self[k].reclen()


class WoWCache(WDBFile):
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		
		rows = 0
		while True:
			address = f.tell() # Get the address of the full row
			id, reclen = unpack("<16si", f.read(20))
			if reclen == 0: # EOF
				break
			
			if id in self._addresses: # Something's wrong here
				log.warning("Multiple instances of row #%r found" % (id))
			self._addresses[id] = (address, reclen)
			f.seek(reclen, os.SEEK_CUR)
			rows += 1
		
		log.info("%i rows total" % (rows))


class DBCFile(DBFile):
	"""
	A DBC file.
	- ...
	"""
	
	def __init__(self, file, build, structure, environment):
		self.header = DBCHeader()
		self.header.load(file)
		if not build:
			build = 0
		self.build = build
		
		super(DBCFile, self).__init__(file, build, structure, environment)
	
	def __check_structure_integrity(self):
		reclen = self.header.reclen
		struct_len = self.structure._reclen()
		if struct_len != reclen:
			log.warning("File structure does not respect DBC reclen. Expected %i, reading %i. (%+i)" % (reclen, struct_len, reclen-struct_len))
		
		field_count = self.header.field_count
		total_fields = len(self.structure)
		if field_count != total_fields:
			# Don't forget implicit fields
			total_fields = len([k for k in self.structure if k.char])
			if field_count != total_fields:
				log.warning("File structure does not respect DBC field count. Expected %i, got %i instead." % (field_count, total_fields))
	
	def __generate_structure(self):
		"""Generates a structure based on header data"""
		# TODO improve it, guess floats and shorter fields.
		if self.header.field_count * 4 == self.header.reclen:
			structure_string = "i" * self.header.field_count
		else:
			raise NotImplementedError
		return GeneratedStructure(structure_string)
	
	def _load_structure(self, structure):
		name = getfilename(self.file.name)
		try:
			self.structure = getstructure(name, self.build, parent=self)
		except StructureNotFound:
			self.structure = self.__generate_structure()
		log.info("Using %s structure build %i" % (self.structure.name, self.build))
		
		self.__check_structure_integrity()
	
	def _parse_row(self, id):
		address, reclen = self._addresses[id]
		self.file.seek(address)
		data = self.file.read(reclen) # We also read id and reclen columns
		row = DBRow(self, data=data)
		self._values[id] = row
	
	def _getstring(self, address):
		f = self.file
		pos = f.tell()
		f.seek(-self.header.stringblocksize, os.SEEK_END) # Go to the stringblock
		f.seek(address, os.SEEK_CUR) # seek to the address in the stringblock
		
		#Read until \0
		chars = []
		while True:
			char = f.read(1)
			if char == "\0":
				break
			if not char:
				if not chars:
					log.warning("No string found at 0x%08x (%i), some values may be corrupt. Fix your structures!" % (address, address - self.header.stringblocksize))
					return ""
				log.warning("Unfinished string, this file may be corrupted.")
				break
			chars.append(char)
		
		f.seek(pos)
		
		return "".join(chars)
	
	def data(self):
		raise NotImplementedError # FIXME
	
	def eof(self):
		raise NotImplementedError # FIXME
	
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		
		rows = 0
		reclen = self.header.reclen
		while rows < self.header.row_count:
			address = f.tell() # Get the address of the full row
			id, = unpack("<i", f.read(4))
			
			if id in self._addresses: # Something's wrong here
				log.warning("Multiple instances of row #%r found" % (id))
			self._addresses[id] = (address, reclen)
			
			f.seek(reclen - 4, os.SEEK_CUR) # minus 4 bytes for id
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
			cursor = 0
			for col in self.structure:
				char = col.char
				dyn = col.dyn
				
				if dyn > dynfields:
					_data = None # The column doesn't exist in this row, we set it to None
				
				elif char == "s":
					if self.structure.signature == "WDBC":
						address, = unpack("<i", data[cursor:cursor+4])
						if address == 0:
							_data = u""
						else:
							try:
								_data = unicode(parent._getstring(address), "utf-8")
							except StructError:
								_data = u""
								#log.warning("Substring not found for %s, some values may be corrupt. Fix your structures!" % (col))
						cursor += 4
					else:
						try:
							_data = unicode(data[cursor:data.index("\x00", cursor)], "utf-8")
							cursor += len(str(_data.encode("utf-8"))) + 1
						except ValueError:
							_data = u""
							cursor += 1
							log.warning("Substring not found for %s, some values may be corrupt. Fix your structures!" % (col))
				
				elif char == "A": # The amount of dynamic columns in the row
					_data = unpack("<i", data[cursor:cursor+4])[0]
					cursor += 4
					dynfields = _data
				
				elif char == "": # ImplicitIDField
					_data = len(parent) + 1 # 1-indexed
				
				elif char == "x": # Data TODO
					_data = repr(data[cursor:cursor+self.data_length])[:50] + "..."
					cursor += self.data_length
				
				else:
					size = col.size
					try:
						_data, = unpack("<%s" % (char), data[cursor:cursor+size])
					except StructError:
						_data = None # There is no data left in the row, we set it to None
					cursor += size
				
				self.append(_data)
			
			if reclen:
				if cursor != reclen+8:
					log.warning("Reclen not respected for row %r. Expected %i, read %i. (%+i)" % (self._id, reclen+8, cursor, reclen+8-cursor))
	
	def __int__(self):
		return self._id
	
	def __getattr__(self, attr):
		if attr in self.structure:
			return self._get_value(attr)
		if attr in self.structure._abstractions: # Union abstractions etc
			field, func = self.structure._abstractions[attr]
			return func(field, self)
		return list.__getattribute__(self, attr)
	
	def __setattr__(self, attr, value):
		"""
		Do not preserve the value in DBRow!
		Use the save method to save.
		"""
		if self.initialized and attr in self.structure:
			self._set_value(attr, value)
		list.__setattr__(self, attr, value)
	
	def __setitem__(self, index, value):
		if not isinstance(index, int):
			raise TypeError("Expected int instance, got %s instead (%r)" % (type(index), index))
		list.__setitem__(self, index, value)
		col = self.structure[index]
		try:
			self._values[col.name] = col.to_python(value, row=self)
		except UnresolvedRelation:
			self._values[col.name] = value
	
	def __dir__(self):
		result = self.__dict__.keys()
		result.extend(self.structure.column_names)
		return result
	
	# introspection support:
	__members__ = property(lambda self: self.__dir__())
	
	
	def _set_value(self, name, value):
		col = self.structure[self.structure.index(name)]
		try:
			self._values[name] = col.to_python(value, self)
		except UnresolvedRelation:
			self._values[name] = value
	
	def _get_value(self, name):
		if name not in self._values:
			raw_value = self[self.structure.index(name)]
			try:
				self._set_value(name, raw_value)
			except UnresolvedRelation, e:
				return UnresolvedObjectRef(e.reference)
			except RelationError:
				return None # Key doesn't exist, or equals 0
		return self._values[name]
	
	def _save(self):
		for name in self._values:
			index = self.structure.index(name)
			col = self.structure[index]
			self[index] = col.from_python(self._values[name])
	
	def _data(self):
		"Convert the column list into a byte stream"
		self._save()
		data = []
		reclen = None
		for k, v in zip(self.structure, self):
			if v == None:
				continue
			elif isinstance(k, RecLenField):
				reclen = k
			elif k.char == "s":
				_data = v.encode("utf-8") + "\x00"
			elif k.char == "A":
				_data = pack("<i", v)
			else:
				_data = pack("<%s" % (k.char), v)
			data.append(str(_data))
		if reclen:
			length = pack("<i", len("".join(data[2:])))
			data[self.structure.index(reclen.name)] = length
		data = "".join(data)
		
		return data
	
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
	
	def reclen(self):
		return len(self._data())-8
	
	def update(self, other):
		for k in other:
			self[k] = other[k]


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
				print "%r, %r in self.addresses" % id
			self._addresses[id] = (address, reclen)
			
			f.seek(reclen - 8, os.SEEK_CUR) # minus 4 bytes for id
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
	if signature == "WDBC":
		cls = DBCFile
		if getfilename(file.name) == "itemsubclass":
			cls = ComplexDBCFile # TODO morph in __new__
	elif signature == "NDRW":
		cls = WoWCache
	else:
		cls = WDBFile
	file = cls(file, build=build, structure=structure, environment=environment)
	file.preload()
	return file


def new(name, build=0, structure=None, environment={}):
	filename = getfilename(name)
	if not structure:
		structure = getstructure(filename, build=build)
	name = structure.name
	
	file = open(name, "wb")
	
	if structure.signature == "WDBC":
		return DBCFile(file, build=build, structure=structure, environment=environment)
	return WDBFile(file, build=build, structure=structure, environment=environment)
