# -*- coding: utf-8 -*-
"""
Utilitary functions
"""

import os.path


def getfilename(val):
	"""
	Returns "item" from /home/adys/Item.dbc
	"""
	return os.path.splitext(os.path.basename(val))[0].lower()

def generate_structure(db):
	"""
	Generates a DBStructure based on header data
	TODO improve it, guess floats and shorter fields.
	"""
	from .structures import GeneratedStructure

	if db.header.field_count * 4 == db.header.reclen:
		structure_string = "i" * db.header.field_count
	else:
		raise NotImplementedError

	return GeneratedStructure(structure_string)


def fopen(f, build=0, structure=None, environment={}):
	from .structures import StructureNotFound, getstructure

	if isinstance(f, basestring):
		# open() the file only if passing a path
		f = open(f, "rb")
	filename = getfilename(f.name)
	f.seek(0)
	signature = f.read(4)

	if signature == "WDB2" or signature == "WCH2":
		from .db2 import DB2File
		cls = DB2File
		try:
			_structure = structure or getstructure(filename)
		except StructureNotFound:
			pass

	elif signature == "WDBC":
		from .dbc import DBCFile, InferredDBCFile
		cls = DBCFile
		try:
			_structure = structure or getstructure(filename)
		except StructureNotFound:
			pass
		else:
			cls = DBCFile
			if getattr(_structure, "implicit_id", None):
				cls = InferredDBCFile

	elif not signature:
		raise IOError()

	elif f.name.endswith(".wcf"):
		from .dbc import WCFFile
		cls = WCFFile
		structure = structure or getstructure(filename)

	else:
		from .wdb import WDBFile
		cls = WDBFile

	f.seek(0)
	return cls.open(f, build=build, structure=structure, environment=environment)


def new(name, build=0, structure=None, environment={}):
	from .structures import getstructure
	file = open(name, "wb")

	if not structure:
		structure = getstructure(getfilename(name), build=build)

	if structure.signature == "WDBC":
		from .dbc import DBCFile
		return DBCFile(file, build=build, structure=structure, environment=environment)

	from .wdb import WDBFile
	return WDBFile(file, build=build, structure=structure, environment=environment)


__envcache = {}
def get(name, build, locale="enUS"):
	from .environment import Environment
	if build == -1:
		build = Environment.highestBuild()

	if build not in __envcache:
		__envcache[build] = {}

	if locale not in __envcache[build]:
		__envcache[build][locale] = Environment(build, locale)

	return __envcache[build][locale].dbFile(name)
