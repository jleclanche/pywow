import sys
import unittest
sys.path.append("../../..")
from wow.wdbc import read_file



class WDBTestCase(unittest.TestCase):
	def test_pagetextcache(self):
		testfile = "/home/adys/src/git/wow/wdbc/tests/pagetextcache.wdb"
		f = read_file(testfile)
		self.assertEqual(f.header.magic, "XTPW")
		self.assertEqual(len(f._offsets), 48)
		self.assertEqual(f[4452].text, "Darkmoon Faire Bill of Sale\r\n\r\n6x Super-effective Gnoll Decoy*\r\n60g 20s 300c")

	def test_pagetextcache(self):
		testfile = "/home/adys/src/git/wow/wdbc/tests/itemtextcache.wdb"
		f = read_file(testfile)
		self.assertEqual(f.header.magic, "XTIW")
		self.assertEqual(len(f._offsets), 1)
		print(f.keys())
		self.assertEqual(f[4452].text, "Darkmoon Faire Bill of Sale\r\n\r\n6x Super-effective Gnoll Decoy*\r\n60g 20s 300c")


if __name__ == "__main__":
	unittest.main()
