#!/usr/bin/python
# -*- coding: utf-8 -*-

class BitFlags(object):
	"""
		v = BitFlags(5, ['race', 'sex', 'alive']) #  v.race is True, v.sex is False, v.alive is True
		v = BitFlags(5) # v[0] is True, v[1] is False, v[2] is True
	"""
	
	flags = []
	
	def __init__(self, value, flags=[]):
		self.bitmask = value
		self.flags = flags
	
	def __repr__(self):
		return '<%s: %s>' % (self.__class__.__name__, int(self))
	
	def __getitem__(self, key):
		assert isinstance(key, int) and key >= 0, "key must be positive integer"
		bit = 1
		bit <<= key
		return bool(self.bitmask & bit)
	
	def __setitem__(self, key, value):
		assert isinstance(key, int) and key >= 0, "key must be positive integer"
		bit = 1
		bit <<= key
		if value:
			self.bitmask |= bit
		else:
			self.bitmask &= ~bit
	
	def __getattr__(self, name):
		if name in self.flags:
			return self[self.flags.index(name)]
		raise AttributeError
	
	def __setattr__(self, name, value):
		if name in self.flags:
			self[self.flags.index(name)] = value
		super(BitFlags, self).__setattr__(name, value)
	
	def __int__(self):
		return self.bitmask
	
	# introspection support:
	__members__ = property(lambda self: self.__dir__())

	def __dir__(self):
		result = self.__dict__.keys()
		result.extend(self.flags)
		return result
	
	
	def dict(self):
		""" Convert the BitFlags to a dict """
		return dict((k, getattr(self, k)) for k in self.flags)
