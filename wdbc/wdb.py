# -*- coding: utf-8 -*-

from struct import pack, unpack, error as StructError
from .log import log
from .structures import fields, getstructure
from .utils import getfilename

from . import DBHeader, DBFile

SEEK_CUR = 1 # os.SEEK_CUR

class WDBHeader(DBHeader):
	"""
	A WDB header, structure as follows:
	- 4 byte string signature (reversed)
	- 4 byte integer build
	- 4 byte string locale (reversed)
	- 4 byte integer unknown - maybe related to dynamic fields?
	- 4 byte integer unknown
	As of build 9438, an additional 4 byte integer indicates the data version for that build.
	"""
	def __len__(self):
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
		ret = pack("<4si4sii", self.signature, self.build, self.locale, self.wdb4, self.wdb5)
		if self.build >= 9438:
			ret += pack("<i", self.version)
		
		return ret


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
		super(WDBFile, self).__init__(file, build, structure, environment)
		
		self.header = WDBHeader()
		if "w" in self.file.mode: # open for writing
			self.header.signature = structure.signature
			self.header.build = build
		else:
			self.header.load(file)
			if not build:
				build = self.header.build
		self.build = build
		
		self.__load_structure(structure)
		
		self.row_header_size = self.structure[0].size + 4
	
	def __load_structure(self, structure):
		if self.header.signature in self.MAGIC:
			name = self.MAGIC[self.header.signature]
		else: # allow for custom structures
			name = getfilename(self.file.name)
		self.structure = getstructure(name, self.build, parent=self)
		log.info("Using %s build %i" % (self.structure, self.build))
	
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
		return unicode(data.read(index + 1)[:-1], "utf-8")
	
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
		"""Update all the dynfields in the file"""
		dyns = [k for k in self.structure.columns if isinstance(k, fields.DynamicFields)]
		for k in self:
			for group in dyns:
				master_name = group[0].name
				amount = 0 # Amount of active fields
				for columns in group[1:]:
					values = [self[k]._raw(col.name) for col in columns]
					if set(values) == set([None]):
						continue
					elif None in values: # TODO log event
						for col in columns:
							if self[k]._raw(col.name) != None:
								setattr(self[0], col.name, 0)
					amount += 1
				setattr(self[k], master_name, amount) # set master to correct field amount
