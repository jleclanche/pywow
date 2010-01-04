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

	def changed_10026(self, base):
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
	
	FLAGS = {
		0x00000002: "conjured",
		0x00000004: "openable",
		0x00000008: "heroic",
		0x00000010: "broken", # Appears as a red icon, unusable (for deprecated items)
		0x00000020: "totem",
		0x00000080: "no_equip_cooldown",
		0x00000200: "wrapper",
		0x00000400: "ignore_backspace",
		0x00000800: "group_loot",
		0x00001000: "refundable",
		0x00002000: "chart",
		0x00040000: "prospectable",
		0x00080000: "unique_equipped",
		0x00200000: "usable_in_arena",
		0x00400000: "thrown",
		0x08000000: "account_bound",
		0x10000000: "enchant_scroll",
		0x20000000: "millable",
		0x80000000: "bop_tradeable"
	}
	
	FLAGS_2 = {
		0x00000001: "horde",
		0x00000002: "alliance",
	}
	
	CLASSES = {
		0x00000001: "warrior",
		0x00000002: "paladin",
		0x00000004: "hunter",
		0x00000008: "rogue",
		0x00000010: "priest",
		0x00000020: "deathknight",
		0x00000040: "shaman",
		0x00000080: "mage",
		0x00000100: "warlock",
		0x00000400: "druid",
	}
	
	RACES = {
		0x00000001: "human",
		0x00000002: "orc",
		0x00000004: "dwarf",
		0x00000008: "nightelf",
		0x00000010: "undead",
		0x00000020: "tauren",
		0x00000040: "gnome",
		0x00000080: "troll",
		0x00000200: "bloodelf",
		0x00000400: "draenei",
	}
	
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
		BitMaskField("flags", flags=FLAGS),
		MoneyField("buy_price"),
		MoneyField("sell_price"),
		IntegerField("slot"),
		BitMaskField("class_mask", flags=CLASSES),
		BitMaskField("race_mask", flags=RACES),
		IntegerField("level"),
		IntegerField("required_level"),
		ForeignKey("required_skill", "SkillLine"),
		IntegerField("required_skill_level"),
		ForeignKey("required_spell", "Spell"),
		IntegerField("required_pvp_rank"),
		IntegerField("required_pvp_medal"),
		ForeignKey("required_faction", "Faction"),
		IntegerField("required_reputation"),
		IntegerField("unique"),
		IntegerField("stack"),
		IntegerField("bag_slots"),
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
		ForeignKey("starts_quest", "questcache"),
		ForeignKey("lock", "Lock"),
		ForeignKey("material", "Material"),
		IntegerField("sheath_type"),
		ForeignKey("randomenchantment", "ItemRandomProperties"),
		IntegerField("block"),
		ForeignKey("itemset", "ItemSet"),
		IntegerField("durability"),
		ForeignKey("zone_bind", "AreaTable"),
		ForeignKey("instance_bind", "Map"),
		IntegerField("bag_category"),
		ForeignKey("tool_category", "TotemCategory"),
		BitMaskField("socket1"),
		IntegerField("socket1info"),
		BitMaskField("socket2"),
		IntegerField("socket2info"),
		BitMaskField("socket3"),
		IntegerField("socket3info"),
		ForeignKey("socket_bonus", "SpellItemEnchantment"),
		ForeignKey("gem_properties", "GemProperties"),
		IntegerField("extendedcost"),
	)

	def changed_5875(self, base):
		"""
		- New disenchant IntegerField
		  UNKNOWN BUILD
		"""
		base.append_fields(
			IntegerField("disenchant"),
		)

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
		base.append_fields(
			FloatField("armordmgmod"),
		)

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
		base.append_fields(ForeignKey("unique_category", "itemlimitcategory"))

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
		base.insert_field(
			DynamicFields("stats", [(
				(IntegerField, "id"),
				(IntegerField, "amt"),
			), 10]
		), before="dmgmin1")
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
		base.delete_fields(
			"dmgmin3", "dmgmax3", "dmgtype3",
			"dmgmin4", "dmgmax4", "dmgtype4",
			"dmgmin5", "dmgmax5", "dmgtype5",
		)
		base.append_fields(
			ForeignKey("required_holiday", "holidays"),
		)

	def changed_10026(self, base):
		self.changed_9614(base)
		base.insert_field(BitMaskField("flags2"), before="buy_price")


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
	
	FLAGS = {
		0x00000001: "objective_stay_alive",
		0x00000002: "party_accept",
		0x00000004: "objective_exploration",
		0x00000008: "sharable",
		0x00000020: "epic",
		0x00000040: "raid",
		0x00000080: "requires_tbc",
		0x00000200: "hidden_rewards",
		0x00000400: "auto_rewarded",
		0x00000800: "tbc_starting_zone",
		0x00001000: "daily",
		0x00008000: "weekly",
	}
	
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
		BitMaskField("flags", flags=FLAGS),
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
		FloatField("coord_x"),
		FloatField("coord_y"),
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
		ForeignKey("next_page", "pagetextcache"),
	)


####################
## DBC structures ##
####################

class Achievement(DBStructure):
	"""
	Achievement.dbc
	Achievement data
	"""
	
	FLAGS = {
		0x00000001: "statistic",
		0x00000040: "show_average",
		0x00000080: "show_progress_bar",
		0x00000100: "serverfirst",
		0x00000200: "serverfirst_raid",
	}
	
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
		BitMaskField("flags", flags=FLAGS),
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
		BitMaskField("weapon_state"),
		BitMaskField("flags"),
		UnknownField(),
		ForeignKey("animation_before", "AnimationData"),
		ForeignKey("real_animation", "AnimationData"),
		IntegerField("flying"), # fly = 3
	)


class AreaGroup(DBStructure):
	"""
	AreaGroup.dbc
	Added during 3.0.x
	XXX What's this used for?
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("area_1", "AreaTable"),
		ForeignKey("area_2", "AreaTable"),
		ForeignKey("area_3", "AreaTable"),
		ForeignKey("area_4", "AreaTable"),
		ForeignKey("area_5", "AreaTable"),
		ForeignKey("area_6", "AreaTable"),
		ForeignKey("next_group", "AreaGroup"),
	)


class AreaPOI(DBStructure):
	"""
	AreaPOI.dbc
	Points of Interest (POI) on the minimap and battlemap.
	Includes text, icons, positioning and other misc things.
	"""
	
	FLAGS = {
		0x004: "zone",
		0x080: "battleground",
		0x200: "show_in_battlemap",
	}
	
	base = Skeleton(
		IDField(),
		UnknownField(),
		IntegerField("icon_normal"),
		IntegerField("icon_damaged"),
		IntegerField("icon_destroyed"),
		IntegerField("horde_icon_normal"),
		IntegerField("horde_icon_damaged"),
		IntegerField("horde_icon_destroyed"),
		IntegerField("alliance_icon_normal"),
		IntegerField("alliance_icon_damaged"),
		IntegerField("alliance_icon_destroyed"),
		UnknownField(),
		FloatField("x"),
		FloatField("y"),
		FloatField("z"),
		ForeignKey("instance", "map"),
		BitMaskField("display_flags", flags=FLAGS),
		ForeignKey("area", "AreaTable"),
		LocalizedFields("name"),
		LocalizedFields("description"),
		IntegerField("world_state"),
		UnknownField(),
	)


class AreaTable(DBStructure):
	"""
	AreaTable.dbc
	Contains all zone and subzone data.
	"""
	
	TERRITORY_FLAGS = { # Sanctuary = 2+4, contested = 0
		0x02: "Horde",
		0x04: "Alliance",
	}
	
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "map"),
		ForeignKey("parent_area", "areatable"),
		IntegerField(), # Fkey but to what?
		BitMaskField("flags"),
		IntegerField(),
		IntegerField(), # 11 or 0
		ForeignKey("sound_ambience", "SoundAmbience"),
		ForeignKey("music", "ZoneMusic"),
		ForeignKey("intro_music", "ZoneIntroMusicTable"),
		IntegerField("level"),
		LocalizedFields("name"),
		BitMaskField("territory_flags", flags=TERRITORY_FLAGS),
		IntegerField(), # 81 61 41 1...
		IntegerField(), # 0
		IntegerField(), # 0
		IntegerField(), # 21 for naxxramas (3456)
		FloatField(), # 1000, -500, -5000
		FloatField(),
		IntegerField(), # 0
	)


class AreaTrigger(DBStructure):
	"""
	AreaTrigger.dbc
	Defines certain areas on the map that presumably tell the server
	to fire a certain event. For example in BWL, telling the goblins
	around vael to run away is a trigger defined here. There are
	also misc triggers out in the middle of space which have 0 size,
	which are most likely used by the server for certain things. One
	such use could be remembering settings per instance, for example,
	draconid colors for Nefarian.
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "map"),
		FloatField("x"),
		FloatField("y"),
		FloatField("z"),
		FloatField("size"),
		FloatField("box_y"),
		FloatField("box_y"),
		FloatField("box_z"),
		FloatField("box_orientation"),
	)


class AuctionHouse(DBStructure):
	"""
	AuctionHouse.dbc
	Data about auction houses and their fees
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("faction", "Faction"),
		IntegerField("auction_fee"),
		IntegerField("deposit_fee"),
		LocalizedFields("name"),
	)


class AttackAnimKits(DBStructure):
	"""
	AttackAnimKits.dbc
	Unknown use
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("animation", "AnimationData"),
		ForeignKey("type", "AttackAnimTypes"),
		BitMaskField(),
		UnknownField(),
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
		IntegerField("type"), # 0 - Hair Style, 1 - Hair Color, 2 - Facial Hairstyle
		LocalizedFields("name"),
		LocalizedFields("unknown"),
		FloatField("price_modifier"),
		ForeignKey("race", "ChrRaces"),
		IntegerField("gender"),
		UnknownField(), # what?: This is option $ID2 in the shop when looking in category $Type. OR "real ID to hair/facial hair"
	)


class BattlemasterList(DBStructure):
	"""
	BattlemasterList.dbc
	Called when talking to a battlemaster.
	Added in TBC
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("map_1", "Map"),
		ForeignKey("map_2", "Map"),
		ForeignKey("map_3", "Map"),
		ForeignKey("map_4", "Map"),
		ForeignKey("map_5", "Map"),
		ForeignKey("map_6", "Map"),
		ForeignKey("map_7", "Map"),
		ForeignKey("map_8", "Map"),
		IntegerField("type"), # 3 for bg, 4 for arena
		IntegerField("min_level"),
		IntegerField("max_level"),
		IntegerField("max_players"),
		IntegerField("level_band"), # 10-19, 20-29, ...
		BooleanField("join_as_group"),
		LocalizedFields("name", locales=OLD_LOCALES)
	)
	
	def changed_9551(self, base):
		base.insert_field(IntegerField("min_players"), before="level_band")
		base.update_locales(LOCALES) # XXX When did locales change?
		base.append_fields(IntegerField("max_group_size"))
	
	def changed_9658(self, base):
		"""
		What's this field? 0 for all arenas
		1- Alterac Valley = 1941
		2- Warsong Gulch = 1942
		3- Arathi Basin = 1943
		7- Eye of the Storm = 2851
		9- Strand of the Ancients = 3695
		"""
		self.changed_9551(base)
		base.append_fields(IntegerField("unknown_9658"))
	
	def changed_10554(self, base):
		self.changed_9658(base)
		base.delete_fields(
			"min_players",
			"level_band",
			"min_level",
			"max_level",
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
		IntegerField("power_type"),
		StringField("pet_name"),
		LocalizedFields("name_male"),
		LocalizedFields("name_female"),
		LocalizedFields("name_unknown"),
		StringField("internal_name"),
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
		StringField("internal_name"),
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
	TODO
	"""
	base = Skeleton(
		IDField(),
		FilePathField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class CinematicSequences(DBStructure):
	"""
	CinematicSequences.dbc
	TODO
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


class Emotes(DBStructure):
	"""
	Emotes.dbc
	Slash-command emotes
	"""
	
	FLAGS = {
		0x008: "talk",
		0x010: "question",
		0x020: "exclamation",
		0x100: "laugh",
	}
	
	base = Skeleton(
		IDField(),
		StringField("name"),
		ForeignKey("animation", "AnimationData"),
		BitMaskField("flags"),
		IntegerField("loop"),
		IntegerField("hold"),
		ForeignKey("sound", "SoundEntries")
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
		IntegerField("ordering"),
		BitMaskField("base_race_mask_1"),
		BitMaskField("base_race_mask_2"),
		BitMaskField("base_race_mask_3"),
		BitMaskField("base_race_mask_4"),
		BitMaskField("base_class_mask_1"),
		BitMaskField("base_class_mask_2"),
		BitMaskField("base_class_mask_3"),
		BitMaskField("base_class_mask_4"),
		IntegerField("base_reputation_1"),
		IntegerField("base_reputation_2"),
		IntegerField("base_reputation_3"),
		IntegerField("base_reputation_4"),
		BitMaskField("flags_1"),
		BitMaskField("flags_2"),
		BitMaskField("flags_3"),
		BitMaskField("flags_4"),
		ForeignKey("parent_faction", "faction"),
		LocalizedFields("name"),
		LocalizedFields("description"),
	)

	def changed_10522(self, base):
		base.insert_field(FloatField(), before="name")
		base.insert_field(FloatField(), before="name")
		base.insert_field(UnknownField(), before="name")
		base.insert_field(UnknownField(), before="name")


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
		IntegerField("color"),
	)


class GlyphProperties(DBStructure):
	"""
	GlyphProperties.dbc
	Glyph data
	"""
	
	FLAGS = {
		0x00000001: "minor",
	}
	
	base = Skeleton(
		IDField(),
		ForeignKey("spell", "spell"),
		BitMaskField("flags", flags=FLAGS),
		ForeignKey("icon", "spellicon"),
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
		FloatField("ratio"),
	)

class gtOCTRegenHP(DBStructure):
	"""
	gtOCTRegenHP.dbc
	"""
	
	base = Skeleton(
		FloatField("ratio"),
	)

class gtOCTRegenMP(DBStructure):
	"""
	gtOCTRegenMP.dbc
	"""
	
	base = Skeleton(
		FloatField("ratio"),
	)

class gtRegenHPPerSpt(DBStructure):
	"""
	gtRegenHPPerSpt.dbc
	"""
	
	base = Skeleton(
		FloatField("ratio"),
	)

class gtRegenMPPerSpt(DBStructure):
	"""
	gtRegenMPPerSpt.dbc
	"""
	
	base = Skeleton(
		FloatField("ratio"),
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
		ForeignKey("required_skill", "skillline"),
		IntegerField("required_skill_level"),
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
		IntegerField("hands"),
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
	
	def changed_10676(self, base):
		base.append_fields(BooleanField("continent"))


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
		StringField("internal_name"),
		IntegerField("type"), # 0: normal, 1: instance, 2: raid, 3: battleground, 4: arena
		BooleanField("battleground"),
		LocalizedFields("name"),
		ForeignKey("zone", "AreaTable"), # instance zone id
		LocalizedFields("description_horde"),
		LocalizedFields("description_alliance"),
		ForeignKey("loading_screen", "LoadingScreens"),
		FloatField(), # BattlefieldMapIconScale
		LocalizedFields("normal_requirements"),
		LocalizedFields("heroic_requirements"),
		LocalizedFields("epic_requirements"),
		ForeignKey("continent", "map"),
		FloatField("entrance_x"),
		FloatField("entrance_y"),
		DurationField("normal_reset", unit="seconds"),
		DurationField("heroic_reset", unit="seconds"),
		DurationField("epic_reset", unit="seconds"),
		DurationField(unit="minutes"),
		IntegerField("expansion"),
		DurationField(unit="seconds"),
	)

	def changed_10026(self, base):
		base.delete_fields("normal_requirements", "heroic_requirements", "epic_requirements", "normal_reset", "heroic_reset", "epic_reset")

	def changed_10083(self, base):
		self.changed_10026(base)
		base.append_fields(IntegerField("max_players"))

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


class Material(DBStructure):
	"""
	Material.dbc
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("page_material", "PageTextMaterial"),
		UnknownField(),
	)
	
	def changed_9901(self, base):
		base.append_fields(
			UnknownField(),
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
		UnknownField(),
		UnknownField(),
		LocalizedFields("name"),
	)


class PageTextMaterial(DBStructure):
	"""
	PageTextMaterial.dbc
	Material (background image) for pages
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
	)


class PowerDisplay(DBStructure):
	"""
	PowerDisplay.dbc
	"""
	base = Skeleton(
		IDField(),
		UnknownField(),
		StringField("name"),
		ByteField(),
		ByteField(),
		ByteField(),
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
	"""
	base = Skeleton(
		IDField(),
		BooleanField("armor"),
		UnknownField(), # Not spellicon
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
		ForeignKey("cost", "skillcostsdata"),
		LocalizedFields("name"),
		LocalizedFields("description"),
		ForeignKey("icon", "spellicon"),
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
	
	FLAGS = {
		0x00000004: "next_melee",
		0x00000020: "tradespell",
		0x00000040: "passive",
		0x00000400: "next_melee_2",
		0x08000000: "usable_while_sitting",
		0x10000000: "not_usable_in_combat",
	}
	
	FLAGS_2 = {
		0x00000004: "channeled",
		0x00000040: "channeled_2",
	}
	
	FLAGS_5 = {
		0x00000040: "cannot_be_stolen"
	}
	
	FLAGS_6 = {
		0x00000002: "no_reagents_during_preparation",
		0x00020000: "usable_while_feared",
		0x00040000: "usable_while_confused",
	}
	
	base = Skeleton(
		IDField(),
		ForeignKey("category", "SpellCategory"),
		IntegerField("dispel_type"),
		ForeignKey("mechanic", "SpellMechanic"),
		BitMaskField("flags_1", flags=FLAGS),
		BitMaskField("flags_2", flags=FLAGS_2),
		BitMaskField("flags_3"),
		BitMaskField("flags_4"),
		BitMaskField("flags_5", flags=FLAGS_5),
		BitMaskField("flags_6", flags=FLAGS_6),
		BitMaskField("flags_7"),
		IntegerField(), ## Added 320?
		BitMaskField("required_stances"),
		IntegerField(), ##
		BitMaskField("excluded_stances"),
		IntegerField(), ##
		BitMaskField("required_target"),
		BitMaskField("required_target_type"),
		IntegerField("required_object_focus"),
		BitMaskField("facing_flags"),
		IntegerField("required_caster_aura"),
		IntegerField("required_target_aura"),
		IntegerField("excluded_caster_aura"),
		IntegerField("excluded_target_aura"),
		ForeignKey("required_caster_spell", "Spell"),
		ForeignKey("required_target_spell", "Spell"),
		ForeignKey("excluded_caster_spell", "Spell"),
		ForeignKey("excluded_target_spell", "Spell"),
		ForeignKey("cast_time", "SpellCastTimes"),
		DurationField("cooldown", unit="milliseconds"),
		DurationField("category_cooldown", unit="milliseconds"),
		BitMaskField("interrupt_flags"),
		BitMaskField("aura_interrupt_flags"),
		BitMaskField("channeling_interrupt_flags"),
		BitMaskField("proc_type_flags"),
		IntegerField("proc_chance"),
		IntegerField("proc_charges"),
		IntegerField("max_level"),
		IntegerField("base_level"),
		IntegerField("level"),
		ForeignKey("duration", "SpellDuration"),
		IntegerField("power_type"),
		IntegerField("power_amount"),
		IntegerField("power_per_level"),
		IntegerField("power_per_second"),
		IntegerField("power_per_second_per_level"),
		ForeignKey("range", "SpellRange"),
		FloatField("missile_speed"),
		ForeignKey("next_spell", "Spell"),
		IntegerField("stack"),
		ForeignKey("required_tool_1", "Item"),
		ForeignKey("required_tool_2", "Item"),
		ForeignKey("required_reagent_1", "Item"),
		ForeignKey("required_reagent_2", "Item"),
		ForeignKey("required_reagent_3", "Item"),
		ForeignKey("required_reagent_4", "Item"),
		ForeignKey("required_reagent_5", "Item"),
		ForeignKey("required_reagent_6", "Item"),
		ForeignKey("required_reagent_7", "Item"),
		ForeignKey("required_reagent_8", "Item"),
		IntegerField("required_reagent_amount_1"),
		IntegerField("required_reagent_amount_2"),
		IntegerField("required_reagent_amount_3"),
		IntegerField("required_reagent_amount_4"),
		IntegerField("required_reagent_amount_5"),
		IntegerField("required_reagent_amount_6"),
		IntegerField("required_reagent_amount_7"),
		IntegerField("required_reagent_amount_8"),
		IntegerField("required_item_category"),
		BitMaskField("required_item_subclasses"),
		BitMaskField("required_item_slots"),
		ForeignKey("effect_1", "SpellEffectNames"),
		ForeignKey("effect_2", "SpellEffectNames"),
		ForeignKey("effect_3", "SpellEffectNames"),
		IntegerField("die_sides_effect_1"),
		IntegerField("die_sides_effect_2"),
		IntegerField("die_sides_effect_3"),
		IntegerField("dice_base_effect_1"),
		IntegerField("dice_base_effect_2"),
		IntegerField("dice_base_effect_3"),
		IntegerField("dice_per_level_effect_1"),
		IntegerField("dice_per_level_effect_2"),
		IntegerField("dice_per_level_effect_3"),
		FloatField("dice_real_per_level_effect_1"),
		FloatField("dice_real_per_level_effect_2"),
		FloatField("dice_real_per_level_effect_3"),
		IntegerField("damage_base_effect_1"),
		IntegerField("damage_base_effect_2"),
		IntegerField("damage_base_effect_3"),
		IntegerField("mechanic_effect_1"),
		IntegerField("mechanic_effect_2"),
		IntegerField("mechanic_effect_3"),
		IntegerField("implicit_target_1_effect_1"),
		IntegerField("implicit_target_1_effect_2"),
		IntegerField("implicit_target_1_effect_3"),
		IntegerField("implicit_target_2_effect_1"),
		IntegerField("implicit_target_2_effect_2"),
		IntegerField("implicit_target_2_effect_3"),
		ForeignKey("radius_effect_1", "SpellRadius"),
		ForeignKey("radius_effect_2", "SpellRadius"),
		ForeignKey("radius_effect_3", "SpellRadius"),
		ForeignKey("aura_effect_1", "SpellAuraNames"),
		ForeignKey("aura_effect_2", "SpellAuraNames"),
		ForeignKey("aura_effect_3", "SpellAuraNames"),
		IntegerField("aura_interval_effect_1"),
		IntegerField("aura_interval_effect_2"),
		IntegerField("aura_interval_effect_3"),
		FloatField("amplitude_effect_1"),
		FloatField("amplitude_effect_2"),
		FloatField("amplitude_effect_3"),
		IntegerField("chain_targets_effect_1"),
		IntegerField("chain_targets_effect_2"),
		IntegerField("chain_targets_effect_3"),
		UnsignedIntegerField("type_effect_1"),
		UnsignedIntegerField("type_effect_2"),
		UnsignedIntegerField("type_effect_3"),
		IntegerField("misc_value_1_effect_1"),
		IntegerField("misc_value_1_effect_2"),
		IntegerField("misc_value_1_effect_3"),
		IntegerField("misc_value_2_effect_1"),
		IntegerField("misc_value_2_effect_2"),
		IntegerField("misc_value_2_effect_3"),
		ForeignKey("trigger_spell_effect_1", "Spell"),
		ForeignKey("trigger_spell_effect_2", "Spell"),
		ForeignKey("trigger_spell_effect_3", "Spell"),
		FloatField("points_combo_effect_1"),
		FloatField("points_combo_effect_2"),
		FloatField("points_combo_effect_3"),
		BitMaskField("class_flags_1_effect_1"),
		BitMaskField("class_flags_1_effect_2"),
		BitMaskField("class_flags_1_effect_3"),
		BitMaskField("class_flags_2_effect_1"),
		BitMaskField("class_flags_2_effect_2"),
		BitMaskField("class_flags_2_effect_3"),
		BitMaskField("class_flags_3_effect_1"),
		BitMaskField("class_flags_3_effect_2"),
		BitMaskField("class_flags_3_effect_3"),
		ForeignKey("visual_1", "SpellVisual"),
		ForeignKey("visual_2", "SpellVisual"),
		ForeignKey("icon", "SpellIcon"),
		ForeignKey("buff_icon", "SpellIcon"),
		IntegerField("priority"),
		LocalizedFields("name"),
		LocalizedFields("rank"),
		LocalizedFields("description", field_type=SpellMacroField),
		LocalizedFields("buff_description", field_type=SpellMacroField),
		IntegerField("mana_cost_percent"),#
		ForeignKey("category_cooldown_start", "SpellCategory"),
		DurationField("cooldown_start", unit="milliseconds"),
		IntegerField("max_target_level"),
		IntegerField(), # m_spellClassSet SpellFamilyName?
		BitMaskField("spell_class_flags_1"),
		BitMaskField("spell_class_flags_2"),
		BitMaskField("spell_class_flags_3"),
		IntegerField("max_targets"),
		IntegerField(), # m_defenseType DmgClass?
		IntegerField(), # m_preventionType?
		IntegerField("stance_bar_order"),
		FloatField("chain_amplitude_effect_1"), # added when? 
		FloatField("chain_amplitude_effect_2"),
		FloatField("chain_amplitude_effect_3"),
		ForeignKey("required_faction", "Faction"),
		IntegerField("required_reputation"),
		IntegerField("required_aura_vision"),
		ForeignKey("required_tool_category_1", "TotemCategory"),
		ForeignKey("required_tool_category_2", "TotemCategory"),
		IntegerField(), # m_requiredAreaGroupId?
		BitMaskField("school_flags"),
		ForeignKey("rune_cost", "SpellRuneCost"),
		ForeignKey("missile", "SpellMissile"),
		ForeignKey("power_display", "PowerDisplay"), # added 3.1?
	)

	def changed_10026(self, base):
		base.append_fields(
			FloatField("multiplier_effect_1"),
			FloatField("multiplier_effect_2"),
			FloatField("multiplier_effect_3"),
			ForeignKey("descriptionvars", "SpellDescriptionVariables"),
		)

	def changed_10522(self, base):
		self.changed_10026(base)
		base.append_fields(
			UnknownField(),
		)


class SpellAuraNames(DBStructure):
	"""
	SpellAuraNames.dbc
	TODO - Structure 1.1.2.4125
	"""
	DEAD = True
	base = Skeleton(
		IDField(),
		IntegerField(),
		StringField("internal_name"),
		LocalizedFields("name", locales=OLD_LOCALES),
	)


class SpellCategory(DBStructure):
	"""
	SpellCategory.dbc
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
		DurationField("cast_time", unit="milliseconds"),
		IntegerField("modifier"),
		DurationField("cast_time_max", unit="milliseconds"),
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
		DurationField("duration_1", unit="milliseconds"),
		DurationField("duration_2", unit="milliseconds"),
		DurationField("duration_3", unit="milliseconds"),
	)


class SpellEffectNames(DBStructure):
	"""
	SpellEffectNames.dbc
	TODO - Structure 1.1.2.4125
	"""
	DEAD = True
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
		IntegerField("type_effect_1"),
		IntegerField("type_effect_2"),
		IntegerField("type_effect_3"),
		IntegerField("amount_min_effect_1"),
		IntegerField("amount_min_effect_2"),
		IntegerField("amount_min_effect_3"),
		IntegerField("amount_max_effect_1"),
		IntegerField("amount_max_effect_2"),
		IntegerField("amount_max_effect_3"),
		IntegerField("effect_1"), #fkey stat/spell
		IntegerField("effect_2"), #fkey stat/spell
		IntegerField("effect_3"), #fkey stat/spell
		LocalizedFields("name"),
		ForeignKey("glow", "ItemVisuals"), # glow?
		IntegerField(),
		ForeignKey("gem", "item"), # added 5610
		ForeignKey("conditions", "SpellItemEnchantmentCondition"), # added 5610
		ForeignKey("required_skill", "SkillLine"), # added 3.x
		IntegerField("required_skill_level"), # added 3.x
	)
	
	def changed_9637(self, base):
		base.append_fields(
			IntegerField("required_level"),
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
		FloatField("radius_min"),
		IntegerField(),
		FloatField("radius_max"),
	)


class SpellRange(DBStructure):
	"""
	SpellRange.dbc
	Spell range data
	"""
	base = Skeleton(
		IDField(),
		FloatField("range_min"),
		FloatField("range_min_friendly"),
		FloatField("range_max"),
		FloatField("range_max_friendly"),
		BitMaskField("flags"),
		LocalizedFields("name"),
		LocalizedFields("tooltipname"),
	)


class SpellRuneCost(DBStructure):
	"""
	SpellRunecost.dbc
	Death Knight abilities' rune costs
	"""
	base = Skeleton(
		IDField(),
		IntegerField("blood"),
		IntegerField("unholy"),
		IntegerField("frost"),
		IntegerField("runic_power"),
	)


class SpellShapeshiftForm(DBStructure):
	"""
	SpellShapeshiftForm.dbc
	Different shapeshifts/stances for spells
	"""
	base = Skeleton(
		IDField(),
		IntegerField("button_position"),
		LocalizedFields("name"),
		BitMaskField("flags"),
		IntegerField("creature_type"),
		ForeignKey("icon", "SpellIcon"),
		IntegerField("attack_speed"),
		IntegerField("model_alliance"),
		IntegerField("model_horde"),
		UnknownField(),
		UnknownField(),
		ForeignKey("spell_1", "Spell"),
		ForeignKey("spell_2", "Spell"),
		ForeignKey("spell_3", "Spell"),
		ForeignKey("spell_4", "Spell"),
		ForeignKey("spell_5", "Spell"),
		ForeignKey("spell_6", "Spell"),
		ForeignKey("spell_7", "Spell"),
		ForeignKey("spell_8", "Spell"),
	)


class SpellVisualEffectName(DBStructure):
	"""
	SpellVisualEffectName.dbc
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
		IntegerField("icon"),
		BitMaskField("classmask"),
		IntegerField("petmask"), #petflags?
		IntegerField("tabpage"),
		StringField("internal_name"),
	)


class TaxiNodes(DBStructure):
	"""
	TaxiNodes.dbc
	Flight paths, teleports, etc.
	"""
	base = Skeleton(
		IDField(),
		IntegerField("instance"),
		FloatField("coord_x"),
		FloatField("coord_y"),
		FloatField("coord_z"),
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
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class WorldMapArea(DBStructure):
	"""
	WorldMapArea.dbc
	Map data for each "zone" (instance)
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "Map"),
		ForeignKey("area", "AreaTable"),
		StringField("name"),
		FloatField("y_1"),
		FloatField("y_2"),
		FloatField("x_1"),
		FloatField("x_2"),
		ForeignKey("virtual_map", "Map"),
		ForeignKey("dungeon_map", "DungeonMap"),
	)
	
	def changed_10116(self, base):
		base.append_fields(
			ForeignKey("parent_area", "WorldMapArea"), # Not for all?!
		)


class WorldMapContinent(DBStructure):
	"""
	WorldMapContinent.dbc
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("instance", "Map"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)
	
	def changed_9901(self, base):
		"""
		XXX Unknown build!
		"""
		base.append_fields(
			UnknownField(),
		)


class WorldMapOverlay(DBStructure):
	"""
	WorldMapOverlay.dbc
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("zone", "WorldMapArea"),
		ForeignKey("area_1", "AreaTable"),
		ForeignKey("area_2", "AreaTable"),
		ForeignKey("area_3", "AreaTable"),
		ForeignKey("area_4", "AreaTable"),
		ForeignKey("area_5", "AreaTable"), # unused
		ForeignKey("area_6", "AreaTable"), # unused
		StringField("name"),
		IntegerField("width"),
		IntegerField("height"),
		IntegerField("left"),
		IntegerField("top"),
		IntegerField("y1"),
		IntegerField("x1"),
		IntegerField("y2"),
		IntegerField("x2"),
	)


class WorldMapTransforms(DBStructure):
	"""
	WorldMapTransforms.dbc
	Coordinate transformations from one
	instance to another - Example:
	Expansion01 -> Azuremyst Isles
	"""
	base = Skeleton(
		IDField(),
		ForeignKey("map", "Map"),
		FloatField(), # x1
		FloatField(), # x2
		FloatField(), # y1
		FloatField(), # y2
		ForeignKey("target_map", "Map"),
		FloatField("target_x"),
		FloatField("target_y"),
		UnknownField(),
	)


class WorldStateZoneSounds(DBStructure):
	"""
	WorldStateZoneSounds.dbc
	"""
	base = Skeleton(
		ImplicitIDField(),
		IntegerField("world_state"),
		IntegerField("value"),
		ForeignKey("area", "AreaTable"),
		ForeignKey("area_wmo", "WMOAreaTable"),
		ForeignKey("intro_music", "ZoneIntroMusicTable"),
		ForeignKey("music", "ZoneMusic"),
		ForeignKey("sound_ambience", "SoundAmbience"),
		ForeignKey("preferences", "SoundProviderPreferences"),
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
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		ForeignKey("sound", "SoundEntries"),
		BooleanField(),
		DurationField(unit="seconds"),
	)


class ZoneMusic(DBStructure):
	"""
	ZoneMusic.dbc
	Music played in a zone
	"""
	base = Skeleton(
		IDField(),
		StringField("name"),
		DurationField("duration_day", unit="milliseconds"),
		DurationField("duration_night", unit="milliseconds"),
		DurationField("loop_wait_day", unit="milliseconds"), # How long until it plays again
		DurationField("loop_wait_night", unit="milliseconds"),
		ForeignKey("music_day", "SoundEntries"),
		ForeignKey("music_night", "SoundEntries"),
	)
