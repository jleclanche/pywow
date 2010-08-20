# -*- coding: utf-8 -*-
"""
PTCH files are a container format for Blizzard patch files.
They begin with a 72 byte header containing some metadata, immediately
followed by a RLE-packed BSDIFF40.
The original BSDIFF40 format is compressed with bzip2 instead of RLE.
"""

from hashlib import md5
from struct import unpack
from binascii import hexlify
from cStringIO import StringIO


class PatchFile(object):
	def __init__(self, file):
		# Parse the header
		file.seek(0)
		assert file.read(4) == "PTCH" # Magic
		
		##
		# Sizes
		# - patchSize: Size of the entire patch data, not including the 'PTCH' signature itself
		# - sizeBefore: Size of the file before patching
		# - sizeAfter: Size of the file after patching
		self.patchSize, self.sizeBefore, self.sizeAfter = unpack("iii", file.read(12))
		
		##
		# MD5 block
		# - md5BlockSize: Size of the MD5 block, including the signature and size
		# - md5Before: MD5 digest of the original (unpatched) file
		# - md5After: MD5 digest of the patched file
		assert file.read(4) == "MD5_"
		self.md5BlockSize, = unpack("i", file.read(4))
		self.md5Before, self.md5After = unpack("16s16s", file.read(32))
		self.md5Before, self.md5After = hexlify(self.md5Before), hexlify(self.md5After)
		
		##
		# XFRM block
		# - xfrmBlockSize: Size of the XFRM block + the packed data
		# - unpackedSize: Unpacked size of the patch data
		assert file.read(4) == "XFRM"
		self.xfrmBlockSize, = unpack("i", file.read(4))
		assert file.read(4) == "BSD0" # patch type?
		self.unpackedSize, = unpack("i", file.read(4))
		
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
	
	
	def bsdiffParse(self):
		diff = StringIO(self.rleUnpack())
		ctrlBlockSize, diffBlockSize, sizeAfter = self.__bsdiffParseHeader(diff)
		
		##
		# The data part of the file is divded into three parts
		# * The control block, which contains the control part every chunk
		# * The diff block, which contains the diff chunks
		# * And the extra block, which contains the extra chunks
		ctrlBlock = StringIO(diff.read(ctrlBlockSize))
		diffBlock = StringIO(diff.read(diffBlockSize))
		extraBlock = StringIO(diff.read())
		diff.close()
		
		return ctrlBlock, diffBlock, extraBlock
	
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
	
	def apply(self, old, validate=True):
		"""
		Apply the patch to the old argument. Returns the output.
		If validate == True, will raise ValueError if the md5 of
		input or output is wrong.
		"""
		if validate:
			hash = md5(old).hexdigest()
			if hash != self.md5Before:
				raise ValueError("Input MD5 fail. Expected %s, got %s." % (self.md5Before, hash))
		ctrlBlock, diffBlock, extraBlock = self.bsdiffParse()
		
		sizeBefore = len(old)
		new = ["\0" for i in range(self.sizeAfter)]
		
		cursor, oldCursor = 0, 0
		while cursor < self.sizeAfter:
			# Read control chunk
			diffChunkSize, extraChunkSize, extraOffset = unpack("iii", ctrlBlock.read(12))
			assert cursor + diffChunkSize <= self.sizeAfter
			
			# Read diff block
			new[cursor:cursor + diffChunkSize] = diffBlock.read(diffChunkSize)
			
			# Add old data to diff string
			for i in range(diffChunkSize):
				# if (oldCursor + i >= 0) and (oldCursor + i < sizeBefore)
				nb, ob = ord(new[cursor + i]), ord(old[oldCursor + i])
				new[cursor + i] = chr((nb + ob) % 256)
			
			# Update cursors
			cursor += diffChunkSize
			oldCursor += diffChunkSize
			assert cursor + extraChunkSize <= self.sizeAfter
			
			# Read extra chunk
			new[cursor:cursor + extraChunkSize] = extraBlock.read(extraChunkSize)
			
			# Update cursors
			cursor += extraChunkSize
			oldCursor += extraOffset
		
		ret = "".join(new)
		
		if validate:
			hash = md5(ret).hexdigest()
			if hash != self.md5After:
				# This likely means a parsing bug
				raise ValueError("Output MD5 fail. Expected %s, got %s" % (self.md5Before, hash))
		
		return ret
