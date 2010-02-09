#!/usr/bin/python
# -*- coding: utf-8 -*-

import wdbc
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = "sigrie.settings"
from xml.dom import minidom
from sigrie.owdb.models import *

from optparse import OptionParser
o = OptionParser()
o.add_option("-b", "--build", type="int", dest="build")
o.add_option("-l", "--locale", type="string", dest="locale", default="enUS")
o.add_option("-v", "--version", type="int", dest="version", default=0)
o.add_option("-D", "--item-dbc", type="string", dest="item_dbc", default=None)

args = o.parse_args(sys.argv[3:])[0]

CONJURED        = 0x00000002
HEROIC          = 0x00000008
UNIQUE_EQUIPPED = 0x00080000
ACCOUNT_BOUND   = 0x08000000

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
	
	ITEM_DBC = None
	
	def __repr__(self):
		return "<Item: %s>" % self.name
	
	def addInfo(self, dom):
		self._id = int(dom.getAttribute("id"))
		self.name = str(dom.getAttribute("name"))
		self.level = int(dom.getAttribute("level"))
		self.quality = int(dom.getAttribute("quality"))
		
		cost = dom.getElementsByTagName("cost")
		if cost:
			cost = cost[0]
			self.sell_price = int(cost.getAttribute("sellPrice") or 0)
			buy = cost.getAttribute("buyPrice")
			self.buy_price = buy and int(buy) or 0
		
		disenchant = dom.getElementsByTagName("disenchantLoot")
		self.disenchant = disenchant and int(disenchant[0].getAttribute("requiredSkillRank")) or -1
	
	def addTooltip(self, dom):
		required_level = _getNode("requiredLevel", dom, int)
		self.required_level = required_level > 0 and required_level or 0
		durability = dom.getElementsByTagName("durability")
		note = [k for k in dom.childNodes if k.nodeName == "desc"]
		if note:
			self.note = note[0].firstChild.data
		self._id = _getNode("id", dom, int)
		self.name = _getNode("name", dom)
		self.flags = 0
		self.bind = _getNode("bonding", dom, int)
		self.stack = _getNode("stackable", dom, int)
		self.slot = _getNode("inventoryType", dom, int)
		self.bag_slots = _getNode("containerSlots", dom, int)
		self.quality = _getNode("overallQualityId", dom, int)
		self.durability = durability and int(durability[0].getAttribute("max")) or 0
		unique = dom.getElementsByTagName("maxCount")
		if unique:
			self.unique = int(unique[0].firstChild.data)
			unique_equipped = unique[0].getAttribute("uniqueEquippable")
			self.flags += unique_equipped and UNIQUE_EQUIPPED or 0
		self.flags += dom.getElementsByTagName("conjured") and CONJURED or 0
		self.flags += dom.getElementsByTagName("heroic") and HEROIC or 0
		self.flags += dom.getElementsByTagName("accountBound") and ACCOUNT_BOUND or 0
		self.unique = _getNode("maxCount", dom, int)
		self.starts_quest = _getNode("startQuestId", dom, int)
		self.block = _getNode("blockValue", dom, int)
		self.fire_resist = _getNode("fireResist", dom, int)
		self.frost_resist = _getNode("frostResist", dom, int)
		self.nature_resist = _getNode("natureResist", dom, int)
		self.shadow_resist = _getNode("shadowResist", dom, int)
		self.arcane_resist = _getNode("arcaneResist", dom, int)
		self.randomenchantment = dom.getElementsByTagName("randomEnchantData") and 1 or 0
		zonebind = _getNode("zoneBound", dom)
		if zonebind:
			self.zone_bind = Zone.objects.filter(name=zonebind)[:1][0]._id
		
		instance_bind = _getNode("instanceBound", dom)
		if instance_bind:
			self.instance_bind = Instance.objects.filter(name=instance_bind)[:1][0]._id
		
		armor = dom.getElementsByTagName("armor")
		if armor:
			self.armor = int(armor[0].firstChild.data)
			self.armordmgmod = int(armor[0].getAttribute("armorBonus"))
		
		gem_properties = _getNode("gemProperties", dom)
		if gem_properties:
			try:
				self.gem_properties = Enchant.objects.filter(name=gem_properties)[:1][0]._id
			except IndexError:
				print "Enchant not found:", repr(gem_properties)
		
		required_spell = _getNode("requiredAbility", dom)
		if required_spell:
			self.required_spell = Spell.objects.filter(name=required_spell)[:1][0]._id
		
		required_skill = dom.getElementsByTagName("requiredSkill")
		if required_skill:
			self.required_skill = Skill.objects.filter(name=required_skill[0].getAttribute("name"))[:1][0].id
			self.required_skill_level = int(required_skill[0].getAttribute("rank"))
		
		required_faction = dom.getElementsByTagName("requiredFaction")
		if required_faction:
			self.required_faction = Faction.objects.get(name=required_faction[0].getAttribute("name")).id
			self.required_reputation = int(required_faction[0].getAttribute("rep"))
		
		classes = dom.getElementsByTagName("class")
		self.class_mask = -1
		if classes:
			for k in classes:
				self.class_mask += CLASSES[k.firstChild.data]
			self.class_mask += 1
		
		races = dom.getElementsByTagName("race")
		self.race_mask = -1
		if races:
			for k in races:
				self.race_mask += RACES[k.firstChild.data]
			self.race_mask += 1
		
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
				setattr(self, "socket_%i" % i, SOCKETS[e.getAttribute("color")])
			sb = _getNode("socketMatchEnchant", dom)
			if sb:
				try:
					self.socketbonus = Enchant.objects.filter(name=sb)[:1][0]._id
				except IndexError:
					print "Socket bonus not found:", repr(sb)
		
		spells = dom.getElementsByTagName("spellData")
		if spells:
			i = 0
			spells = spells[0]
			createdItem = spells.getElementsByTagName("itemTooltip")
			if createdItem:
				createdItem = createdItem[0]
				spells = [node for node in spells.childNodes if node.nodeName == "spell"]
				for _i, e in enumerate(spells):
					if createdItem.parentNode == e:
						spells.pop(_i)
						i += 1
						try:
							self.spell1 = Spell.objects.filter(created_item__name=_getNode("name", createdItem))[:1][0].id
						except IndexError:
							self.spell1 = 2 # dead spell
						self.note = _getNode("desc", e)
						self.spellcharges1 = _getNode("charges", e, int)
						self.spelltrigger1 = 6 # learning
						break
			else:
				spells = spells.getElementsByTagName("spell")
			
			for e in spells:
				i+=1
				trigger = _getNode("trigger", e, int)
				text = _getNode("desc", e)
				charges = _getNode("charges", e, int)
				setattr(self, "spellcharges%i" % i, charges)
				setattr(self, "spelltrigger%i" % i, trigger)
				
				if trigger == 6: # learning
					self.note = text
					setattr(self, "spell%i" % i, 2) # use a dead spell
					continue
				
				try:
					setattr(self, "spell%i" % i, Spell.objects.filter(description=text)[:1][0].id)
				except IndexError:
					try:
						_text = text.split("\n")[0][:-1]
						setattr(self, "spell%i" % i, Spell.objects.filter(description__istartswith=_text)[:1][0].id)
					except IndexError:
						print "Spell not found: %r" % text
		
		itemset = dom.getElementsByTagName("setData")
		if itemset:
			itemset = _getNode("name", itemset[0])
			self.itemset = ItemSet.objects.filter(name=itemset)[:1][0].id
		
		if ArmoryItem.ITEM_DBC and self._id in ArmoryItem.ITEM_DBC:
			item = ArmoryItem.ITEM_DBC[self._id]
			self.category = item.category
			self.subcategory = item.subcategory
			self.depclass = item.depclass
			self.display = item.display
			self.slot = item.slot
			self.sheath_type = item.sheath_type
	
	
	def assignTo(self, f):
		kwargs = self.__dict__
		kwargs["_id"] = self._id
		f[self._id] = kwargs


def main():
	try:
		OUT = sys.argv[2]
	except IndexError:
		print "Usage: %s /path/to/dump armory-itemcache.wdb --item-dbc=/path/to/Item.dbc" % (sys.argv[0])
		exit()
	
	ls = os.listdir(sys.argv[1])
	ls.sort()
	d = {}
	i = 0
	
	if args.item_dbc:
		ArmoryItem.ITEM_DBC = wdbc.fopen(args.item_dbc, build=args.build)
	
	for f in ls:
		i += 1
		try:
			id = int(f.split("i=")[1])
		except IndexError:
			continue
		
		txt = minidom.parse("%s/%s" % (sys.argv[1], f))
		
		print "Reading %s - %i / %i" % (f, i, len(ls))
		
		if f.startswith("item-tooltip"):
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
	
	f = wdbc.new(name="itemcache", build=args.build)
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
