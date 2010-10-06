# -*- coding: utf-8 -*-
"""
Glyphs
 - GlyphProperties.dbc
"""

from .. import *
from ..globalstrings import *


class Glyph(Model):
	MAJOR = 0
	MINOR = 1
	PRIME = 2
	
	def getTypeText(self):
		return {
			self.MINOR: MINOR_GLYPH,
			self.MAJOR: MAJOR_GLYPH,
			self.PRIME: PRIME_GLYPH,
		}.get(self.obj.type, "")

class GlyphTooltip(Tooltip):
	def __init__(self, obj, renderer=None):
		self.obj = obj
		self.renderer = renderer
		self.keys = []
		self.values = []
	
	def render(self):
		
		self.append("name", self.obj.getName())
		self.append("type", self.obj.getTypeText())
		self.append("description", self.obj.getDescription())
		
		ret = self.values
		self.values = []
		return ret

class GlyphProxy(object):
	"""
	WDBC proxy for glyphs
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("GlyphProperties.dbc", build=-1)
	
	def get(self, id):
		from ..spells import Spell, SpellProxy
		Spell.initProxy(SpellProxy)
		row = self.__file[id]
		self.spell = Spell(row._raw("spell"))
		return row
	
	def getDescription(self, row):
		return "blah"
		return self.spell.getDescription()
	
	def getName(self, row):
		return self.spell.name_enus
	
	def getSpellIcon(self, row):
		return self.spell.getIcon()
