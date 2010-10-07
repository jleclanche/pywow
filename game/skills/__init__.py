# -*- coding: utf-8 -*-
"""
Skills
 - SkillLine.dbc
 - SkillLineAbility.dbc (spell lookups)
"""

from .. import *
from ..globalstrings import *


class Skill(Model):
	@classmethod
	def getTypeText(self):
		return {
			self.MINOR: MINOR_GLYPH,
			self.MAJOR: MAJOR_GLYPH,
			self.PRIME: PRIME_GLYPH,
		}.get(self.obj.type, "")


class SkillProxy(object):
	"""
	WDBC proxy for skills
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("SkillLine.dbc", build=-1)
		self.spells = wdbc.get("SkillLineAbility.dbc", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getSpells(self, row):
		from ..spells import Spell, SpellProxy
		Spell.initProxy(SpellProxy)
		lookups = row.skilllineability__skill
		return [Spell(k._raw("spell")) for k in lookups]
