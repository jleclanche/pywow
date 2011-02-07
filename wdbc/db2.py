# -*- coding: utf-8 -*-

from struct import unpack
from .dbc import DBCFile
from .log import log
from .structures import getstructure, LocalizedStringField, LocalizedField
from .utils import getfilename

from . import DBHeader

SEEK_CUR = 1 # os.SEEK_CUR

class DB2Header(DBHeader):
	def __len__(self):
		if self.build < 12834:
			return 32
		return 48
	
	def load(self, file):
		self.signature, self.row_count, self.field_count, self.reclen, self.stringblocksize, self.dbhash, self.build, self.timestamp = unpack("<4s7i", file.read(32))
		if self.build >= 12834:
			if self.signature == "WCH2" and self.build < 12942:
				# Work around a bug in cataclysm beta which doesn't take in account the first \0
				log.warning("Old adb file, working around stringblock bug")
				self.stringblocksize += 1
			self.unk1, self.unk2, self.locale, self.unk3 = unpack("<4i", file.read(16))
	
	def get_block_size(self):
		if self.build < 12834:
			return 0
		return self.unk2 * 6 - len(self) * 3 if self.unk2 else 0


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
	
	def preload(self):
		f = self.file
		f.seek(len(self.header))
		_ = f.read(self.header.get_block_size())
		
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
