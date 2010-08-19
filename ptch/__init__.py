# -*- coding: utf-8 -*-
"""
PTCH files are a container format for Blizzard patch files.
They begin with a 72 byte header containing some metadata, immediately
followed by a RLE-packed BSDIFF40.
The original BSDIFF40 format is compressed with bzip2 instead of RLE.
"""

#from hashlib import md5
from struct import unpack
from binascii import hexlify
from cStringIO import StringIO


class PatchFile(object):
	def __init__(self, file):
		# Parse the header
		file.seek(0)
		assert file.read(4) == "PTCH"
		unk1 = file.read(4)
		self.sizeBefore, self.sizeAfter = unpack("ii", file.read(8))
		assert file.read(4) == "MD5_"
		assert unpack("i", file.read(4)) == (0x28, )
		self.md5Before, self.md5After = unpack("16s16s", file.read(32))
		self.md5Before, self.md5After = hexlify(self.md5Before), hexlify(self.md5After)
		assert file.read(4) == "XFRM"
		file.read(4)
		assert file.read(4) == "BSD0"
		self.fileSize, = unpack("i", file.read(4))
		
		self.compressedDiff = file.read()
		
		file.close()
	
	def __repr__(self):
		header = ("sizeBefore", "sizeAfter", "md5Before", "md5After", "fileSize")
		return "%s(%s)" % (self.__class__.__name__, ", ".join("%s=%r" % (k, getattr(self, k)) for k in header))
	
	def __bsdiffParseHeader(self, diff):
		"""
		The BSDIFF header is as follows:
		 - 8 bytes magic "BSDIFF40"
		 - 8 bytes control block size
		 - 8 bytes diff block size
		 - 8 bytes new file size
		We read all this and make sure it's all valid.
		"""
		assert diff.read(8) == "BSDIFF40"
		ctrlBlockSize, diffBlockSize, sizeAfter = unpack("QQQ", diff.read(24))
		assert ctrlBlockSize > 0 and diffBlockSize > 0
		assert sizeAfter == self.sizeAfter
		return ctrlBlockSize, diffBlockSize, sizeAfter
	
	def rleUnpack(self):
		"""
		Read the RLE-packed data and
		return the unpacked output.
		"""
		data = StringIO(self.compressedDiff)
		ret = []
		
		byte = data.read(1)
		while byte:
			byte = ord(byte)
			# Is it a repeat control?
			if byte & 0x80:
				count = (byte & 0x7F) + 1
				ret.append(data.read(count))
			
			else:
				ret.append("\0" * (byte+1))
			
			byte = data.read(1)
		
		return "".join(ret)
	
	def apply(self, orig):
		diff = StringIO(self.rleUnpack())
		ctrlBlockSize, diffBlockSize, sizeAfter = self.__bsdiffParseHeader(diff)
		
		# Emulate C pointers
		# Dirty until we can pythonize that
		new = ["\0" for i in range(sizeAfter)]
		old = [c for c in orig]
		oldsize = len(orig)
		oldpos, newpos = 0, 0
		
		ctrlBlock = StringIO(diff.read(ctrlBlockSize))
		while newpos < sizeAfter:
			# Read control block
			ctrl = unpack("iii", ctrlBlock.read(12))
			
			assert newpos + ctrl[0] <= sizeAfter
			
			# Read diff block
			diffBlock = diff.read(ctrl[0])
			new[newpos:newpos + ctrl[0]] = [c for c in diffBlock]
			
			# Add old data to diff string
			for i in range(ctrl[0]):
				if (oldpos + i >= 0) and (oldpos + i < oldsize):
					nb, ob = ord(new[newpos + i]), ord(old[oldpos+i])
					new[newpos + i] = chr((ord(nb) + ord(ob)) % 255)
			
			# Adjust pointers
			newpos += ctrl[0]
			oldpos += ctrl[0]
			
			assert newpos + ctrl[1] <= sizeAfter
			
			# Read extra block
			extraBlock = diff.read(ctrl[1])
			new[newpos:newpos + ctrl[1]] = [c for c in extraBlock]
			
			newpos += ctrl[1]
			oldpos += ctrl[2]
		
		return "".join(new)
