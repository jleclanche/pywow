# -*- coding: utf-8 -*-

import os
from .structures import GeneratedStructure

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
