# -*- coding: utf-8 -*-
#!/usr/bin/python

from pywow.structures import Structure, Skeleton
from pywow.structures.fields import *

class SoldItemCache(Structure):
	signature = "CISW"
	
	CLASSES = {
		0x001: "WARRIOR",
		0x002: "PALADIN",
		0x004: "HUNTER",
		0x008: "ROGUE",
		0x010: "PRIEST",
		0x020: "DEATHKNIGHT",
		0x040: "SHAMAN",
		0x080: "MAGE",
		0x100: "WARLOCK",
		0x400: "DRUID",
	}
	
	fields = Skeleton(
		IDField(),
		RecLenField(),
		ForeignKey("vendor", "creaturecache"),
		ForeignKey("item", "itemcache"),
		IntegerField("limited_quantity"),
		IntegerField("stack"),
		IntegerField("honor"),
		IntegerField("arena"),
		IntegerField("rating"),
		IntegerField("bracket"),
		BitMaskField("shown_to_classes", flags=CLASSES),
		
		# extended cost
		ForeignKey("item_cost_1", "itemcache"),
		IntegerField("item_amount_1"),
		ForeignKey("item_cost_2", "itemcache"),
		IntegerField("item_amount_2"),
		ForeignKey("item_cost_3", "itemcache"),
		IntegerField("item_amount_3"),
		ForeignKey("item_cost_4", "itemcache"),
		IntegerField("item_amount_4"),
		ForeignKey("item_cost_5", "itemcache"),
		IntegerField("item_amount_5"),
	)

class TrainedSpellCache(Structure):
	signature = "CSTW"
	
	fields = Skeleton(
		IDField(),
		RecLenField(),
		ForeignKey("trainer", "creaturecache"),
		ForeignKey("spell", "spell"),
		IntegerField("cost"),
		IntegerField("required_level"),
		ForeignKey("required_skill", "skillline"),
		IntegerField("required_skill_level"),
		ForeignKey("required_spell_1", "spell"),
		ForeignKey("required_spell_2", "spell"),
	)
