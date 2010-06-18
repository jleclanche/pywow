# -*- coding: utf-8 -*-

from ..structures import Skeleton, Structure, UnknownField, IDField


class GeneratedStructure(Structure):
	"""Dynamically generated DBC structure."""
	def __init__(self, structure_string, *pargs, **kwargs):
		columns = []
		fields = [IDField()] + [UnknownField() for s in structure_string][1:]
		self.fields = Skeleton(*fields)
		Structure.__init__(self)
