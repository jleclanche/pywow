#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from .fields import IDField, LocalizedFields, RecLenField, UnknownField
from ..logger import log


class StructureError(Exception):
	pass

class DBStructure(list):
	""" A database structure. """
	signature = "WDBC"
	def __init__(self, build=0, parent=None):
		self.name = type(self).__name__.lower()
		self.parent = parent # DBC file
		self.pkeys = []
		self.column_names = []
		self.reclen = 0
		names = []
		
		def _lazy_rename(col):
			names.append(col.name)
			i = names.count(col.name)
			if i > 1:
				col.name = "%s_%d" % (col.name, i-1)
		
		self.columns = copy.deepcopy(self.base)
		self.builds = sorted([int(m[8:]) for m in dir(self) if m.startswith("changed_")])
		
		if self.builds and build:
			_builds = sorted([k for k in self.builds if k <= build])
			if _builds:
				getattr(self, "changed_%i" % _builds[-1:][0])(self.columns)
		
		for col in self.columns:
			if hasattr(col, "get_fields"):
				for _col in col.get_fields():
					_lazy_rename(_col)
					self.add_column(_col)
			else:
				if isinstance(col, IDField):
					self.pkeys.append(col)
				elif isinstance(col, RecLenField):
					self.reclen = len(self) + 1
				_lazy_rename(col)
				self.add_column(col)
	
	def __contains__(self, name):
		return name in self.column_names
	
	def add_column(self, col):
		col.parent = self
		self.append(col)
		self.column_names.append(col.name)
	
	def get_column(self, column_name):
		index = self.index(column_name)
		return self[index]
	
	def _reclen(self):
		return sum(k.size for k in self)
	
	def index(self, column_name):
		return self.column_names.index(column_name)


class Skeleton(list):
	"""The database's actual structure. Used to concatenate columns into a single structure."""
	def __init__(self, *fields):
		for field in fields:
			self.append(field)
	
	def insert_field(self, field, before):
		names = [f.name for f in self]
		try:
			self.insert(names.index(before), field)
		except ValueError:
			raise StructureError("%r is not a valid column reference for insert_field" % (before))
	
	def append_fields(self, *fields):
		for field in fields:
			self.append(field)
	
	def delete_fields(self, *fields):
		names = [field.name for field in self]
		
		for field in fields:
			try:
				self.pop(names.index(field))
				names.pop(names.index(field))
			except ValueError:
				raise StructureError("%r is not a valid column to delete" % (field))
	
	def insert_fields(self, fields, before):
		for field in fields:
			self.insert_field(field, before=before)
	
	def update_locales(self, locales):
		updated = False
		for field in self:
			if isinstance(field, LocalizedFields):
				field.update_locales(locales)
				updated = True
		
		if not updated:
			raise StructureError("No locales to update for update_locales")


class _Generated(DBStructure):
	"""Dynamically generated DBC structure."""
	def __init__(self, structure_string, *pargs, **kwargs):
		columns = []
		self.base = Skeleton(*[UnknownField() for s in structure_string])
		DBStructure.__init__(self)
