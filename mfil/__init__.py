# -*- coding: utf-8 -*-
"""
MFIL - Blizzard Manifest File
Used for Blizzard Installer

Version 1:
 - Simple dictionary
 - Simple list

Version 2:
 - Dictionary
 - Nested keys
"""

SEEK_CUR = 1

class MFILError(Exception):
	"""
	Generic MFIL exception
	"""
	pass

class MFIL(dict):
	"""
	Dictionary class for Blizzard Manifest Files
	"""
	
	def __init__(self, file):
		file.seek(0)
		self.file = file
		key, value = self.parseKey(), self.parseValue()
		if key == "version":
			self.version = value
		else:
			raise MFILError("Unknown MFIL version")
		
		self.parse()
	
	def parseKey(self):
		ret = []
		while True:
			c = self.file.read(1)
			
			if not c or c == "=":
				break
			
			ret.append(c)
		return "".join(ret)
	
	def parseValue(self):
		ret = []
		while True:
			c = self.file.read(1)
			
			if not c or c == "\n":
				break
			
			if c == "\r":
				if self.file.read(1) == "\n":
					break
				else:
					self.file.seek(-1, SEEK_CUR)
			
			ret.append(c)
		return "".join(ret)

class MFIL2(MFIL):
	"""
	MFIL version 2
	Keys that start with a tab are child keys of the others
	The class should look like MFIL({
		parentKey: {
			parentValue: {
				key: value,
				key2, value2,
			}, ...
		}, ...
	})
	"""
	
	def parse(self):
		while True:
			key, value = self.parseKey(), self.parseValue()
			
			if not key:
				break
			
			if key == "version":
				self.version = value
			
			elif key.startswith("\t"):
				key = key[1:]
				self[k1][k2][key] = value
			
			else:
				if key not in self:
					self[key] = {}
				self[key][value] = {}
				k1, k2 = key, value
