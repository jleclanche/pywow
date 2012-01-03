# -*- coding: utf-8 -*-

from collections import namedtuple
from struct import unpack
from .dbc import DBCFile
from .log import log
from .structures import getstructure, LocalizedStringField, LocalizedField
from .utils import getfilename


SEEK_CUR = 1 # os.SEEK_CUR

class DB2File(DBCFile):
	"""
	New DB format introduced in build 12803
	"""

	def _readHeader(self):
		data = self.file.read(32)
		self.headerStructure = "<4s7i"
		fields = ["signature", "row_count", "field_count", "reclen", "stringblocksize", "dbhash", "build", "timestamp"]
		signature, row_count, field_count, reclen, stringblocksize, dbhash, build, timestamp = unpack(self.headerStructure, data)


		if build <= 12880:
			# Old style headers, 32 bytes
			DB2Header = namedtuple("DB2Header", fields)
			header = DB2Header(signature, row_count, field_count, reclen, stringblocksize, dbhash, build, timestamp)
		else:
			self.headerStructure = "<4s11i"
			fields += ["lookup_start", "lookup_end", "locale", "unk"]
			DB2Header = namedtuple("DB2Header", fields)
			lookup_start, lookup_end, locale, unk = unpack("<4i", self.file.read(4*4))

			if signature == "WCH2" and build < 12942:
				# Work around a bug in cataclysm beta which doesn't take in account the first \0
				log.warning("Old adb file, working around stringblock bug")
				stringblocksize += 1
			header = DB2Header(signature, row_count, field_count, reclen, stringblocksize, dbhash, build, timestamp, lookup_start, lookup_end, locale, unk)

			# Skip the index block... we'll have to use it some day..
			if lookup_start != lookup_end:
				size = (lookup_end - lookup_start + 1) * 6
				if size < 0:
					log.error("lookup size < 0: %i. This file is corrupt. Expect breakage!" % (size))
				else:
					self.file.seek(size, SEEK_CUR)

		return header
