from ..structure import Structure, register
from ..fields import *


@register(magic="XTIW", name="itemtextcache.wdb")
class ItemTextCache(Structure):
	id = IntegerField()
	text = StringField()
