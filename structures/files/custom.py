# -*- coding: utf-8 -*-
#!/usr/bin/python

from ..base import DBStructure, Skeleton
from ..fields import *

CLASSES = ["WARRIOR", "PALADIN", "HUNTER", "ROGUE", "PRIEST",
	"DEATHKNIGHT", "SHAMAN", "MAGE", "WARLOCK", "", "DRUID"]

class SoldItemCache(DBStructure):
	signature = "CISW"
	
	base = Skeleton(
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

class TrainedSpellCache(DBStructure):
	signature = "CSTW"
	
	base = Skeleton(
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
