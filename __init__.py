#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import getsize, basename, splitext, exists
from struct import pack, unpack, error as StructError

from .structures.fields import RelationError, UnresolvedRelation, UnresolvedObjectRef, DynamicFields
from .structures import _Generated, StructureError, getstructure
from .locales import L
from .logger import log


def getfilename(val):
	"Returns 'item' from /home/adys/Item.dbc"
	return splitext(basename(val))[0].lower()

def getsignature(path):
	"Attempts to find the signature of the given file"
	f = open(path, "rb")
	sig = f.read(4)
	f.close()
	return sig

magic = {
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

signatures = dict([(magic[k], k) for k in magic])

class DBHeader(object):
	"""A WDBC header file."""
	def __init__(self, parent):
		self.parent = parent
	
	def __repr__(self):
		return "DBHeader(%s)" % ", ".join(["%s=%r" % (k, getattr(self, k)) for k in ("signature", "build", "locale", "wdb4",
					"wdb5", "version", "row_count", "field_count", "reclen", "stringblocksize") if hasattr(self, k)])
	
	def __setattr__(self, key, value):
		if key == "build":
			self.parent.build = value
		return object.__setattr__(self, key, value)
	
	def __return(self):
		if self.signature == "WDBC":
			return (self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize)
		else:
			if self.build < 9438:
				return (self.signature, self.build, self.locale, self.wdb4, self.wdb5)
			else:
				return (self.signature, self.build, self.locale, self.wdb4, self.wdb5, self.version)
	
	
	def _load_data(self):
		"Load header data from the parent."
		self.signature = self.parent.signature
		if self.signature == "WDBC":
			self.row_count = len(self.parent)
			self.field_count = len(self.parent.structure)
			self.reclen = self.field_count * 4 # TODO
			if not hasattr(self, "stringblocksize"):
				self.stringblocksize = 0 # TODO
		else:
			self.build = self.parent.build
			if not hasattr(self, "locale"): self.locale = "SUne" # TODO
			if not hasattr(self, "wdb4"): self.wdb4 = 0 #8316 # TODO
			if not hasattr(self, "wdb5"): self.wdb5 = 0 #3 # TODO
			if self.build >= 9438 and not hasattr(self, "version"):
				self.version = 0
	
	def _load_stream(self, data):
		"Load header data from a byte stream."
		self.signature = data[:4]
		if self.signature == "WDBC":
			self.row_count, self.field_count, self.reclen, self.stringblocksize = unpack("4i", data[4:20])
		else:
			self.build, self.locale, self.wdb4, self.wdb5 = unpack("i4sii", data[4:20])
			if self.build >= 9438:
				self.version = unpack("i", data[20:24])[0]
	
	
	def data(self):
		self._load_data()
		return pack(self.structure(), *self.__return())
	
	def structure(self):
		if self.signature == "WDBC":
			return "4s4i"
		else:
			if self.build < 9438:
				return "4si4sii"
			else:
				return "4si4s3i"
	
	def length(self):
		if self.signature == "WDBC":
			return 20
		else:
			if self.build < 9438:
				return 20
			else:
				return 24


class DBFile(dict):
	"""A generic WDB or DBC file."""
	writable = True
	
	def __init__(self, path="", build=0, name="", environment={}, mode="r", structure=None):
		self.path = path				# Read/Write location
		self.filename = name			# Logical filename
		self.structure = structure		# Absolute structure
		self.sort = []				# Row sort order
		self.build = build			# Build number
		self.header = DBHeader(self)		# Full header
		self.strblk = ""				# Stringblock
		self.environment = environment	# Full environment
		self.mode = mode				# Mode (read/write)
		
		if hasattr(self.structure, "signature"):
			self.signature = self.structure.signature
		
		self._postinit()
	
	def __repr__(self):
		return "%s(path=%r, build=%r, name=%r, mode=%r)" % (self.__class__.__name__, self.path, self.build, self.filename, self.mode)
	
	
	def _init_parse(self):
		"Initiate parsing of a file. Used only in read mode."
		assert self.path, L["PATH_NOT_SET"]
		assert exists(self.path), L["PATH_NOT_VALID"]
		
		f = open(self.path)
		self.header._load_stream(f.read(24))
		f.close()
		
		self.signature = self.header.signature
		
		if not self.filename:
			if self.signature != "WDBC" and self.signature in magic:
				self.filename = magic[self.signature]
			else:
				self.filename = getfilename(self.path)
		
		if not self.build:
			if self.signature == "WDBC":
				log.warning(L["BUILD_NOT_SET"]) 
			else:
				self.build = self.header.build
			
		if not self.structure:
			self.load_structure(self.filename, self.build)
		
		log.info(L["READING_FILE"] % self.path) 
	
	def _postinit(self):
		if self.mode == "r" and self.path:
			self.load()
		elif self.mode == "w":
			if not self.writable:
				raise TypeError(L["FILETYPE_NOT_WRITABLE"] % self.__class__.__name__)
			if not self.structure:
				self.load_structure()
	
	
	def append(self, row):
		"Appends a row at the end of the file. Returns the new row's index."
		l = len(self) + 1
		if "_id" not in row:
			row["_id"] = l
		self[l] = row
		
		return l
	
	def clear(self):
		"Deletes every row in the file"
		for k in self.keys():
			del self[k]
	
	def filter(self, args, limit=0):
		results = []
		match = len(args)
		for k in self:
			i = 0
			for arg in args:
				if self[k][arg] != args[arg]:
					break
				i += 1
			if i == match:
				results.append(k)
				if len(results) >= limit:
					return results
		
		return results
	
	def parse(self):
		raise NotImplementedError
	
	def load(self, path=""):
		"Load a file. If path is not given, reloads the current file."
		path = path or self.path
		self.path = path
		self.parse()
	
	def load_structure(self, filename=None, build=None):
		self.structure = getstructure(filename or self.filename, build or self.build, parent=self)
		self.signature = self.structure.signature
		log.info(L["USING_STRUCTURE"] % (self.filename, self.build))
	
	def merge(self, other):
		"Merge another file into self"
		for k in other:
			self[k] = other[k].dict()
	
	def rows(self):
		"Return a list of all rows in the file"
		return [self[k] for k in self]
	
	def update(self, other):
		"Merge a file with an identical structure into self"
		if self.structure != other.structure:
			raise ValueError
		dict.update(self, other)
	
	def write(self, filename=""):
		"Write the cache to disk, defaulting filename to original file"
		filename = filename or self.path or os.devnull
		data = self.data()
		f = open(filename, "w")
		f.write(data)
		f.close()
		log.info(L["WRITTEN_BYTES"] % (len(data), filename))


class DBRow(list):
	"""
	A database row.
	Names of the variables of that class should not be used in field names of structures
	"""
	initialized = False
	
	def __init__(self, parent, data=None, columns=None, reclen=0):
		self._parent = parent 
		self._values = {} # Columns values storage
		self._postload = [] # temporarily store col/val for _add_data once the column is loaded
		self.structure = parent.structure
		
		self.initialized = True # need for normal work __setattr__
		
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
						log.warning(L["COLUMN_NOT_FOUND"] % k)
		
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
						if data[cursor:cursor+4] == "\x00\x00\x00\x00":
							_data = ""
						else:
							_data = unicode(parent._getstring(unpack("<i", data[cursor:cursor+4])[0]), "utf-8")
						cursor += 4
					else:
						_data = unicode(data[cursor:data.index("\x00", cursor)], "utf-8")
						cursor += len(str(_data.encode("utf-8"))) + 1
				
				elif char == "A": # The amount of dynamic columns in the row
					_data = unpack("<i", data[cursor:cursor+4])[0]
					cursor += 4
					dynfields = _data
				
				elif char == "": # ImplicitIDField
					_data = len(parent) + 1 # 1-indexed
				
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
					log.warning(L["RECLEN_NOT_RESPECTED"] % (self._id, reclen+8, cursor, reclen+8-cursor))
	
	def __int__(self):
		return self._id
	
	def __getattr__(self, attr):
		if attr in self.structure:
			return self._get_value(attr)
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
			raise TypeError
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
		index = self.structure.index(name)
		col = self.structure[index]
		try:
			self._values[name] = col.to_python(value, self)
		except UnresolvedRelation:
			self._values[name] = value
	
	def _get_value(self, name):
		if name not in self._values:
			index = self.structure.index(name)
			raw_value = self[index]
			try:
				self._set_value(name, raw_value)
			except UnresolvedRelation, ex:
				return UnresolvedObjectRef(ex.reference)
			except RelationError:
				return None # Key doesn't exist, or equals 0
		return self._values[name]
	
	def _save(self):
		for name in self._values:
			index = self.structure.index(name)
			col = self.structure[index]
			self[index] = col.from_python(self._values[name])
	
	def data(self):
		"Convert the column list into a byte stream"
		self._save()
		data = []
		for k, v in zip(self.structure, self):
			if v == None:
				continue
			elif k.char == "s":
				_data = v.encode("utf-8") + "\x00"
			elif k.char == "A":
				_data = pack("<i", v)
			else:
				_data = pack("<%s" % k.char, v)
			data.append(str(_data))
		if self.structure.reclen:
			data[self.structure.reclen-1] = pack("<i", len("".join(data[2:])))
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
		return len(self.data())-8
	
	def update(self, other):
		for k in other:
			self[k] = other[k]


class WDBFile(DBFile):
	"""
	A non-encrypted WDB file.
	- Every WDB file must contain build and locale info.
	- The first column of every WDB file is an unique ID primary key. If you want
	  more than one primary key, you will need to use a DBC file.
	- The second column specifies the record length (reclen). The reclen is the
	  size in bytes of the following row (not counting the id and reclen itself).
	- EOF is 8 NULL bytes (corresponding to id and reclen of 0).
	"""
	def __setitem__(self, key, item):
		if type(item) in (list, dict) and item:
			DBFile.__setitem__(self, key, DBRow(self, columns=item))
			#if str(key).isdigit(): self[key].id = int(key)
		else:
			DBFile.__setitem__(self, key, item)
	
	
	def _setrow(self, data, reclen):
		row = DBRow(self, data=data, reclen=reclen)
		if row[0] in self:
			log.warning(L["MULTIPLE_ROW_INSTANCE"] % row[0])
		self[row[0]] = row
		self.sort.append(row[0])
	
	
	def data(self):
		"""Convert the data dict into a byte stream"""
		header = self.header.data()
		data = "".join([self[k].data() for k in self])
		eof = "\x00" * 8
		return header+data+eof
	
	def parse(self):
		"""Parse a wdb file and build dict out of it"""
		self._init_parse()
		filename = self.path
		size = getsize(filename)
		f = open(filename, "rb")
		f.seek(self.header.length())
		
		while size - f.tell() > 8: # while not EOF
			data = f.read(8)
			recid, reclen = unpack("ii", data)
			data += f.read(reclen)
			self._setrow(data, reclen)
		
		f.close()
		log.info(L["TOTAL_ROWS"] % len(self.rows()))
	
	def update_dynfields(self):
		"""Update all the dynfields in the file"""
		dyns = [k for k in self.structure.columns if isinstance(k, DynamicFields)]
		for k in self:
			for group in dyns:
				self[k][group[0].name] = 0 # set master to 0
				for fields in group[1:]:
					values = [self[k][col.name] for col in fields]
					if set(values) == set([None]):
						continue
					elif None in values: # TODO log event
						for col in fields:
							if self[k][col.name] != None:
								self[k][col.name] = 0
					self[k][group[0].name] += 1
	
	def update_reclens(self):
		"""Update all the reclens in the file"""
		for k in self:
			self[k]["_reclen"] = self[k].reclen()


class EncryptedWDBFile(WDBFile):
	"""
	An encryted WDB file (not implemented).
	- Header is never encrypted.
	- EOF is 20 NULL bytes.
	"""
	pass



class DBCFile(DBFile):
	"""
	A regular DBC file.
	"""
	def __setitem__(self, key, item):
		if type(item) in (list, dict) and item:
			DBFile.__setitem__(self, key, DBRow(self, columns=item))
			if key.isdigit(): self[key].id = key
		else:
			DBFile.__setitem__(self, key, item)
	
	
	def _setrow(self, data):
		row = DBRow(self, data=data, reclen=self.header.reclen-8)
		if row[0] in self:
			log.warning(L["MULTIPLE_ROW_INSTANCE"] % row[0])
		self[row[0]] = row
	
	def _init_strblk(self):
		log.info(L["READING_STRINGBLOCK"] % self.path)
		f = open(self.path, "rb")
		f.seek(-self.header.stringblocksize, 2)
		self.strblk = f.read()
		f.close()
	
	def _getstring(self, addr):
		"""Return a string, given a pointer in the blockstring"""
		if not self.strblk:
			self._init_strblk()
		try:
			val = self.strblk[addr:addr+self.strblk[addr:addr+1024].index("\x00")]
		except ValueError:
			try:
				val = self.strblk[addr:addr+self.strblk[addr:addr+2048].index("\x00")]
			except ValueError:
				log.critical(L["SUBSTRING_NOT_FOUND"] % addr)
				raise
		return val
	
	def _generate_structure(self):
		"""Generates a structure based on header data"""
		# TODO improve it, guess floats and shorter fields.
		if self.header.field_count * 4 == self.header.reclen:
			structure_string = "i" * self.header.field_count
		else:
			raise NotImplementedError
		return _Generated(structure_string)

	
	def parse(self):
		"""Parse a dbc file and build dict out of it"""
		self._init_parse()
		filename = self.path
		size = getsize(filename)
		f = open(filename, "rb")
		f.seek(self.header.length())
		
		reclen = self.header.reclen
		struct_len = self.structure._reclen()
		if struct_len != reclen:
			log.warning(L["DBC_RECLEN_NOT_RESPECTED"] % (reclen, struct_len, reclen-struct_len))
		
		row_count = self.header.row_count
		while row_count > len(self): # while lacking rows
			self._setrow(f.read(reclen))
		
		field_count = self.header.field_count
		total_fields = len(self.structure)
		if field_count != total_fields:
			# Don't forget implicit fields
			total_fields = len([k for k in self.structure if k.char])
			if field_count != total_fields:
				log.warning(L["DBC_INCORRECT_FIELD_COUNT"] % (field_count, total_fields))
		
		log.info(L["TOTAL_ROWS"] % (row_count))
		f.close()
	
	
	def data(self):
		"""Convert the data dict into a byte string"""
		header = self.header.data()
		data = "".join([self[k].data() for k in self])
		eof = "\x00" * 8
		return header+data+eof


class ComplexDBCFile(DBCFile):
	"""
	A DBC file with two or more primary keys.
	TODO test writing
	"""
	def _setrow(self, data):
		row = DBRow(self, data=data)
		id1, id2 = row[0], row[1] #TODO row.pkeys
		if id1 not in self:
			self[id1] = {}
		self[id1][id2] = row
	
	
	def rows(self):
		"Return a list of all rows in the file"
		li = []
		for k in self:
			for j in self[k]:
				li.append(self[k][j])
		return li # [[self[k][j] for j in self[k]] for k in self] ?


class UnknownDBCFile(DBCFile):
	"""
	A DBC file with an unknown structure.
	"""
	writable = False
	def load_structure(self, filename=None, build=None):
		self.structure = self._generate_structure()
		log.info(L["USING_GENERATED_STRUCTURE"] % (self.filename, self.build))


# TODO we need to use DBFile as base and
# change class dynamically in __new__
def fopen(*pargs, **kwargs):
	try:
		name = "name" in kwargs and kwargs["name"] or pargs[0]
	except IndexError:
		raise TypeError("Required argument 'name' not found")
	sig = getsignature(name)
	if sig == "WDBC":
		filename = "name" in kwargs and kwargs["name"] or getfilename(name).lower()
		if filename == "itemsubclass": # TODO
			return ComplexDBCFile(*pargs, **kwargs)
		try:
			getstructure(filename)
		except StructureError:
			return UnknownDBCFile(*pargs, **kwargs)
		return DBCFile(*pargs, **kwargs)
	
	return WDBFile(*pargs, **kwargs)


def new(*pargs, **kwargs):
	if not "name" in kwargs:
		if not "structure" in kwargs:
			raise TypeError(L["FILENAME_NOT_SPECIFIED"])
		name = kwargs["structure"].__class__.__name__.lower()
	else:
		name = kwargs["name"]
	
	s = "structure" in kwargs and kwargs["structure"] or getstructure(name)
	
	if s.signature == "WDBC":
		return DBCFile(mode="w", *pargs, **kwargs)
	
	return WDBFile(mode="w", *pargs, **kwargs)
