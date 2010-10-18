# -*- coding: utf-8 -*-
"""
Items
 - itemcache.wdb (1.x->4.x)
 - Item.dbc + itemcache.wdb (2.x->4.x)
 - Item-sparse.db2 (4.x)
"""

from __future__ import division
from .. import *
from .. import durationstring
from ..globalstrings import *


TRIGGER_ONUSE     = 0
TRIGGER_ONEQUIP   = 1
TRIGGER_ONPROC    = 2
TRIGGER_INVENTORY = 5
TRIGGER_LEARNING  = 6

def price(value):
	if not value:
		return 0, 0, 0
	g = divmod(value, 10000)[0]
	s = divmod(value, 100)[0] % 100
	c = value % 100
	return g, s, c

class Item(Model):
	
	def getQualityColor(self):
		return {
			0: GREY,   # Poor
			1: WHITE,  # Common
			2: GREEN,  # Uncommon
			3: BLUE,   # Rare
			4: PURPLE, # Epic
			5: ORANGE, # Legendary
			6: GOLD,   # Artifact
			7: GOLD,   # Heirloom
		}.get(self.quality, WHITE)
	
	def getBindingText(self):
		if self.isAccountBound():
			return ITEM_BIND_TO_ACCOUNT
		
		return {
			1: ITEM_BIND_ON_PICKUP,
			2: ITEM_BIND_ON_EQUIP,
			3: ITEM_BIND_ON_USE,
			4: ITEM_BIND_QUEST,
		}.get(self.bind, "")
	
	def getSlotText(self):
		return {
			#INVTYPE_WEAPONMAINHAND_PET = "Main Attack"
			 1: INVTYPE_HEAD,
			 2: INVTYPE_NECK,
			 3: INVTYPE_SHOULDER,
			 4: INVTYPE_BODY,
			 5: INVTYPE_CHEST,
			 6: INVTYPE_WAIST,
			 7: INVTYPE_LEGS,
			 8: INVTYPE_FEET,
			 9: INVTYPE_WRIST,
			10: INVTYPE_HAND,
			11: INVTYPE_FINGER,
			12: INVTYPE_TRINKET,
			13: INVTYPE_WEAPON,
			14: INVTYPE_SHIELD,
			15: INVTYPE_RANGED,
			16: INVTYPE_CLOAK, # INVTYPE_BACK ?
			17: INVTYPE_2HWEAPON,
			18: INVTYPE_BAG,
			19: INVTYPE_TABARD,
			20: INVTYPE_ROBE,
			21: INVTYPE_WEAPONMAINHAND,
			22: INVTYPE_WEAPONOFFHAND,
			23: INVTYPE_HOLDABLE,
			24: INVTYPE_AMMO,
			25: INVTYPE_THROWN,
			26: INVTYPE_RANGEDRIGHT,
			#27: INVTYPE_QUIVER,
			28: INVTYPE_RELIC,
		}.get(self.slot, "")
	
	def getTooltip(self):
		return ItemTooltip(self)
	
	def getTriggerText(self, trigger):
		"""
		Return the trigger text for an item spell trigger
		An empty string means no trigger text.
		None means the trigger should be hidden.
		"""
		if trigger == TRIGGER_ONUSE:
			return ITEM_SPELL_TRIGGER_ONUSE
		if trigger == TRIGGER_ONEQUIP:
			return ITEM_SPELL_TRIGGER_ONEQUIP
		if trigger == TRIGGER_ONPROC:
			return ITEM_SPELL_TRIGGER_ONPROC
		if trigger == TRIGGER_INVENTORY:
			return ""
		if trigger == TRIGGER_LEARNING:
			return ITEM_SPELL_TRIGGER_ONUSE


class ItemTooltip(Tooltip):
	def tooltip(self):
		hideNote = False # for recipes, mounts, etc
		
		self.append("name", self.obj.name, self.obj.getQualityColor())
		
		#if self.obj.quality and env.colorblind:
		#	self.append("quality", self.obj.getQuality())
		
		glyph = self.obj.getGlyph()
		if glyph:
			self.append("glyph", glyph.getTypeText(), color=CYAN)
		
		if self.obj.isHeroic():
			self.append("heroic", ITEM_HEROIC, GREEN)
		
		if self.obj.isChart():
			self.append("chart", ITEM_SIGNABLE, GREEN)
		
		self.append("requiredZone", self.obj.getRequiredZone())
		self.append("requiredInstance", self.obj.getRequiredInstance())
		
		if self.obj.isConjured():
			self.append("conjured", ITEM_CONJURED)
		
		self.append("binding", self.obj.getBindingText())
		
		if self.obj.isUniqueEquipped():
			self.append("unique", ITEM_UNIQUE_EQUIPPABLE)
		elif self.obj.unique:
			if self.obj.unique > 1:
				self.append("unique", ITEM_UNIQUE_MULTIPLE % (self.obj.unique))
			else:
				self.append("unique", ITEM_UNIQUE)
		elif self.obj.unique_category:
			pass
		
		if self.obj.starts_quest:
			self.append("startsQuest", ITEM_STARTS_QUEST)
		
		isLocked, lockType, lockSkillLevel = self.obj.getLockInfo()
		if isLocked:
			self.append("locked", LOCKED, RED)
			self.append("lock", ITEM_MIN_SKILL % ("Lockpicking", lockSkillLevel), RED)
		
		slot = self.obj.getSlotText()
		bagSlots = self.obj.getBagSlots()
		subClassId, subClassName = self.obj.getSubClassInfo()
		if slot:
			if bagSlots:
				self.append("slot", CONTAINER_SLOTS % (bagSlots, slot))
			elif self.showSubClass():
				self.append("slot", slot)
				self.append("subclass", subClassName, side=Tooltip.RIGHT)
			else:
				self.append("slot", slot)
		elif self.showSubClass():
			self.append("subclass", subClassName)
		
		damageMin, damageMax, speed = self.obj.getDamageInfo()
		if damageMax:
			speed = speed / 1000
			dps = (damageMin + damageMax) / (2 * speed)
			self.append("damage", DAMAGE_TEMPLATE % (damageMin, damageMax))
			self.append("speed", "%s %.2f" % (SPEED, speed), side=Tooltip.RIGHT)
			self.append("dps", DPS_TEMPLATE % (dps))
		
		armor, extraArmor = self.obj.getArmor()
		if armor:
			if extraArmor:
				self.append("armor", ARMOR_TEMPLATE % (armor + extraArmor), color=GREEN)
			else:
				self.append("armor", ARMOR_TEMPLATE % (armor))
		
		block = self.obj.getBlock()
		if block:
			self.append("block", SHIELD_BLOCK_TEMPLATE % (block))
		
		for stat, amount in self.obj.getStats():
			text = stat.getText(amount)
			if not stat.isSpecial():
				self.append("stat", stat.getText(amount))
		
		# enchant
		
		for socket in self.obj.getSockets():
			self.append("socket", socket.getText(), color=GREY)
		
		socketBonus = self.obj.getSocketBonus()
		if socketBonus:
			self.append("socketBonus", ITEM_SOCKET_BONUS % (socketBonus.getName()), color=GREY)
		
		self.append("gemProperties", self.obj.getGemProperties())
		
		# random ench
		
		duration = self.obj.getDuration()
		if duration:
			duration = durationstring.duration(duration, durationstring.SHORT)
			self.append("duration", ITEM_DURATION % (duration))
		
		holiday = self.obj.getRequiredHoliday()
		if holiday:
			self.append("requiredHoliday", ITEM_REQ_SKILL % (self.obj.getRequiredHoliday()))
		
		# race reqs
		
		requiredClasses = self.obj.getRequiredClasses()
		if requiredClasses:
			self.append("requiredClasses", ITEM_CLASSES_ALLOWED % (", ".join(cls.getName() for cls in requiredClasses)))
		
		minDurability, maxDurability = self.obj.getDurabilityInfo()
		if minDurability:
			self.append("durability", DURABILITY_TEMPLATE % (minDurability, maxDurability))
		
		if self.obj.required_level > 1:
			self.append("requiredLevel", ITEM_MIN_LEVEL % (self.obj.required_level))
		
		if self.showItemLevel():
			self.append("level", ITEM_LEVEL % (self.obj.level))
		
		# (required arena rating)
		
		requiredSkill, requiredSkillLevel = self.obj.getRequiredSkillInfo()
		if requiredSkill and requiredSkillLevel:
			self.append("requiredSkill", ITEM_MIN_SKILL % (requiredSkill, requiredSkillLevel))
		
		self.formatAppend("requiredSpell", ITEM_REQ_SKILL, self.obj.getRequiredSpell())
		
		requiredFaction, requiredReputation = self.obj.getRequiredFaction()
		if requiredFaction: # and requiredReputation?
			self.append("requiredFaction", ITEM_REQ_REPUTATION % (requiredFaction, requiredReputation))
		
		for stat, amount in self.obj.getStats():
			text = stat.getText(amount)
			if stat.isSpecial() and not stat.isExtraArmor():
				self.append("specialStat", "%s %s" % (ITEM_SPELL_TRIGGER_ONEQUIP, text), color=GREEN)
		
		for spell, trigger, charges, cooldown, category, cooldownCategory, createdItem in self.obj.getSpells():
			if spell:
				triggerText = self.obj.getTriggerText(trigger)
				if triggerText is None:
					continue
				
				glyph = spell.getGlyphLearned()
				
				if trigger == TRIGGER_LEARNING:
					if glyph:
						text = "%s\n\n%s" % (ITEM_GLYPH_ONUSE, glyph.getDescription())
					
					else:
						hideNote = True
						text = self.obj.note or "(null)"
				else:
					text = spell.getDescription()
				
				if text:
					if triggerText:
						text = triggerText + " " + text
					
					self.append("spells", text, GREEN)
				
				if createdItem:
					self.appendEmptyLine()
					self.append("createdItem", ItemTooltip(createdItem))
					self.appendEmptyLine()
					reagents = spell.getReagents()
					if reagents:
						text = []
						for item, amount in reagents:
							if amount == 1:
								text.append(item.name)
							else:
								text.append("%s (%d)" % (item.name, amount))
						
						self.append("reagents", "Requires %s" % (", ".join(text))) # FIXME globalstring
		
		# charges
		
		itemSet = self.obj.getItemSet()
		if itemSet:
			from ..itemsets import ItemSetTooltip
			self.appendEmptyLine()
			self.append("itemSet", ItemSetTooltip(itemSet))
		
		if not hideNote:
			self.append("note", self.obj.note and '"%s"' % (self.obj.note), YELLOW)
		
		# openable
		
		if self.obj.isReadable():
			self.append("page", ITEM_CAN_BE_READ, GREEN)
		
		# disenchanting
		
		if self.obj.sell_price:
			g, s, c = price(self.obj.sell_price)
			text = SELL_PRICE + ":"
			if g: text += " %ig" % (g)
			if s: text += " %is" % (s)
			if c: text += " %ic" % (c)
			self.append("sellPrice", text)
		
		ret = self.values
		self.values = []
		return ret
	
	def showItemLevel(self):
		return self.obj.category.id in (2, 4, 5, 6)
	
	def showSubClass(self):
		category = self.obj.category.id
		subcategory = self.obj.subcategory
		slot = self.obj.slot
		if category in (2, 4, 6):
			if slot == 16: # cloak
				return False
			if category == 2 and subcategory == 14:
				return False
			if category == 4 and subcategory == 0:
				return False
			return True
		if category == 15 and subcategory == 5:
			return True
		return False


class ItemProxy(object):
	"""
	WDBC proxy for items
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("Item-sparse.db2", build=12942)
		self.__item = wdbc.get("Item.db2", build=12942)
	
	
	def get(self, id):
		ret = self.__file[id]
		item = self.__item[id]
		ret.category = item.category
		ret.subcategory = item.subcategory
		return ret
	
	def isAccountBound(self, row):
		return row.flags.account_bound
	
	def isChart(self, row):
		return row.flags.chart
	
	def isConjured(self, row):
		return row.flags.conjured
	
	def isHeroic(self, row):
		return row.flags.heroic
	
	def isReadable(self, row):
		return bool(row._raw("page"))
	
	def isUniqueEquipped(self, row):
		return row.flags.unique_equipped
	
	def getArmor(self, row):
		from . import levels
		#return row.armor # old
		return levels.getArmor(row.level, row.category.id, row.subcategory, row.quality, row.slot), self.getExtraArmor(row)
	
	def getBagSlots(self, row):
		return row.bag_slots
	
	def getBlock(self, row):
		#return row.block # old
		return 0
	
	def getDamageInfo(self, row):
		from . import levels
		damageMin, damageMax = levels.getDamage(row.level, row.category.id, row.subcategory, row.quality, row.slot, row.flags, row.speed)
		return damageMin, damageMax, row.speed
	
	def getDurabilityInfo(self, row):
		# return min, max
		return row.durability, row.durability
	
	def getDuration(self, row):
		return row.duration
	
	def getExtraArmor(self, row):
		ret = 0
		for stat, amount in self.getStats(row):
			if stat.isExtraArmor():
				ret += amount
		return ret
	
	def getGemProperties(self, row):
		if row.gem_properties and row.gem_properties.enchant:
			return row.gem_properties.enchant.name_enus
		return ""
	
	def getGlyph(self, row):
		for spellInfo in self.getSpells(row):
			glyph = spellInfo[0].getGlyphLearned()
			if glyph:
				return glyph
	
	def getItemSet(self, row):
		id = row._raw("itemset")
		if id:
			from ..itemsets import ItemSet
			return ItemSet(id)
	
	def getLockInfo(self, row):
		row = row.lock
		if row:
			for i in range(1, 9):
				type = getattr(row, "type_%i" % (i))
				if type:
					level = getattr(row, "required_skill_level_%i" % (i))
					return True, type, level
		return False, 0, 0
	
	def getName(self, row):
		return row.name
	
	def getRequiredClasses(self, row):
		from ..classes import ChrClass
		return ChrClass.getClassesFromMask(row.class_mask)
	
	def getRequiredFaction(self, row):
		requiredReputation = globals().get("FACTION_STANDING_LABEL%i" % (row.required_reputation + 1), "")
		if row.required_faction:
			return row.required_faction.name_enus, requiredReputation
		return "", requiredReputation
	
	def getRequiredHoliday(self, row):
		if row.required_holiday:
			return row.required_holiday.name.name_enus
		return ""
	
	def getRequiredInstance(self, row):
		if row._raw("required_instance") and row.required_instance:
			return row.required_instance.name_enus
		return ""
	
	def getRequiredSkillInfo(self, row):
		requiredSkillLevel = row.required_skill_level
		if row.required_skill:
			return row.required_skill.name_enus, requiredSkillLevel
		return "", requiredSkillLevel
	
	def getRequiredSpell(self, row):
		if row.required_spell:
			return row.required_spell.name_enus
		return ""
	
	def getRequiredZone(self, row):
		if row.required_zone:
			return row.required_zone.name_enus
		return ""
	
	def getSpells(self, row):
		from ..spells import Spell
		spells = ("spell_%i", "spell_trigger_%i", "spell_charges_%i", "spell_cooldown_%i", "spell_category_%i", "spell_cooldown_category_%i")
		ret = []
		for i in range(1, 6):
			r = []
			for k in spells:
				r.append(row._raw(k % (i)))
			
			spell = r[0]
			if spell:
				r[0] = spell = Spell(spell)
				r.append(spell.getCreatedItem())
				ret.append(r)
		
		return ret
	
	def getSocketBonus(self, row):
		id = row._raw("socket_bonus")
		if id:
			from ..enchants import Enchant
			return Enchant(id)
	
	def getSockets(self, row):
		from .sockets import Socket
		ret = []
		for i in range(1, 4):
			socket = getattr(row, "socket_%i" % (i))
			if socket:
				ret.append(Socket(socket))
		return ret
	
	def getStats(self, row):
		from ..stats import Stat
		ret = []
		for i in range(1, 10):
			stat = getattr(row, "stats_id_%i" % (i))
			amount = getattr(row, "stats_amount_%i" % (i))
			if amount:
				ret.append((Stat(stat), amount))
		return ret
	
	def getSubClassInfo(self, row):
		category = row.category.itemsubclass__category
		subcategory = None
		for x in category:
			if x.subcategory == row.subcategory:
				subcategory = x
		if subcategory:
			return subcategory.id, subcategory.name_enus
		return None, None

Item.initProxy(ItemProxy)
