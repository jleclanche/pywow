# -*- coding: utf-8 -*-

import os.path
from .structures import GeneratedStructure, StructureNotFound, getstructure

def getfilename(val):
	"Returns 'item' from /home/adys/Item.dbc"
	return os.path.splitext(os.path.basename(val))[0].lower()

def generate_structure(db):
	"""
	Generates a DBStructure based on header data
	"""
	# TODO improve it, guess floats and shorter fields.
	if db.header.field_count * 4 == db.header.reclen:
		structure_string = "i" * db.header.field_count
	else:
		raise NotImplementedError
	return GeneratedStructure(structure_string)


def fopen(name, build=0, structure=None, environment={}):
	from .db2 import DB2File
	from .dbc import DBCFile, InferredDBCFile
	from .wdb import WDBFile
	file = open(name, "rb")
	signature = file.read(4)
	if signature == "WDB2" or signature == "WCH2":
		cls = DB2File
		try:
			_structure = structure or getstructure(getfilename(file.name))
		except StructureNotFound:
			pass
		
	
	elif signature == "WDBC":
		cls = DBCFile
		try:
			_structure = structure or getstructure(getfilename(file.name))
		except StructureNotFound:
			pass
		else:
			cls = DBCFile
			if getattr(_structure, "implicit_id", None):
				cls = InferredDBCFile
	
	elif not signature:
		raise IOError()
	
	elif name.endswith(".wcf"):
		cls = WCFFile
		structure = structure or getstructure(getfilename(file.name))
	
	else:
		cls = WDBFile
	
	file = cls(file, build=build, structure=structure, environment=environment)
	file.preload()
	return file


def new(name, build=0, structure=None, environment={}):
	from .dbc import DBCFile
	from .wdb import WDBFile
	filename = getfilename(name)
	if not structure:
		structure = getstructure(filename, build=build)
	
	file = open(name, "wb")
	
	if structure.signature == "WDBC":
		return DBCFile(file, build=build, structure=structure, environment=environment)
	return WDBFile(file, build=build, structure=structure, environment=environment)


__envcache = {}
def get(name, build):
	from .environment import Environment
	if build not in __envcache:
		__envcache[build] = Environment(build)
	return __envcache[build][name]
