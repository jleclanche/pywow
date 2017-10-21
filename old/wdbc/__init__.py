def read_file(path):
	f = open(path, "rb")
	magic = f.read(4)
	f.seek(0)
	from . import wdb
	return wdb.read_file(f)
