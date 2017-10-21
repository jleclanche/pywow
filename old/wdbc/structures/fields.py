import struct
from itertools import takewhile


class Field(object):
	pass


class StringField(Field):
	def parse(self, data):
		c = data.read(1)
		ret = []
		while c and c != b"\0":
			ret.append(c)
			c = data.read(1)
		return b"".join(ret).decode("utf-8")


class IntegerField(Field):
	def parse(self, data):
		return struct.unpack("<i", data.read(4))


class ShortField(Field):
	def parse(self, data):
		return struct.unpack("<h", data.read(2))


class ForeignKey(IntegerField):
	def __init__(self, to, *args):
		self.to = to
		super().__init__(*args)
