# -*- coding: utf-8 -*-
"""
game.items.level
 Item armor and damage dynamically calculated from the DBCs
 New in Cataclysm
"""

from math import floor
from pywow import wdbc

ITEM_CLASS_WEAPON             = 2
ITEM_CLASS_ARMOR              = 4
ITEM_QUALITY_POOR             = 0
ITEM_QUALITY_COMMON           = 1
ITEM_QUALITY_UNCOMMON         = 2
ITEM_QUALITY_RARE             = 3
ITEM_QUALITY_EPIC             = 4
ITEM_QUALITY_LEGENDARY        = 5
ITEM_QUALITY_ARTIFACT         = 6
ITEM_QUALITY_HEIRLOOM         = 7
ITEM_SUBCLASS_ARMOR_CLOTH     = 1
ITEM_SUBCLASS_ARMOR_LEATHER   = 2
ITEM_SUBCLASS_ARMOR_MAIL      = 3
ITEM_SUBCLASS_ARMOR_PLATE     = 4
ITEM_SUBCLASS_WEAPON_BOW      = 2
ITEM_SUBCLASS_WEAPON_GUN      = 3
ITEM_SUBCLASS_WEAPON_THROWN   = 16
ITEM_SUBCLASS_WEAPON_CROSSBOW = 18
ITEM_SUBCLASS_WEAPON_WAND     = 19
INVTYPE_CHEST                 = 5
INVTYPE_WEAPON                = 13
INVTYPE_SHIELD                = 14
INVTYPE_RANGED                = 15
INVTYPE_2HWEAPON              = 17
INVTYPE_ROBE                  = 20
INVTYPE_WEAPONMAINHAND        = 21
INVTYPE_WEAPONOFFHAND         = 22
INVTYPE_THROWN                = 25
INVTYPE_RANGEDRIGHT           = 26


qualities = ("poor", "common", "uncommon", "rare", "epic", "legendary", "artifact")
types = ("no_armor", "cloth", "leather", "mail", "plate")


def getDamageDBC(subcategory, slot, flags):
	if slot in (INVTYPE_WEAPON, INVTYPE_WEAPONMAINHAND, INVTYPE_WEAPONOFFHAND):
		if flags & 0x200:
			return "ItemDamageOneHandCaster"
		return "ItemDamageOneHand"
	
	if slot == INVTYPE_2HWEAPON:
		if flags & 0x200:
			return "ItemDamageTwoHandCaster"
		return "ItemDamageTwoHand"
	
	if slot in (INVTYPE_RANGED, INVTYPE_THROWN, INVTYPE_RANGEDRIGHT):
		if subcategory in (ITEM_SUBCLASS_WEAPON_BOW, ITEM_SUBCLASS_WEAPON_GUN, ITEM_SUBCLASS_WEAPON_CROSSBOW):
			return "ItemDamageRanged"
		if subcategory == ITEM_SUBCLASS_WEAPON_THROWN:
			return "ItemDamageThrown"
		if subcategory == ITEM_SUBCLASS_WEAPON_WAND:
			return "ItemDamageWand"

def getDamage(level, category, subcategory, quality, slot, flags, speed):
	if not (1 <= level <= 1000):
		return 0, 0
	
	if category != ITEM_CLASS_WEAPON:
		dps = 0.0
	
	if quality >= ITEM_QUALITY_HEIRLOOM:
		return 0, 0
	
	dbc = getDamageDBC(subcategory, slot, flags)
	if not dbc:
		dps = 0.0
	else:
		dbc = wdbc.get(dbc, build=-1)
		dps = getattr(dbc[level], qualities[quality])
	
	min = int(floor(dps * speed / 1000 * 0.7 + 0.5))
	max = int(floor(dps * speed / 1000 * 1.3 + 0.5))
	return min, max


def getArmor(level, category, subcategory, quality, slot):
	if quality >= ITEM_QUALITY_HEIRLOOM:
		return 0
	
	if not (1 <= level <= 1000):
		return 0
	
	if slot == INVTYPE_SHIELD:
		dbc = wdbc.get("ItemArmorShield", build=-1)
		total = getattr(dbc[level], qualities[quality])
		return int(floor(total + 0.5))
	
	if slot == INVTYPE_ROBE:
		slot = INVTYPE_CHEST
	
	if category != ITEM_CLASS_ARMOR or not slot:
		return 0
	
	if subcategory not in (ITEM_SUBCLASS_ARMOR_CLOTH, ITEM_SUBCLASS_ARMOR_LEATHER, ITEM_SUBCLASS_ARMOR_MAIL, ITEM_SUBCLASS_ARMOR_PLATE):
		return 0
	
	ArmorLocation = wdbc.get("ArmorLocation", build=-1)
	ItemArmorTotal = wdbc.get("ItemArmorTotal", build=-1)
	ItemArmorQuality = wdbc.get("ItemArmorQuality", build=-1)
	
	total = getattr(ItemArmorTotal[level], types[subcategory])
	_quality = getattr(ItemArmorQuality[level], qualities[quality])
	_slot = getattr(ArmorLocation[slot], types[subcategory])
	
	return int(floor(total * _quality * _slot + 0.5))

