# -*- coding: utf-8 -*-

import os
import re
import mpq
from .db2 import DB2File
from .dbc import DBCFile
from .main import DBFile
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

	def _open(self, file):
		from .structures import getstructure
		handle = self.mpq.open(file)
		name = getfilename(file)
		structure = getstructure(name)
		if name in ("item", "item-sparse"):
			cls = DB2File
		else:
			cls = DBCFile
		return cls.open(handle, build=self.build, structure=structure, environment=self)

	@classmethod
	def patchFiles(cls, locale="enUS"):
		files = {}
		base = os.path.join(defaultBase(), "Data")

		# Old-style wow-updates (oldest) first
		sre = re.compile(r"^wow-update-(\d+).MPQ$")
		for f in os.listdir(base):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild = int(match.groups()[0])
				files[fileBuild] = [os.path.join(base, f)]

		# Special cases:
		# wow-update*-13623 has both old-style and new-style patches.
		# The new style ones are corrupt. We'll just assume that if
		# we have both old-style and new-style, old-style takes priority.
		sre = re.compile(r"^wow-update-%s-(\d+).MPQ$" % (locale))
		base = os.path.join(base, locale)
		for f in os.listdir(base):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild = int(match.groups()[0])
				if fileBuild not in files:
					files[fileBuild] = [os.path.join(base, f)]

		return files

	@classmethod
	def highestBuild(cls):
		return sorted(cls.patchFiles().keys())[-1]

	def _dbFileName(self, name):
		# In order to avoid duplicates, we need to standardize the filename
		name = name.lower()
		base, ext = os.path.splitext(name)
		if ext:
			# Check against valid extensions
			if ext not in (".dbc", ".wdb", ".db2", ".dba"):
				raise ValueError("%r is not a known DBFile format" % (ext))
		else:
			# No extension, we need to guess it
			if name.endswith("cache"):
				name += ".wdb"
			else:
				name += ".dbc"

		return name

	def hasDbFile(self, name):
		name = self._dbFileName(name)
		if name in self._cache:
			return True
		return "DBFilesClient/%s" % (name) in self.mpq

	def dbFile(self, name):
		name = self._dbFileName(name)
		if name not in self._cache:
			if name.endswith(".wdb"):
				raise NotImplementedError("Cache files are not supported in environments")
			self._cache[name] = self._open("DBFilesClient/%s" % (name))

		return self._cache[name]

	def patchList(self):
		patches = self.patchFiles()
		builds = sorted(patches.keys())
		ret = []
		for build in builds:
			if build > self.build:
				# We only want the patches that correspond to the environment's build
				break

			for f in patches[build]:
				ret.append(f)

		return ret
