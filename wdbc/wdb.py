# -*- coding: utf-8 -*-

from collections import namedtuple
from struct import pack, unpack, error as StructError
from .log import log
from .main import DBFile
from .structures import fields, getstructure
from .utils import getfilename


SEEK_CUR = 1 # os.SEEK_CUR

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

	def _readHeader(self):
		self.headerStructure = "<4s4i"
		data = self.file.read(20)
		fields = ["signature", "build", "locale", "wdb4", "wdb5"]
		signature, build, locale, wdb4, wdb5 = unpack(self.headerStructure, data)

		if build < 9438:
			# Old style headers, 20 bytes
			WDBHeader = namedtuple("WDBHeader", fields)
			self.header = WDBHeader(signature, build, locale, wdb4, wdb5)
		else:
			fields.append("version")
			WDBHeader = namedtuple("WDBHeader", fields)
			version, = unpack("<i", self.file.read(4))
			self.headerStructure = "<4s5i"
			self.header = WDBHeader(signature, build, locale, wdb4, wdb5, version)

	def _readAddresses(self):
		while True:
			address = self.file.tell() # Get the address of the full row
			id = self._parse_field(self.file, self.structure[0])
			if not id:
				# We reached EOF
				break

			reclen = self._parse_field(self.file, self.structure[1])
			self._add_row(id, address, reclen)
			self.file.seek(reclen, SEEK_CUR)

	def setStructure(self, structure):
		if self.header.signature in self.MAGIC:
			name = self.MAGIC[self.header.signature]
		else: # allow for custom structures
			name = getfilename(self.file.name)
		self.structure = getstructure(name, self.build, parent=self)
		log.info("Using %s build %i" % (self.structure, self.build))
		self.row_header_size = self.structure[0].size + 4

	def _parse_row(self, id):
		address, reclen = self._addresses[id]
		self.file.seek(address)
		data = self.file.read(reclen + self.row_header_size) # We also read id and reclen columns
		row = self.parse_row(data, reclen) # assign to DBRow
		self._values[id] = row

	def _parse_string(self, data):
		pos = data.tell()
		index = data.read().index("\x00")
		data.seek(pos)
		return data.read(index + 1)[:-1].decode("ascii", "ignore")

	def eof(self):
		return "\0" * self.row_header_size

	def data(self):
		ret = []
		for row in self:
			row = self[row]
			row._save()
			_data = []
			reclen = None

			for field, value in zip(self.structure, row):
				if value is None:
					continue
				elif isinstance(field, fields.RecLenField):
					reclen = len(_data)
					_data.append(0)
				elif isinstance(field, fields.StringField):
					_data.append(value.encode("utf-8") + "\x00")
				elif isinstance(field, fields.StringField):
					_data.append(pack("<I", value))
				else:
					_data.append(pack("<%s" % (field.char), value))

			length = len("".join(_data[2:]))
			_data[reclen] = pack("<I", length)
			ret.append("".join(_data))

		return "".join(ret)

	def preload(self):
		f = self.file
		f.seek(len(self.header))

		rows = 0
		structure_string = "<%si" % (self.structure[0].char)
		while True:
			address = f.tell() # Get the address of the full row
			try:
				id, reclen = unpack(structure_string, f.read(self.row_header_size))
			except StructError:
				log.warning("Breaking early, possible corruption")
				break

			if reclen == 0: # EOF
				break

			self._add_row(id, address, reclen)

			f.seek(reclen, SEEK_CUR)
			rows += 1

	def update_dynfields(self):
		"""
		Update all the dynamic fields in the file
		"""
		# Build a list lookup for dynamic fields: [[master, [a, b], [a, b], ...], ...]
		dyns = [k for k in self.structure.columns if isinstance(k, fields.DynamicFields)]

		for id in self:
			# For each id in the file...
			for group in dyns:
				# ... and each group of dynamic fields...

				master_name = group[0].name
				amount = 0 # Amount of active fields

				for columns in group[1:]:
					# Iterate through each list of columns (excluding the master)
					# First we get a list of each value
					values = [self[id]._raw(col.name) for col in columns]

					# If the values are all none, we keep going
					if set(values) == set([None]):
						continue

					# Otherwise this field is active
					amount += 1

				# finally, update the master to the current amount
				setattr(self[id], master_name, amount)
