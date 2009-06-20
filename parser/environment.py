#!/usr/bin/python
# -*- coding: utf-8 -*-

import wdbc

class Environment(dict):
	def __init__(self, path, files, build):
		for f in files:
			self[wdbc.getfilename(f)] = wdbc.fopen(path+f, build=build, environment=self)
