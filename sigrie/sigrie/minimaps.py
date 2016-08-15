#!/usr/bin/python

import os, os.path
import re
import sys
import Image

sys.path.append("/home/adys/src/bzr/python-image/pilgrim/")
from BLPImagePlugin import BLPImageFile as BLP
from shutil import copyfile


class ParsingError(Exception):
	pass

def tounix(path):
	"Helper to convert a path to unix paths"
	return path.replace("\\", "/") # convert to unix filenames

def splitchunkname(name):
	"Helper to split blp filenames into basename, x, y"
	pattern = r"(.+)([0-9][0-9])_([0-9][0-9])\.blp"
	sre = re.match(pattern, name)
	basename, x, y = sre.groups()
	return basename, x, y

def calcsize(list):
	"Calculate the total size of an image given a list of coords"
	xhigh, yhigh = 0, 0
	for x, y in list:
		if x >= xhigh:
			xhigh = x+1
		if y >= yhigh:
			yhigh = y+1
	return xhigh * 256, yhigh * 256

def main():
	trs = open("md5translate.trs", "r")
	hashtable = {}
	key = None
	
	# Parse md5translate.trs and build a lookup table
	print "Parsing md5translate.trs"
	for line in trs.readlines():
		line = line.lower().strip()
		if not line:
			continue
		
		if line.startswith("dir: "):
			key = tounix(line.replace("dir: ", ""))
			if not key:
				raise ParsingError
			hashtable[key] = {}
			continue
		
		if not key:
			raise ParsingError
		
		name, hash = line.split("\t")
		name = tounix(name)
		hashtable[key][name] = hash
	
	print "Translating files"
	## Now translate the files into a new folder
	translated_dir = "translated/"
	if not os.path.exists(translated_dir):
		os.mkdir(translated_dir)
	for key, translate in hashtable.items():
		key = key.replace("/", "_")
		path = translated_dir + key + "/"
		
		if key.startswith("wmo"):
			continue
		
		for trs_file, md5_file in translate.items():
			trs_file = trs_file.replace("/", "_")
			if os.path.exists(md5_file):
				copyfile(md5_file, translated_dir + trs_file)
	
	# Finally, build png files out of the minimaps in translated dir
	converted_dir = "converted/"
	if not os.path.exists(converted_dir):
		os.mkdir(converted_dir)
	maps = {}
	for chunk in os.listdir(translated_dir):
		basename, x, y = splitchunkname(chunk)
		if basename not in maps:
			maps[basename] = []
		maps[basename].append((int(x), int(y)))
	
	for map in maps:
		print maps[map]
		img = Image.new("RGBA", calcsize(maps[map]))
		for x, y in maps[map]:
			print x, y
			blp = BLP(translated_dir + "%s%02i_%02i.blp" % (map, x, y))
			img.paste(blp, (x*256, y*256))
		path = converted_dir + map + ".png"
		img.save(path)
		print "Saving...", path

if __name__ == "__main__":
	try:
		main()
	except ParsingError:
		print "Error reading md5translate.trs"
		exit(1)
