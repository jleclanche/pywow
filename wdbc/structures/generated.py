# -*- coding: utf-8 -*-

from ..structures import Skeleton, Structure, UnknownField


class GeneratedStructure(Structure):
	"""Dynamically generated DBC structure."""
	def __init__(self, structure_string, *pargs, **kwargs):
		columns = []
		self.fields = Skeleton(*[UnknownField() for s in structure_string])
		Structure.__init__(self)
