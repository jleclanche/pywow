# -*- coding: utf-8 -*-

from __future__ import division

from cStringIO import StringIO
from datetime import timedelta
from math import ceil, floor


SEEK_CUR = 1 # os.SEEK_CUR

BOOLEANS = ("G", "g", "l")

PAPERDOLL_VALUES = {
	"ap":   "ATTACK_POWER",
	"ar":   "ARMOR",
	"bh":   "BONUS_HEALING",
	"hnd":  "MAIN_WPN_HANDS",
	"int":  "INTELLECT",
	"mw":   "MAIN_WPN_DMG",
	"mwb":  "MAIN_WPN_BASEDMG",
	"mws":  "MAIN_WPN_SPEED",
	"pa":   "PERCENT_ARCANE",
	"pfi":  "PERCENT_FIRE",
	"pfr":  "PERCENT_FROST",
	"ph":   "PERCENT_HOLY",
	"pn":   "PERCENT_NATURE",
	"ps":   "PERCENT_SHADOW",
	"pbh":  "PERCENT_BONUS_HEALING",
	"pbhd": "PERCENT_BONUS_HEALING_DAMAGE",
	"pl":   "PLAYER_LVL",
	"rap":  "RANGED_ATTACK_POWER",
	"rwb":  "RANGED_WPN_BASEDMG",
	"sp":   "SPELL_POWER",
	"spa":  "SPELL_POWER_ARCANE",
	"spfi": "SPELL_POWER_FIRE",
	"spfr": "SPELL_POWER_FROST",
	"sph":  "SPELL_POWER_HOLY",
	"spi":  "SPIRIT",
	"spn":  "SPELL_POWER_NATURE",
	"sps":  "SPELL_POWER_SHADOW",
}

FUNCTIONS = ["ceil", "cond", "eq", "floor", "gte", "gt", "lte", "max", "min"]

class VariableNotFound(Exception):
	"""
	Raised when a description variable
	does not exist.
	"""
	pass

class Range(object):
	def __init__(self, min, max):
		self.min = abs(min)
		self.max = abs(max)
	
	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.min, self.max)
	
	def __str__(self):
		if self.max > self.min:
			return "%i to %i" % (self.min, self.max)
		return str(int(self.max))
	
	def __cmp__(self, other):
		return self.max - other
	
	def __mul__(self, value):
		return Range(self.min * value, self.max * value)
	
	def __div__(self, value):
		return Range(self.min / value, self.max / value)
	
	def __truediv__(self, value):
		return self.__div__(value)


class Condition(object):
	"""
	Condition for a spell conditional block
	These conditions can be evaluated against
	a paperdoll with the evaluate method.
	Examples:
		s25306
		!a66109
		(s25306|!((!a48165)|a66109))
		(s56810 |s25306|!((!a48165)|a66109))
	FIXME For now, evaluate only supports
	simple condition formats, such as "s12345"
	"""
	def __init__(self, condition):
		self.condition = condition.strip()
	
	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.condition)
	
	def is_else(self):
		# Check if the condition is "empty"
		# Such a case is reserved for else clauses
		return not self.condition.startswith("?")
	
	def evaluate(self, paperdoll):
		self.identifiers = []
		if self.is_else():
			return True
		
		cond = self.condition[1:]
		
		if not (cond.startswith("a") or cond.startswith("s")):
			return False
		
		char, id = cond[0], cond[1:]
		if not id.isdigit():
			return False
		
		self.identifiers.append(cond)
		d = paperdoll.get(char) or {}
		if int(id) in d:
			return True
		
		return False


class StringLookup(object):
	"""
	Lookup class for the parser
	StringLookup will never do any parsing, but
	only return proper formats for given values.
	"""
	def __init__(self, spell, proxy, braced=False):
		self.spell = spell
		self.last_value = 0
		self.braced = braced # Whether or not we are inside braces
		self.proxy = proxy
	
	def get_value(self, spell, value):
		return self.proxy.get_value(self, spell, value)
	
	def get_effect(self, spell, effect, ordering):
		return self.proxy.get_effect(self, spell, effect, ordering)
	
	def get_spell(self, id):
		return self.proxy.get_spell(self, id)
	
	def __macro_M(self, spell, identifier, effect):
		value = self.get_effect(spell, "damage_base", effect)
		sides = self.get_effect(spell, "die_sides", effect)
		dice = 1
		return value + (sides * dice)
	
	def __macro_m(self, spell, identifier, effect):
		value = self.get_effect(spell, "damage_base", effect)
		sides = self.get_effect(spell, "die_sides", effect)
		return value + min(sides, 1)
	
	def __macro_s(self, spell, identifier, effect):
		min = self.__macro_m(spell, identifier, effect)
		max = self.__macro_M(spell, identifier, effect)
		return Range(min, max)
	
	def __macro_t(self, spell, identifier, effect):
		return self.get_effect(spell, "aura_interval", effect) / 1000
	
	
	def format_boolean(self, identifier, values):
		if identifier.lower() == "g":
			return "<%s/%s>" % (values)
		
		if identifier == "l":
			x = self.last_value
			if self.last_value > 1:
				return values[1]
			return values[0]
	
	def format_duration(self, duration):
		# TODO make this prettier, remove the braced conds
		if not isinstance(duration, timedelta):
			duration = timedelta(microseconds=duration)
		
		if duration <= timedelta(milliseconds=0):
			if self.braced:
				return "0"
			return "until cancelled"
		
		if duration < timedelta(minutes=1):
			if self.braced:
				return str(duration.seconds)
			return "%d sec" % (duration.seconds)
		
		if duration < timedelta(hours=1):
			if self.braced:
				return str(duration.seconds / 60)
			return "%d min" % (duration.seconds / 60)
		
		if duration == timedelta(hours=1):
			if self.braced:
				return str(duration.seconds / 3600)
			return "%d hour" % (duration.seconds / 3600)
		
		if duration < timedelta(days=1):
			if self.braced:
				return str(duration.seconds / 3600)
			return "%d hrs" % (duration.seconds / 3600)
		
		if self.braced:
			return str(duration.days)
		return "%d days" % (duration.days)
	
	def format_function(self, identifier, args):
		if identifier == "lte":
			return "()"
		return "%s(%s)" % (identifier, args)
	
	def format_macro(self, spell, identifier, effect):
		spell = self.get_spell(spell)
		effect = int(effect)
		if not spell:
			return "$" + identifier + str(effect)
		
		if identifier == "A":
			value = self.get_effect(spell, "radius_max", effect)
			if not value: # FIXME is this right?
				value = self.get_effect(spell, "radius_min", effect)
			return int(value)
		
		if identifier == "a":
			value = self.get_effect(spell, "radius_min", effect)
			return int(value)
		
		if identifier == "bc": # 48165, 69406, 69416
			return self.get_effect(spell, "multiplier", effect)
		
		if identifier == "b":
			value = self.get_effect(spell, "points_combo", effect)
			return int(value)
		
		if identifier == "d":
			value = self.get_value(spell, "duration_1") # FIXME use duration class
			return self.format_duration(value)
		
		if identifier == "e":
			return self.get_effect(spell, "amplitude", effect)
		
		if identifier == "f" or identifier == "F":
			value = self.get_effect(spell, "chain_amplitude", effect)
			return value
		
		if identifier == "h":
			return self.get_value(spell, "proc_chance")
		
		if identifier == "i":
			return self.get_value(spell, "max_targets")
		
		if identifier == "M":
			return self.__macro_M(spell, identifier, effect)
		
		if identifier == "m":
			return self.__macro_m(spell, identifier, effect)
		
		if identifier == "n":
			return self.get_value(spell, "proc_charges")
		
		if identifier == "o":
			duration = self.get_value(spell, "duration_1") / 1000
			tick = self.get_effect(spell, "aura_interval", effect) or 5000
			damage = self.__macro_s(spell, identifier, effect)
			return damage * int(duration / tick)
		
		if identifier == "q":
			return self.get_effect(spell, "misc_value_1", effect)
		
		if identifier == "r":
			return self.get_value(spell, "range_max")
		
		if identifier == "s" or identifier == "S":
			return self.__macro_s(spell, identifier, effect)
		
		if identifier == "t":
			value = self.__macro_t(spell, identifier, effect)
			if not value.is_integer():
				return "%.2f" % (value)
			return int(value)
		
		if identifier == "u":
			return self.get_value(spell, "stack")
		
		if identifier == "v":
			return self.get_value(spell, "max_target_level")
		
		if identifier == "x":
			return self.get_effect(spell, "chain_targets", effect)
		
		if identifier == "z":
			return "<Home>"
	
	
	def format_paperdoll(self, identifier):
		return identifier


class SpellString(str):
	"""
	Parsing class
	We pass all sorts of formatting and
	lookups to the StringLookup class
	"""
	
	def __init__(self, arg):
		self.conditions = [] # for get_condition_identifiers
		super(SpellString, self).__init__()
	
	def __read_alpha(self, buffer):
		"""
		Parse a chain of alphabetic characters
		"""
		ret = []
		token = buffer.read(1)
		while token.isalpha():
			ret.append(token)
			token = buffer.read(1)
		if token:
			buffer.seek(-1, SEEK_CUR)
		return "".join(ret)
	
	def __read_alphanum(self, buffer):
		ret = []
		token = buffer.read(1)
		
		while token.isalnum():
			ret.append(token)
			token = buffer.read(1)
		
		buffer.seek(-1, SEEK_CUR)
		return "".join(ret)
	
	def __read_block(self, buffer, startchr, endchr):
		"""
		Parse a string from startchr until endchr
		"""
		token = buffer.read(1)
		while token != startchr:
			token = buffer.read(1)
			if not token:
				raise ValueError("read_block could not find beginning of block")
		
		ret = []
		count = 1
		while count:
			token = buffer.read(1)
			if token == startchr:
				count += 1
			elif token == endchr:
				count -= 1
			if count:
				ret.append(token)
			if not token:
				break
		
		return "".join(ret)
	
	def __read_number(self, buffer):
		"""
		Parse a chain of numeric characters
		and build a number with them
		"""
		ret = []
		token = buffer.read(1)
		while token.isdigit():
			ret.append(token)
			token = buffer.read(1)
		buffer.seek(-1, SEEK_CUR)
		return int("".join(ret) or 0)
	
	def __read_until(self, buffer, char, break_space=False):
		"""
		Helper to parse until a specific character
		"""
		ret = []
		token = buffer.read(1)
		while token != char:
			if break_space and token.isspace():
				return
			ret.append(token)
			token = buffer.read(1)
			if not token:
				break
		return "".join(ret)
	
	
	def __parse_boolean(self, buffer):
		"""
		Parse the immediately available
		boolean from the buffer and
		return both values.
		Example:
		Summon $s $lan ally:many allies;...
		The $gsorcerer:sorceress; casts...
		"""
		val1 = self.__read_until(buffer, ":")
		val2 = self.__read_until(buffer, ";")
		
		return val1, val2
	
	
	def __parse_conditional(self, buffer):
		"""
		Parse the immediately available conditional block
		"""
		ret = []
		
		while True:
			condition = Condition(self.__read_until(buffer, "["))
			buffer.seek(-1, SEEK_CUR)
			value = self.__read_block(buffer, startchr="[", endchr="]")
			value = SpellString(value).format(self.obj, proxy=self.proxy)
			ret.append((condition, value))
			if condition.is_else():
				break
		
		return ret
	
	
	def __parse_function_args(self, buffer):
		"""
		Parse the immediately available
		block of function arguments,
		returning a tuple of the arguments.
		"""
	
	def __parse_macro(self, buffer):
		"""
		Parse the immediately available
		macro or variable and return
		the spell, identifier and effect
		"""
		
		# Parse an optional id
		spell = self.__read_number(buffer)
		
		##
		# FIXME technically, the effects do not exist, as
		# WoW parses the identifier alphanumerically
		# Do we really want that? It's easier to go back.
		
		# Parse an alphabetic identifier
		identifier = self.__read_alpha(buffer)
		
		# effect id should be the next char
		effect = buffer.read(1)
		
		# However it's optional. If it's not here
		# we have to go back one char.
		if effect and effect not in ("1", "2", "3"):
			buffer.seek(-1, SEEK_CUR)
			effect = ""
		
		return spell, identifier, effect
	
	
	def __parse_operator(self, buffer):
		num = self.__read_until(buffer, ";", break_space=True)
		try:
			num = float(num)
		except TypeError:
			return None, None
		
		spell, identifier, effect = self.__parse_macro(buffer)
		if not effect: # XXX should this be done in format_macro?
			effect = "1"
		var = self.formatter.format_macro(spell, identifier, effect)
		
		return num, var
	
	
	def __parse_next(self, buffer):
		"""
		Parse the immediately available
		variable from the buffer and
		return the formatted result.
		"""
		token = buffer.read(1)
		
		_tell = buffer.tell()
		# Is it an operator?
		if token == "/":
			num, var = self.__parse_operator(buffer)
			if num is None:
				buffer.seek(_tell - 1)
				return "$"
			
			if isinstance(var, str):
				return var
			
			ret = (var / num)
			if isinstance(ret, Range):
				ret = ret.min # XXX is this right?
			if int(ret) != ret:
				return "%.1f" % ret
			return str(int(ret))
		
		if token == "*":
			num, var = self.__parse_operator(buffer)
			ret = var * num
			if isinstance(ret, float):
				ret = int(round(ret))
			return str(ret)
		
		# Is it a conditional?
		if token == "?":
			buffer.seek(-1, SEEK_CUR)
			blocks = self.__parse_conditional(buffer)
			
			# Prepare the condition cache
			# This shouldn't be done here, but anyway...
			for condition, value in blocks:
				condition.evaluate({})
				self.conditions.extend(condition.identifiers)
			
			# blocks is a list of (condition, value) tuples
			# We evaluate the paperdoll against each of them
			# and return when we get a hit
			
			for condition, value in blocks:
				if condition.evaluate(self.paperdoll):
					return value
			
			return
		
		if token == "<":
			buffer.seek(-1, SEEK_CUR)
			identifier = self.__read_block(buffer, startchr="<", endchr=">")
			try:
				value = self.get_variable(identifier)
				return SpellString(value).format(self.obj, proxy=self.proxy)
			except VariableNotFound:
				return "<%s>" % (identifier)
		
		if token == "{":
			buffer.seek(-1, SEEK_CUR)
			block = self.__read_block(buffer, startchr="{", endchr="}")
			
			# Attempt to read decimals formatting
			decimals = 0
			token = buffer.read(1)
			if token == ".":
				decimals = self.__read_number(buffer)
			elif token:
				# Step one char back, only if we are not at the end
				buffer.seek(-1, SEEK_CUR)
			
			block = SpellString(block).format(self.obj, proxy=self.proxy, braced=True)
			try: # FIXME
				block = eval(block)
				if decimals:
					block = round(block, decimals)
				return "%g" % (block)
			except Exception:
				return "[%s]" % (block)
		
		# At this point, we need to check for functions and variables
		# but only if we don't already have a digit
		if not token.isdigit():
			_tell = buffer.tell()
			buffer.seek(-1, SEEK_CUR)
			identifier = self.__read_alpha(buffer)
			
			if identifier in FUNCTIONS:
				args = self.__parse_function_args(buffer)
				return self.formatter.format_function(identifier, args)
			
			if identifier.lower() in PAPERDOLL_VALUES:
				return self.formatter.format_paperdoll(identifier)
			
			
			# We didn't find any valid identifier
			if not identifier:
				return "$"
			
			# Nothing left to check for but booleans
			# The values get messed with the identifier however, so we need to
			# look at only the first char
			if identifier[0] in BOOLEANS:
				identifier = identifier[0]
				buffer.seek(_tell)
				values = self.__parse_boolean(buffer)
				return self.formatter.format_boolean(token, values)
		
		# It's probably a variable then
		buffer.seek(-1, SEEK_CUR)
		spell, identifier, effect = self.__parse_macro(buffer)
		
		if identifier:
			spell = int(spell or 0)
			effect = int(effect or 1)
			
			value = self.formatter.format_macro(spell, identifier, effect)
			self.formatter.last_value = value
			return str(value)
		
		
		if not token or token.isspace():
			return token
		
		return token
	
	def get_variable(self, identifier):
		"""
		Queries the cache for a description variable
		or builds the cache if there isn't one yet.
		"""
		if not hasattr(self, "__sdvcache"):
			self.__sdvcache = {}
			buffer = str(self.obj.description_variables.variables)
			buffer = StringIO(buffer)
			token = buffer.read(1)
			while token:
				if token == "$":
					variable = self.__read_until(buffer, "=")
					value = self.__read_until(buffer, "\n").strip()
					self.__sdvcache[variable] = value
				token = buffer.read(1)
		
		if identifier not in self.__sdvcache:
			raise VariableNotFound(identifier)
		
		return self.__sdvcache[identifier]
	
	def get_condition_identifiers(self):
		"""
		Return all identifiers from every
		Condition in the SpellString.
		"""
		return set(self.conditions)
	
	def format(self, obj, proxy, braced=False, paperdoll={}):
		if "$" not in self:
			return self
		self.obj = obj
		self.proxy = proxy
		self.paperdoll = paperdoll
		self.formatter = StringLookup(obj, proxy=proxy, braced=braced)
		buffer = StringIO(self)
		ret = []
		
		while True:
			token = buffer.read(1)
			if not token: # string is over
				break
			
			if token == "$":
				ret.append(self.__parse_next(buffer))
			else:
				ret.append(token)
		
		return "".join(ret)


class WDBCProxy(object):
	"""
	Default proxy for wdbc-like structure
	"""
	
	value_lookup_old = {
		"radius_min": "radius__radius_min"
	}
	
	@classmethod
	def get_value_old(self, instance, spell, value):
		if value == "duration_1":
			duration = spell.duration
			if not duration:
				return 0
			return duration._raw("duration_1") * 1000
		
		if value in self.value_lookup_old:
			value = self.value_lookup_old[value]
		
		try:
			return getattr(spell, value)
		except AttributeError, e:
			return 0
	
	effect_lookup_old = {
		"radius_min_effect_%i": "radius_effect_%i__radius_min",
	}
	
	@classmethod
	def get_effect_old(self, instance, spell, effect, ordering):
		field = "%s_effect_%%i" % (effect)
		if field in self.effect_lookup_old:
			field = self.effect_lookup_old[field]
		field = field % (ordering)
		try:
			return getattr(spell, field)
		except AttributeError, e:
			return 0
	
	
	value_lookup = {
		"proc_chance": "aura_options__proc_chance",
		"proc_charges": "aura_options__proc_charges",
		"radius_min": "radius__radius_min",
		"max_target_level": "target_restrictions__max_target_level",
		"max_targets": "target_restrictions__max_targets",
	}
	
	@classmethod
	def get_value(self, instance, spell, value):
		if value == "duration_1":
			duration = spell.duration
			if not duration:
				return 0
			return duration._raw("duration_1") * 1000
		
		if value in self.value_lookup:
			value = self.value_lookup[value]
		
		try:
			return getattr(spell, value)
		except AttributeError, e:
			return 0
	
	@classmethod
	def get_effect(self, instance, spell, effect, ordering):
		if spell._parent.build < 12232:
			return self.get_effect_old(instance, spell, effect, ordering)
		
		effects = spell.spelleffect__spell
		effects = [k for k in effects if k.ordering+1 == ordering] or effects
		row = effects[0]
		ret = getattr(row, effect)
		return ret if ret != None else 0
	
	@classmethod
	def get_spell(self, instance, id):
		spell_id = instance.spell._id
		id = id or spell_id
		if id == spell_id:
			return instance.spell
		try:
			return instance.spell._parent[id]
		except KeyError:
			return None
