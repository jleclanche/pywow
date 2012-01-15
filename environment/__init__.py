"""
WoW-style MPQ-based environments
"""
import os
import re
import mpq


class BuildNotFound(Exception):
	pass

class Base(object):
	def __init__(self, rawPath, build=None):
		self.rawPath = rawPath
		if build is not None:
			self.setBuild(build)

	def __repr__(self):
		if hasattr(self, "_path"):
			return "Base(%r)" % (self.path())
		return "Base(%r)" % (self.rawPath)

	def build(self):
		return int(re.match(r"^(\d+).direct$", os.path.basename(self.path())).groups()[0])

	def builds(self):
		"""
		Returns a dict of base paths for build numbers in {build: path} format
		"""
		sre = re.compile(r"^(\d+).direct$")
		ret = {}
		for f in os.listdir(self.rawPath):
			# Here we parse each <build>.direct/
			match = sre.match(os.path.basename(f))
			if match:
				ret[int(match.groups()[0])] = f

		return ret

	def dataDir(self):
		return os.path.join(self.path(), "Data")

	def localeDir(self, locale):
		return os.path.join(self.dataDir(), locale)

	def path(self):
		if not hasattr(self, "_path"):
			raise RuntimeError("Cannot access Base.path() if Base does not have a build")

		return os.path.join(self.rawPath, self._path)

	def patchFiles(self, locale="enUS"):
		"""
		Returns a dict of build: patch MPQs.
		"""
		files = {}

		# Old-style wow-updates (oldest) first
		path = self.dataDir()
		sre = re.compile(r"^wow-update-(\d+).MPQ$")
		for f in os.listdir(path):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild = int(match.groups()[0])
				files[fileBuild] = [os.path.join(path, f)]

		# Special cases:
		# wow-update*-13623 has both old-style and new-style patches.
		# The new style ones are corrupt. We'll just assume that if
		# we have both old-style and new-style, old-style takes priority.
		path = self.localeDir(locale)
		sre = re.compile(r"^wow-update-%s-(\d+).MPQ$" % (locale))
		for f in os.listdir(path):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild = int(match.groups()[0])
				if fileBuild not in files:
					files[fileBuild] = [os.path.join(path, f)]

		return files

	def setBuild(self, build):
		highestMatch = 0
		bases = self.builds()
		for baseBuild in bases:
			# We want the highest possible match:
			# - filter out anything higher than the requested build
			# - filter out anything lower than our highest match
			if baseBuild <= build and baseBuild > highestMatch:
				highestMatch = baseBuild

		if not highestMatch:
			raise BuildNotFound(build)

		self._path = bases[highestMatch]


def defaultBase():
	# Try $MPQ_BASE_DIR, otherwise use ~/mpq/WoW
	return Base(os.environ.get("MPQ_BASE_DIR", os.path.join(os.path.expanduser("~"), "mpq", "WoW")))

def highestBase():
	base = defaultBase()
	bases = base.builds()
	base.setBuild(sorted(bases.keys())[-1])
	return base

def highestBuild():
	return sorted(highestBase().patchFiles().keys())[-1]

class Environment(object):
	def __init__(self, build, locale="enUS", base=defaultBase()):
		base.setBuild(build)
		self.base = base
		self.build = build
		self.locale = locale
		self.path = os.path.join(self.base.localeDir(locale), "locale-%s.MPQ" % (locale))

		self.mpq = mpq.MPQFile(self.path)
		if build != base.build():
			for patch in self.patchList():
				self.mpq.patch(patch)

		self._cache = {}

	def __repr__(self):
		return "Environment(build=%r, locale=%r, base=%r)" % (self.build, self.locale, self.base)

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
			if name in ("item", "item-sparse"):
				name += ".db2"
			elif name.endswith("cache"):
				name += ".wdb"
			else:
				name += ".dbc"

		return name

	def _dbFileOpen(self, file):
		from ..wdbc.db2 import DB2File
		from ..wdbc.dbc import DBCFile
		from ..wdbc.structures import getstructure
		from ..wdbc.utils import getfilename
		handle = self.open(file)
		name = getfilename(file)
		structure = getstructure(name)
		if name in ("item", "item-sparse"):
			cls = DB2File
		else:
			cls = DBCFile
		return cls.open(handle, build=self.build, structure=structure, environment=self)

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
			self._cache[name] = self._dbFileOpen("DBFilesClient/%s" % (name))

		return self._cache[name]

	def open(self, file):
		return self.mpq.open(file)

	def patchList(self):
		patches = self.base.patchFiles()
		builds = sorted(patches.keys())
		ret = []

		# Raise BuildNotFound if we can't patch up to the desired build
		# We should raise it in __init__ instead, but it would involve duplicate code
		if self.build not in builds:
			raise BuildNotFound(self.build)

		for build in builds:
			if build > self.build:
				# We only want the patches that correspond to the environment's build
				break

			for f in patches[build]:
				ret.append(f)

		return ret
