#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pilgrim.codecs import BLP
from sigrie.settings import MEDIA_ROOT

SIGRIE_WOW_PATH = MEDIA_ROOT + "wow/"

def main():
	for dir in os.listdir("pageimages/interface"):
		dir = "interface/%s" % (dir)
		fullpath = SIGRIE_WOW_PATH + dir
		if not os.path.exists(fullpath):
			os.makedirs(fullpath)
		
		for G in os.listdir("pageimages/" + dir):
			print "Converting...", G
			try:
				f = BLP("pageimages/%s/%s" % (dir, G))
				f.save("%s/%s.png" % (fullpath, G.replace(".blp", "")))
			except Exception, e:
				print "WARNING:", e, "(press any key to continue)"
				raw_input()

if __name__ == "__main__":
	main()
