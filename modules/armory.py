#!/usr/bin/python
# -*- coding: utf-8 -*-

import wdbc
from xml.dom import minidom

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
	
	def addTooltip(self, dom):
		_lvlreq = _getNode("requiredLevel", dom, int)
		_dura = dom.getElementsByTagName("durability")
		_desc = [k for k in dom.childNodes if k.nodeName == "desc"]
		if _desc:
			self.desc = _desc[0].firstChild.data
		self.id = _getNode("id", dom, int)
		self.name = _getNode("name", dom)
		self.bind = _getNode("bonding", dom, int)
		self.quality = _getNode("overallQualityId", dom, int)
		self.durability = _dura and int(_dura[0].getAttribute("max")) or 0
		self.speed = int(_getNode("speed", dom, float) * 1000)
		self.unique = _getNode("maxCount", dom, int)
		self.queststart = _getNode("startQuestId", dom, int)
		self.block = _getNode("blockValue", dom, int)
		self.fireresist = _getNode("fireResist", dom, int)
		self.frostresist = _getNode("frostResist", dom, int)
		self.natureresist = _getNode("natureResist", dom, int)
		self.shadowresist = _getNode("shadowResist", dom, int)
		self.arcaneresist = _getNode("arcaneResist", dom, int)
#		self.note = _getNode("desc", dom)
		self.armor = _getNode("armor", dom, int)
		self.levelreq = _lvlreq > 0 and _lvlreq or 0
		
		classes = dom.getElementsByTagName("class")
		self.classreq = 0
		if classes:
			for k in classes:
				self.classreq += CLASSES[k.firstChild.data]
		
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
		
		sockets = dom.getElementsByTagName("socket")
		if sockets:
			i = 0
			for e in sockets:
				i+=1
				setattr(self, "socket%i" % i, SOCKETS[e.getAttribute("color")])
	
	def assignTo(self, f):
		kwargs = self.__dict__
		kwargs["_id"] = self.id
		f[self.id] = kwargs


def main():
	ls = listdir(sys.argv[1])
	d = {}
	i = 0
	for f in ls:
		i += 1
		id = int(f.split("i=")[1])
		if id < 44000: continue
		
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
				d[id].addData(elements[0])
	import wdbc
	
	f = wdbc.new(name="itemcache", build=9806)
	for item in d:
		d[item].assignTo(f)
	f.header.wdb4 = 512
	f.header.wdb5 = 5
	f.header.version = 1
	f.update_dynfields()
	f.update_reclens()
	f.write("/home/adys/armory.wdb")
	

if __name__ == "__main__":
	main()
