# -*- coding: utf-8 -*-

from pywow.structures import Skeleton, Structure
from pywow.structures.fields import UnknownField


class GeneratedStructure(Structure):
	"""Dynamically generated DBC structure."""
	def __init__(self, structure_string, *pargs, **kwargs):
		columns = []
		self.fields = Skeleton(*[UnknownField() for s in structure_string])
		Structure.__init__(self)
