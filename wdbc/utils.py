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


def fopen(name, build=0, structure=None, environment={}):
	from .structures import StructureNotFound, getstructure
	
	file = open(name, "rb")
	filename = getfilename(name)
	signature = file.read(4)
	
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
	
	elif name.endswith(".wcf"):
		from .dbc import WCFFile
		cls = WCFFile
		structure = structure or getstructure(filename)
	
	else:
		from .wdb import WDBFile
		cls = WDBFile
	
	file = cls(file, build=build, structure=structure, environment=environment)
	file.preload()
	
	return file


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
def get(name, build):
	if build == -1:
		from .environment import get_latest_build
		build = get_latest_build()
	
	if build not in __envcache:
		from .environment import Environment
		__envcache[build] = Environment(build)
	
	return __envcache[build][name]
