#!/usr/bin/python
# -*- coding: utf-8 -*-

import wdbc
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = "sigrie.settings"
from xml.dom import minidom
from optparse import OptionParser
from sigrie.owdb.models import *

CONJURED = 2
UNIQUE_EQUIPPED = 524288

SOCKETS = {
	"Meta": 1,
	"Red": 2,
	"Yellow": 4,
	"Blue": 8,
}

CLASSES = {
	"Warrior": 1,
	"Paladin": 2,
	"Hunter": 4,
	"Rogue": 8,
	"Priest": 16,
	"Death Knight": 32,
	"Shaman": 64,
	"Mage": 128,
	"Warlock": 256,
	"Druid": 1024,
}

RACES = {
	"Human": 1,
	"Dwarf": 4,
	"Night Elf": 8,
	"Gnome": 64,
	"Draenei": 1024,
	"Orc": 2,
	"Troll": 128,
	"Tauren": 32,
	"Undead": 16,
	"Blood Elf": 512,
}

STATS = {
	"bonusAgility": 3,
	"bonusStrength": 4,
	"bonusIntellect": 5,
	"bonusSpirit": 6,
	"bonusStamina": 7,
	"bonusDefenseSkillRating": 12,
	"bonusDodgeRating": 13,
	"bonusParryRating": 14,
	"bonusBlockRating": 15,
	"bonusHitMeleeRating": 16,
	"bonusHitRangedRating": 17,
	"bonusHitSpellRating": 18,
	"bonusCritMeleeRating": 19,
	"bonusCritRangedRating": 20,
	"bonusCritSpellRating": 21,
	"bonusHitTakenMeleeRating": 22,
	"bonusHitTakenRangedRating": 23,
	"bonusHitTakenSpellRating": 24,
	"bonusCritTakenMeleeRating": 25,
	"bonusCritTakenRangedRating": 26,
	"bonusCritTakenSpellRating": 27,
	"bonusHasteMeleeRating": 28,
	"bonusHasteRangedRating": 29,
	"bonusHasteSpellRating": 30,
	"bonusHitRating": 31,
	"bonusCritRating": 32,
	"bonusHitTakenRating": 33,
	"bonusCritTakenRating": 34,
	"bonusResilienceRating": 35,
	"bonusHasteRating": 36,
	"bonusExpertiseRating": 37,
	"bonusAttackPower": 38,
	"bonusFeralAttackPower": 40,
	"bonusManaRegen": 43,
	"bonusArmorPenetration": 44,
	"bonusSpellPower": 45,
}

def _getNode(tag, dom, type=str):
	try:
		return type(dom.getElementsByTagName(tag)[0].firstChild.data)
	except IndexError:
		return type()

class ArmoryItem(object):
	def __repr__(self):
		return "<Item: %s>" % self.name
	
	def addInfo(self, dom):
		self.id = int(dom.getAttribute("id"))
		self.name = str(dom.getAttribute("name"))
		self.level = int(dom.getAttribute("level"))
		self.quality = int(dom.getAttribute("quality"))
		
		cost = dom.getElementsByTagName("cost")
		if cost:
			cost = cost[0]
			self.sellprice = int(cost.getAttribute("sellPrice") or 0)
			buy = cost.getAttribute("buyPrice")
			self.buyprice = buy and int(buy) or 0
		
		disenchanting = dom.getElementsByTagName("disenchantLoot")
		self.disenchanting = disenchanting and int(disenchanting[0].getAttribute("requiredSkillRank")) or -1
	
	def addTooltip(self, dom):
		_lvlreq = _getNode("requiredLevel", dom, int)
		self.levelreq = _lvlreq > 0 and _lvlreq or 0
		_dura = dom.getElementsByTagName("durability")
		_desc = [k for k in dom.childNodes if k.nodeName == "desc"]
		if _desc:
			self.note = _desc[0].firstChild.data
		self.id = _getNode("id", dom, int)
		self.name = _getNode("name", dom)
		self.flags = 0
		self.bind = _getNode("bonding", dom, int)
		self.stack = _getNode("stackable", dom, int)
		self.slot = _getNode("inventoryType", dom, int)
		self.quality = _getNode("overallQualityId", dom, int)
		self.durability = _dura and int(_dura[0].getAttribute("max")) or 0
		_unique = dom.getElementsByTagName("maxCount")
		if _unique:
			self.unique = int(_unique[0].firstChild.data)
			unique_equipped = _unique[0].getAttribute("uniqueEquippable")
			self.flags += unique_equipped and UNIQUE_EQUIPPED or 0
		self.flags = dom.getElementsByTagName("conjured") and CONJURED or 0
		self.unique = _getNode("maxCount", dom, int)
		self.queststart = _getNode("startQuestId", dom, int)
		self.block = _getNode("blockValue", dom, int)
		self.fireresist = _getNode("fireResist", dom, int)
		self.frostresist = _getNode("frostResist", dom, int)
		self.natureresist = _getNode("natureResist", dom, int)
		self.shadowresist = _getNode("shadowResist", dom, int)
		self.arcaneresist = _getNode("arcaneResist", dom, int)
		self.randomenchantment1 = dom.getElementsByTagName("randomEnchantData") and 1 or 0
		zonebind = _getNode("zoneBound", dom)
		if zonebind:
			self.zonebind = Zone.objects.filter(name=zonebind)[:1][0].id
		
		instancebind = _getNode("instanceBound", dom)
		if instancebind:
			self.instancebind = Instance.objects.filter(name=instancebind)[:1][0].id
		
		armor = dom.getElementsByTagName("armor")
		if armor:
			self.armor = int(armor[0].firstChild.data)
			armorBonus = armor[0].getAttribute("armorBonus")
			self.armordmgmod = armorBonus and 1 or 0
		
		_gemprops = _getNode("gemProperties", dom)
		if _gemprops:
			try:
				self.gemproperties = Enchant.objects.filter(name=_gemprops)[:1][0].id
			except IndexError:
				pass
		
		_spellreq = _getNode("requiredAbility", dom)
		if _spellreq:
			self.spellreq = Spell.objects.filter(name=_spellreq)[:1][0].id
		
		_skillreq = dom.getElementsByTagName("requiredSkill")
		if _skillreq:
			self.skillreq = Skill.objects.filter(name=_skillreq[0].getAttribute("name"))[:1][0].id
			self.skilllevelreq = int(_skillreq[0].getAttribute("rank"))
		
		_factionreq = dom.getElementsByTagName("requiredFaction")
		if _factionreq:
			self.factionreq = Faction.objects.get(name=_factionreq[0].getAttribute("name")).id
			self.reputationreq = int(_factionreq[0].getAttribute("rep"))
		
		classes = dom.getElementsByTagName("class")
		self.classreq = -1
		if classes:
			for k in classes:
				self.classreq += CLASSES[k.firstChild.data]
			self.classreq += 1
		
		races = dom.getElementsByTagName("race")
		self.racereq = -1
		if races:
			for k in races:
				self.racereq += RACES[k.firstChild.data]
			self.racereq += 1
		
		i = 0
		for tag in STATS:
			stats = dom.getElementsByTagName(tag)
			if stats:
				for e in stats:
					i += 1
					setattr(self, "stats_id_dyn%i" % i, STATS[tag])
					setattr(self, "stats_amt_dyn%i" % i, int(e.firstChild.data))
		
		damage = dom.getElementsByTagName("damage")
		if damage:
			i = 0
			for e in damage:
				i += 1
				setattr(self, "dmgmin%i" % i, _getNode("min", e, int))
				setattr(self, "dmgmax%i" % i, _getNode("max", e, int))
				setattr(self, "dmgtype%i" % i, _getNode("type", e, int))
		self.speed = int(_getNode("speed", dom, float) * 1000)
		
		sockets = dom.getElementsByTagName("socketData")
		if sockets:
			sockets = sockets[0].getElementsByTagName("socket")
			i = 0
			for e in sockets:
				i+=1
				setattr(self, "socket%i" % i, SOCKETS[e.getAttribute("color")])
			sb = _getNode("socketMatchEnchant", dom)
			if sb:
				self.socketbonus = Enchant.objects.filter(name=sb)[:1][0].id
		
		spells = dom.getElementsByTagName("spellData")
		if spells:
			spells = spells[0].getElementsByTagName("spell")
			i = 0
			for e in spells:
				i+=1
				trigger = _getNode("trigger", e, int)
				text = _getNode("desc", e)
				charges = _getNode("charges", e, int)
				if charges:
					setattr(self, "spellcharges%i", charges)
				
				setattr(self, "spelltrigger%i" % i, trigger)
				if trigger == 6: # learning
					self.note = text
					setattr(self, "spell%i" % i, 2) # use a dead spell
					continue
				
				try:
					setattr(self, "spell%i" % i, Spell.objects.filter(spell_text=text)[:1][0].id)
				except IndexError:
					try:
						_text = text.split("\n")[0][:-1]
						setattr(self, "spell%i" % i, Spell.objects.filter(spell_text__istartswith=_text)[:1][0].id)
					except IndexError:
						print "Spell not found: %r" % text
		
		itemset = dom.getElementsByTagName("setData")
		if itemset:
			itemset = _getNode("name", itemset[0])
			self.itemset = ItemSet.objects.filter(name=itemset)[:1][0].id
	
	
	def assignTo(self, f):
		kwargs = self.__dict__
		kwargs["_id"] = self.id
		f[self.id] = kwargs


def main():
	try:
		OUT = sys.argv[2]
	except IndexError:
		print "Usage: %s /path/to/dump armory-itemcache.wdb" % (sys.argv[0])
		exit()
	
	ls = os.listdir(sys.argv[1])
#	ls.sort()
	d = {}
	i = 0
	for f in ls:
		i += 1
		try:
			id = int(f.split("i=")[1])
		except IndexError:
			continue
		
		txt = minidom.parse("%s/%s" % (sys.argv[1], f))
		
		if f.startswith("item-tooltip"):
			print "Reading %s - %i / %i" % (f, i, len(ls))
			elements = txt.getElementsByTagName("itemTooltip")
			if elements:
				for item in elements:
					if _getNode("id", item):
						if id not in d:
							d[id] = ArmoryItem()
						d[id].addTooltip(item)
		
			txt.unlink()
		
		elif f.startswith("item-info"):
			elements = txt.getElementsByTagName("item")
			if elements:
				if id not in d:
					d[id] = ArmoryItem()
				d[id].addInfo(elements[0])
	
	f = wdbc.new(name="itemcache", build=10192)
	for item in d:
		d[item].assignTo(f)
	f.header.locale = "BGne"
	f.header.wdb4 = 516
	f.header.wdb5 = 5
	f.header.version = 0
	f.update_dynfields()
	f.update_reclens()
	f.write(OUT)
	

if __name__ == "__main__":
	main()
