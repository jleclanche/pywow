#!/usr/bin/python
# -*- coding: utf-8 -*-
"""A simple bitmask class."""

from bitarray import bitarray

try:
	bin
except NameError:
	_bin = lambda n: n>0 and (_bin(n>>1).lstrip('0')+str(n&1)) or "0"
	bin = lambda n: "0b%s" % _bin(n)


class BitMask(object):
	def __init__(self, value):
		value = value >= 0 and value or 0
		value = bin(value)[2:]
		self.array = bitarray(32)
		self.array.setall(False)
		self.array[-len(value):] = bitarray(value)
		self.array = self.array[::-1]
	
	def __int__(self):
		return int(self.array.to01(), 2)
	
	def __repr__(self):
		return self.array.__repr__()
	
	def __setitem__(self, key, value):
		self.array[key] = bool(value)
	
	def expand(self, flags):
		return dict(zip(flags, self.array))
	
	def expand_list(self, flags):
		return [flags[i] for i, k in enumerate(self.array) if k]
	
	def explode(self):
		return [2**i for i, k in enumerate(self.array) if k]
	
	def implode(self):
		return [i for i, k in enumerate(self.array) if k]
