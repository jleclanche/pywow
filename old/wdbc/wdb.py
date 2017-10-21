import struct
from collections import namedtuple
from io import BytesIO


class WDBObject(object):
	def __init__(self):
		self._rows = {}
		self._offsets = {}
		self.structure = None

	def __del__(self):
		self.file.close()

	def __getitem__(self, item):
		if item not in self._rows:
			if item in self._offsets:
				self.fetch(item)
			else:
				raise IndexError
		return self._rows[item]

	def fetch(self, item):
		self.file.seek(self._offsets[item])
		id, length = struct.unpack("<2i", self.file.read(8))
		assert id == item

		data = BytesIO(self.file.read(length))

		cols = []
		for field in self.structure.values():
			cols.append(field.parse(data))
		self._rows[id] = self.row_class(*cols)

	def guess_structure(self):
		from .structures.structure import get_structure
		return get_structure(magic=self.header.magic)

	def keys(self):
		return self._offsets.keys()

	def read_file(self, file):
		self.file = file
		self.read_header(file)
		print(self.file.tell())
		self.structure = self.guess_structure()()
		self.row_class = namedtuple("WDBRow", self.structure)
		self.read_data(file)

	def read_header(self, data):
		fields = ["magic", "build", "locale", "wdb4", "wdb5"]
		values = list(struct.unpack("<4s4i", data.read(20)))
		values[0] = values[0].decode("utf-8")

		if values[1] >= 9438:
			fields.append("version")
			values += struct.unpack("<i", data.read(4))
		header_class = namedtuple("WDBHeader", fields)
		self.header = header_class(*values)

	def read_data(self, data):
		while True:
			row_header = data.read(8)
			if len(row_header) < 8:
				print("Early EOF, expect breakage")
				break
			id, length = struct.unpack("<2i", row_header)
			print(id, length, self.header)
			if id == 0:
				break
			self._offsets[id] = data.tell() - 8
			data.seek(length, 1)


def read_file(file):
	wdb = WDBObject()
	wdb.read_file(file)
	return wdb
