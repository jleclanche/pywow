#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..base import DBStructure, Skeleton
from ..fields import *

####################
## WDB structures ##
####################

class CreatureCache(DBStructure):
	"""
	creaturecache.wdb
	NPC/mob data
	"""
	signature = "BOMW"
	base = Skeleton(
		IDField(),
		RecLenField(),
		StringField("name"),
		StringField("name2"),
		StringField("name3"),
		StringField("name4"),
		StringField("title"),
		StringField("cursor"),
		BitMaskField("flags"),
		IntegerField("category"), #dragonkin, ...
		IntegerField("family"), # hunter pet family
		IntegerField("type"), # elite, rareelite, boss, rare
		IntegerField(), #spellicon?
		IntegerField("model"), #fkey
		IntegerField("model2"),
		IntegerField("model3"),
		IntegerField("model4"),
		FloatField(),
		FloatField(),
		ByteField("leader"),
	)

	def changed_9614(self, base):
		base.insert_field(IntegerField(), before="model")
		base.append_fields(
			IntegerField(),
			IntegerField(),
			IntegerField(),
			IntegerField(),
			IntegerField(),
		)

	def changed_10072(self, base):
		self.changed_9614(base)
		base.append_fields(
			UnknownField(),
			UnknownField(),
		)



class GameObjectCache(DBStructure):
	"""
	gameobjectcache.wdb
	World object data
	"""
	signature = "BOGW"
	base = Skeleton(
		IDField(),
		RecLenField(),
		IntegerField("type"),
		ForeignKey("display", "gameobjectdisplayinfo"),
		StringField("name"),
		StringField("name2"),
		StringField("name3"),
		StringField("name4"),
		StringField(),
		StringField("description"),
		StringField(),
		IntegerField("health"), # not always
		IntegerField("action"),
		IntegerField(), # gfk: spell, envdmg?
		BitMaskField(),
		BitMaskField(),
		BitMaskField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField("scale"),
		ForeignKey("loot", "item"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)

	def changed_10314(self, base):
		"""
		TODO
		"""
		base.append_fields(
			UnknownField(),
			UnknownField(),
		)


class ItemCache(DBStructure):
	"""
	itemcache.wdb
	Item data, cached on in-game item query
	"""
	signature = "BDIW"

	flags = ["unk1", "conjured", "openable", "heroic",
		"deprecated", "totem", "unk64", "no_equip_cooldown",
		"unk256", "wrapper", "ignore_bagspace", "group_loot",
		"refundable", "chart", "unk16384", "unk32768",
		"unk65536", "unk131072", "prospectable", "unique_equipped",
		"unk1048576", "usable_in_arena", "thrown", "unk8388608",
		"unk16777216", "unk33554432", "unk67108864", "account_bound",
		"enchant_scroll", "millable"]

	classes = ["warrior", "paladin", "hunter", "rogue", "priest",
		"deathknight", "shaman", "mage", "warlock", "", "druid"]

	races = ["human", "orc", "dwarf", "nightelf", "undead", "tauren",
		"gnome", "troll", "", "bloodelf", "draenei", "",
		"", "", ""]

	base = Skeleton(
		IDField(),
		RecLenField(),
		ForeignKey("category", "itemclass"),
		ForeignKey("subcategory", "itemsubclass"),
		StringField("name"),
		StringField("name2"),
		StringField("name3"),
		StringField("name4"),
		ForeignKey("display", "itemdisplayinfo"),
		IntegerField("quality"),
		BitMaskField("flags", flags=flags),
		MoneyField("buyprice"),
		MoneyField("sellprice"),
		IntegerField("slot"),
		BitMaskField("classreq", flags=classes),
		BitMaskField("racereq", flags=races),
		IntegerField("level"),
		IntegerField("levelreq"),
		ForeignKey("skillreq", "skillline"),
		IntegerField("skilllevelreq"),
		ForeignKey("spellreq", "spell"),
		IntegerField("pvprankreq"),
		IntegerField("pvpmedalreq"),
		ForeignKey("factionreq", "faction"),
		IntegerField("reputationreq"),
		IntegerField("unique"),
		IntegerField("stack"),
		IntegerField("bagslots"),
#		DynamicFields("stats", [(
#			(IntegerField, "id"),
#			(IntegerField, "amt"),
#		), 10]),
		IntegerField("stats_id_dyn1"),
		IntegerField("stats_amt_dyn1"),
		IntegerField("stats_id_dyn2"),
		IntegerField("stats_amt_dyn2"),
		IntegerField("stats_id_dyn3"),
		IntegerField("stats_amt_dyn3"),
		IntegerField("stats_id_dyn4"),
		IntegerField("stats_amt_dyn4"),
		IntegerField("stats_id_dyn5"),
		IntegerField("stats_amt_dyn5"),
		IntegerField("stats_id_dyn6"),
		IntegerField("stats_amt_dyn6"),
		IntegerField("stats_id_dyn7"),
		IntegerField("stats_amt_dyn7"),
		IntegerField("stats_id_dyn8"),
		IntegerField("stats_amt_dyn8"),
		IntegerField("stats_id_dyn9"),
		IntegerField("stats_amt_dyn9"),
		IntegerField("stats_id_dyn10"),
		IntegerField("stats_amt_dyn10"),
		FloatField("dmgmin1"),
		FloatField("dmgmax1"),
		IntegerField("dmgtype1"),
		FloatField("dmgmin2"),
		FloatField("dmgmax2"),
		IntegerField("dmgtype2"),
		FloatField("dmgmin3"),
		FloatField("dmgmax3"),
		IntegerField("dmgtype3"),
		FloatField("dmgmin4"),
		FloatField("dmgmax4"),
		IntegerField("dmgtype4"),
		FloatField("dmgmin5"),
		FloatField("dmgmax5"),
		IntegerField("dmgtype5"),
		IntegerField("armor"),
		IntegerField("holyresist"),
		IntegerField("fireresist"),
		IntegerField("natureresist"),
		IntegerField("frostresist"),
		IntegerField("shadowresist"),
		IntegerField("arcaneresist"),
		IntegerField("speed"),
		IntegerField("ammo"),
		FloatField(),
		ForeignKey("spell1", "spell"),
		IntegerField("spelltrigger1"),
		IntegerField("spellcharges1"),
		IntegerField("spellcooldown1"),
		IntegerField("spellcategory1"),
		IntegerField("spellcooldowncategory1"),
		ForeignKey("spell2", "spell"),
		IntegerField("spelltrigger2"),
		IntegerField("spellcharges2"),
		IntegerField("spellcooldown2"),
		IntegerField("spellcategory2"),
		IntegerField("spellcooldowncategory2"),
		ForeignKey("spell3", "spell"),
		IntegerField("spelltrigger3"),
		IntegerField("spellcharges3"),
		IntegerField("spellcooldown3"),
		IntegerField("spellcategory3"),
		IntegerField("spellcooldowncategory3"),
		ForeignKey("spell4", "spell"),
		IntegerField("spelltrigger4"),
		IntegerField("spellcharges4"),
		IntegerField("spellcooldown4"),
		IntegerField("spellcategory4"),
		IntegerField("spellcooldowncategory4"),
		ForeignKey("spell5", "spell"),
		IntegerField("spelltrigger5"),
		IntegerField("spellcharges5"),
		IntegerField("spellcooldown5"),
		IntegerField("spellcategory5"),
		IntegerField("spellcooldowncategory5"),
		IntegerField("bind"),
		StringField("note"),
		ForeignKey("page", "pagetextcache"),
		ForeignKey("pagelanguage", "languages"),
		ForeignKey("pagestationery", "stationery"),
		ForeignKey("queststart", "questcache"),
		ForeignKey("lock", "lock"),
		IntegerField("material"),
		IntegerField("sheathtype"),
		ForeignKey("randomenchantment", "itemrandomproperties"),
		IntegerField("block"),
		ForeignKey("itemset", "itemset"),
		IntegerField("durability"),
		ForeignKey("zonebind", "areatable"),
		ForeignKey("instancebind", "map"),
		IntegerField("bagcategory"),
		ForeignKey("toolcategory", "totemcategory"),
		BitMaskField("socket1"),
		IntegerField("socket1info"),
		BitMaskField("socket2"),
		IntegerField("socket2info"),
		BitMaskField("socket3"),
		IntegerField("socket3info"),
		ForeignKey("socketbonus", "spellitemenchantment"),
		ForeignKey("gemproperties", "gemproperties"),
		IntegerField("extendedcost"),
	)

	def changed_5875(self, base):
		"""
		- New disenchant IntegerField
		  UNKNOWN BUILD
		"""
		base.append_fields(IntegerField("disenchant"))

	def changed_6022(self, base):
		"""
		- New unknown IntegerField before name field
		"""
		self.changed_5875(base)
		base.insert_field(IntegerField("depclass"), before="name")

	def changed_6213(self, base):
		"""
		- New unknown IntegerField
		"""
		self.changed_6022(base)
		base.insert_field(ForeignKey("randomenchantment2", "itemrandomsuffix"), before="block")

	def changed_6577(self, base):
		"""
		- New armordmgmod FloatField
		"""
		self.changed_6213(base)
		base.append_fields(FloatField("armordmgmod"))

	def changed_7382(self, base):
		"""
		- New ItemCondExtCosts fkey before disenchant field
		  UNKNOWN BUILD
		"""
		self.changed_6577(base)
		base.insert_field(IntegerField("extendedcostcond"), before="disenchant")


	def changed_7994(self, base):
		"""
		- Removed extendedcost and extendedcostcond fields
		  UNKNOWN BUILD
		"""
		self.changed_7382(base)
		base.delete_fields("extendedcost", "extendedcostcond")

	def changed_8268(self, base):
		"""
		- Added duration field at the end, replacing the old server overwrite model
		  This might be changed_8209.
		"""
		self.changed_7994(base)
		base.append_fields(DurationField("duration", unit="seconds"))

	def changed_8391(self, base):
		"""
		- New uniquecategory field at the end, fkey of new ItemLimitCategory.dbc file
		"""
		self.changed_8268(base)
		base.append_fields(ForeignKey("uniquecategory", "itemlimitcategory"))

	def changed_8471(self, base):
		"""
		- Made the 20 stats column dynamic
		- New scalingdist and scalingflags fields after the new stats columns
		"""
		self.changed_8391(base)
		base.delete_fields(
			"stats_id_dyn1", "stats_amt_dyn1",
			"stats_id_dyn2", "stats_amt_dyn2",
			"stats_id_dyn3", "stats_amt_dyn3",
			"stats_id_dyn4", "stats_amt_dyn4",
			"stats_id_dyn5", "stats_amt_dyn5",
			"stats_id_dyn6", "stats_amt_dyn6",
			"stats_id_dyn7", "stats_amt_dyn7",
			"stats_id_dyn8", "stats_amt_dyn8",
			"stats_id_dyn9", "stats_amt_dyn9",
			"stats_id_dyn10", "stats_amt_dyn10",
		)
		base.insert_field(DynamicFields("stats", [(
			(IntegerField, "id"),
			(IntegerField, "amt"),
		), 10]), before="dmgmin1")
		base.insert_field(ForeignKey("scaling_stats", "scalingstatdistribution"), before="dmgmin1")
		base.insert_field(BitMaskField("scaling_flags"), before="dmgmin1")

	def changed_8478(self, base):
		self.changed_8268(base)

	def changed_8770(self, base):
		self.changed_8471(base)

	def changed_9614(self, base):
		"""
		- Deleted unused dmgmin, dmgmax and dmgtype 3-5 fields
		- Added new unknown IntegerField at the end
		"""
		self.changed_8770(base)
		base.delete_fields("dmgmin3", "dmgmax3", "dmgtype3",
			"dmgmin4", "dmgmax4", "dmgtype4",
			"dmgmin5", "dmgmax5", "dmgtype5")
		base.append_fields(ForeignKey("holidayreq", "holidays"))

	def changed_10026(self, base):
		self.changed_9614(base)
		base.insert_field(BitMaskField("flags2"), before="buyprice")


class ItemNameCache(DBStructure):
	"""
	itemnamecache.wdb
	Cached itemset data
	"""
	signature = "BDNW"
	base = Skeleton(
		IDField(),
		RecLenField(),
		StringField("name"),
		IntegerField("slot"),
	)


class ItemTextCache(DBStructure):
	"""
	itemtextcache.wdb
	Mails and misc
	"""
	signature = "XTIW"
	base = Skeleton(
		IDField(),
		RecLenField(),
		StringField(),
	)


class NPCCache(DBStructure):
	"""
	npccache.wdb
	NPC gossip data
	"""
	signature = "BDNW"
	base = Skeleton(
		IDField(),
		RecLenField(),
		FloatField(),
		StringField("text1"),
		StringField("text1"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text2"),
		StringField("text2"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text3"),
		StringField("text3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text4"),
		StringField("text4"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text5"),
		StringField("text5"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text6"),
		StringField("text6"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text7"),
		StringField("text7"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		StringField("text8"),
		StringField("text8"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class QuestCache(DBStructure):
	"""
	questcache.wdb
	Quest data, cached on in-game quest query
	"""
	signature = "TSQW"

	flags = ["unk1", "unk2", "unk4", "requires_server_event",
		"unused16", "turnin_invisible_without", "raid", "requires_burningcrusade",
		"unk256", "unk512", "flagger", "unk2048",
		"daily", "flags_pvp", "unk16384"]

	get_kill_relation = lambda x, value: value == value & 0x7fffffff and "creaturecache" or "gameobjectcache"
	get_kill_value = lambda x, value: value & 0x7fffffff

	base = Skeleton(
		IDField(),
		RecLenField(),
		ForeignKey("self", "questcache"),
		IntegerField("tag"),
		IntegerField("level"),
		IntegerField("category"),
		ForeignKey("type", "questinfo"),
		IntegerField("suggested_players"),
		IntegerField("factionreq1"),
		IntegerField("reputationreq1"),
		IntegerField("factionreq2"),
		IntegerField("reputationreq2"),
		IntegerField("followup"),
		IntegerField("money_reward"),
		IntegerField("money_reward_cap"),
		ForeignKey("spell_reward", "spell"),
		ForeignKey("spell_trigger", "spell"),
		IntegerField("unknown_308"), #added 3.0.8, unused apart from 200 in 13233/13234
		ForeignKey("provided_item", "item"),
		BitMaskField("flags", flags=flags),
		ForeignKey("title_reward", "chartitles"), #added 2.4
		IntegerField("required_player_kills"), #added 8334
		IntegerField("bonus_talents"), #added 8471
		ForeignKey("rewarditem1", "item"),
		IntegerField("rewarditemamt1"),
		ForeignKey("rewarditem2", "item"),
		IntegerField("rewarditemamt2"),
		ForeignKey("rewarditem3", "item"),
		IntegerField("rewarditemamt3"),
		ForeignKey("rewarditem4", "item"),
		IntegerField("rewarditemamt4"),
		ForeignKey("rewarditemchoice1", "item"),
		IntegerField("rewarditemchoiceamt1"),
		ForeignKey("rewarditemchoice2", "item"),
		IntegerField("rewarditemchoiceamt2"),
		ForeignKey("rewarditemchoice3", "item"),
		IntegerField("rewarditemchoiceamt3"),
		ForeignKey("rewarditemchoice4", "item"),
		IntegerField("rewarditemchoiceamt4"),
		ForeignKey("rewarditemchoice5", "item"),
		IntegerField("rewarditemchoiceamt5"),
		ForeignKey("rewarditemchoice6", "item"),
		IntegerField("rewarditemchoiceamt6"),
		ForeignKey("instance", "map"),
		CoordField("xcoord"),
		CoordField("ycoord"),
		UnknownField(),
		StringField("name"),
		StringField("objective"),
		StringField("description"),
		StringField("summary"),
		GenericForeignKey("killreq1", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("killamtreq1"), # TODO changed_9551 (cf commit 151)
		ForeignKey("questitem1", "item"),
		GenericForeignKey("killreq2", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("killamtreq2"),
		ForeignKey("questitem2", "item"),
		GenericForeignKey("killreq3", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("killamtreq3"),
		ForeignKey("questitem3", "item"),
		GenericForeignKey("killreq4", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("killamtreq4"),
		ForeignKey("questitem4", "item"),
		ForeignKey("itemreq1", "item"),
		IntegerField("itemamtreq1"),
		ForeignKey("itemreq2", "item"),
		IntegerField("itemamtreq2"),
		ForeignKey("itemreq3", "item"),
		IntegerField("itemamtreq3"),
		ForeignKey("itemreq4", "item"),
		IntegerField("itemamtreq4"),
		ForeignKey("itemreq5", "item"),
		IntegerField("itemamtreq5"),
		StringField("objectivetext1"),
		StringField("objectivetext2"),
		StringField("objectivetext3"),
		StringField("objectivetext4"),
	)

	def changed_10026(self, base):
		base.insert_field(ForeignKey("itemreq6", "item"), before="objectivetext1")
		base.insert_field(IntegerField("itemamtreq6"), before="objectivetext1")

	def changed_10522(self, base):
		self.changed_10026(base)
		base.insert_field(FloatField("honor_reward"), before="provided_item")
		base.insert_field(UnknownField(), before="rewarditem1")
		base.insert_field(IntegerField("arenareward"), before="rewarditem1")
		base.insert_field(ForeignKey("factionreward1", "faction"), before="instance")
		base.insert_field(ForeignKey("factionreward2", "faction"), before="instance")
		base.insert_field(ForeignKey("factionreward3", "faction"), before="instance")
		base.insert_field(ForeignKey("factionreward4", "faction"), before="instance")
		base.insert_field(ForeignKey("factionreward5", "faction"), before="instance")
		base.insert_field(IntegerField("reputationreward1"), before="instance")
		base.insert_field(IntegerField("reputationreward2"), before="instance")
		base.insert_field(IntegerField("reputationreward3"), before="instance")
		base.insert_field(IntegerField("reputationreward4"), before="instance")
		base.insert_field(IntegerField("reputationreward5"), before="instance")
		base.insert_field(IntegerField("reputationcap1"), before="instance")
		base.insert_field(IntegerField("reputationcap2"), before="instance")
		base.insert_field(IntegerField("reputationcap3"), before="instance")
		base.insert_field(IntegerField("reputationcap4"), before="instance")
		base.insert_field(IntegerField("reputationcap5"), before="instance")
		base.insert_field(StringField("quick_summary"), before="killreq1")

	def changed_10554(self, base):
		self.changed_10522(base)
		base.insert_field(IntegerField("level_obtained"), before="category")
		base.insert_field(UnknownField(), before="money_reward")

	def changed_10772(self, base):
		self.changed_10554(base)
		base.insert_field(UnknownField(), before="killreq2")
		base.insert_field(UnknownField(), before="killreq3")
		base.insert_field(UnknownField(), before="killreq4")
		base.insert_field(UnknownField(), before="itemreq1")


class PageTextCache(DBStructure):
	"""
	pagetextcache.wdb
	Cached page data
	"""
	signature = "XTPW"
	base = Skeleton(
		IDField(),
		RecLenField(),
		StringField("text"),
		ForeignKey("nextpage", "pagetextcache"),
	)


####################
## DBC structures ##
####################

class Achievement(DBStructure):
	"""
	Achievement.dbc
	Achievement data
	"""

	flags = ["statistic", "unk2", "unk4", "unk8",
		"unk16", "unk32", "average", "unk128",
		"serverfirst", "serverfirst_raid", ]

	base = Skeleton(
		IDField(),
		IntegerField("faction"),
		ForeignKey("instance", "map"),
		ForeignKey("parent", "achievement"),
		LocalizedFields("name"),
		LocalizedFields("objective"),
		ForeignKey("category", "achievement_category"),
		IntegerField("points"),
		IntegerField(),
		BitMaskField("flags", flags=flags),
		ForeignKey("icon", "spellicon"),
		LocalizedFields("reward"),
		IntegerField("amountreq"),
		ForeignKey("ancestor", "achievement"),
	)


class Achievement_Category(DBStructure):
	"""
	Achievement_Category.dbc
	Achievement categories
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("parent", "achievement_category"),
		LocalizedFields("name"),
		IntegerField("groupsort"),
	)


class Achievement_Criteria(DBStructure):
	"""
	Achievement_Criteria.dbc
	Achievement criterias
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("achievement", "achievement"),
		IntegerField("type"),
		IntegerField("value1"),
		IntegerField("value2"),
		IntegerField("value3"),
		IntegerField("value4"),
		IntegerField("value5"),
		IntegerField("value6"),
		LocalizedFields("name"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		DurationField("timer", unit="seconds"),
		IntegerField("sort"),
	)


class AnimationData(DBStructure):
	"""
	AnimationData.dbc
	Animation data
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		BitMaskField(),
		BitMaskField(),
		BitMaskField(),
		IntegerField(),
		IntegerField(),
		IntegerField("flying"), # fly = 3
	)


class AreaGroup(DBStructure):
	"""
	AreaGroup.dbc
	TODO
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class AreaPOI(DBStructure):
	"""
	AreaPOI.dbc
	Map/Minimap POIs (no guard data)
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(), #icon neutral normal
		IntegerField(), #icon neutral damaged
		IntegerField(), #icon neutral destroyed
		IntegerField(), #icon alliance normal
		IntegerField(), #icon alliance damaged
		IntegerField(), #icon alliance destroyed
		IntegerField(), #icon horde normal
		IntegerField(), #icon horde damaged
		IntegerField(), #icon horde destroyed
		IntegerField(),
		CoordField(),
		CoordField(),
		CoordField(),
		ForeignKey("instance", "map"),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
		LocalizedFields("description"),
		IntegerField(),
		IntegerField(),
	)


class AreaTable(DBStructure):
	"""
	AreaTable.dbc
	Contains all zone and subzone data.
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "map"),
		ForeignKey("parentarea", "areatable"),
		IntegerField(),
		BitMaskField(),
		IntegerField(),
		IntegerField(), # SoundAmbience
		IntegerField(), # ZoneMusic
		IntegerField(), # ZoneIntroMusicTable
		IntegerField(),
		IntegerField("level"),
		LocalizedFields("name"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		IntegerField(),
	)


class AreaTrigger(DBStructure):
	"""
	AreaTrigger.dbc
	Zone/Subzone locations
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "map"),
		CoordField(),
		CoordField(),
		CoordField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class AuctionHouse(DBStructure):
	"""
	AuctionHouse.dbc
	Used in mails sent by the Auction House
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class AttackAnimKits(DBStructure):
	"""
	AttackAnimKits.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		ForeignKey("animtype", "attackanimtypes"),
		IntegerField(),
		IntegerField(),
	)


class AttackAnimTypes(DBStructure):
	"""
	AttackAnimTypes.dbc
	Attack animation types...
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
	)


class BarberShopStyle(DBStructure):
	"""
	Hairstyles, facial hair, etc
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		LocalizedFields("name"),
		LocalizedFields("unknown"),
		FloatField(), #scale?
		IntegerField(),
		IntegerField(), #gender?
		IntegerField(),
	)


class BattlemasterList(DBStructure):
	"""
	BattlemasterList.dbc
	Called when talking to a battlemaster.
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("joinmap1", "map"),
		ForeignKey("joinmap2", "map"),
		ForeignKey("joinmap3", "map"),
		ForeignKey("joinmap4", "map"),
		ForeignKey("joinmap5", "map"),
		ForeignKey("joinmap6", "map"),
		ForeignKey("joinmap7", "map"),
		ForeignKey("joinmap8", "map"),
		IntegerField("instancetype"), # 3 for bg, 4 for arena
		IntegerField("levelreq"),
		IntegerField("levelmax"),
		IntegerField("maxplayeramount"),
		IntegerField(), # 9 for eots/sota, 0 for rest. expansion related?
		IntegerField(), # all 1
		LocalizedFields("name"),
		IntegerField(), # related to max group, 5 for av 15 for sota. rest 40, wtf?
	)


class BankBagSlotPrices(DBStructure):
	"""
	BankBagSlotPrices.dbc
	Price for bank bag slots.
	"""
	base = Skeleton(
		IDField(),
		MoneyField("price"),
	)


class CameraShakes(DBStructure):
	"""
	CameraShakes.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class Cfg_Categories(DBStructure):
	"""
	Cfg_Categories.dbc
	Server localizations
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		BooleanField("tournament"),
		LocalizedFields("name"),
	)


class Cfg_Configs(DBStructure):
	"""
	Cfg_Configs.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(), #previous id or something
		BooleanField(),
		BooleanField(),
	)


class CharBaseInfo(DBStructure):
	"""
	CharBaseInfo.dbc
	Unknown use
	"""
	base = Skeleton(
		ShortField(),
	)


class CharTitles(DBStructure):
	"""
	CharTitles.dbc
	Player titles
	"""
	base = Skeleton(
		IDField(),
		IntegerField(), # related to achievements?
		LocalizedFields("title"),
		LocalizedFields("title2"),
		IntegerField("index"),
	)


class CharacterFacialHairStyles(DBStructure):
	"""
	CharacterFacialHairStyles.dbc
	Character facial hair styles (..?)
	"""
	base = Skeleton(
		IntegerField(),
		BooleanField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class ChatChannels(DBStructure):
	"""
	ChatChannels.dbc
	Default chat channels
	"""
	base = Skeleton(
		IDField(),
		BitMaskField("flags"),
		IntegerField(),
		LocalizedFields("localname"),
		LocalizedFields("name"),
	)


class ChatProfanity(DBStructure):
	"""
	ChatProfanity.dbc
	Chat filtering
	"""
	base = Skeleton(
		IDField(),
		StringField("filter"),
		IntegerField("language"),
	)


class ChrClasses(DBStructure):
	"""
	ChrClasses.dbc
	Class properties
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField("powertype"),
		StringField("petname"),
		LocalizedFields("namemale"),
		LocalizedFields("namefemale"),
		LocalizedFields("nameunknown"),
		StringField("internalname"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("expansionreq"),
	)


class ChrRaces(DBStructure):
	"""
	ChrRaces.dbc
	Player race data (including some inaccessible)
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		StringField("abbreviation"),
		FloatField(), #scale?
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		StringField("internalname"),
		IntegerField(),
		LocalizedFields("namemale"),
		LocalizedFields("namefemale"),
		LocalizedFields("nameunknown"),
		StringField("facialhair"),
		StringField("earrings"),
		StringField("horns"),
		IntegerField("expansionreq"),
	)


class CinematicCamera(DBStructure):
	"""
	CinematicCamera.dbc
	TODO - Structure 1.1.2.4125
	"""
	base = Skeleton(
		IDField(),
		FilePathField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)



class CreatureDisplayInfo(DBStructure):
	"""
	CreatureDisplayInfo.dbc
	Display data for NPCs
	"""
	base = Skeleton(
		IDField(),
		#ForeignKey("inherits", "creaturedisplayinfo"), #not always valid...
		IntegerField(),
		IntegerField(), # again, inherits? dunno
		IntegerField(), # go figure
		FloatField("scale"),
		IntegerField("alpha"),
		StringField("file1"),
		StringField("file2"),
		StringField("file3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)



class CreatureType(DBStructure):
	"""
	CreatureType.dbc
	Creature types
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField(),
	)



class CurrencyCategory(DBStructure):
	"""
	CurrencyCategory.dbc
	Currency categories
	"""
	base = Skeleton(
		IDField(),
		IntegerField(), # 3 for unused, rest 0
		LocalizedFields("name"),
	)



class CurrencyTypes(DBStructure):
	"""
	CurrencyTypes.dbc
	Currency data
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("item", "item"),
		ForeignKey("category", "currencycategory"),
		IntegerField(),
	)


class DanceMoves(DBStructure):
	"""
	DanceMoves.dbc
	Not yet implemented.
	"""
	base = Skeleton(
		IDField(),
		IntegerField("category"),
		IntegerField("length"),
		IntegerField(),
		BitMaskField("flags"),
		StringField("name"),
		LocalizedFields("description"),
		IntegerField(),
	)


class DeathThudLookups(DBStructure):
	"""
	DeathThudLookups.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class DungeonMap(DBStructure):
	"""
	DungeonMap.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		IntegerField(),
	)


class Exhaustion(DBStructure):
	"""
	Exhaustion.dbc
	China's exhaustion system?
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		LocalizedFields("name"),
		FloatField(),
	)


class Faction(DBStructure):
	"""
	Faction.dbc
	In-game faction data.
	"""
	base = Skeleton(
		IDField(),
		IntegerField(), # ordering?
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(), # class-friendly (DK/Mage/Druid etc)?
		IntegerField(),
		IntegerField(),
		IntegerField("startrep1"),
		IntegerField("startrep2"),
		IntegerField("startrep3"),
		IntegerField("startrep4"),
		BitMaskField("flags"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		ForeignKey("parent_faction", "faction"),
		LocalizedFields("name"),
		LocalizedFields("description"),
	)

	def changed_10522(self, base):
		base.insert_field(UnknownField(), before="parent_faction")
		base.insert_field(FloatField(), before="parent_faction")
		base.insert_field(FloatField(), before="parent_faction")
		base.insert_field(UnknownField(), before="parent_faction")


class FactionGroup(DBStructure):
	"""
	FactionGroup.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		StringField("internal_name"),
		LocalizedFields("name"),
	)


class FileData(DBStructure):
	"""
	FileData.dbc
	Movie file data
	"""
	base = Skeleton(
		IDField(),
		StringField("filename"),
		FilePathField("path"),
	)


class GameTables(DBStructure):
	"""
	GameTables.dbc
	Unknown use
	"""
	base = Skeleton(
		StringIDField(),
		IntegerField(), # 1-100
		IntegerField(),
	)



class GameTips(DBStructure):
	"""
	GameTips.dbc
	Loading screen tips.
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("description"),
	)


class GemProperties(DBStructure):
	"""
	GemProperties.dbc
	Gem data
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("enchant", "spellitemenchantment"),
		BooleanField(),
		BooleanField(),
		IntegerField("gemcolor"),
	)


class GlyphProperties(DBStructure):
	"""
	GlyphProperties.dbc
	Glyph data
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("spell", "spell"),
		BitMaskField(),
		IntegerField(),
	)

class GlyphSlot(DBStructure):
	"""
	GlyphSlot.dbc
	"""
	base = Skeleton(
		IDField(),
		IntegerField("type"),
		IntegerField("ordering"),
	)

class gtCombatRatings(DBStructure):
	"""
	gtCombatRatings.dbc
	"""
	base = Skeleton(
		FloatField('ratio'),
	)

class gtOCTRegenHP(DBStructure):
	"""
	gtOCTRegenHP.dbc
	"""

	base = Skeleton(
		FloatField('ratio'),
	)

class gtOCTRegenMP(DBStructure):
	"""
	gtOCTRegenMP.dbc
	"""

	base = Skeleton(
		FloatField('ratio'),
	)

class GtRegenHPPerSpt(DBStructure):
	"""
	gtRegenHPPerSpt.dbc
	"""

	base = Skeleton(
		FloatField('ratio'),
	)

class GtRegenMPPerSpt(DBStructure):
	"""
	gtRegenMPPerSpt.dbc
	"""

	base = Skeleton(
		FloatField('ratio'),
	)


class HelmetGeosetVisData(DBStructure):
	"""
	HelmetGeosetVisData.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class HolidayDescriptions(DBStructure):
	"""
	HolidayDescriptions.dbc
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("description"),
	)


class HolidayNames(DBStructure):
	"""
	HolidayNames.dbc
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class Holidays(DBStructure):
	"""
	Holidays.dbc
	"""
	base = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		ForeignKey("name", "holidaynames"),
		ForeignKey("description", "holidaydescriptions"),
		StringField("icon"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class Item(DBStructure):
	"""
	Item.dbc
	Contains all in-game items, and their display data.
	Used for icons, dressing room, etc.
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("category", "itemclass"),
		ForeignKey("subcategory", "itemsubclass"),
		IntegerField("depclass"),
		IntegerField(), # sheath or something
		ForeignKey("display", "itemdisplayinfo"),
		IntegerField("slot"),
		IntegerField("sheathtype"),
	)


class ItemBagFamily(DBStructure):
	"""
	ItemBagFamily.dbc
	Item bag categories
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class ItemClass(DBStructure):
	"""
	ItemClass.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class ItemCondExtCost(DBStructure):
	"""
	ItemCondExtCost.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		ForeignKey("extcost", "itemextendedcost"),
		IntegerField(),
	)


class ItemDisplayInfo(DBStructure):
	"""
	ItemDisplayInfo.dbc
	Item display data. Icons, models, ...
	"""
	base = Skeleton(
		IDField(),
		StringField("model"),
		StringField("model2"),
		StringField("texture"),
		StringField("texture2"),
		StringField("icon"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		StringField("texture3"),
		StringField("texture4"),
		StringField("texture5"),
		StringField("texture6"),
		StringField("texture7"),
		StringField("texture8"),
		StringField("texture9"),
		StringField("texture10"),
		IntegerField(),
		IntegerField(),
	)


class ItemExtendedCost(DBStructure):
	"""
	ItemExtendedCost.dbc
	Extended cost data (buy with items, honor points, arena points, ...)
	"""
	base = Skeleton(
		IDField(),
		IntegerField("honorpoints"),
		IntegerField("arenapoints"),
		ForeignKey("item1", "item"),
		ForeignKey("item2", "item"),
		ForeignKey("item3", "item"),
		ForeignKey("item4", "item"),
		ForeignKey("item5", "item"),
		IntegerField("itemamt1"),
		IntegerField("itemamt2"),
		IntegerField("itemamt3"),
		IntegerField("itemamt4"),
		IntegerField("itemamt5"),
		IntegerField("personalratingreq"),
		UnknownField(), # maybe pvprankreq?
	)

	def changed_10026(self, base):
		base.insert_field(IntegerField("bracket"), before="item1")


class ItemLimitCategory(DBStructure):
	"""
	ItemLimitCategory.dbc
	Unique item categories
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("amount"),
		BooleanField("equipped"),
	)


class ItemPetFood(DBStructure):
	"""
	ItemPetFood.dbc
	Hunter pet food categories
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class ItemPurchaseGroup(DBStructure):
	"""
	ItemPurchaseGroup.dbc
	"Group" buys, seems to be a feature not in-game. Only one row (34529, 34530, 33006)
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("item1", "item"),
		ForeignKey("item2", "item"),
		ForeignKey("item3", "item"),
		ForeignKey("item4", "item"),
		ForeignKey("item5", "item"),
		ForeignKey("item6", "item"),
		ForeignKey("item7", "item"),
		ForeignKey("item8", "item"),
		LocalizedFields("name"),
	)


class ItemRandomProperties(DBStructure):
	"""
	ItemRandomProperties.dbc
	Random enchantments for items (of stamina, ...)
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class ItemSet(DBStructure):
	"""
	ItemSet.dbc
	Contains data for item sets. Item IDs linked are
	requested directly in itemtextcache.wdb
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		ForeignKey("item1", "itemtextcache"),
		ForeignKey("item2", "itemtextcache"),
		ForeignKey("item3", "itemtextcache"),
		ForeignKey("item4", "itemtextcache"),
		ForeignKey("item5", "itemtextcache"),
		ForeignKey("item6", "itemtextcache"),
		ForeignKey("item7", "itemtextcache"),
		ForeignKey("item8", "itemtextcache"),
		ForeignKey("item9", "itemtextcache"),
		ForeignKey("item10", "itemtextcache"),
		ForeignKey("item11", "itemtextcache"),
		ForeignKey("item12", "itemtextcache"),
		ForeignKey("item13", "itemtextcache"),
		ForeignKey("item14", "itemtextcache"),
		ForeignKey("item15", "itemtextcache"),
		ForeignKey("item16", "itemtextcache"),
		ForeignKey("item17", "itemtextcache"),
		ForeignKey("bonus1", "spell"),
		ForeignKey("bonus2", "spell"),
		ForeignKey("bonus3", "spell"),
		ForeignKey("bonus4", "spell"),
		ForeignKey("bonus5", "spell"),
		ForeignKey("bonus6", "spell"),
		ForeignKey("bonus7", "spell"),
		ForeignKey("bonus8", "spell"),
		IntegerField("piecesreqbonus1"),
		IntegerField("piecesreqbonus2"),
		IntegerField("piecesreqbonus3"),
		IntegerField("piecesreqbonus4"),
		IntegerField("piecesreqbonus5"),
		IntegerField("piecesreqbonus6"),
		IntegerField("piecesreqbonus7"),
		IntegerField("piecesreqbonus8"),
		ForeignKey("skillreq", "skillline"),
		IntegerField("skilllevelreq"),
	)


class ItemSubClass(DBStructure):
	"""
	ItemSubClass.dbc
	Item subclasses
	"""
	base = Skeleton(
		IDField(),
		IDField(),
		IntegerField(),
		BitMaskField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("handsamt"),
		LocalizedFields("name"),
		LocalizedFields("categoryname"),
	)


class ItemSubClassMask(DBStructure):
	"""
	ItemSubClassMask.dbc
	Unknown use
	"""
	base = Skeleton(
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class Languages(DBStructure):
	"""
	Languages.dbc
	Player/NPC language data
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class LightSkybox(DBStructure):
	"""
	LightSkybox.dbc
	Skybox data
	"""
	base = Skeleton(
		IDField(),
		FilePathField("path"),
		IntegerField(),
	)


class LiquidMaterial(DBStructure):
	"""
	LiquidMaterial.dbc
	Unknown use. Lava/Water? Only 3 rows (1, 2, 3).
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
	)


class LoadingScreens(DBStructure):
	"""
	LoadingScreens.dbc
	Loading screen lookups
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		FilePathField("path"),
	)


class Lock(DBStructure):
	"""
	Lock.dbc
	Various locks (items, objects, ...)
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(), #fkey item?
		IntegerField(), #fkey item?
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("itemlockpick"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class MailTemplate(DBStructure):
	"""
	MailTemplate.dbc
	In-game mails recieved.
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("title"),
		LocalizedFields("message"),
	)


class Map(DBStructure):
	"""
	Map.dbc
	Instance data
	"""
	base = Skeleton(
		IDField(),
		StringField("internalname"),
		IntegerField("type"), # 0: normal, 1: instance, 2: raid, 3: battleground, 4: arena
		BooleanField("battleground"),
		LocalizedFields("name"),
		ForeignKey("parentzone", "areatable"), # instance zone id
		LocalizedFields("descriptionhorde"),
		LocalizedFields("descriptionalliance"),
		UnknownField(),
		FloatField("visionrange"),
		LocalizedFields("normalreqs"),
		LocalizedFields("heroicreqs"),
		LocalizedFields("epicreqs"),
		ForeignKey("continent", "map"),
		CoordField("entrancex"),
		CoordField("entrancey"),
		DurationField("normalreset", unit="seconds"),
		DurationField("heroicreset", unit="seconds"),
		DurationField("epicreset", unit="seconds"),
		IntegerField("someunknownfield1"),
		IntegerField("someunknownfield2"),
		DurationField(unit="seconds"),
	)

	def changed_10026(self, base):
		base.delete_fields("normalreqs", "heroicreqs", "epicreqs", "normalreset", "heroicreset", "epicreset")

	def changed_10083(self, base):
		self.changed_10026(base)
		base.append_fields(IntegerField("playeramount"))

	def changed_10522(self, base):
		self.changed_10083(base)
		base.insert_field(UnknownField(), before="battleground")


class MapDifficulty(DBStructure):
	"""
	MapDifficulty.dbc
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "map"),
		IntegerField("mode"),
		LocalizedFields("requirements"),
		DurationField("resettime"),
		IntegerField("raidsize"),
		UnknownField(),
	)

class Movie(DBStructure):
	"""
	Movie.dbc
	Supposedly for movies. 3 rows at the time: 1, 2, 14
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
	)


class MovieFileData(DBStructure):
	"""
	MovieFileData.dbc
	Movie resolution data
	"""
	base = Skeleton(
		IDField(),
		IntegerField("resolution"), #800 or 1024
	)


class MovieVariation(DBStructure):
	"""
	MovieVariation.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		ForeignKey("resolution", "moviefiledata"),
	)


class NameGen(DBStructure):
	"""
	NameGen.dbc
	Character creation name generator data
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField("class"),
		IntegerField("gender"),
	)


class Package(DBStructure):
	"""
	Package.dbc
	Single row, probably internal use.
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class PetLoyalty(DBStructure):
	"""
	PetLoyalty.dbc
	Hunter pet loyalty
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class PetPersonality(DBStructure):
	"""
	PetPersonality.dbc
	UNUSED
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class Resistances(DBStructure):
	"""
	Resistances.dbc
	TODO
	"""
	base = Skeleton(
		IDField(),
		UnknownField(), # is_armor
		UnknownField(),
		LocalizedFields("name"),
	)


class QuestInfo(DBStructure):
	"""
	QuestInfo.dbc
	Quest type names
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class QuestSort(DBStructure):
	"""
	QuestSort.dbc
	Additional sort fields for quests
	Note: Zones are directly gathered from AreaTable.dbc
	linked by a negative id in questcache.wdb
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class ScalingStatDistribution(DBStructure):
	"""
	ScalingStatDistribution.dbc
	"""
	base = Skeleton(
		IDField(),
		IntegerField("stat_1"),
		IntegerField("stat_2"),
		IntegerField("stat_3"),
		IntegerField("stat_4"),
		IntegerField("stat_5"),
		IntegerField("stat_6"),
		IntegerField("stat_7"),
		IntegerField("stat_8"),
		IntegerField("stat_9"),
		IntegerField("stat_10"),
		IntegerField("modifier_1"),
		IntegerField("modifier_2"),
		IntegerField("modifier_3"),
		IntegerField("modifier_4"),
		IntegerField("modifier_5"),
		IntegerField("modifier_6"),
		IntegerField("modifier_7"),
		IntegerField("modifier_8"),
		IntegerField("modifier_9"),
		IntegerField("modifier_10"),
		IntegerField("max_level"),
	)


class ScalingStatValues(DBStructure):
	"""
	ScalingStatValues.dbc
	Heirloom stat scaling (one row per level)
	"""
	base = Skeleton(
		IDField(),
		IntegerField("level"),
		IntegerField("coefficient_1"),
		IntegerField("coefficient_2"),
		IntegerField("coefficient_3"),
		IntegerField("coefficient_4"),
		IntegerField("armor_modifier_1"),
		IntegerField("armor_modifier_2"),
		IntegerField("armor_modifier_3"),
		IntegerField("armor_modifier_4"),
		IntegerField("dps_modifier_1"),
		IntegerField("dps_modifier_2"),
		IntegerField("dps_modifier_3"),
		IntegerField("dps_modifier_4"),
		IntegerField("dps_modifier_5"),
		IntegerField("dps_modifier_6"),
		IntegerField("spellpower"),
		IntegerField("coefficient_5"),
		IntegerField("coefficient_6"),
		IntegerField("no_armor"),
		IntegerField("cloth"),
		IntegerField("leather"),
		IntegerField("mail"),
		IntegerField("plate"),
	)

	def changed_10026(self, base):
		"""
		5 new fields
		"""
		pass


class ScreenEffect(DBStructure):
	"""
	ScreenEffect.dbc
	Fullscreen graphic effects
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField("type"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class ServerMessages(DBStructure):
	"""
	ServerMessages.dbc
	Server-wide broadcast messages (in-game chat)
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("message"),
	)


class SkillLine(DBStructure):
	"""
	SkillLine.dbc
	Contains all skill-related data.
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("category", "skilllinecategory"),
		IntegerField(), # Internal only
		LocalizedFields("name"),
		LocalizedFields("description"),
		IntegerField(),
		LocalizedFields("action"),
		BooleanField("tradeskill"),
	)


class SkillLineAbility(DBStructure):
	"""
	SkillLineAbility.dbc
	turns_green is averaged with: a + (b-a)/2
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("skill", "skillline"),
		ForeignKey("spell", "spell"),
		BitMaskField(), #racemask
		BitMaskField(), #classmask
		BitMaskField(), #raceexclude
		BitMaskField(), #classexclude
		IntegerField("required_skill_level"),
		ForeignKey("parent", "spell"),
		UnknownField(),
		IntegerField("turns_grey"),
		IntegerField("turns_yellow"),
		UnknownField(),
		UnknownField(),
		#UnknownField(), Deleted somewhere between 4125 and 9551
	)

class SkillLineCategory(DBStructure):
	"""
	SkillLineCategory.dbc
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("sort")
	)


class SpamMessages(DBStructure):
	"""
	SpamMessages.dbc
	Regex matches for spam check (?)
	"""
	base = Skeleton(
		IDField(),
		StringField("regex"),
	)


class Spell(DBStructure):
	"""
	Spell.dbc
	Contains all spell data.
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("category", "spellcategory"),
		IntegerField("dispeltype"),
		IntegerField("mechanic"),
		BitMaskField("flags1"),
		BitMaskField("flags2"),
		BitMaskField("flags3"),
		IntegerField(), ## XXX
		IntegerField(), ## XXX
		IntegerField(), ## XXX
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("stancereq"),
		IntegerField("unusablestance"),
		IntegerField(),
		IntegerField("npctypereq"),
		IntegerField("focusobject"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		ForeignKey("casttime", "spellcasttimes"),
		DurationField("categorycooldown", unit="milliseconds"),
		DurationField("cooldown", unit="milliseconds"),
		IntegerField(),
		IntegerField(),
		BitMaskField("channelingflags"),
		IntegerField(),
		IntegerField("procchance"),
		IntegerField("proccharges"),
		IntegerField(),
		IntegerField("level"),
		IntegerField("levelreq"),
		ForeignKey("duration", "spellduration"),
		IntegerField("powercosttype"),
		IntegerField("powercostamount"),
		IntegerField(),
		IntegerField("powercostpersec"),
		IntegerField(),
		ForeignKey("range", "spellrange"),
		FloatField("missilespeed"),
		IntegerField(),
		IntegerField("maxstack"),
		IntegerField("toolreq1"),
		IntegerField("toolreq2"),
		ForeignKey("reagentreq1", "item"),
		ForeignKey("reagentreq2", "item"),
		ForeignKey("reagentreq3", "item"),
		ForeignKey("reagentreq4", "item"),
		ForeignKey("reagentreq5", "item"),
		ForeignKey("reagentreq6", "item"),
		ForeignKey("reagentreq7", "item"),
		ForeignKey("reagentreq8", "item"),
		IntegerField("reagentamtreq1"),
		IntegerField("reagentamtreq2"),
		IntegerField("reagentamtreq3"),
		IntegerField("reagentamtreq4"),
		IntegerField("reagentamtreq5"),
		IntegerField("reagentamtreq6"),
		IntegerField("reagentamtreq7"),
		IntegerField("reagentamtreq8"),
		IntegerField("itemcategoryreq"),
		IntegerField("itemsubcategoryreq"),
		IntegerField("slotreq"),
		ForeignKey("effect1", "spelleffectnames", dead=True),
		ForeignKey("effect2", "spelleffectnames", dead=True),
		ForeignKey("effect3", "spelleffectnames", dead=True),
		IntegerField("diesideseffect1"),
		IntegerField("diesideseffect2"),
		IntegerField("diesideseffect3"),
		IntegerField("dicebaseeffect1"),
		IntegerField("dicebaseeffect2"),
		IntegerField("dicebaseeffect3"),
		IntegerField("diceperleveleffect1"),
		IntegerField("diceperleveleffect2"),
		IntegerField("diceperleveleffect3"),
		FloatField(),
		FloatField(),
		FloatField(),
		IntegerField("damageeffect1"),
		IntegerField("damageeffect2"),
		IntegerField("damageeffect3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		ForeignKey("radiuseffect1", "spellradius"),
		ForeignKey("radiuseffect2", "spellradius"),
		ForeignKey("radiuseffect3", "spellradius"),
		ForeignKey("auraeffect1", "spellauranames", dead=True),
		ForeignKey("auraeffect2", "spellauranames", dead=True),
		ForeignKey("auraeffect3", "spellauranames", dead=True),
		IntegerField("intervaleffect1"),
		IntegerField("intervaleffect2"),
		IntegerField("intervaleffect3"),
		FloatField("valueeffect1"),
		FloatField("valueeffect2"),
		FloatField("valueeffect3"),
		IntegerField("maxtargetseffect1"),
		IntegerField("maxtargetseffect2"),
		IntegerField("maxtargetseffect3"),
		IntegerField("argeffect1"),
		IntegerField("argeffect2"),
		IntegerField("argeffect3"),
		IntegerField("misceffect1"),
		IntegerField("misceffect2"),
		IntegerField("misceffect3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		ForeignKey("triggerspelleffect1", "spell"),
		ForeignKey("triggerspelleffect2", "spell"),
		ForeignKey("triggerspelleffect3", "spell"),
		FloatField("procchanceeffect1"),
		FloatField("procchanceeffect2"),
		FloatField("procchanceeffect3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		IntegerField(),#
		ForeignKey("spellicon", "spellicon"),
		ForeignKey("bufficon", "spellicon"),
		IntegerField("priority"),
		LocalizedFields("name"),
		LocalizedFields("rank"),
		LocalizedFields("spelldescription", field_type=SpellMacroField),
		LocalizedFields("buffdescription", field_type=SpellMacroField),
		IntegerField("percentbasemanacost"),#
		IntegerField("globalcooldowncategory"),
		DurationField("globalcooldown", unit="milliseconds"),
		IntegerField("maxtargetlevel"),
		IntegerField(),
		BitMaskField(),
		IntegerField(),
		IntegerField(),
		IntegerField("maxtargets"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField("finishercoeffect1"), # XXX
		FloatField("finishercoeffect2"),
		FloatField("finishercoeffect3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("toolcategoryreq"),
		IntegerField("toolcategoryreq2"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)

	def changed_10026(self, base):
		base.append_fields(
			FloatField("coeffeffect1"),
			FloatField("coeffeffect2"),
			FloatField("coeffeffect3"),
			ForeignKey("descriptionvars", "spelldescriptionvariables"),
		)

	def changed_10522(self, base):
		self.changed_10026(base)
		base.append_fields(
			UnknownField(),
		)


# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

class Stell(DBStructure):

	base = Skeleton(
		IDField(),
		IntegerField("category"),
		IntegerField("dispeltype"),
		IntegerField(),
		IntegerField(),
		IntegerField("mechanic"),
		BitMaskField(),
		BitMaskField(),
		BitMaskField(),
		IntegerField("stancereq"),
		IntegerField("unusablestance"),
		IntegerField(),
		BitMaskField(),
		BitMaskField(),
		BitMaskField(),
		BitMaskField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("casttime"),
		IntegerField("cooldowncategory"),
		IntegerField("cooldown"),
		IntegerField(),
		BitMaskField(),
		BitMaskField(),
		BitMaskField(),
		IntegerField("procchance"),
		IntegerField("proccharges"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField("missilespeed"),
		IntegerField("toolreq1"),
		IntegerField("toolreq2"),
		ForeignKey("reagentreq1", "item"),
		ForeignKey("reagentreq2", "item"),
		ForeignKey("reagentreq3", "item"),
		ForeignKey("reagentreq4", "item"),
		ForeignKey("reagentreq5", "item"),
		ForeignKey("reagentreq6", "item"),
		ForeignKey("reagentreq7", "item"),
		ForeignKey("reagentreq8", "item"),
		IntegerField("reagentamtreq1"),
		IntegerField("reagentamtreq2"),
		IntegerField("reagentamtreq3"),
		IntegerField("reagentamtreq4"),
		IntegerField("reagentamtreq5"),
		IntegerField("reagentamtreq6"),
		IntegerField("reagentamtreq7"),
		IntegerField("reagentamtreq8"),
		IntegerField("itemcategoryreq"),
		IntegerField("itemsubcategoryreq"),
		IntegerField("slotreq"),
		IntegerField("effect1"),
		IntegerField("effect2"),
		IntegerField("effect3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField("maxtargetseffect1"),
		IntegerField("maxtargetseffect2"),
		IntegerField("maxtargetseffect3"),
		IntegerField("argeffect1"),
		IntegerField("argeffect2"),
		IntegerField("argeffect3"),
		IntegerField("misceffect1"),
		IntegerField("misceffect2"),
		IntegerField("misceffect3"),
		ForeignKey("triggerspell1", "spell"),
		ForeignKey("triggerspell2", "spell"),
		ForeignKey("triggerspell3", "spell"),
		FloatField("procchanceeffect1"),
		FloatField("procchanceeffect2"),
		FloatField("procchanceeffect3"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		StringField("name_enus"),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		BitMaskField("name_locflags"),
		StringField("rank_enus"),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		BitMaskField("rank_locflags"),
		StringField("spelldescription_enus"),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		BitMaskField("spelldescription_locflags"),
		StringField("buffdescription_enus"),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		BitMaskField("buffdescription_locflags"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		BitMaskField(),
		BitMaskField("unknown_bitmask"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		FloatField(),
	)


class SpellAuraNames(DBStructure):
	"""
	SpellAuraNames.dbc
	TODO - Structure 1.1.2.4125
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		StringField("internalname"),
		LocalizedFields("name", locales=OLD_LOCALES),
	)


class SpellCategory(DBStructure):
	"""
	SpellCategory.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
	)


class SpellCastTimes(DBStructure):
	"""
	SpellCastTimes.dbc
	Spell cast time info
	"""
	base = Skeleton(
		IDField(),
		DurationField("casttime1", unit="milliseconds"),
		IntegerField("modifier"),
		DurationField("casttime2", unit="milliseconds"),
	)


class SpellDescriptionVariables(DBStructure):
	"""
	SpellDescriptionVariables.dbc
	Used in spellstrings
	"""
	base = Skeleton(
		IDField(),
		StringField("variables"),
	)


class SpellDuration(DBStructure):
	"""
	SpellDuration.dbc
	Spell duration data
	"""
	base = Skeleton(
		IDField(),
		DurationField("duration", unit="milliseconds"),
		IntegerField("modifier"),
		DurationField("maxduration", unit="milliseconds"),
	)


class SpellEffectNames(DBStructure):
	"""
	SpellEffectNames.dbc
	TODO - Structure 1.1.2.4125
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name", locales=OLD_LOCALES),
	)


class SpellIcon(DBStructure):
	"""
	SpellIcon.dbc
	Spell icons
	"""
	base = Skeleton(
		IDField(),
		FilePathField("path"),
	)


class SpellItemEnchantment(DBStructure):
	"""
	SpellItemEnchantment.dbc
	Item enchants (Including temporary
	enchants and socketbonuses)
	"""
	base = Skeleton(
		IDField(),
		IntegerField("charges"),
		IntegerField("typeeffect1"),
		IntegerField("typeeffect2"),
		IntegerField("typeeffect3"),
		IntegerField("amounteffect1"),
		IntegerField("amounteffect2"),
		IntegerField("amounteffect3"),
		IntegerField("amounteffect1"), # ?? dup
		IntegerField("amounteffect2"), # ??
		IntegerField("amounteffect3"), # ??
		IntegerField("effect1"), #fkey stat/spell
		IntegerField("effect2"), #fkey stat/spell
		IntegerField("effect3"), #fkey stat/spell
		LocalizedFields("name"),
		IntegerField(), # glow?
		IntegerField(),
		ForeignKey("gem", "item"),
		IntegerField(), # SpellItemEnchantmentCondition?
		ForeignKey("skillreq", "skillline"),
		IntegerField("skilllevelreq"),
		UnknownField(), # added 9447?
	)


class SpellMechanic(DBStructure):
	"""
	SpellMechanic.dbc
	Spell mechanic names
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class SpellRadius(DBStructure):
	"""
	SpellRadius.dbc
	Spell radius data
	"""
	base = Skeleton(
		IDField(),
		FloatField("minradius"),
		IntegerField(),
		FloatField("maxradius"),
	)


class SpellRange(DBStructure):
	"""
	SpellRange.dbc
	Spell range data
	"""
	base = Skeleton(
		IDField(),
		FloatField("minrange1"),
		FloatField("minrange2"),
		FloatField("maxrange1"),
		FloatField("maxrange2"),
		IntegerField(),
		LocalizedFields("name"),
		LocalizedFields("tooltipname"),
	)


class SpellVisualEffectName(DBStructure):
	"""
	SpellVisualEffectName.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		FilePathField("path"),
		FloatField(),
		FloatField(),
		FloatField(), #scale?
		FloatField(), #alpha?
	)


class Startup_Strings(DBStructure):
	"""
	Startup_Strings.dbc
	Runtime messages and warnings
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		LocalizedFields("message"),
	)


class Stationery(DBStructure):
	"""
	Stationery.dbc
	In-game mail background
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("item", "itemcache"),
		StringField("name"),
		UnknownField(),
	)

class Talent(DBStructure):
	"""
	Talent.dbc		
	"""
	base = Skeleton(
		IDField(),
		ForeignKey('tab', 'talenttab'),
		UnsignedIntegerField('row'),
		UnsignedIntegerField('col'),
		#UnsignedIntegerField('rankid1'),
		#UnsignedIntegerField('rankid2'),
		#UnsignedIntegerField('rankid3'),
		#UnsignedIntegerField('rankid4'),
		#UnsignedIntegerField('rankid5'),
		ListField('rankid', length=5),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnsignedIntegerField('depends_on'),
		UnknownField(),
		UnknownField(),
		UnsignedIntegerField('depends_on_rank'),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)

class TalentTab(DBStructure):
	"""
	TalentTab.dbc
	Talent panel tabs
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("nameflags"),
		IntegerField("spellicon"),
		BitMaskField("classmask"),
		IntegerField("petmask"), #petflags?
		IntegerField("tabpage"),
		StringField("internalname"),
	)


class TaxiNodes(DBStructure):
	"""
	TaxiNodes.dbc
	Flight paths, teleports, etc.
	"""
	base = Skeleton(
		IDField(),
		IntegerField("instance"),
		CoordField("xcoord"),
		CoordField("ycoord"),
		CoordField("zcoord"),
		LocalizedFields("name"),
		IntegerField(),
		IntegerField(),
	)

class TotemCategory(DBStructure):
	"""
	TotemCategory.dbc
	Item tools, totems etc
	"""
	base = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("category"),
		BitMaskField("flags"),
	)


class TransportPhysics(DBStructure):
	"""
	TransportPhysics.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class UnitBloodLevels(DBStructure):
	"""
	UnitBloodLevels.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class Weather(DBStructure):
	"""
	Weather.dbc
	Weather lookups
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		IntegerField(),
	)


class WorldChunkSounds(DBStructure):
	"""
	WorldChunkSounds.dbc
	Unknown use and structure - NULLED OUT
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class WorldMapArea(DBStructure):
	"""
	WorldMapArea.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		IntegerField(),
		IntegerField(),
	)


class WorldStateZoneSounds(DBStructure):
	"""
	WorldStateZoneSounds.dbc
	Unknown use
	"""
	base = Skeleton(
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class WowError_Strings(DBStructure):
	"""
	WowError_Strings.dbc
	Localization called by WowError.exe when the game crashes.
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		LocalizedFields("description"),
	)


class ZoneIntroMusicTable(DBStructure):
	"""
	ZoneIntroMusicTable.dbc
	TODO
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField(),
		BooleanField(),
		IntegerField(),
	)


class ZoneMusic(DBStructure):
	"""
	ZoneMusic.dbc
	TODO
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)

