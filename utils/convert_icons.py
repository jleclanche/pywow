#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import sys
from PIL import ImageOps
from pilgrim.codecs import BLP
from sigrie.settings import MEDIA_ROOT

SIGRIE_ICONS_PATH = MEDIA_ROOT + "img/icons/"
SIGRIE_ICONS_GREYSCALE_PATH = SIGRIE_ICONS_PATH + "greyscale/"

def main():
	path = "icons/"
	if not os.path.exists(SIGRIE_ICONS_GREYSCALE_PATH):
		os.makedirs(SIGRIE_ICONS_GREYSCALE_PATH)
	
	listdir = os.listdir(path)
	total = len(listdir)
	for i, name in enumerate(listdir):
		pc = int((i / total) * 100)
		print "\r" + " " * 150,
		print "\rConverting %i/%i (%i%%)..." % (i, total, pc), name,
		sys.stdout.flush()
		try:
			f = BLP(path + name)
			name = name.replace(".blp", ".png")
			f.save(SIGRIE_ICONS_PATH + name)
			f = ImageOps.grayscale(f)
			f.save(SIGRIE_ICONS_GREYSCALE_PATH + name)
		except Exception, e:
			print "WARNING:", e, "(press any key to continue)"
			raw_input()
	
	print "\r", "%i icons converted" % (total)

if __name__ == "__main__":
	main()
