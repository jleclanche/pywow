from ..structure import Structure, register
from ..fields import *


@register(magic="XTPW", name="pagetextcache.wdb")
class PageTextCache(Structure):
	id = IntegerField()
	next_page = ForeignKey("PageTextCache")
	unk = ShortField()
	text = StringField()
