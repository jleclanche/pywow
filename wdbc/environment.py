#!/usr/bin/python
# -*- coding: utf-8 -*-

import wdbc
from .log import log

class Environment(dict):
	def __init__(self, path, files, build):
		for f in files:
			try:
				self[wdbc.getfilename(f)] = wdbc.fopen(path+f, build=build, environment=self)
			except IOError:
				log.warning("File %r not found" % (f))
