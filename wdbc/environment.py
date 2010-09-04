# -*- coding: utf-8 -*-

import os
from .. import wdbc

stripfilename = wdbc.getfilename

DEFAULT_CACHE_DIR = "/var/www/sigrie/caches/"

class Environment(object):
	def __init__(self, build, locale="enGB", base=DEFAULT_CACHE_DIR):
		self.build = build
		self.path = "%s/%i/%s/" % (base, build, locale)
		if not os.path.exists(self.path):
			raise ValueError(self.path)
		
		self.files = {}
		self.__cache = {}
		processed = []
		for f in os.listdir(self.path):
			_f = f.lower()
			if _f.endswith(".db2") or _f.endswith(".dbc") or _f.endswith(".wdb"):
				if _f.replace(".dbc", ".db2") in processed: # Give .db2 files priority over .dbc ones
					continue
				self.files[stripfilename(f)] = self.path + f
				processed.append(_f)
	
	def __getitem__(self, item):
		item = stripfilename(item)
		if item not in self.__cache:
			self.__cache[item] = wdbc.fopen(self.files[item], build=self.build, environment=self)
		return self.__cache[item]
	
	def __contains__(self, item):
		return stripfilename(item) in self.files
	
	def __iter__(self):
		return self.files.__iter__()
	
	def __len__(self):
		return self.files.__len__()
