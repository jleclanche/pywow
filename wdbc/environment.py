# -*- coding: utf-8 -*-

import os
import re
import mpq
from .dbc import DBCFile
from .utils import getfilename, fopen


def defaultBase():
	# Try $MPQ_BASE_DIR, otherwise use ~/mpq/WoW/12911.direct/Data
	return os.environ.get("MPQ_BASE_DIR", os.path.join(os.path.expanduser("~"), "mpq", "WoW", "12911.direct"))


def readBuild(base):
	with open(os.path.join(base, "build"), "rb") as f:
		build = f.read().strip()
	return int(build)

class Environment(object):
	def __init__(self, build, locale="enUS", base=defaultBase()):
		baseBuild = readBuild(base)
		self.base = os.path.join(base, "Data")
		self.build = build
		self.locale = locale
		self.path = os.path.join(self.base, locale, "locale-%s.MPQ" % (locale))

		self.mpq = mpq.MPQFile(self.path)
		if build != readBuild(base):
			for patch in self.patchList():
				self.mpq.patch(patch)

		self._cache = {}

	def __contains__(self, item):
		return getfilename(item) in self.files

	def __getitem__(self, item):
		return self.dbFile(item)

	def _open(self, file):
		from .structures import getstructure
		handle = self.mpq.open(file)
		structure = getstructure(getfilename(file))
		return DBCFile(handle, build=self.build, structure=structure, environment=self)

	@classmethod
	def highestBuild(cls):
		build = 0
		base = os.path.join(defaultBase(), "Data")
		sre = re.compile(r"^wow-update-(\d+).MPQ$")
		for f in os.listdir(base):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild, = match.groups()
				fileBuild = int(fileBuild)
				if fileBuild >= build:
					build = fileBuild

		locale = "enUS"
		base = os.path.join(base, locale)
		sre = re.compile(r"^wow-update-%s-(\d+).MPQ$" % (locale))
		for f in os.listdir(base):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild, = match.groups()
				fileBuild = int(fileBuild)
				if fileBuild >= build:
					build = fileBuild

		return build

	def dbFile(self, name):
		if item not in self._cache:
			self._cache[item] = self._open("DBFilesClient/%s" % (item))
		return self._cache[item]

	def patchList(self):
		ret = []
		base = self.base

		# Old-style wow-updates
		sre = re.compile(r"^wow-update-(\d+).MPQ$")
		for f in os.listdir(base):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild, = match.groups()
				if int(fileBuild) <= self.build:
					ret.append(f)

		sre = re.compile(r"^wow-update-%s-(\d+).MPQ$" % (self.locale))
		base = os.path.join(base, self.locale)
		for f in os.listdir(base):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild, = match.groups()
				if int(fileBuild) <= self.build:
					ret.append(f)

		return ret
