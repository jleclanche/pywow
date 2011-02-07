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
 - Multiple identical keys
"""

SEEK_CUR = 1

class MFILError(Exception):
	"""
	Generic MFIL exception
	"""
	pass

class MFIL(object):
	"""
	Dictionary class for Blizzard Manifest Files
	"""
	
	def __init__(self, file):
		if isinstance(file, str):
			file = open(file, "r")
		self.file = file
		key, value = self.parseKey(), self.parseValue()
		if key == "version":
			self.version = value
		else:
			raise MFILError("Unknown MFIL version")
		
		self.parse()
		file.close()
	
	def parseKey(self):
		ret = []
		self.nextLine = self.file.readline()
		for c in self.nextLine:
			if c == "=":
				self.nextLine = self.nextLine[len(ret)+1:]
				break
			
			elif c == "\r" or c == "\n":
				self.nextLine = ""
				break
			
			ret.append(c)
		return "".join(ret)
	
	def parseValue(self):
		ret = []
		for c in self.nextLine:
			if c == "\r" or c == "\n":
				break
			
			ret.append(c)
		return "".join(ret)

class MFIL1(MFIL, list):
	"""
	MFIL version 1
	Key/value pairs, followed by a list of values
	(usually a file manifest)
	The class should look like MFIL([
		{key: value, ...},
		value2
		value3,
		...
	])
	"""
	
	def parse(self):
		self.append({})
		while True:
			key, value = self.parseKey(), self.parseValue()
			
			if not key:
				break
			
			elif not value:
				self.append(key)
			
			else:
				self[0][key] = value

class MFIL2(MFIL, dict):
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
			
			elif key.startswith("\t"):
				key = key[1:]
				if key in self[k1][k2]:
					if not isinstance(self[k1][k2][key], list):
						self[k1][k2][key] = [self[k1][k2][key]]
					self[k1][k2][key].append(value)
				else:
					self[k1][k2][key] = value
			
			else:
				if key not in self:
					self[key] = {}
				self[key][value] = {}
				k1, k2 = key, value
