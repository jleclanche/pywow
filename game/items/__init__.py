# -*- coding: utf-8 -*-
"""
Items
 - itemcache.wdb (1.x->4.x)
 - Item.dbc + itemcache.wdb (2.x->4.x)
 - Item-sparse.db2 (4.x)
"""
from .. import *
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
	def __init__(self, obj, renderer=None):
		self.obj = obj
		self.renderer = renderer
		self.keys = []
		self.values = []
	
	def render(self):
		hideNote = False # for recipes, mounts, etc
		
		self.append("name", self.obj.name, self.obj.getQualityColor())
		
		#if self.obj.quality and env.colorblind:
		#	self.append("quality", self.obj.getQuality())
		
		# glyph
		
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
			# XXX Skill(633).getName()
			self.append("locked", LOCKED)
			self.append("lock", ITEM_MIN_SKILL % ("Lockpicking", lockSkillLevel))
		
		# subclass
		
		self.append("slot", self.obj.getSlotText())
		
		# damage
		
		# armor
		
		# block
		
		# stats
		
		# enchant
		
		for socket in self.obj.getSockets():
			self.append("socket", "%i socket" % (socket))
		
		self.append("gemProperties", self.obj.getGemProperties())
		
		# random ench
		
		# duration
		
		self.append("requiredHoliday", self.obj.getRequiredHoliday())
		
		# race/class reqs
		
		minDurability, maxDurability = self.obj.getDurability()
		if minDurability:
			self.append("durability", DURABILITY_TEMPLATE % (minDurability, maxDurability))
		
		if self.obj.required_level > 1:
			self.append("requiredLevel", ITEM_MIN_LEVEL % (self.obj.required_level))
		
		if self.obj.showItemLevel():
			self.append("level", ITEM_LEVEL % (self.obj.level))
		
		# (required arena rating)
		
		requiredSkill, requiredSkillLevel = self.obj.getRequiredSkill()
		if requiredSkill and requiredSkillLevel:
			self.append("requiredSkill", ITEM_MIN_SKILL % (requiredSkill, requiredSkillLevel))
		
		self.formatAppend("requiredSpell", ITEM_REQ_SKILL, self.obj.getRequiredSpell())
		
		requiredFaction, requiredReputation = self.obj.getRequiredFaction()
		if requiredFaction: # and requiredReputation?
			self.append("requiredFaction", ITEM_REQ_REPUTATION % (requiredFaction, requiredReputation))
		
		# special stats
		
		for spell, trigger, charges, cooldown, category, cooldownCategory in self.obj.getSpells():
			if spell:
				triggerText = self.obj.getTriggerText(trigger)
				if triggerText is None:
					continue
				
				if trigger == TRIGGER_LEARNING:
					hideNote = True
					text = self.obj.note or "(null)"
				else:
					text = spell.getDescription()
				
				if not text:
					continue
				
				if triggerText:
					text = triggerText + " " + text
				
				self.append("spells", text, GREEN)
		
		# charges
		
		# itemset
		
		if not hideNote:
			self.append("note", self.obj.note and '"%s"' % (self.obj.note))
		
		# openable
		
		if self.obj.isReadable():
			self.append("page", ITEM_CAN_BE_READ, GREEN)
		
		# disenchanting
		
		if self.obj.sell_price:
			g, s, c = price(self.obj.sell_price)
			text = SELL_PRICE + ":"
			if g: text += " %i {gold}" % (g)
			if s: text += " %i {silver}" % (s)
			if c: text += " %i {copper}" % (c)
			self.append("sellPrice", text)
		
		ret = self.values
		self.values = []
		return ret


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
		ret.category = item._raw("category")
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
	
	def getDurability(self, row):
		# return min, max
		return row.durability, row.durability
	
	def getGemProperties(self, row):
		if row.gem_properties and row.gem_properties.enchant:
			return row.gem_properties.enchant.name_enus
		return ""
	
	def getLockInfo(self, row):
		row = row.lock
		if row:
			for i in range(1, 9):
				type = getattr(row, "type_%i" % (i))
				if type:
					level = getattr(row, "required_skill_level_%i" % (i))
					return True, type, level
		return False, 0, 0
	
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
	
	def getRequiredSkill(self, row):
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
		from ..spells import Spell, SpellProxy
		Spell.initProxy(SpellProxy)
		spells = ("spell_%i", "spell_trigger_%i", "spell_charges_%i", "spell_cooldown_%i", "spell_category_%i", "spell_cooldown_category_%i")
		ret = []
		for i in range(1, 6):
			r = []
			for k in spells:
				r.append(row._raw(k % (i)))
			
			r[0] = r[0] and Spell(r[0])
			# Only return valid spells
			if r[0]:
				ret.append(r)
		
		return ret
	
	def getSockets(self, row):
		ret = []
		for i in range(1, 4):
			socket = getattr(row, "socket_%i" % (i))
			print ">>>>>>", socket, bool(socket)
			if socket:
				ret.append(socket)
		return ret
	
	def showItemLevel(self, row):
		return row.category in (2, 4, 6)
