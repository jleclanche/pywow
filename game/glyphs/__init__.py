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
	SKILL_GLYPHS = 810
	
	@classmethod
	def getAllSpells(cls):
		from ..skills import Skill, SkillProxy
		Skill.initProxy(SkillProxy)
		return Skill(cls.SKILL_GLYPHS).getSpells()
	
	@classmethod
	def getAllForClass(cls, chrClass):
		spells = cls.getAllSpells()
		ret = []
		for spell in spells:
			glyph = spell.getGlyphLearned()
			if glyph and glyph.getSpell().getGlyphInfo() == chrClass:
				ret.append(spell)
		return ret
	
	def getTypeText(self):
		return {
			self.MINOR: MINOR_GLYPH,
			self.MAJOR: MAJOR_GLYPH,
			self.PRIME: PRIME_GLYPH,
		}.get(self.getType(), "")

class GlyphTooltip(Tooltip):
	def tooltip(self):
		
		self.append("name", self.obj.getName())
		self.append("type", self.obj.getTypeText())
		self.append("description", self.obj.getDescription(), YELLOW)
		
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
		return self.spell.getDescription()
	
	def getName(self, row):
		return self.spell.name_enus
	
	def getSpell(self, row):
		return self.spell
	
	def getSpellIcon(self, row):
		return self.spell.getIcon()
	
	def getType(self, row):
		return row.type
