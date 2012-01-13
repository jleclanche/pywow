#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path
import sys
from PIL import Image
from pilgrim.codecs import BLP
from pywow import wdbc
from pywow.environment import highestBuild

BASE_DIR = "maps/"
BUILD = highestBuild()

MAP_SIZE = (1002, 668)
CHUNK_SIZE = 256
REVEALED_DIR = "revealed/"
UNREVEALED_DIR = "unrevealed/"


class Directory(object):
	"""
	dict-like object for directories
	"""
	def __init__(self, path):
		if not os.path.isdir(path):
			raise ValueError("%r is not a directory" % (path))
		self.path = path
		self.__dircache = os.listdir(path)
		self.__files = {}

	def __repr__(self):
		return self.__dircache.__repr__()

	def __contains__(self, item):
		return self.__dircache.__contains__(item)

	def __getitem__(self, item):
		if item not in self.__files:
			if item not in self.__dircache:
				raise KeyError(item)
			self.__files[item] = open(os.path.join(self.path, item))
		return self.__files[item]


class Map(object):
	def __init__(self, name):
		self.name = name
		self.files = Directory(BASE_DIR + name)
		self.wmo = wdbc.get("WorldMapOverlay", build=BUILD)

	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.name)


	def __get_bg_chunk(self, index, level=0):
		if level: # multilevel
			return "%s%i_%i.blp" % (self.name, level, index)
		return "%s%i.blp" % (self.name, index)

	def __build_chunk(self, row):
		name, width, height = row.name, row.width, row.height
		def getamount(x):
			# Helper - get the amount of images needed to cover a 256x block
			a, b = divmod(x, CHUNK_SIZE)
			return a + min(1, b)
		width_amount = getamount(width) # horizontally
		height_amount = getamount(height) # and vertically

		chunk = Image.new("RGBA", (width_amount * CHUNK_SIZE, height_amount * CHUNK_SIZE))

		coords_width = 0
		coords_height = 0

		# Build top to bottom ...
		for a in xrange(height_amount):
			# ... and left to right
			for b in xrange(width_amount):
				filename = "%s%i.blp" % (name.lower(), (a * width_amount + b) + 1)
				#assert filename in self.files
				if filename not in self.files:
					return chunk
				f = self.files[filename]
				chunkbit = BLP(f)
				chunkbit_width, chunkbit_height = chunkbit.size
				coords = (
					coords_width,
					coords_height,
				)
				chunk.paste(chunkbit, coords)
				coords_width += chunkbit_width

			# Flush coords
			coords_width = 0
			coords_height += chunkbit_height

		return chunk

	def __build_background(self):
		img = Image.new("RGBA", MAP_SIZE)

		i = 0
		for a in xrange(3):
			for b in xrange(4):
				i += 1
				chunk = BLP(self.files[self.__get_bg_chunk(i)])
				img.paste(chunk, (CHUNK_SIZE * b, CHUNK_SIZE * a))

		return img

	def __build_foreground(self):
		bg = self.bg
		# Do a reverse lookup on WorldMapOverlay.dbc
		lookups = [k for k in self.wmo if self.wmo[k].zone.name.lower() == self.name]
		for chunk in lookups:
			row = self.wmo[chunk]
			name, left, top = row.name, row.left, row.top
			if name:
				img = self.__build_chunk(row)
				bg.paste(img, (left, top), mask=img)
		return bg

	def __build_multilevel(self):
		bgs = []
		level = 0
		while True:
			level += 1
			img = Image.new("RGBA", MAP_SIZE)
			i = 0
			for a in xrange(3):
				for b in xrange(4):
					i += 1
					try:
						chunk = BLP(self.files[self.__get_bg_chunk(i, level=level)])
					except KeyError:
						return bgs
					img.paste(chunk, (CHUNK_SIZE * b, CHUNK_SIZE * a))
			print "Level %i..." % (level)
			bgs.append(img)


	def build(self):
		print self
		try:
			self.bg = self.__build_background()
			self.bg.save(UNREVEALED_DIR + "%s.png" % (self.name))
		except KeyError: # Multi-level map
			bgs = self.__build_multilevel()
			for i, bg in enumerate(bgs):
				bg.save(UNREVEALED_DIR + "%s%i.png" % (self.name, i+1))
				bg.save(REVEALED_DIR + "%s%i.png" % (self.name, i+1))
			return

		self.fg = self.__build_foreground()
		self.fg.save(REVEALED_DIR + "%s.png" % (self.name))


def main():
	if not os.path.exists(REVEALED_DIR):
		os.mkdir(REVEALED_DIR)
	if not os.path.exists(UNREVEALED_DIR):
		os.mkdir(UNREVEALED_DIR)

	if len(sys.argv) > 1:
		for arg in sys.argv[1:]:
			if arg in os.listdir(BASE_DIR):
				Map(arg).build()

	else:
		for map in os.listdir(BASE_DIR):
			try:
				Map(map).build()
			except ValueError as e:
				print "WARNING:", e

if __name__ == "__main__":
	main()
