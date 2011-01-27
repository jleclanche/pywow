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

class MFIL(dict):
	"""
	Dictionary class for Blizzard Manifest Files
	"""
	
	def __init__(self, file):
		file.seek(0)
		self.file = file
		while True:
			key, value = self.parseKey(), self.parseValue()
			
			if not key:
				break
			
			if key == "version":
				self.version = value
			
			elif key.startswith("\t"):
				key = key[1:]
				self[k1][k2][key] = value
				#{transport: {default: {k:v, k:v}}}
			
			else:
				if key not in self:
					self[key] = {}
				self[key][value] = {}
				k1, k2 = key, value
	
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
