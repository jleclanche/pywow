"""
Bitflags logic
"""

class BitMask(object):
	"""
	Base BitMask class
	"""

	def __init__(self, value, flags={}):
		self._values = dict(zip(flags.keys(), flags.values()))
		if isinstance(value, dict):
			value = sum(self._values.keys())
		elif not isinstance(value, int):
			from ..structures import StructureError
			raise StructureError("BitMask value must be an int or a dict (got %r instead)" % (type(value)))
		self._bitmask = value
		self._flags = flags

	def __repr__(self):
		return '<%s: 0x%X>' % (self.__class__.__name__, self._bitmask)

	def __getitem__(self, key):
		assert isinstance(key, int) and key >= 0, "key must be a positive integer"
		return self._bitmask & key == key

	def __setitem__(self, key, value):
		assert isinstance(key, int) and key >= 0, "key must be a positive integer"
		bit = 1 << key-1

	def __int__(self):
		return self._bitmask

	def __and__(self, other):
		return self._bitmask.__and__(other)

	def __xor__(self, other):
		return self._bitmask.__xor__(other)

	def __or__(self, other):
		return self._bitmask.__or__(other)

	def __nonzero__(self):
		return self._bitmask.__nonzero__()

	def _get_values(self):
		ret = []
		for k, v in self._flags.items():
			if self[k]:
				ret.append(v)
		return ret


class BitFlags(BitMask):
	"""
	v = BitFlags(5, {0x1: "race", 0x2: "sex", 0x4: "alive"}) #  v.race is True, v.sex is False, v.alive is True
	v = BitFlags(5) # v[0] is True, v[1] is False, v[2] is True
	"""

	def __init__(self, value, flags={}):
		self._values = dict(zip(flags.values(), flags.keys()))
		if isinstance(value, dict):
			value = sum(self._values[k] for k in value)
		if not isinstance(value, int):
			from ..structures import StructureError
			raise StructureError("BitFlags value must be an int or a dict (got %r instead)" % (type(value)))
		self._bitmask = value
		self._flags = flags

	def __getattr__(self, name):
		values = object.__getattribute__(self, "_values")
		if name in values:
			return self[values[name]]
		return object.__getattribute__(self, name)

	def __setattr__(self, name, value):
		if name != "_values" and name in self._values.keys():
			self[self._values[name]] = value
		super(BitFlags, self).__setattr__(name, value)

	def __dir__(self):
		result = self.__dict__.keys()
		result.extend(self._values.keys())
		return result


	def dict(self):
		"""
		Convert the BitFlags to a dict
		"""
		return dict((k, getattr(self, k)) for k in self._flags)
