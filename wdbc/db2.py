# -*- coding: utf-8 -*-

from struct import unpack
from .dbc import DBCFile
from .log import log
from .structures import getstructure
from .utils import getfilename

from . import DBHeader

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