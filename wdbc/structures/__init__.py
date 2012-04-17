"""
Base logic for pywow structures
"""

from structures import Structure, Skeleton
from .fields import *
from .main import *
from .generated import GeneratedStructure


class StructureNotFound(Exception):
	pass

class StructureLoader():
	wowfiles = None

	@classmethod
	def setup(cls):
		if cls.wowfiles is None:
			cls.wowfiles = {}
			for name in globals():
				try:
					if not issubclass(globals()[name], Structure):
						continue
				except TypeError:
					continue
				cls.wowfiles[name.lower()] = globals()[name]

	@classmethod
	def getstructure(cls, name, build=0, parent=None):
		name = name.replace("-", "_")
		if name in cls.wowfiles:
			return cls.wowfiles[name](build, parent)
		raise StructureNotFound("Structure not found for file %r" % (name))

StructureLoader.setup()
getstructure = StructureLoader.getstructure


class LocalizedStringField(Structure):
	"""
	Structure for the LocalizedField class
	"""
	fields = Skeleton(
		StringField("enus"),
		StringField("kokr"),
		StringField("frfr"),
		StringField("dede"),
		StringField("zhcn"),
		StringField("zhtw"),
		StringField("eses"),
		StringField("esmx"),
		BitMaskField("locflags")
	)

	def changed_5595(self, fields):
		fields.insert_fields((
			StringField("ruru"),
			StringField("unk1"),
			StringField("unk2"),
			StringField("unk3"),
			StringField("unk4"),
			StringField("unk5"),
			StringField("unk6"),
			StringField("unk7"),
		), before="locflags")

	def changed_11927(self, fields):
		self.changed_5595(fields)
		fields.delete_fields(
			"kokr", "frfr", "dede",
			"zhcn", "zhtw", "eses",
			"esmx", "ruru", "unk1",
			"unk2", "unk3", "unk4",
			"unk5", "unk6", "unk7",
			"locflags",
		)

	def changed_11993(self, fields):
		self.changed_5595(fields)

	def changed_12025(self, fields):
		self.changed_11927(fields)
