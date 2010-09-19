# -*- coding: utf-8 -*-

import os
from .utils import getfilename, fopen

DEFAULT_CACHE_DIR = "/var/www/sigrie/caches/"

class BaseLookup(list):
	"""
	List class that will standardize the name
	and return a list of matches on getitem.
	"""
	
	def __contains__(self, item):
		return getfilename(item) in [getfilename(k) for k in self]
	
	def __getitem__(self, item):
		item = item.lower()
		ret = set()
		for key in self:
			if getfilename(key) == getfilename(item):
				ret.add(key)
		return ret

class Environment(object):
	def __init__(self, build, locale="enGB", base=DEFAULT_CACHE_DIR):
		self.build = build
		self.path = "%s/%i/%s/" % (base, build, locale)
		if not os.path.exists(self.path):
			raise ValueError("%r: No such file or directory" % (self.path))
		
		self.__cache = {}
		self.files = BaseLookup(os.listdir(self.path))
	
	def __contains__(self, item):
		return getfilename(item) in self.files
	
	def __getitem__(self, item):
		item = getfilename(item)
		if item not in self.__cache:
			self.__cache[item] = self.__open(self.files[item])
		return self.__cache[item]
	
	def __iter__(self):
		return self.files.__iter__()
	
	def __len__(self):
		return self.files.__len__()
	
	def __open(self, files):
		files = list(files)
		if not files:
			raise KeyError()
		
		if len(files) == 1:
			return fopen(self.path + files[0], build=self.build, environment=self)
		
		if len(files) == 2:
			db2, adb = sorted(files, key=lambda x: x.endswith(".adb")) # sort the db2 file first, the adb file after
			assert db2.endswith(".db2")
			db2 = fopen(self.path + db2, build=self.build, environment=self)
			
			assert adb.endswith(".adb")
			adb = fopen(self.path + adb, build=self.build, environment=self)
			
			db2.update(adb) # Merge the two files
			return db2
		
		raise TypeError(files)

def get_latest_build():
	return sorted([k.isdigit() and int(k) or 0 for k in os.listdir(DEFAULT_CACHE_DIR)])[-1]
