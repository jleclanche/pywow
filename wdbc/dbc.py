# -*- coding: utf-8 -*-

from collections import namedtuple
from struct import pack, unpack
from .log import log
from .main import DBHeader, DBFile
from .structures import fields, StructureNotFound, getstructure, LocalizedStringField, LocalizedField
from .utils import getfilename, generate_structure


SEEK_CUR = 1 # os.SEEK_CUR
SEEK_END = 2 # os.SEEK_END

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
		self.header = self._parse_header()
		self.build = build
		self.__load_structure(structure)

	def _parse_header(self):
		DBCHeader = namedtuple("DBCHeader", ["signature", "row_count", "field_count", "reclen", "stringblocksize"])
		data = self.file.read(20)
		return DBCHeader(*unpack("<4s4i", data))

	def _header_data(self):
		return pack("<4s4i", *self.header)

	def __check_padding(self, file, field):
		"""
		In 4.0.0 DBCs, fields are padded to their own size
		within the file. Example:
		byte, int -> byte, pad, pad, pad, int
		"""
		address = file.tell()
		seek = (address % field.size)
		seek = seek and -(seek - field.size)
		file.seek(seek, SEEK_CUR)

	def __load_structure(self, structure):
		name = getfilename(self.file.name)
		try:
			self.structure = getstructure(name, self.build, parent=self)
		except StructureNotFound:
			self.structure = generate_structure(self)

		# Generate the Localized Fields
		fieldidx = []
		for i, field in enumerate(self.structure):
			if isinstance(field, LocalizedField):
				fieldidx.append((i, field.name))

		if fieldidx:
			from copy import copy
			fields = LocalizedStringField(build=self.build)
			for i, name in reversed(fieldidx):
				# Build a copy of the fields
				toinsert = [copy(field).rename("%s_%s" % (name, field.name)) for field in fields]
				self.structure[i:i+1] = toinsert

		log.info("Using %s build %i" % (self.structure, self.build))

		self.check_integrity()

	def _parse_field(self, data, field, row=None):
		if self.build in (11927, 12025):
			self.__check_padding(data, field)
		return super(DBCFile, self)._parse_field(data, field, row)

	def _parse_row(self, id):
		address, reclen = self._addresses[id]
		self.file.seek(address)
		data = self.file.read(reclen) # We also read id and reclen columns
		row = self.parse_row(data) # assign to DBRow
		self._values[id] = row

	def _parse_string(self, data):
		address, = unpack("<I", data.read(4))
		if not address:
			return ""

		f = self.file
		pos = f.tell()
		f.seek(-self.header.stringblocksize, SEEK_END) # Go to the stringblock
		f.seek(address, SEEK_CUR) # seek to the address in the stringblock

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

		rows = 0
		field = self.structure[0]
		row_header_size = field.size
		reclen = self.header.reclen
		while rows < self.header.row_count:
			address = f.tell() # Get the address of the full row
			id = self._parse_field(f, field)

			self._add_row(id, address, reclen)

			f.seek(reclen - row_header_size, SEEK_CUR) # minus length of id
			rows += 1


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

			f.seek(reclen - row_header_size, SEEK_CUR) # minus length of id
			rows += 1


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

			f.seek(reclen, SEEK_CUR)
			rows += 1


class UnknownDBCFile(DBCFile):
	"""
	A DBC file with an unknown structure.
	"""
	writable = False
	def load_structure(self, filename=None, build=None):
		self.structure = self._generate_structure()
		log.warn("Using generated structure for file %s, build %i" % (self.filename, self.build))
