#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pywow import mpq

def main():
	f = mpq.Archive(sys.argv[1])
	#f = mpq.Archive("~/wow/Data/expansion.mpq")
	print f

if __name__ == "__main__":
	main()
