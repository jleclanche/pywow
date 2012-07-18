"""
WoW-style MPQ-based environments
"""
import os
import re
import mpq


class BuildNotFound(Exception):
	pass

class LocaleNotFound(Exception):
	pass

class Base(object):
	"""
	A Base is a helper class that points to a base directory for an environment.
	In its raw state (without a build), the base only has a raw path (Base.rawPath).
	The raw path points to the directory that contains all the possible build bases.

	The base's build can be set with Base.setBuild(build). Once that build is set,
	base.path() will become accessible. That path points to <rawPath>/<build>.

	Base.dataPath() is a helper that points to <path>/Data.
	Base.localePath() is a helper that points to <dataPath>/<locale>.
	"""

	def __init__(self, rawPath, build=None):
		self.rawPath = rawPath
		if build is not None:
			self.setBuild(build)

	def __repr__(self):
		if hasattr(self, "_path"):
			return "Base(%r)" % (self.path())
		return "Base(%r)" % (self.rawPath)

	@classmethod
	def default(cls):
		"""
		Returns a Base instance with the default path.
		Looks for $MPQ_BASE_DIR environment variable first. Uses $HOME/mpq/WoW otherwise.
		"""
		return cls(os.environ.get("MPQ_BASE_DIR", os.path.join(os.path.expanduser("~"), "mpq", "WoW")))

	def build(self):
		"""
		Returns the base's build.

		Cannot be accessed if the Base build is not set.
		"""
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

	def dataPath(self):
		"""
		Points to the directory where the data files are stored
		<path>/Data

		Cannot be accessed if the Base build is not set.
		"""
		return os.path.join(self.path(), "Data")

	def hasLocale(self, locale):
		"""
		Returns True if \a locale is offered by the base.

		Cannot be accessed if the Base build is not set.
		"""
		valid = ("enUS", "esMX", "enGB", "esES", "frFR", "deDE", "ruRU", "koKR", "zhTW", "enTW", "ptBR", "ptPT", "zhCN", "enCN", "itIT")
		if locale in valid:
			if os.path.exists(self.localePath(locale)):
				return True
		return False

	def localePath(self, locale):
		"""
		Points to the directory where the locale files are stored
		<dataPath>/<locale>

		Cannot be accessed if the Base build is not set.
		"""
		return os.path.join(self.dataPath(), locale)

	def path(self):
		"""
		Points to the base's build directory.

		Cannot be accessed if the Base build is not set.
		"""
		if not hasattr(self, "_path"):
			raise RuntimeError("Cannot access Base.path() if Base does not have a build")

		return os.path.join(self.rawPath, self._path)

	def mfilFiles(self):
		"""
		Returns a dict of mfil paths for build numbers in {build: path} format
		"""
		files = {}
		path = self.path()
		sre = re.compile(r"^wow-(\d+)-\w+.mfil")
		for f in os.listdir(path):
			match = sre.match(f)
			if match:
				fileBuild = int(match.groups()[0])
				files[fileBuild] = os.path.join(path, f)

		return files

	def patchFiles(self, locale):
		"""
		Returns a dict of patch MPQs in {build: path} format

		Cannot be accessed if the Base build is not set.
		"""
		files = {}

		# Old-style wow-updates (oldest) first
		path = self.dataPath()
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
		path = self.localePath(locale)
		sre = re.compile(r"^wow-update-%s-(\d+).MPQ$" % (locale))
		for f in os.listdir(path):
			match = sre.match(os.path.basename(f))
			if match:
				fileBuild = int(match.groups()[0])
				if fileBuild not in files:
					files[fileBuild] = [os.path.join(path, f)]

		return files

	def setBuild(self, build):
		"""
		Sets the Base's build.
		"""
		bases = self.builds()
		# First, check for an exact match so we don't have to be inefficient
		if build in bases:
			self._path = bases[build]
			return

		# Now, get rid of all the bases higher than our build
		for baseBuild in bases:
			if baseBuild > build:
				del bases[baseBuild]

		# And now, get rid of the bases that do not contain our build
		for baseBuild, path in bases.items():
			self._path = path
			if build not in self.patchFiles("enUS").keys():
				del bases[baseBuild]

		# Raise BuildNotFound if we don't have any more bases at this point
		if not bases:
			raise BuildNotFound(build)

		# Finally, get the highest match and set the path appropriately
		self._path = bases[sorted(k for k in bases)[-1]]

def highestBase():
	base = Base.default()
	bases = base.builds()
	base.setBuild(sorted(bases.keys())[-1])
	return base

def highestBuild():
	ret = 0
	base = Base.default()
	for build in base.builds():
		base.setBuild(build)
		i = sorted(base.patchFiles("enUS").keys())[-1]
		if i > ret:
			ret = i

	return ret

def archivesForFlags(flags):
	"""
	Returns a list of archives that may be opened with \a flags
	%(l)s is to be replaced by the locale in the paths
	Archives may not exist, os.path.exists should be run on all returned paths
	"""
	archives = []

	if flags & Environment.ARCHIVE_LOCALE:
		archives.append("%(l)s/locale-%(l)s.MPQ")
		if flags & Environment.ARCHIVE_SPEECH:
			archives.append("%(l)s/speech-%(l)s.MPQ")
			if flags & Environment.ARCHIVE_EXPANSION1:
				archives.append("%(l)s/expansion1-speech-%(l)s.MPQ")
			if flags & Environment.ARCHIVE_EXPANSION2:
				archives.append("%(l)s/expansion2-speech-%(l)s.MPQ")
			if flags & Environment.ARCHIVE_EXPANSION3:
				archives.append("%(l)s/expansion3-speech-%(l)s.MPQ")
			if flags & Environment.ARCHIVE_EXPANSION4:
				archives.append("%(l)s/expansion4-speech-%(l)s.MPQ")

	if flags & Environment.ARCHIVE_MODEL:
		archives.append("model.MPQ")
		archives.append("art.MPQ")

	if flags & Environment.ARCHIVE_TEXTURE:
		archives.append("texture.MPQ")
		archives.append("itemtexture.MPQ")
		archives.append("art.MPQ")

	if flags & Environment.ARCHIVE_WORLD:
		archives.append("world.MPQ")
		archives.append("world2.MPQ")

	if flags & Environment.ARCHIVE_SOUND:
		archives.append("sound.MPQ")

	if flags & Environment.ARCHIVE_INTERFACE:
		archives.append("interface.MPQ")

	if flags & Environment.ARCHIVE_MISC:
		archives.append("misc.MPQ")

	if flags & Environment.ARCHIVE_BASE:
		archives.append("base-OSX.MPQ")
		archives.append("base-Win.MPQ")

	if flags & Environment.ARCHIVE_EXPANSION1:
		archives.append("expansion1.MPQ")
	if flags & Environment.ARCHIVE_EXPANSION2:
		archives.append("expansion2.MPQ")
	if flags & Environment.ARCHIVE_EXPANSION3:
		archives.append("expansion3.MPQ")
	if flags & Environment.ARCHIVE_EXPANSION4:
		archives.append("expansion4.MPQ")

	if flags & Environment.ARCHIVE_ALTERNATE:
		archives.append("alternate.MPQ")

	if flags & Environment.ARCHIVE_OLDWORLD:
		archives.append("OldWorld.MPQ")
		if flags & Environment.ARCHIVE_LOCALE:
			archives.append("%(l)s/OldWorld-%(l)s.MPQ")

	# Remove dupes
	ret = []
	for k in archives:
		if k not in ret:
			ret.append(k)

	return ret

class Environment(object):

	ARCHIVE_OLDWORLD = 0x1
	ARCHIVE_LOCALE = 0x2
	ARCHIVE_SPEECH = 0x4
	ARCHIVE_TEXTURE = 0x8
	ARCHIVE_MODEL = 0x10
	ARCHIVE_WORLD = 0x20
	ARCHIVE_SOUND = 0x40
	ARCHIVE_INTERFACE = 0x80
	ARCHIVE_BASE = 0x100
	ARCHIVE_MISC = 0x200
	ARCHIVE_ALTERNATE = 0x400
	ARCHIVE_EXPANSION1 = 0x800
	ARCHIVE_EXPANSION2 = 0x1000
	ARCHIVE_EXPANSION3 = 0x2000
	ARCHIVE_EXPANSION4 = 0x4000
	ARCHIVE_EXPANSION_ALL = ARCHIVE_EXPANSION1 | ARCHIVE_EXPANSION2 | ARCHIVE_EXPANSION3 | ARCHIVE_EXPANSION4
	ARCHIVE_ALL = 0xfffffffe # Everything except OLDWORLD

	def __init__(self, build, locale="enUS", base=Base.default(), openFlags=ARCHIVE_ALL):
		base.setBuild(build)
		self.base = base
		self.build = build

		if not self.base.hasLocale(locale):
			raise LocaleNotFound(locale)
		self.locale = locale

		patchlist = self.patchList()
		self.archives = {}
		self.mpq = mpq.MPQFile()
		for path in archivesForFlags(openFlags):
			path = os.path.join(self.base.dataPath(), path % {"l": locale})
			if os.path.exists(path):
				self.mpq.add_archive(path)

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
		"""
		Returns the patch chain for the Environment's build
		Attempts to figure it out by:
		 - Looking for a mfil matching the build
		 - If it doesn't exist, looking for a __chain__ file
		 - If it doesn't exist either, just getting it from the list of builds
		"""
		ret = []
		patches = self.base.patchFiles(self.locale)
		builds = sorted(patches.keys())

		# Raise BuildNotFound if we can't patch up to the desired build
		# We should raise it in __init__ instead, but it would involve duplicate code
		if self.build not in builds:
			raise BuildNotFound("Could not find build %i in %r" % (self.build, builds))

		# Look for a mfil matching the build
		mfilPath = self.base.mfilFiles().get(self.build)
		if mfilPath:
			from mfil import MFIL2
			mfil = MFIL2(mfilPath)
			baseBuild = self.base.build()
			retBuilds = []

			for k, d in mfil["file"].items():
				build = d.get("fileversion", "")
				if not build.isdigit():
					continue
				build = int(build)

				if build > baseBuild and build not in retBuilds:
					retBuilds.append(build)

			ret = []
			for build in sorted(retBuilds):
				for f in patches[build]:
					ret.append(f)

			return ret

		# Look for __chain__ otherwise
		chainPath = os.path.join(self.base.path(), "__chain__")
		if os.path.exists(chainPath):
			with open(chainPath, "r") as f:
				for line in f:
					line = [int(x) for x in line.strip().split() if x.isdigit()]
					if line and line[0] == self.build:
						for build in line[1:]:
							for f in patches[build]:
								ret.append(f)

						return ret

		# fallback algorithm
		for build in builds:
			if build > self.build:
				# We only want the patches that correspond to the environment's build
				break

			for f in patches[build]:
				ret.append(f)

		return ret
