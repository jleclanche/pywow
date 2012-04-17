from cStringIO import StringIO
from struct import pack, unpack, error as StructError
from .log import log
from .structures import fields


class DBFile(object):
	"""
	Base class for WDB and DBC files
	"""

	@classmethod
	def open(cls, file, build, structure, environment):
		if isinstance(file, basestring):
			file = open(file, "rb")

		instance = cls(file, build, environment)
		instance._readHeader()
		instance.setStructure(structure)
		instance._rowDynamicFields = 0 # Dynamic fields index, used when parsing a row
		instance._readAddresses()

		return instance

	def __init__(self, file=None, build=None, environment=None):
		self._addresses = {}
		self._values = {}
		self.file = file
		self.build = build
		self.environment = environment

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
			raise TypeError("DBFile indices must be integers, not %s" % (type(item)))

		if isinstance(value, DBRow):
			self._values[item] = value
			self._addresses[item] = -1
		else:
			# FIXME technically we should allow DBRow, but this is untested and will need resetting parent
			raise TypeError("Unsupported type for DBFile.__setitem__: %s" % (type(value)))

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
			log.warning("Multiple instances of row %r found in %s" % (id, self.file.name))
		self._addresses[id] = (address, reclen)

	def _parse_field(self, data, field, row=None):
		"""
		Parse a single field in stream.
		"""
		if field.dyn > self._rowDynamicFields:
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
				self._rowDynamicFields = ret

			else:
				ret, = unpack("<%s" % (field.char), data.read(field.size))
		except StructError:
			log.warning("Field %s could not be parsed properly" % (field))
			ret = None

		return ret

	def supportsSeeking(self):
		return hasattr(self.file, "seek")

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

	def parse_row(self, data, reclen=0):
		"""
		Assign data to a DBRow instance
		"""
		return DBRow(self, data=data, reclen=reclen)

	def values(self):
		"""
		Return a list of the file's values
		"""
		return [self[id] for id in self]

	def setRow(self, key, **values):
		self.__setitem__(key, DBRow(self, columns=values))

	def size(self):
		if hasattr(self.file, "size"):
			return self.file.size()
		elif isinstance(self.file, file):
			from os.path import getsize
			return getsize(self.file.name)
		raise NotImplementedError

	def update(self, other):
		"""
		Update file from iterable other
		"""
		for k in other:
			self[k] = other[k]

	def write(self, filename=""):
		"""
		Write the file data on disk. If filename is not given, use currently opened file.
		"""
		_filename = filename or self.file.name

		data = self.header.data() + self.data() + self.eof()

		f = open(_filename, "wb") # Don't open before calling data() as uncached rows would be empty
		f.write(data)
		f.close()
		log.info("Written %i bytes at %s" % (len(data), f.name))

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
					log.warning("Reclen not respected for row %r. Expected %i, read %i. (%+i)" % (self.id, real_reclen, data.tell(), real_reclen-data.tell()))

	def __dir__(self):
		result = self.__dict__.keys()
		result.extend(self.structure.column_names)
		return result

	def __getattr__(self, attr):
		if attr in self.structure:
			return self._get_value(attr)

		if attr in self.structure._abstractions: # Union abstractions etc
			field, func = self.structure._abstractions[attr]
			return func(field, self)

		if "__" in attr:
			return self._query(attr)

		return super(DBRow, self).__getattribute__(attr)

	def __int__(self):
		return self.id

	def __setattr__(self, attr, value):
		# Do not preserve the value in DBRow! Use the save method to save.
		if self.initialized and attr in self.structure:
			self._set_value(attr, value)
		return super(DBRow, self).__setattr__(attr, value)

	def __setitem__(self, index, value):
		if not isinstance(index, int):
			raise TypeError("Expected int instance, got %s instead (%r)" % (type(index), index))
		list.__setitem__(self, index, value)
		col = self.structure[index]
		self._values[col.name] = col.to_python(value, row=self)


	def _get_reverse_relation(self, table, field):
		"""
		Return a list of rows matching the reverse relation
		"""
		if not hasattr(self._parent, "_reverse_relation_cache"):
			self._parent._reverse_relation_cache = {}
		cache = self._parent._reverse_relation_cache

		tfield = table + "__" + field
		if tfield not in cache:
			cache[tfield] = {}
			# First time lookup, let's build the cache
			table = self._parent.environment.dbFile(table)
			for row in table:
				row = table[row]
				id = row._raw(field)
				if id not in cache[tfield]:
					cache[tfield][id] = []
				cache[tfield][id].append(row)

		return cache[tfield].get(self.id, None)

	def _matches(self, **kwargs):
		for k, v in kwargs.items():
			if not self._query(k, v):
				return False
		return True

	def _query(self, rel, value=None):
		"""
		Parse a django-like multilevel relationship
		"""
		rels = rel.split("__")
		if "" in rels: # empty string
			raise ValueError("Invalid relation string")

		first = rels[0]
		if not hasattr(self, first):
			if self._parent.environment.hasDbFile(first):
				# Handle reverse relations, eg spell__item for item table
				remainder = rel[len(first + "__"):]
				return self._get_reverse_relation(first, remainder)

			raise ValueError("Invalid relation string")

		ret = self
		rels = rels[::-1]

		special = {
			"contains": lambda x, y: x in y,
			"exact": lambda x, y: x == y,
			"icontains": lambda x, y: x.lower() in y.lower(),
			"iexact": lambda x, y: x.lower() == y.lower(),
			"gt": lambda x, y: x > y,
			"gte": lambda x, y: x >= y,
			"lt": lambda x, y: x < y,
			"lte": lambda x, y: x <= y,
		}

		while rels:
			if rels[-1] in special:
				if len(rels) != 1:
					# icontains always needs to be the last piece of the relation string
					raise ValueError("Invalid relation string")

				return special[rels[-1]](value, ret)
			else:
				ret = getattr(ret, rels.pop())

		return ret

	def _set_value(self, name, value):
		index = self.structure.index(name)
		col = self.structure[index]
		self._values[name] = col.to_python(value, self)
		self[index] = value

	def _get_value(self, name):
		if name not in self._values:
			raw_value = self[self.structure.index(name)]

			self._set_value(name, raw_value)

		return self._values[name]

	def _raw(self, name):
		"""
		Returns the raw value from field 'name'
		"""
		index = self.structure.index(name)
		return self[index]

	def _save(self):
		for name in self._values:
			index = self.structure.index(name)
			col = self.structure[index]
			self[index] = col.from_python(self._values[name])

	def _field(self, name):
		"""
		Returns the field 'name'
		"""
		index = self.structure.index(name)
		return self.structure[index]

	def _default(self):
		"""
		Change all fields to their default values
		"""
		del self[:]
		self._values = {}
		for col in self.structure:
			char = col.char
			if col.dyn:
				self.append(None)
			elif char == "s":
				self.append("")
			elif char == "f":
				self.append(0.0)
			else:
				self.append(0)


	def dict(self):
		"""
		Return a dict of the row as colname: value
		"""
		return dict(zip(self.structure.column_names, self))

	def update(self, other):
		for k in other:
			self[k] = other[k]

	@property
	def id(self):
		"Temporary hack to transition between _id and id"
		return self._id
