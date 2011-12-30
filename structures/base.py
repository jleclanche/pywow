# -*- coding: utf-8 -*-

import copy


class StructureError(Exception):
	pass


class Structure(list):
	"""
	An arbitrary structure.
	The "fields" class property should be defined. as a Skeleton.
	"""
	signature = "WDBC"

	@property
	@classmethod
	def name(cls): # ItemCache.name == "itemcache"
		return cls.__name__.lower()

	def __repr__(self):
		return "<Structure %s>" % (self.__class__.__name__)

	def __init__(self, build=0, parent=None):
		self.parent = parent # DBC file
		self.primary_keys = []
		self._abstractions = {}
		names = []

		def _lazy_rename(col):
			names.append(col.name)
			i = names.count(col.name)
			if i > 1:
				col.name = "%s_%d" % (col.name, i-1)

		self.columns = copy.deepcopy(self.fields)
		builds = self.get_builds()

		if builds and build:
			builds = sorted(k for k in builds if k <= build)
			if builds:
				getattr(self, "changed_%i" % builds[-1])(self.columns)

		for col in self.columns:
			if hasattr(col, "get_abstraction"): # Abstraction for Union
				name, func = col.get_abstraction()
				self._abstractions[name] = (col, func)

			if hasattr(col, "get_fields"):
				for _col in col.get_fields():
					_lazy_rename(_col)
					self.add_column(_col)
			else:
				if col.primary_key:
					self.primary_keys.append(col)
				_lazy_rename(col)
				self.add_column(col)

	def __contains__(self, name):
		return name in self.column_names

	@property
	def column_names(self):
		return [k.name for k in self]

	def add_column(self, col):
		col.parent = self
		self.append(col)

	def get_column(self, column_name):
		index = self.index(column_name)
		return self[index]

	def _reclen(self):
		return sum(k.size for k in self)

	def index(self, column_name):
		return self.column_names.index(column_name)

	def get_builds(self):
		return sorted(int(m[8:]) for m in dir(self) if m.startswith("changed_"))


class Skeleton(list):
	"""
	The database's actual structure. Used to concatenate columns into a single structure.
	"""
	def __init__(self, *fields):
		for field in fields:
			self.append(field)

	def append_fields(self, *fields):
		for field in fields:
			self.append(field)

	def insert_field(self, field, before="", after=""):
		if (before and after) or (not before and not after):
			raise TypeError("insert_field expected 1 'before' or 'after' argument, got %i" % (int(bool(before)) + int(bool(after))))
		names = [f.name for f in self]
		try:
			if before:
				self.insert(names.index(before), field)
			elif after:
				self.insert(names.index(after) + 1, field)
		except ValueError:
			raise StructureError("%r is not a valid column reference for insert_field" % (before or after))

	def insert_fields(self, fields, before="", after=""):
		if after:
			fields = reversed(fields)
		for field in fields:
			self.insert_field(field, before=before, after=after)

	def delete_fields(self, *fields):
		names = [field.name for field in self]

		for field in fields:
			try:
				self.pop(names.index(field))
				names.pop(names.index(field))
			except ValueError:
				raise StructureError("%r is not a valid column to delete" % (field))

	def rename_field(self, before, after):
		index = [field.name for field in self].index(before)
		self[index].name = after
