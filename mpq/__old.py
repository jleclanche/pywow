# -*- coding: utf-8 -*-

from struct import pack, unpack

class MPQ(object):
	def __init__(self, file):
		self.file = file
		self.__parse_header()
	
	def __repr__(self):
		return "MPQ(file=%r, version=%r)" % (self.file.name, self.version)
	
	def __parse_header(self):
		f = self.file
		f.seek(0)
		
		magic = f.read(3)
		print magic
		if magic != "MPQ":
			raise ValueError("bad magic")
		
		shunt = f.read(1)
		if shunt == "\x1B":
			print "Houston, we have a shunt"
			self.shunt = True
			_ = f.read(4)
			header_offset = unpack("<I", f.read(4))
		elif shunt == "\x1A":
			self.shunt = False
			print "That ain't no shunt"
		else:
			raise ValueError("Shunt the hell up")
		
		self.header_length, self.archive_length, self.version, self.block_size = unpack("<IIHH", f.read(12))
		self.block_size = 0x200 << self.block_size
		self.hashtable_offset, self.datatable_offset, self.hashtable_entries, self.hashtable_offset = unpack("<4I", f.read(16))
		
		if self.version == 1:
			self.extended_block_offset = unpack("<Q", f.read(8))
			self.hashtable_highword, self.datatable_highword = unpack("<HH", f.read(4))
	
	def open(self):
		print self.__dict__

def fopen(filename):
	f = open(filename, "rb")
	f = MPQ(f)
	f.open()
	print f
