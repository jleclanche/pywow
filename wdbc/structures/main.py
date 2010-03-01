#!/usr/bin/python
# -*- coding: utf-8 -*-

from .gameobject import GAME_OBJECT_TYPES
from ..structures import *


##
# WDB structures
#

class CreatureCache(Structure):
	"""
	creaturecache.wdb
	NPC/mob data
	"""
	signature = "BOMW"
	fields = Skeleton(
		IDField(),
		RecLenField(),
		StringField("name"),
		StringField("name2"),
		StringField("name3"),
		StringField("name4"),
		StringField("title"),
		StringField("cursor"),
		BitMaskField("flags"),
		ForeignKey("category", "CreatureType"), #dragonkin, ...
		ForeignKey("family", "CreatureFamily"), # hunter pet family
		IntegerField("type"), # elite, rareelite, boss, rare
		ForeignKey("tamed_spells", "CreatureSpellData"),
		ForeignKey("model_1", "CreatureDisplayInfo"),
		ForeignKey("model_2", "CreatureDisplayInfo"), # added in 2.2
		ForeignKey("model_3", "CreatureDisplayInfo"), # added in 2.2
		ForeignKey("model_4", "CreatureDisplayInfo"), # added in 2.2
		FloatField(),
		FloatField(),
		ByteField("leader"),
	)

	def changed_9614(self, fields):
		fields.insert_field(ForeignKey("vehicle_spells", "CreatureSpellData"), before="model_1")
		fields.append_fields(
			ForeignKey("quest_item_1", "Item"),
			ForeignKey("quest_item_2", "Item"),
			ForeignKey("quest_item_3", "Item"),
			ForeignKey("quest_item_4", "Item"),
			IntegerField(),
		)

	def changed_10026(self, fields):
		self.changed_9614(fields)
		fields.append_fields(
			UnknownField(),
			UnknownField(),
		)


class GameObjectCache(Structure):
	"""
	gameobjectcache.wdb
	World object data
	"""
	signature = "BOGW"
	
	fields = Skeleton(
		IDField(),
		RecLenField(),
		IntegerField("type"),
		ForeignKey("display", "GameObjectDisplayInfo"),
		StringField("name"),
		StringField("name2"),
		StringField("name3"),
		StringField("name4"),
		StringField("cursor"),
		StringField("action"),
		StringField(),
		Union("data",
			fields = (
				IntegerField("data_1"),
				IntegerField("data_2"),
				IntegerField("data_3"),
				IntegerField("data_4"),
				IntegerField("data_5"),
				IntegerField("data_6"),
				IntegerField("data_7"),
				IntegerField("data_8"),
				IntegerField("data_9"),
				IntegerField("data_10"),
				IntegerField("data_11"),
				IntegerField("data_12"),
				IntegerField("data_13"),
				IntegerField("data_14"),
				IntegerField("data_15"),
				IntegerField("data_16"),
				IntegerField("data_17"),
				IntegerField("data_18"),
				IntegerField("data_19"),
				IntegerField("data_20"),
				IntegerField("data_21"),
				IntegerField("data_22"),
				IntegerField("data_23"),
				IntegerField("data_24"),
			),
			get_structure = lambda row: GAME_OBJECT_TYPES[row.type]
		),
		FloatField("scale"),
		ForeignKey("quest_item_1", "Item"),
		ForeignKey("quest_item_2", "Item"),
		ForeignKey("quest_item_3", "Item"),
		ForeignKey("quest_item_4", "Item"),
	)

	def changed_10314(self, fields):
		fields.append_fields(
			ForeignKey("quest_item_5", "Item"),
			ForeignKey("quest_item_6", "Item"),
		)


class ItemCache(Structure):
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
	
	fields = Skeleton(
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
		IntegerField("holy_resist"),
		IntegerField("fire_resist"),
		IntegerField("nature_resist"),
		IntegerField("frost_resist"),
		IntegerField("shadow_resist"),
		IntegerField("arcane_resist"),
		IntegerField("speed"),
		IntegerField("ammo"),
		FloatField(),
		ForeignKey("spell1", "spell"),
		IntegerField("spelltrigger1"),
		IntegerField("spellcharges1"),
		DurationField("spell_cooldown_1", unit="milliseconds"),
		IntegerField("spellcategory1"),
		IntegerField("spell_cooldown_category_1"),
		ForeignKey("spell2", "spell"),
		IntegerField("spelltrigger2"),
		IntegerField("spellcharges2"),
		DurationField("spell_cooldown_2", unit="milliseconds"),
		IntegerField("spellcategory2"),
		IntegerField("spell_cooldown_category_2"),
		ForeignKey("spell3", "spell"),
		IntegerField("spelltrigger3"),
		IntegerField("spellcharges3"),
		DurationField("spell_cooldown_3", unit="milliseconds"),
		IntegerField("spellcategory3"),
		IntegerField("spell_cooldown_category_3"),
		ForeignKey("spell4", "spell"),
		IntegerField("spelltrigger4"),
		IntegerField("spellcharges4"),
		DurationField("spell_cooldown_4", unit="milliseconds"),
		IntegerField("spellcategory4"),
		IntegerField("spell_cooldown_category_4"),
		ForeignKey("spell5", "spell"),
		IntegerField("spelltrigger5"),
		IntegerField("spellcharges5"),
		DurationField("spell_cooldown_5", unit="milliseconds"),
		IntegerField("spellcategory5"),
		IntegerField("spell_cooldown_category_5"),
		IntegerField("bind"),
		StringField("note"),
		ForeignKey("page", "pagetextcache"),
		ForeignKey("pagelanguage", "Languages"),
		ForeignKey("pagestationery", "Stationery"),
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
		BitMaskField("socket_1"),
		IntegerField("socket_info_1"),
		BitMaskField("socket_2"),
		IntegerField("socket_info_2"),
		BitMaskField("socket_3"),
		IntegerField("socket_info_3"),
		ForeignKey("socket_bonus", "SpellItemEnchantment"),
		ForeignKey("gem_properties", "GemProperties"),
		IntegerField("extended_cost"),
	)
	
	def changed_5875(self, fields):
		"""
		- New disenchant IntegerField
		  UNKNOWN BUILD
		"""
		fields.append_fields(
			IntegerField("disenchant"),
		)
	
	def changed_6022(self, fields):
		"""
		- New unknown IntegerField before name field
		"""
		self.changed_5875(fields)
		fields.insert_field(IntegerField("depclass"), before="name")
	
	def changed_6213(self, fields):
		"""
		- New unknown IntegerField
		"""
		self.changed_6022(fields)
		fields.insert_field(ForeignKey("randomenchantment2", "itemrandomsuffix"), before="block")
	
	def changed_6577(self, fields):
		"""
		- New armordmgmod FloatField
		"""
		self.changed_6213(fields)
		fields.append_fields(
			FloatField("armordmgmod"),
		)
	
	def changed_7382(self, fields):
		"""
		- New ItemCondExtCosts fkey before disenchant field
		  UNKNOWN BUILD
		"""
		self.changed_6577(fields)
		fields.insert_field(IntegerField("extended_cost_cond"), before="disenchant")
	
	def changed_7994(self, fields):
		"""
		- Removed extendedcost and extendedcostcond fields
		  UNKNOWN BUILD
		"""
		self.changed_7382(fields)
		fields.delete_fields("extended_cost", "extended_cost_cond")
	
	def changed_8268(self, fields):
		"""
		- Added duration field at the end, replacing the old server overwrite model
		  This might be changed_8209.
		"""
		self.changed_7994(fields)
		fields.append_fields(DurationField("duration", unit="seconds"))
	
	def changed_8391(self, fields):
		"""
		- New uniquecategory field at the end, fkey of new ItemLimitCategory.dbc file
		"""
		self.changed_8268(fields)
		fields.append_fields(ForeignKey("unique_category", "ItemLimitCategory"))
	
	def changed_8471(self, fields):
		"""
		- Made the 20 stats column dynamic
		- New scalingdist and scalingflags fields after the new stats columns
		"""
		self.changed_8391(fields)
		fields.delete_fields(
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
		fields.insert_field(
			DynamicFields("stats", ((
				(IntegerField, "id"),
				(IntegerField, "amt"),
			), 10)
		), before="dmgmin1")
		fields.insert_field(ForeignKey("scaling_stats", "scalingstatdistribution"), before="dmgmin1")
		fields.insert_field(BitMaskField("scaling_flags"), before="dmgmin1")
	
	def changed_8478(self, fields):
		self.changed_8268(fields)
	
	def changed_8770(self, fields):
		self.changed_8471(fields)
	
	def changed_9614(self, fields):
		"""
		- Deleted unused dmgmin, dmgmax and dmgtype 3-5 fields
		- Added new unknown IntegerField at the end
		"""
		self.changed_8770(fields)
		fields.delete_fields(
			"dmgmin3", "dmgmax3", "dmgtype3",
			"dmgmin4", "dmgmax4", "dmgtype4",
			"dmgmin5", "dmgmax5", "dmgtype5",
		)
		fields.append_fields(
			ForeignKey("required_holiday", "holidays"),
		)
	
	def changed_10026(self, fields):
		self.changed_9614(fields)
		fields.insert_field(BitMaskField("flags2"), before="buy_price")


class ItemNameCache(Structure):
	"""
	itemnamecache.wdb
	Cached itemset data
	"""
	signature = "BDNW"
	fields = Skeleton(
		IDField(),
		RecLenField(),
		StringField("name"),
		IntegerField("slot"),
	)


class ItemTextCache(Structure):
	"""
	itemtextcache.wdb
	Mails and misc
	"""
	signature = "XTIW"
	fields = Skeleton(
		IDField(),
		RecLenField(),
		StringField(),
	)


class NPCCache(Structure):
	"""
	npccache.wdb
	NPC gossip data
	"""
	signature = "BDNW"
	fields = Skeleton(
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


class QuestCache(Structure):
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
		0x00002000: "flags_pvp",
		0x00008000: "weekly",
	}
	
	get_kill_relation = lambda x, value: value == value & 0x7fffffff and "creaturecache" or "gameobjectcache"
	get_kill_value = lambda x, value: value & 0x7fffffff

	fields = Skeleton(
		IDField(),
		RecLenField(),
		ForeignKey("self", "questcache"),
		IntegerField("tag"),
		IntegerField("level"),
		IntegerField("category"), # GFK QuestInfo/AreaTable
		ForeignKey("type", "QuestInfo"),
		IntegerField("suggested_players"),
		ForeignKey("required_faction_1", "Faction"),
		IntegerField("required_reputation_1"),
		ForeignKey("required_faction_2", "Faction"),
		IntegerField("required_reputation_2"),
		IntegerField("followup"),
		IntegerField("money_reward"),
		IntegerField("money_reward_cap"),
		ForeignKey("spell_reward", "Spell"),
		ForeignKey("spell_trigger", "Spell"),
		UnknownField(), # unused apart from 200 in 13233/13234
		ForeignKey("provided_item", "Item"),
		BitMaskField("flags", flags=FLAGS),
		ForeignKey("item_reward_1", "Item"),
		IntegerField("item_reward_amount_1"),
		ForeignKey("item_reward_2", "Item"),
		IntegerField("item_reward_amount_2"),
		ForeignKey("item_reward_3", "Item"),
		IntegerField("item_reward_amount_3"),
		ForeignKey("item_reward_4", "Item"),
		IntegerField("item_reward_amount_4"),
		ForeignKey("item_choice_reward_1", "Item"),
		IntegerField("item_choice_reward_amount_1"),
		ForeignKey("item_choice_reward_2", "Item"),
		IntegerField("item_choice_reward_amount_2"),
		ForeignKey("item_choice_reward_3", "Item"),
		IntegerField("item_choice_reward_amount_3"),
		ForeignKey("item_choice_reward_4", "Item"),
		IntegerField("item_choice_reward_amount_4"),
		ForeignKey("item_choice_reward_5", "Item"),
		IntegerField("item_choice_reward_amount_5"),
		ForeignKey("item_choice_reward_6", "Item"),
		IntegerField("item_choice_reward_amount_6"),
		ForeignKey("instance", "Map"),
		FloatField("coord_x"),
		FloatField("coord_y"),
		UnknownField(),
		StringField("name"),
		StringField("objective"),
		StringField("description"),
		StringField("summary"),
		GenericForeignKey("required_kill_1", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("required_kill_amount_1"),
		ForeignKey("quest_item_1", "Item"),
		GenericForeignKey("required_kill_2", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("required_kill_amount_2"),
		ForeignKey("quest_item_2", "Item"),
		GenericForeignKey("required_kill_3", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("required_kill_amount_3"),
		ForeignKey("quest_item_3", "Item"),
		GenericForeignKey("required_kill_4", get_relation=get_kill_relation, get_value=get_kill_value),
		IntegerField("required_kill_amount_4"),
		ForeignKey("quest_item_4", "Item"),
		ForeignKey("required_item_1", "Item"),
		IntegerField("required_item_amount_1"),
		ForeignKey("required_item_2", "Item"),
		IntegerField("required_item_amount_2"),
		StringField("objective_text_1"),
		StringField("objective_text_2"),
		StringField("objective_text_3"),
		StringField("objective_text_4"),
	)
	
	def changed_8125(self, fields):
		fields.insert_field(ForeignKey("title_reward", "CharTitles"), before="item_reward_1")
	
	def changed_8770(self, fields):
		self.changed_8125(fields)
		fields.insert_fields((
			IntegerField("required_player_kills"),
			IntegerField("bonus_talents"),
		), before="item_reward_1")
		fields.insert_fields((
			ForeignKey("required_item_3", "Item"),
			IntegerField("required_item_amount_3"),
			ForeignKey("required_item_4", "Item"),
			IntegerField("required_item_amount_4"),
		), before="objective_text_1")
	
	def changed_9355(self, fields):
		self.changed_8770(fields)
		fields.insert_fields((
			ForeignKey("required_item_5", "Item"),
			IntegerField("required_item_amount_5"),
		), before="objective_text_1")
	
	def changed_10026(self, fields):
		self.changed_9355(fields)
		fields.insert_fields((
			ForeignKey("required_item_6", "Item"),
			IntegerField("required_item_amount_6"),
		), before="objective_text_1")
	
	##
	# QuestFactionReward.dbc has two rows.
	# Row 1 is for positive gains, row 2 is for
	# negative gains. If the questcache value is
	# positive, row 2 is linked; otherwise row 1.
	get_reputation_reward_row = lambda x, row, value: 2 if value < 0 else 1
	get_reputation_reward_column = lambda x, row, value: "reputation_gain_%i" % (abs(value))
	
	def changed_10522(self, fields):
		self.changed_10026(fields)
		fields.insert_field(FloatField("honor_reward_multiplier"), before="provided_item")
		fields.insert_field(IntegerField("arena_reward"), before="item_reward_1")
		fields.insert_field(UnknownField(), before="item_reward_1")
		fields.insert_fields([
			ForeignKey("faction_reward_1", "Faction"),
			ForeignKey("faction_reward_2", "Faction"),
			ForeignKey("faction_reward_3", "Faction"),
			ForeignKey("faction_reward_4", "Faction"),
			ForeignKey("faction_reward_5", "Faction"),
			ForeignCell("reputation_reward_1", "QuestFactionReward", get_row=self.get_reputation_reward_row, get_column=self.get_reputation_reward_column),
			ForeignCell("reputation_reward_2", "QuestFactionReward", get_row=self.get_reputation_reward_row, get_column=self.get_reputation_reward_column),
			ForeignCell("reputation_reward_3", "QuestFactionReward", get_row=self.get_reputation_reward_row, get_column=self.get_reputation_reward_column),
			ForeignCell("reputation_reward_4", "QuestFactionReward", get_row=self.get_reputation_reward_row, get_column=self.get_reputation_reward_column),
			ForeignCell("reputation_reward_5", "QuestFactionReward", get_row=self.get_reputation_reward_row, get_column=self.get_reputation_reward_column),
			IntegerField("reputation_override_1"),
			IntegerField("reputation_override_2"),
			IntegerField("reputation_override_3"),
			IntegerField("reputation_override_4"),
			IntegerField("reputation_override_5"),
		], before="instance")
		fields.insert_field(StringField("quick_summary"), before="required_kill_1")
	
	def changed_10554(self, fields):
		self.changed_10522(fields)
		fields.insert_field(IntegerField("required_level"), before="category")
		fields.insert_field(
			ForeignCell("experience_reward", "QuestXP",
				get_row = lambda row, value: row.level,
				get_column = lambda row, value: "experience_%i" % (value) if value else None,
			),
		before="money_reward")
	
	def changed_10772(self, fields):
		self.changed_10554(fields)
		fields.insert_field(IntegerField("quest_item_amount_1"), before="required_kill_2") # XXX thats not it ...
		fields.insert_field(IntegerField("quest_item_amount_2"), before="required_kill_3")
		fields.insert_field(IntegerField("quest_item_amount_3"), before="required_kill_4")
		fields.insert_field(IntegerField("quest_item_amount_4"), before="required_item_1")


class PageTextCache(Structure):
	"""
	pagetextcache.wdb
	Cached page data
	"""
	signature = "XTPW"
	fields = Skeleton(
		IDField(),
		RecLenField(),
		StringField("text"),
		ForeignKey("next_page", "pagetextcache"),
	)

class WoWCache(Structure):
	"""
	wowcache.wdb
	Warden data
	"""
	signature = "NDRW"
	fields = Skeleton(
		HashField("_id"),
		RecLenField(),
		IntegerField("data_length"),
		DataField("data", master="data_length")
	)


##
# DBC Structures
#

class Achievement(Structure):
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
	
	fields = Skeleton(
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


class Achievement_Category(Structure):
	"""
	Achievement_Category.dbc
	Achievement categories
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("parent", "achievement_category"),
		LocalizedFields("name"),
		IntegerField("groupsort"),
	)


class Achievement_Criteria(Structure):
	"""
	Achievement_Criteria.dbc
	Achievement criterias
	"""
	fields = Skeleton(
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


class AnimationData(Structure):
	"""
	AnimationData.dbc
	Animation data
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		BitMaskField("weapon_state"),
		BitMaskField("flags"),
		UnknownField(),
		ForeignKey("animation_before", "AnimationData"),
		ForeignKey("real_animation", "AnimationData"),
		IntegerField("flying"), # fly = 3
	)


class AreaGroup(Structure):
	"""
	AreaGroup.dbc
	Added during 3.0.x
	XXX What's this used for?
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("area_1", "AreaTable"),
		ForeignKey("area_2", "AreaTable"),
		ForeignKey("area_3", "AreaTable"),
		ForeignKey("area_4", "AreaTable"),
		ForeignKey("area_5", "AreaTable"),
		ForeignKey("area_6", "AreaTable"),
		ForeignKey("next_group", "AreaGroup"),
	)


class AreaPOI(Structure):
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
	
	fields = Skeleton(
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


class AreaTable(Structure):
	"""
	AreaTable.dbc
	Contains all zone and subzone data.
	"""
	
	TERRITORY_FLAGS = { # Sanctuary = 2+4, contested = 0
		0x02: "Horde",
		0x04: "Alliance",
	}
	
	fields = Skeleton(
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


class AreaTrigger(Structure):
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
	fields = Skeleton(
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


class AttackAnimKits(Structure):
	"""
	AttackAnimKits.dbc
	Unknown use
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("animation", "AnimationData"),
		ForeignKey("type", "AttackAnimTypes"),
		BitMaskField(),
		UnknownField(),
	)


class AttackAnimTypes(Structure):
	"""
	AttackAnimTypes.dbc
	Attack animation types...
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
	)


class AuctionHouse(Structure):
	"""
	AuctionHouse.dbc
	Data about auction houses and their fees
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("faction", "Faction"),
		IntegerField("auction_fee"),
		IntegerField("deposit_fee"),
		LocalizedFields("name"),
	)


class BarberShopStyle(Structure):
	"""
	Hairstyles, facial hair, etc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("type"), # 0 - Hair Style, 1 - Hair Color, 2 - Facial Hairstyle
		LocalizedFields("name"),
		LocalizedFields("unknown"),
		FloatField("price_modifier"),
		ForeignKey("race", "ChrRaces"),
		IntegerField("gender"),
		UnknownField(), # what?: This is option $ID2 in the shop when looking in category $Type. OR "real ID to hair/facial hair"
	)


class BattlemasterList(Structure):
	"""
	BattlemasterList.dbc
	Called when talking to a battlemaster.
	Added in TBC
	"""
	fields = Skeleton(
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
	
	def changed_9551(self, fields):
		fields.insert_field(IntegerField("min_players"), before="level_band")
		fields.update_locales(LOCALES) # XXX When did locales change?
		fields.append_fields(IntegerField("max_group_size"))
	
	def changed_9658(self, fields):
		"""
		What's this field? 0 for all arenas
		1- Alterac Valley = 1941
		2- Warsong Gulch = 1942
		3- Arathi Basin = 1943
		7- Eye of the Storm = 2851
		9- Strand of the Ancients = 3695
		"""
		self.changed_9551(fields)
		fields.append_fields(IntegerField("unknown_9658"))
	
	def changed_10554(self, fields):
		self.changed_9658(fields)
		fields.delete_fields(
			"min_players",
			"level_band",
			"min_level",
			"max_level",
		)


class BankBagSlotPrices(Structure):
	"""
	BankBagSlotPrices.dbc
	Price for bank bag slots.
	"""
	fields = Skeleton(
		IDField(),
		MoneyField("price"),
	)


class BannedAddons(Structure):
	"""
	BannedAddons.dbc
	"""
	fields = Skeleton(
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
	)


class CameraShakes(Structure):
	"""
	CameraShakes.dbc
	Just shakin'
	Example:
	CGCamera::AddShake( Col2, Type, Col4*0.027777778, Col5, Col6, Col7, Col8 );
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField("type"),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class Cfg_Categories(Structure):
	"""
	Cfg_Categories.dbc
	Server localizations
	"""
	fields = Skeleton(
		IDField(),
		BitMaskField("flags"), # 256: russia, 205: eu
		IntegerField("type"), # 0: Development, 1: US and EU, 4: Russia, 10: Korea, 17: Taiwan & China
		BooleanField("tournament"),
		LocalizedFields("name"),
	)


class Cfg_Configs(Structure):
	"""
	Cfg_Configs.dbc
	What the hell is this used for? Servers?
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(), # always id-1
		BooleanField(),
		BooleanField(),
	)


class CharacterCreateCameras(Structure):
	"""
	CharacterCreateCameras.dbc
	Removed in 6320
	"""
	DEAD = True
	fields = Skeleton(
		IDField(),
		BooleanField(),
		BooleanField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class CharacterFacialHairStyles(Structure):
	"""
	CharacterFacialHairStyles.dbc
	Used for all facial changes, hair styles, markings, tusks...
	"""
	implicit_id = True
	fields = Skeleton(
		ForeignKey("race", "ChrRaces"),
		IntegerField("gender"),
		IntegerField("specific_id"),
		#UnknownField(), Removed in 2.x
		#UnknownField(),
		#UnknownField(),
		IntegerField("geoset_1"), # http://www.madx.dk/wowdev/wiki/index.php?title=M2/WotLK/.skin#Mesh_part_ID
		IntegerField("geoset_2"),
		IntegerField("geoset_3"),
		IntegerField("geoset_4"), # unsigned? row 189
		IntegerField("geoset_5"), # unsigned? row 189
	)


class CharBaseInfo(Structure):
	"""
	CharBaseInfo.dbc
	Defines availability of classes for the different races.
	"""
	implicit_id = True
	fields = Skeleton(
		ForeignByte("race", "ChrRaces"), #, field=ByteField),
		ForeignByte("class", "ChrClasses"), #, field=ByteField),
	)


class CharHairGeosets(Structure):
	"""
	CharHairGeosets.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("race", "ChrRaces"),
		IntegerField("gender"),
		IntegerField("hair_type"),
		IntegerField("geoset"), # Defines the connection between HairType and Geoset number in MDX model
		BooleanField("bald"),
	)


class CharHairTextures(Structure):
	"""
	CharHairTextures.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("race", "ChrRaces"),
		IntegerField("gender"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class CharSections(Structure):
	"""
	CharHairTextures.dbc
	Defines the textures for the different types of
	character-variations that involve a texture only.
	These are hair, beards, the base skin etc.
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("race", "ChrRaces"),
		IntegerField("gender"),
		IntegerField("general_type"), # See http://www.madx.dk/wowdev/wiki/index.php?title=CharSections.dbc
		FilePathField("texture_1"),
		FilePathField("texture_2"),
		FilePathField("texture_3"),
		BitMaskField("flags"),
		IntegerField("type"),
		IntegerField("variation"), # CharVariations.dbc?
	)


class CharStartOutfit(Structure):
	"""
	CharStartOutfit.dbc
	Items characters get when they are created.
	Also includes hearthstone/food, etc.
	"""
	fields = Skeleton(
		IDField(),
		ByteField("race"),
		ByteField("class"),
		ByteField("gender"),
		ByteField("padding"), # pad byte
		ForeignKey("item_1", "Item"),
		ForeignKey("item_2", "Item"),
		ForeignKey("item_3", "Item"),
		ForeignKey("item_4", "Item"),
		ForeignKey("item_5", "Item"),
		ForeignKey("item_6", "Item"),
		ForeignKey("item_7", "Item"),
		ForeignKey("item_8", "Item"),
		ForeignKey("item_9", "Item"),
		ForeignKey("item_10", "Item"),
		ForeignKey("item_11", "Item"),
		ForeignKey("display_1", "ItemDisplayInfo"),
		ForeignKey("display_2", "ItemDisplayInfo"),
		ForeignKey("display_3", "ItemDisplayInfo"),
		ForeignKey("display_4", "ItemDisplayInfo"),
		ForeignKey("display_5", "ItemDisplayInfo"),
		ForeignKey("display_6", "ItemDisplayInfo"),
		ForeignKey("display_7", "ItemDisplayInfo"),
		ForeignKey("display_8", "ItemDisplayInfo"),
		ForeignKey("display_9", "ItemDisplayInfo"),
		ForeignKey("display_10", "ItemDisplayInfo"),
		ForeignKey("display_11", "ItemDisplayInfo"),
		ForeignKey("display_12", "ItemDisplayInfo"),
		IntegerField("inventory_type_1"),
		IntegerField("inventory_type_2"),
		IntegerField("inventory_type_3"),
		IntegerField("inventory_type_4"),
		IntegerField("inventory_type_5"),
		IntegerField("inventory_type_6"),
		IntegerField("inventory_type_7"),
		IntegerField("inventory_type_8"),
		IntegerField("inventory_type_9"),
		IntegerField("inventory_type_10"),
		IntegerField("inventory_type_11"),
		IntegerField("inventory_type_12"),
	)
	
	def changed_9901(self, fields):
		"""
		Doubled all the items
		XXX When did this happen?
		"""
		fields.insert_fields([
			ForeignKey("item_12", "Item"),
			ForeignKey("item_13", "Item"),
			ForeignKey("item_14", "Item"),
			ForeignKey("item_15", "Item"),
			ForeignKey("item_16", "Item"),
			ForeignKey("item_17", "Item"),
			ForeignKey("item_18", "Item"),
			ForeignKey("item_19", "Item"),
			ForeignKey("item_20", "Item"),
			ForeignKey("item_21", "Item"),
			ForeignKey("item_22", "Item"),
			ForeignKey("item_23", "Item"),
			ForeignKey("item_24", "Item"),
		], before="display_1")
		
		fields.insert_fields([
			ForeignKey("display_13", "ItemDisplayInfo"),
			ForeignKey("display_14", "ItemDisplayInfo"),
			ForeignKey("display_15", "ItemDisplayInfo"),
			ForeignKey("display_16", "ItemDisplayInfo"),
			ForeignKey("display_17", "ItemDisplayInfo"),
			ForeignKey("display_18", "ItemDisplayInfo"),
			ForeignKey("display_19", "ItemDisplayInfo"),
			ForeignKey("display_20", "ItemDisplayInfo"),
			ForeignKey("display_21", "ItemDisplayInfo"),
			ForeignKey("display_22", "ItemDisplayInfo"),
			ForeignKey("display_23", "ItemDisplayInfo"),
			ForeignKey("display_24", "ItemDisplayInfo"),
		], before="inventory_type_1")
		
		fields.append_fields(
			IntegerField("inventory_type_13"),
			IntegerField("inventory_type_14"),
			IntegerField("inventory_type_15"),
			IntegerField("inventory_type_16"),
			IntegerField("inventory_type_17"),
			IntegerField("inventory_type_18"),
			IntegerField("inventory_type_19"),
			IntegerField("inventory_type_20"),
			IntegerField("inventory_type_21"),
			IntegerField("inventory_type_22"),
			IntegerField("inventory_type_23"),
			IntegerField("inventory_type_24"),
		)


class CharTitles(Structure):
	"""
	CharTitles.dbc
	Player titles
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(), # related to achievements?
		LocalizedFields("title"),
		LocalizedFields("title_female"),
		IntegerField("index"),
	)


class CharVariations(Structure):
	"""
	CharVariations.dbc
	"""
	fields = Skeleton(
		IDField(), # shared with ChrRaces
		IntegerField("gender"),
		UnknownField(),
		BitMaskField(),
		BitMaskField(),
		UnknownField(),
	)


class ChatChannels(Structure):
	"""
	ChatChannels.dbc
	Default chat channels
	"""
	fields = Skeleton(
		IDField(),
		BitMaskField("flags"),
		IntegerField(),
		LocalizedFields("localname"),
		LocalizedFields("name"),
	)


class ChatProfanity(Structure):
	"""
	ChatProfanity.dbc
	Chat filtering
	"""
	fields = Skeleton(
		IDField(),
		StringField("filter"),
		IntegerField("language"),
	)


class ChrClasses(Structure):
	"""
	ChrClasses.dbc
	Class properties
	"""
	fields = Skeleton(
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
		ForeignKey("cinematic", "CinematicSequences"), # Only for Death Knight
		IntegerField("expansionreq"),
	)


class ChrRaces(Structure):
	"""
	ChrRaces.dbc
	Player race data (including some inaccessible)
	"""
	fields = Skeleton(
		IDField(),
		BitMaskField("flags"),
		ForeignKey("faction_template", "FactionTemplate"),
		ForeignKey("exploration_sound", "SoundEntries"),
		ForeignKey("model_male", "CreatureDisplayInfo"),
		ForeignKey("model_female", "CreatureDisplayInfo"),
		StringField("abbreviation"), # Used for helmet models
		FloatField("scale"),
		UnknownField(), # 1 = Horde, 7 = Alliance & not playable?
		ForeignKey("creature_type", "CreatureType"),
		UnknownField(), # always 15007
		UnknownField(), # 1090 for dwarves, 1096 for the others. Getting stored in CGUnit at CGUnit::PostInit.
		StringField("internal_name"),
		ForeignKey("cinematic", "CinematicSequences"),
		LocalizedFields("name_male"),
		LocalizedFields("name_female"),
		LocalizedFields("name_neutral"),
		StringField("feature_1"), # facial_hair
		StringField("feature_2"), # earrings
		StringField("feature_3"), # horns
		IntegerField("expansion"),
	)
	
	def changed_10048(self, fields):
		fields.delete_fields("scale")
	
	def changed_10433(self, fields):
		self.changed_10048(fields)
		fields.insert_field(UnknownField(), before="name_male") # Faction?


class CinematicCamera(Structure):
	"""
	CinematicCamera.dbc
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("path"),
		ForeignKey("voiceover", "SoundEntries"),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class CinematicSequences(Structure):
	"""
	CinematicSequences.dbc
	"""
	fields = Skeleton(
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


class CreatureDisplayInfo(Structure):
	"""
	CreatureDisplayInfo.dbc
	Display data for NPCs
	"""
	fields = Skeleton(
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


class CreatureDisplayInfoExtra(Structure):
	"""
	CreatureDisplayInfoExtra.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("gender"),
		IntegerField("skin_color"),
		IntegerField("face_type"),
		IntegerField("hair_type"),
		IntegerField("hair_style"),
		IntegerField("beard_style"),
		ForeignKey("head", "ItemDisplayInfo"),
		ForeignKey("shoulders", "ItemDisplayInfo"),
		ForeignKey("shirt", "ItemDisplayInfo"),
		ForeignKey("chest", "ItemDisplayInfo"),
		ForeignKey("belt", "ItemDisplayInfo"),
		ForeignKey("legs", "ItemDisplayInfo"),
		ForeignKey("feet", "ItemDisplayInfo"),
		ForeignKey("rings", "ItemDisplayInfo"),
		ForeignKey("hands", "ItemDisplayInfo"),
		ForeignKey("wrists", "ItemDisplayInfo"),
		ForeignKey("back", "ItemDisplayInfo"), # added 5849
		UnknownField(),
		UnknownField(), # added 5991
		StringField("texture")
	)


class CreatureFamily(Structure):
	"""
	CreatureFamily.dbc
	"""
	fields = Skeleton(
		IDField(),
		FloatField(),
		ForeignKey("pet_personality", "PetPersonality"),
		FloatField(),
		UnknownField(),
		ForeignKey("skills", "SkillLine"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		ForeignKey("pet_food", "ItemPetFood"),
		LocalizedFields("name"),
		FilePathField("icon"),
	)


class CreatureModelData(Structure):
	"""
	CreatureModelData.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("weapon_display_info"),
		FilePathField("path"),
		UnknownField(),
		FloatField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
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
		FloatField(),
		FloatField(),
		FloatField(), # Added later...
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class CreatureSoundData(Structure):
	"""
	CreatureSoundData.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(),
		UnknownField(), # SoundEntries
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(),
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(), # SoundEntries
		UnknownField(),
		UnknownField(), # SoundEntries
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(), # SoundEntries
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		IntegerField(), # Added later...
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class CreatureSpellData(Structure):
	"""
	CreatureSpellData.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("spell_1", "Spell"),
		ForeignKey("spell_2", "Spell"),
		ForeignKey("spell_3", "Spell"),
		ForeignKey("spell_4", "Spell"),
		UnknownField(), # cooldown? its always 100....
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class CreatureType(Structure):
	"""
	CreatureType.dbc
	Creature types
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField(),
	)



class CurrencyCategory(Structure):
	"""
	CurrencyCategory.dbc
	Currency categories
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(), # 3 for unused, rest 0
		LocalizedFields("name"),
	)


class CurrencyTypes(Structure):
	"""
	CurrencyTypes.dbc
	Currency data
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("item", "Item"),
		ForeignKey("category", "currencycategory"),
		IntegerField(),
	)


class DanceMoves(Structure):
	"""
	DanceMoves.dbc
	Not yet implemented.
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("type"),
		UnknownField(),
		UnknownField(),
		BitMaskField("flags"),
		StringField("name"),
		LocalizedFields("description"),
		IntegerField(),
	)


class DeathThudLookups(Structure):
	"""
	DeathThudLookups.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("class", "ChrClasses"),
		ForeignKey("race", "ChrRaces"),
		ForeignKey("dirt_sound", "SoundEntries"),
		ForeignKey("water_sound", "SoundEntries"),
	)


class DeclinedWord(Structure):
	"""
	DeclinedWord.dbc
	Only russian strings so far...
	"""
	fields = Skeleton(
		IDField(),
		StringField("text"),
	)


class DeclinedWordCases(Structure):
	"""
	DeclinedWordCases.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("declined_word", "DeclinedWord"),
		UnknownField(),
		StringField("text"),
	)


class DungeonEncounter(Structure):
	"""
	DungeonEncounter.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("instance", "Map"),
		IntegerField("difficulty"),
		UnknownField(),
		IntegerField("ordering"),
		LocalizedFields("name"),
		UnknownField(),
	)


class DungeonMap(Structure):
	"""
	DungeonMap.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("instance", "Map"),
		IntegerField("floor"), # which map floor
		FloatField("y_1"),
		FloatField("y_2"),
		FloatField("x_1"),
		FloatField("x_2"),
		ForeignKey("parent_map", "WorldMapArea"),
	)


class DungeonMapChunk(Structure):
	"""
	DungeonMapChunk.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("map", "Map"),
		ForeignKey("wmo", "WMOAreaTable"), # key="group"
		ForeignKey("dungeon_map", "DungeonMap"),
		FloatField(),
	)


class DurabilityCosts(Structure):
	"""
	DurabilityCosts.dbc
	Each column corresponds to a class.subclass category for items.
	(Current - Ma) * ItemClassModifier * QualityModifier
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("cost_2_0"),
		IntegerField("cost_2_1"),
		IntegerField("cost_2_2"),
		IntegerField("cost_2_3"),
		IntegerField("cost_2_4"),
		IntegerField("cost_2_5"),
		IntegerField("cost_2_6"),
		IntegerField("cost_2_7"),
		IntegerField("cost_2_8"),
		IntegerField("cost_2_9"),
		IntegerField("cost_2_10"),
		IntegerField("cost_2_11"),
		IntegerField("cost_2_12"),
		IntegerField("cost_2_13"),
		IntegerField("cost_2_14"),
		IntegerField("cost_2_15"),
		IntegerField("cost_2_16"),
		IntegerField("cost_2_17"),
		IntegerField("cost_2_18"),
		IntegerField("cost_2_19"),
		IntegerField("cost_2_20"),
		IntegerField("cost_4_0"),
		IntegerField("cost_4_1"),
		IntegerField("cost_4_2"),
		IntegerField("cost_4_3"),
		IntegerField("cost_4_4"),
		IntegerField("cost_4_5"),
		IntegerField("cost_4_6"),
		IntegerField("cost_4_7"),
	)


class DurabilityQuality(Structure):
	"""
	DurabilityQuality.dbc
	"""
	fields = Skeleton(
		IDField(),
		FloatField("modifier"),
	)


class Emotes(Structure):
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
	
	fields = Skeleton(
		IDField(),
		StringField("name"),
		ForeignKey("animation", "AnimationData"),
		BitMaskField("flags"),
		IntegerField("loop"),
		IntegerField("hold"),
		ForeignKey("sound", "SoundEntries")
	)


class Exhaustion(Structure):
	"""
	Exhaustion.dbc
	China's exhaustion system?
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		FloatField(),
		FloatField(),
		FloatField(),
		LocalizedFields("name"),
		FloatField(),
	)

class Faction(Structure):
	"""
	Faction.dbc
	In-game faction data.
	"""
	fields = Skeleton(
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

	def changed_10522(self, fields):
		fields.insert_field(FloatField(), before="name")
		fields.insert_field(FloatField(), before="name")
		fields.insert_field(UnknownField(), before="name")
		fields.insert_field(UnknownField(), before="name")


class FactionGroup(Structure):
	"""
	FactionGroup.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		StringField("internal_name"),
		LocalizedFields("name"),
	)

class FactionTemplate(Structure):
	"""
	FactionTemplate.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("faction", "Faction"),
		BitMaskField("flags"),
		BitMaskField("support_flags"), # LUA::GetFactionForRace shifts 1 by col 2 in FactionGroup and & it with this column.
		BitMaskField("friendly_flags"),
		BitMaskField("hostile_mask"),
		ForeignKey("enemy_faction_1", "Faction"),
		ForeignKey("enemy_faction_2", "Faction"),
		ForeignKey("enemy_faction_3", "Faction"),
		ForeignKey("enemy_faction_4", "Faction"),
		ForeignKey("friendly_faction_1", "Faction"),
		ForeignKey("friendly_faction_2", "Faction"),
		ForeignKey("friendly_faction_3", "Faction"),
		ForeignKey("friendly_faction_4", "Faction"),
	)


class FileData(Structure):
	"""
	FileData.dbc
	Movie file data
	"""
	fields = Skeleton(
		IDField(),
		StringField("filename"),
		FilePathField("path"),
	)


class FootprintTextures(Structure):
	"""
	FootprintTextures.dbc
	Paths to the footprint textures
	visible on snow, sand, etc.
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("path"),
	)


class GameObjectArtKit(Structure):
	"""
	GameObjectArtKit.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("texture_1"),
		StringField("texture_2"),
		StringField("texture_3"),
		FilePathField("model_1"),
		FilePathField("model_2"),
		FilePathField("model_3"),
		FilePathField("model_4"),
	)


class GameObjectDisplayInfo(Structure):
	"""
	GameObjectDisplayInfo.dbc
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("model"),
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
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
	)


class GameTables(Structure):
	"""
	GameTables.dbc
	Unknown use
	"""
	fields = Skeleton(
		StringField(primary_key=True),
		IntegerField(), # 1-100
		IntegerField(),
	)


class GameTips(Structure):
	"""
	GameTips.dbc
	Loading screen tips.
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("description"),
	)


class GemProperties(Structure):
	"""
	GemProperties.dbc
	Gem data
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("enchant", "SpellItemEnchantment"),
		BooleanField(),
		BooleanField("unique_equipped"),
		IntegerField("color"),
	)


class GlyphProperties(Structure):
	"""
	GlyphProperties.dbc
	Glyph data
	"""
	
	FLAGS = {
		0x00000001: "minor",
	}
	
	fields = Skeleton(
		IDField(),
		ForeignKey("spell", "spell"),
		BitMaskField("flags", flags=FLAGS),
		ForeignKey("icon", "spellicon"),
	)


class GlyphSlot(Structure):
	"""
	GlyphSlot.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("type"),
		IntegerField("ordering"),
	)


class GMTicketCategory(Structure):
	"""
	GMTicketCategory.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class GroundEffectDoodad(Structure):
	"""
	GroundEffectDoodad.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("model"),
		BooleanField(),
	)


class GroundEffectTexture(Structure):
	"""
	GroundEffectTexture.dbc
	Used for determining what doodads get used for the effects on textures
	(the ID thats used is the effectID on the base texture of each map chunk).
	These doodads are the little tiny plants & rocks you see on the ground.
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("doodad_effect_1"),
		IntegerField("doodad_effect_2"),
		IntegerField("doodad_effect_3"),
		IntegerField("doodad_effect_4"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class gtCombatRatings(Structure):
	"""
	gtCombatRatings.dbc
	"""
	fields = Skeleton(
		FloatField("ratio"),
	)

class gtOCTRegenHP(Structure):
	"""
	gtOCTRegenHP.dbc
	"""
	
	fields = Skeleton(
		FloatField("ratio"),
	)

class gtOCTRegenMP(Structure):
	"""
	gtOCTRegenMP.dbc
	"""
	
	fields = Skeleton(
		FloatField("ratio"),
	)

class gtRegenHPPerSpt(Structure):
	"""
	gtRegenHPPerSpt.dbc
	"""
	
	fields = Skeleton(
		FloatField("ratio"),
	)

class gtRegenMPPerSpt(Structure):
	"""
	gtRegenMPPerSpt.dbc
	"""
	
	fields = Skeleton(
		FloatField("ratio"),
	)


class HelmetGeosetVisData(Structure):
	"""
	HelmetGeosetVisData.dbc
	Unknown use
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
	)


class HolidayDescriptions(Structure):
	"""
	HolidayDescriptions.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("description"),
	)


class HolidayNames(Structure):
	"""
	HolidayNames.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class Holidays(Structure):
	"""
	Holidays.dbc
	"""
	fields = Skeleton(
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
		ForeignKey("name", "HolidayNames"),
		ForeignKey("description", "HolidayDescriptions"),
		StringField("icon"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class Item(Structure):
	"""
	Item.dbc
	Contains all in-game items, and their display data.
	Used for icons, dressing room, etc.
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("category", "itemclass"),
		ForeignKey("subcategory", "itemsubclass"),
		IntegerField("depclass"),
		IntegerField(), # sheath or something
		ForeignKey("display", "itemdisplayinfo"),
		IntegerField("slot"),
		IntegerField("sheath_type"),
	)


class ItemBagFamily(Structure):
	"""
	ItemBagFamily.dbc
	Item bag categories
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class ItemClass(Structure):
	"""
	ItemClass.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class ItemCondExtCost(Structure):
	"""
	ItemCondExtCost.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		ForeignKey("extended_cost", "ItemExtendedCost"),
		IntegerField(),
	)


class ItemDisplayInfo(Structure):
	"""
	ItemDisplayInfo.dbc
	Item display data. Icons, models, ...
	"""
	fields = Skeleton(
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


class ItemExtendedCost(Structure):
	"""
	ItemExtendedCost.dbc
	Extended cost data (buy with items, honor points, arena points, ...)
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("honor_points"),
		IntegerField("arena_points"),
		ForeignKey("item_1", "Item"),
		ForeignKey("item_2", "Item"),
		ForeignKey("item_3", "Item"),
		ForeignKey("item_4", "Item"),
		ForeignKey("item_5", "Item"),
		IntegerField("item_amount_1"),
		IntegerField("item_amount_2"),
		IntegerField("item_amount_3"),
		IntegerField("item_amount_4"),
		IntegerField("item_amount_5"),
		IntegerField("required_personal_rating"),
		UnknownField(), # maybe pvprankreq?
	)

	def changed_10026(self, fields):
		fields.insert_field(IntegerField("bracket"), before="item1")


class ItemGroupSounds(Structure):
	"""
	ItemGroupSounds.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("sound_pickup", "SoundEntries"),
		ForeignKey("sound_putdown", "SoundEntries"),
		ForeignKey("sound", "SoundEntries"),
		UnknownField()
	)


class ItemLimitCategory(Structure):
	"""
	ItemLimitCategory.dbc
	Unique item categories
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("amount"),
		BooleanField("equipped"),
	)


class ItemPetFood(Structure):
	"""
	ItemPetFood.dbc
	Hunter pet food categories
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class ItemPurchaseGroup(Structure):
	"""
	ItemPurchaseGroup.dbc
	"Group" buys, seems to be a feature not in-game. Only one row (34529, 34530, 33006)
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("item1", "Item"),
		ForeignKey("item2", "Item"),
		ForeignKey("item3", "Item"),
		ForeignKey("item4", "Item"),
		ForeignKey("item5", "Item"),
		ForeignKey("item6", "Item"),
		ForeignKey("item7", "Item"),
		ForeignKey("item8", "Item"),
		LocalizedFields("name"),
	)


class ItemRandomProperties(Structure):
	"""
	ItemRandomProperties.dbc
	Random enchantments for items (of stamina, ...)
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		IntegerField(),
		LocalizedFields("name"),
	)


class ItemSet(Structure):
	"""
	ItemSet.dbc
	Contains data for item sets. Item IDs linked are
	requested directly in itemtextcache.wdb
	"""
	fields = Skeleton(
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


class ItemSubClass(Structure):
	"""
	ItemSubClass.dbc
	Item subclasses
	"""
	fields = Skeleton(
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


class ItemSubClassMask(Structure):
	"""
	ItemSubClassMask.dbc
	Used for Spell.dbc Subclass requirements
	FIXME Structure is tricky here, we need to
	handle a double fkey to a multi-id table...
	Association( "subclass_association"
		ForeignKey("id1", "ItemSubClass", column="id_1"),
		ForeignMask("id2", "ItemSubClass", column="id_2"),
	)
	row.subclass_association == DBRowList([
		
	])
	"""
	implicit_id = True
	fields = Skeleton(
		IntegerField("id1"),
		BitMaskField("id2_mask"),
		LocalizedFields("name"),
	)


class ItemVisualEffects(Structure):
	"""
	ItemVisualEffects.dbc
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("model"),
	)


class ItemVisuals(Structure):
	"""
	ItemVisuals.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("visual_1", "ItemVisualEffects"), # Something's wrong, some of those have insane ids...
		ForeignKey("visual_2", "ItemVisualEffects"),
		ForeignKey("visual_3", "ItemVisualEffects"),
		ForeignKey("visual_4", "ItemVisualEffects"),
		ForeignKey("visual_5", "ItemVisualEffects"),
	)


class Languages(Structure):
	"""
	Languages.dbc
	Player/NPC language data
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class LanguageWords(Structure):
	"""
	LanguageWords.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("language", "Languages"),
		StringField("word"),
	)


class LFGDungeons(Structure):
	"""
	LFGDungeons.dbc
	"""
	
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("level_1"), # level_min
		IntegerField("level_2"),
		IntegerField("level_3"),
		IntegerField("level_4"),
		IntegerField("level_5"),
		ForeignKey("instance", "Map"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		IntegerField("faction"), # -1 = all, 0 = Horde, 1 = Alliance
		StringField("icon"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class LFGDungeonExpansion(Structure):
	"""
	LFGDungeonExpansion.dbc
	"""
	
	fields = Skeleton(
		IDField(),
		ForeignKey("lfg_1", "LFGDungeons"),
		UnknownField(),
		ForeignKey("lfg_2", "LFGDungeons"),
		IntegerField("level_1"),
		IntegerField("level_2"),
		IntegerField("level_3"),
		IntegerField("level_4"),
	)


class LFGDungeonGroup(Structure):
	"""
	LFGDungeonGroup.dbc
	"""
	
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		UnknownField(),
		UnknownField(),
		IntegerField("type"), # 1 = normal, 2 = raid, 5 = heroic
	)


class Light(Structure):
	"""
	Light.dbc
	This is the starting file for what controls the lights, fogs, sky color,
	water color, and well other similar items. This information prior to 1.9
	used to be stored in the .lit files but in 1.9 was moved to Light.dbc and
	the other Light* DBC files.
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("instance", "Map"),
		FloatField("x"),
		FloatField("y"),
		FloatField("z"),
		FloatField("inner_radius"),
		FloatField("outer_radius"),
		IntegerField("sky_settings"),
		IntegerField("fog_settings"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class LightFloatBand(Structure):
	"""
	LightFloatBand.dbc
	Controls the various values that are related to floats in .lit files
	which was believed just to be the sky positions. There is 6 rows
	corresponding to every ID so take the ID*6 to get the proper start ID
	to look at it and the next 5 rows after it go along with it as well.
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("entry_count"),
		UnsignedIntegerField("time_1"),
		UnsignedIntegerField("time_2"),
		UnsignedIntegerField("time_3"),
		UnsignedIntegerField("time_4"),
		UnsignedIntegerField("time_5"),
		UnsignedIntegerField("time_6"),
		UnsignedIntegerField("time_7"),
		UnsignedIntegerField("time_8"),
		UnsignedIntegerField("time_9"),
		UnsignedIntegerField("time_10"),
		UnsignedIntegerField("time_11"),
		UnsignedIntegerField("time_12"),
		UnsignedIntegerField("time_13"),
		UnsignedIntegerField("time_14"),
		UnsignedIntegerField("time_15"),
		UnsignedIntegerField("time_16"),
		UnsignedIntegerField("color_1"),
		UnsignedIntegerField("color_2"),
		UnsignedIntegerField("color_3"),
		UnsignedIntegerField("color_4"),
		UnsignedIntegerField("color_5"),
		UnsignedIntegerField("color_6"),
		UnsignedIntegerField("color_7"),
		UnsignedIntegerField("color_8"),
		UnsignedIntegerField("color_9"),
		UnsignedIntegerField("color_10"),
		UnsignedIntegerField("color_11"),
		UnsignedIntegerField("color_12"),
		UnsignedIntegerField("color_13"),
		UnsignedIntegerField("color_14"),
		UnsignedIntegerField("color_15"),
		UnsignedIntegerField("color_16"),
	)


class LightIntBand(Structure):
	"""
	LightIntBand.dbc
	Controls the various values that are related to floats in .lit files
	which was believed just to be the sky positions. There is 18 rows
	corresponding to every ID so take the ID*18 to get the proper start ID
	to look at it and the next 17 rows after it go along with it as well.
	See http://www.sourcepeek.com/wiki/LightIntBand.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("entry_count"),
		UnsignedIntegerField("time_1"),
		UnsignedIntegerField("time_2"),
		UnsignedIntegerField("time_3"),
		UnsignedIntegerField("time_4"),
		UnsignedIntegerField("time_5"),
		UnsignedIntegerField("time_6"),
		UnsignedIntegerField("time_7"),
		UnsignedIntegerField("time_8"),
		UnsignedIntegerField("time_9"),
		UnsignedIntegerField("time_10"),
		UnsignedIntegerField("time_11"),
		UnsignedIntegerField("time_12"),
		UnsignedIntegerField("time_13"),
		UnsignedIntegerField("time_14"),
		UnsignedIntegerField("time_15"),
		UnsignedIntegerField("time_16"),
		UnsignedIntegerField("color_1"),
		UnsignedIntegerField("color_2"),
		UnsignedIntegerField("color_3"),
		UnsignedIntegerField("color_4"),
		UnsignedIntegerField("color_5"),
		UnsignedIntegerField("color_6"),
		UnsignedIntegerField("color_7"),
		UnsignedIntegerField("color_8"),
		UnsignedIntegerField("color_9"),
		UnsignedIntegerField("color_10"),
		UnsignedIntegerField("color_11"),
		UnsignedIntegerField("color_12"),
		UnsignedIntegerField("color_13"),
		UnsignedIntegerField("color_14"),
		UnsignedIntegerField("color_15"),
		UnsignedIntegerField("color_16"),
	)


class LightParams(Structure):
	"""
	LightParams.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField("fog_add"),
		FloatField("clear_water_alpha"),
		FloatField(),
		FloatField("deep_water_alpha"),
		FloatField(),
	)


class LightSkybox(Structure):
	"""
	LightSkybox.dbc
	Skybox data
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("path"),
		IntegerField("type"), # 2 = aurora, ...?
	)


class LiquidMaterial(Structure):
	"""
	LiquidMaterial.dbc
	Unknown use. Lava/Water? Only 3 rows (1, 2, 3).
	Added with WotLK
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
	)


class LiquidType(Structure):
	"""
	LiquidType.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		BitMaskField("flags"),
		IntegerField("type"),
		ForeignKey("sound", "SoundEntries"),
		ForeignKey("spell", "Spell"),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		FloatField(),
		BooleanField(),
		UnknownField(),
		ForeignKey("material", "LiquidMaterial"), # this defines the shaders used.*
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
		StringField(),
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
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		BooleanField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)
	# *  (1: "*sLiquidWater", 2: "*sLiquidMagma", 3: "*sLiquidProcWater%s" where %s is an appendix that is currently always "")

class LoadingScreenTaxiSplines(Structure):
	"""
	LoadingScreenTaxiSplines.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("taxi", "TaxiPath"),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		BooleanField(),
	)


class LoadingScreens(Structure):
	"""
	LoadingScreens.dbc
	Loading screen lookups
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		FilePathField("path"),
	)
	
	def changed_10676(self, fields):
		fields.append_fields(BooleanField("continent"))


class Lock(Structure):
	"""
	Lock.dbc
	Various locks (items, objects, ...)
	"""
	PROPERTY_TYPES = {
		1: "Item",
		2: "LockProperties",
		3: "Lock", # FIXME
	}
	properties_relation = lambda x, value: PROPERTY_TYPES[value]
	
	fields = Skeleton(
		IDField(),
		IntegerField("type_1"),
		IntegerField("type_2"),
		IntegerField("type_3"),
		IntegerField("type_4"),
		IntegerField("type_5"),
		IntegerField("type_6"),
		IntegerField("type_7"),
		IntegerField("type_8"),
		GenericForeignKey("properties_1", get_relation=properties_relation),
		GenericForeignKey("properties_2", get_relation=properties_relation),
		GenericForeignKey("properties_3", get_relation=properties_relation),
		GenericForeignKey("properties_4", get_relation=properties_relation),
		GenericForeignKey("properties_5", get_relation=properties_relation),
		GenericForeignKey("properties_6", get_relation=properties_relation),
		GenericForeignKey("properties_7", get_relation=properties_relation),
		GenericForeignKey("properties_8", get_relation=properties_relation),
		IntegerField("required_skill_1"),
		IntegerField("required_skill_2"),
		IntegerField("required_skill_3"),
		IntegerField("required_skill_4"),
		IntegerField("required_skill_5"),
		IntegerField("required_skill_6"),
		IntegerField("required_skill_7"),
		IntegerField("required_skill_8"),
		IntegerField("action_1"),
		IntegerField("action_2"),
		IntegerField("action_3"),
		IntegerField("action_4"),
		IntegerField("action_5"),
		IntegerField("action_6"),
		IntegerField("action_7"),
		IntegerField("action_8"),
	)


class LockType(Structure):
	"""
	LockType.dbc
	"""
	
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		LocalizedFields("state"),
		LocalizedFields("process"),
		StringField("internal_name"),
	)


class MailTemplate(Structure):
	"""
	MailTemplate.dbc
	In-game mails recieved.
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("title"),
		LocalizedFields("message"),
	)


class Map(Structure):
	"""
	Map.dbc
	Instance data
	"""
	fields = Skeleton(
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

	def changed_10026(self, fields):
		fields.delete_fields(
			"normal_requirements",
			"heroic_requirements",
			"epic_requirements",
			"normal_reset",
			"heroic_reset",
			"epic_reset"
		)

	def changed_10083(self, fields):
		self.changed_10026(fields)
		fields.append_fields(IntegerField("max_players"))

	def changed_10522(self, fields):
		self.changed_10083(fields)
		fields.insert_field(UnknownField(), before="battleground")


class MapDifficulty(Structure):
	"""
	MapDifficulty.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("instance", "map"),
		IntegerField("mode"),
		LocalizedFields("requirements"),
		DurationField("resettime"),
		IntegerField("raidsize"),
		UnknownField(),
	)


class Material(Structure):
	"""
	Material.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("page_material", "PageTextMaterial"),
		UnknownField(),
	)
	
	def changed_9901(self, fields):
		fields.append_fields(
			UnknownField(),
			UnknownField(),
		)


class Movie(Structure):
	"""
	Movie.dbc
	Supposedly for movies. 3 rows at the time: 1, 2, 14
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		IntegerField(),
	)


class MovieFileData(Structure):
	"""
	MovieFileData.dbc
	Movie resolution data
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("resolution"), #800 or 1024
	)


class MovieVariation(Structure):
	"""
	MovieVariation.dbc
	Unknown use
	"""
	fields = Skeleton(
		IDField(),
		IntegerField(),
		ForeignKey("resolution", "moviefiledata"),
	)


class NameGen(Structure):
	"""
	NameGen.dbc
	Character creation name generator data
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField("class"),
		IntegerField("gender"),
	)


class NamesProfanity(Structure):
	"""
	NamesProfanity.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("pattern"),
		IntegerField("language"),
	)


class NamesReserved(Structure):
	"""
	NamesReserved.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("pattern"),
		IntegerField("language"),
	)


class NPCSounds(Structure):
	"""
	NPCSounds.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("greeting", "SoundEntries"),
		ForeignKey("farewell", "SoundEntries"),
		ForeignKey("pissed", "SoundEntries"),
		UnknownField(), #dbank? seriously?
	)


class ObjectEffect(Structure):
	"""
	ObjectEffect.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		UnknownField(),
		UnknownField(),
		IntegerField("sound_dbc"), # SoundDBC, int, 1 for SoundEntries.dbc, 2 for SoundEntriesAdvanced.dbc.
		IntegerField("sound"), # gfk
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		ForeignKey("modified", "ObjectEffectModifier")
	)


class ObjectEffectGroup(Structure):
	"""
	ObjectEffectGroup.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
	)


class ObjectEffectModifier(Structure):
	"""
	ObjectEffectModifier.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class ObjectEffectPackage(Structure):
	"""
	ObjectEffectPackage.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
	)


class ObjectEffectPackageElem(Structure):
	"""
	ObjectEffectPackageElem.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("package", "ObjectEffectPackage"),
		ForeignKey("group", "ObjectEffectGroup"),
		IntegerField("movement_state") # see http://www.madx.dk/wowdev/wiki/index.php?title=ObjectEffectPackageElem.dbc
	)


class OverrideSpellData(Structure):
	"""
	OverrideSpellData.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("spell_1", "Spell"),
		ForeignKey("spell_2", "Spell"),
		ForeignKey("spell_3", "Spell"),
		ForeignKey("spell_4", "Spell"),
		ForeignKey("spell_5", "Spell"),
		ForeignKey("spell_6", "Spell"),
		ForeignKey("spell_7", "Spell"),
		ForeignKey("spell_8", "Spell"),
		ForeignKey("spell_9", "Spell"),
		ForeignKey("spell_10", "Spell"),
		UnknownField(),
	)


class Package(Structure):
	"""
	Package.dbc
	This contains possible alternate icons for ingame mail.
	It's set in MailboxMessageInfo member #70 (+0x118).
	You can set a package with LUA:SetPackage(index) which is actually
	sent when you send the next mail. May only work for deliveries with items.
	This is not used in the current client's UI and is likely to be filtered serverside.
	Note: This is the field behind stationary in the CMSG_SEND_MAIL packet.
	"""
	fields = Skeleton(
		IDField(),
		StringField("icon"),
		MoneyField("price"), # in copper?
		LocalizedFields("name"),
	)


class PageTextMaterial(Structure):
	"""
	PageTextMaterial.dbc
	Material (background image) for pages
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
	)


class PaperDollItemFrame(Structure):
	"""
	PaperDollItemFrame.dbc
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("path"),
		IntegerField("slot"),
	)


class PetitionType(Structure):
	"""
	PetitionType.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		UnknownField(),
	)


class PetLoyalty(Structure):
	"""
	PetLoyalty.dbc
	Hunter pet loyalty
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class PetPersonality(Structure):
	"""
	PetPersonality.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
	)


class PowerDisplay(Structure):
	"""
	PowerDisplay.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		StringField("name"),
		ByteField(),
		ByteField(),
		ByteField(),
	)


class PvpDifficulty(Structure):
	"""
	PvpDifficulty.dbc
	Battleground/arena brackets
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("instance", "Map"),
		IntegerField("ordering"),
		IntegerField("level_min"),
		IntegerField("level_max"),
		UnknownField(), # something to do with ordering
	)


class QuestFactionReward(Structure):
	"""
	QuestFactionReward.dbc
	Two rows - one for positive gains and
	one for negative gains
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("reputation_gain_0"),
		IntegerField("reputation_gain_1"),
		IntegerField("reputation_gain_2"),
		IntegerField("reputation_gain_3"),
		IntegerField("reputation_gain_4"),
		IntegerField("reputation_gain_5"),
		IntegerField("reputation_gain_6"),
		IntegerField("reputation_gain_7"),
		IntegerField("reputation_gain_8"),
		IntegerField("reputation_gain_9"),
	)


class QuestInfo(Structure):
	"""
	QuestInfo.dbc
	Quest type names
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class QuestSort(Structure):
	"""
	QuestSort.dbc
	Additional sort fields for quests
	Note: Zones are directly gathered from AreaTable.dbc
	linked by a negative id in questcache.wdb
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class QuestXP(Structure):
	"""
	QuestXP.dbc
	Quest experience amounts
	100 rows, one for each level
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		IntegerField("experience_1"),
		IntegerField("experience_2"),
		IntegerField("experience_3"),
		IntegerField("experience_4"),
		IntegerField("experience_5"),
		IntegerField("experience_6"),
		IntegerField("experience_7"),
		IntegerField("experience_8"),
		UnknownField(),
	)


class RandPropPoints(Structure):
	"""
	RandPropPoints.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("epic_points_1"),
		IntegerField("epic_points_2"),
		IntegerField("epic_points_3"),
		IntegerField("epic_points_4"),
		IntegerField("epic_points_5"),
		IntegerField("rare_points_1"),
		IntegerField("rare_points_2"),
		IntegerField("rare_points_3"),
		IntegerField("rare_points_4"),
		IntegerField("rare_points_5"),
		IntegerField("uncommon_points_1"),
		IntegerField("uncommon_points_2"),
		IntegerField("uncommon_points_3"),
		IntegerField("uncommon_points_4"),
		IntegerField("uncommon_points_5"),
	)


class Resistances(Structure):
	"""
	Resistances.dbc
	"""
	fields = Skeleton(
		IDField(),
		BooleanField("armor"),
		UnknownField(), # Not spellicon
		LocalizedFields("name"),
	)


class ScalingStatDistribution(Structure):
	"""
	ScalingStatDistribution.dbc
	"""
	fields = Skeleton(
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


class ScalingStatValues(Structure):
	"""
	ScalingStatValues.dbc
	Heirloom stat scaling (one row per level)
	"""
	fields = Skeleton(
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

	def changed_10026(self, fields):
		"""
		TODO 5 new fields
		"""
		pass


class ScreenEffect(Structure):
	"""
	ScreenEffect.dbc
	Fullscreen graphic effects
	Types:
	0: EffectGlow, -Fog
	1: FFXEffects, -Fog
	2: ffxNetherWorld
	3: ffxSpecial / EffectGlow, -Fog, +color
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		IntegerField("type"),
		UnsignedIntegerField("color"), # in hex
		IntegerField("screen_edge_size"),
		IntegerField("greyscale"),
		UnknownField(),
		ForeignKey("light", "LightParams"),
		ForeignKey("ambience", "SoundAmbience"),
		ForeignKey("music", "ZoneMusic"),
	)


class ServerMessages(Structure):
	"""
	ServerMessages.dbc
	Server-wide broadcast messages (in-game chat)
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("message"),
	)


class SheatheSoundLookups(Structure):
	"""
	SheatheSoundLookups.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		ForeignKey("sound_sheath", "SoundEntries"),
		ForeignKey("sound_unsheath", "SoundEntries"),
	)


class SkillCostsData(Structure):
	"""
	SkillCostsData.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class SkillLine(Structure):
	"""
	SkillLine.dbc
	Contains all skill-related data.
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("category", "SkillLineCategory"),
		ForeignKey("cost", "SkillCostsData"),
		LocalizedFields("name"),
		LocalizedFields("description"),
		ForeignKey("icon", "SpellIcon"),
		LocalizedFields("action"),
		BooleanField("tradeskill"),
	)


class SkillLineAbility(Structure):
	"""
	SkillLineAbility.dbc
	turns_green is averaged with: a + (b-a)/2
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("skill", "SkillLine"),
		ForeignKey("spell", "Spell"),
		ForeignMask("required_races", "ChrRaces"),
		ForeignMask("required_classes", "ChrClasses"),
		ForeignMask("excluded_races", "ChrRaces"),
		ForeignMask("excluded_classes", "ChrClasses"),
		IntegerField("required_skill_level"),
		ForeignKey("parent", "Spell"),
		UnknownField(), # acquireMethod learnOnGetSkill ?!
		IntegerField("turns_grey"),
		IntegerField("turns_yellow"),
		UnknownField(), # Character points ?! [2]
		UnknownField(),
		#UnknownField(), Deleted somewhere between 4125 and 9551
	)


class SkillLineCategory(Structure):
	"""
	SkillLineCategory.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("sort")
	)


class SkillTiers(Structure):
	"""
	SkillTiers.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("value_1"),
		IntegerField("value_2"),
		IntegerField("value_3"),
		IntegerField("value_4"),
		IntegerField("value_5"),
		IntegerField("value_6"),
		IntegerField("value_7"),
		IntegerField("value_8"),
		IntegerField("value_9"),
		IntegerField("value_10"),
		IntegerField("value_11"),
		IntegerField("value_12"),
		IntegerField("value_13"),
		IntegerField("value_14"),
		IntegerField("value_15"),
		IntegerField("value_16"),
		IntegerField("max_value_1"),
		IntegerField("max_value_2"),
		IntegerField("max_value_3"),
		IntegerField("max_value_4"),
		IntegerField("max_value_5"),
		IntegerField("max_value_6"),
		IntegerField("max_value_7"),
		IntegerField("max_value_8"),
		IntegerField("max_value_9"),
		IntegerField("max_value_10"),
		IntegerField("max_value_11"),
		IntegerField("max_value_12"),
		IntegerField("max_value_13"),
		IntegerField("max_value_14"),
		IntegerField("max_value_15"),
		IntegerField("max_value_16"),
	)


class SoundAmbience(Structure):
	"""
	SoundAmbience.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("day", "SoundEntries"),
		ForeignKey("night", "SoundEntries"),
	)


class SoundCharacterMacroLines(Structure):
	"""
	SoundCharacterMacroLines.dbc
	"""
	DEAD = True
	fields = Skeleton(
		IDField(),
		UnknownField(),
		IntegerField("gender"),
		ForeignKey("races", "ChrRaces"),
		ForeignKey("sound", "SoundEntries"),
	)


class SoundEmitters(Structure):
	"""
	SoundEmitters.dbc
	Seems to replace the ADT-sound-emitters.
	Mainly used for waterfalls.
	"""
	fields = Skeleton(
		IDField(),
		FloatField("x"),
		FloatField("y"),
		FloatField("z"),
		FloatField("radius_1"), # XXX
		FloatField("radius_2"),
		FloatField("radius_3"),
		ForeignKey("sound", "SoundEntriesAdvanced"),
		ForeignKey("map", "Map"),
		StringField("name"),
	)


class SoundEntries(Structure):
	"""
	SoundEntries.dbc
	Defines many kinds of sounds ingame.
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("type"),
		StringField("name"),
		FilePathField("filename_1"),
		FilePathField("filename_2"),
		FilePathField("filename_3"),
		FilePathField("filename_4"),
		FilePathField("filename_5"),
		FilePathField("filename_6"),
		FilePathField("filename_7"),
		FilePathField("filename_8"),
		FilePathField("filename_9"),
		FilePathField("filename_10"),
		IntegerField("parameters_1"),
		IntegerField("parameters_2"),
		IntegerField("parameters_3"),
		IntegerField("parameters_4"),
		IntegerField("parameters_5"),
		IntegerField("parameters_6"),
		IntegerField("parameters_7"),
		IntegerField("parameters_8"),
		IntegerField("parameters_9"),
		IntegerField("parameters_10"),
		FilePathField("path"),
		FloatField("volume"),
		BitMaskField("flags"),
		FloatField("distance_min"),
		FloatField("distance_cutoff"),
		IntegerField("eax_definition"),
		UnknownField(),
	)


class SoundEntriesAdvanced(Structure):
	"""
	SoundEntriesAdvanced.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("sound", "SoundEntries"),
		FloatField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		StringField("name"),
	)

class SoundFilter(Structure):
	"""
	SoundFilter.dbc
	Death knight voice filters
	See http://www.madx.dk/wowdev/wiki/index.php?title=SoundFilter.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField(),
	)


class SoundFilterElem(Structure):
	"""
	SoundFilterElem.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("filter", "SoundFilter"),
		UnknownField(),
		UnknownField(),
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


class SoundProviderPreferences(Structure):
	"""
	SoundProviderPreferences.dbc
	World of Warcraft uses the FMod Sound Library by Firelite Technologies
	http://www.fmod.org/ - The data stored in this table corresponds
	with the struct FMOD_REVERB_PROPERTIES in the FMod API.
	For more indepth descriptions of these properties under win32,
	check the EAX2 and EAX3 documentation at http://developer.creative.com/
	under the downloads section.
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		UnknownField(),
		UnknownField(),
		FloatField("volume"), # 20 = full volume
		FloatField("environment_size"),
		FloatField("environment_diffusion"),
		IntegerField("room_mid_frequency"),
		IntegerField("room_high_frequency"),
		FloatField("decay_hf_ratio"),
		IntegerField("reflections"),
		FloatField("reflections_delay"),
		IntegerField("reverb"),
		FloatField("reverb_delay"),
		FloatField("room_low_frequency"),
		FloatField("hl_reference"),
		FloatField("echo_depth"),
		FloatField("diffusion"),
		FloatField("echo_time"),
		FloatField(), # EnvDiffusion says wowdev
		FloatField("modulation_time"),
		FloatField("modulation_depth"),
		FloatField("lf_reference"),
		FloatField("room_rolloff_factor"),
	)


class SoundSamplePreferences(Structure):
	"""
	SoundSamplePreferences.dbc
	Two rows only
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		FloatField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
	)


class SoundWaterType(Structure):
	"""
	SoundWaterType.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("liquid_type", "LiquidType"),
		BitMaskField("fluid_speed"), # Water speed. 0x0 = still; 0x4 = slow; 0x8 fast
		ForeignKey("sound", "SoundEntries"),
	)


class SpamMessages(Structure):
	"""
	SpamMessages.dbc
	Regex matches for spam check (?)
	"""
	fields = Skeleton(
		IDField(),
		StringField("regex"),
	)


class Spell(Structure):
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
	
	fields = Skeleton(
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
		BitMaskField("required_stances"),
		BitMaskField("excluded_stances"),
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
	)
	
	def changed_9614(self, fields): # between 9614 and 9637
		fields.append_fields(ForeignKey("power_display", "PowerDisplay"))

	def changed_10026(self, fields):
		self.changed_9614(fields)
		fields.insert_field(UnknownField(), before="required_stances") # Likely int->bigint
		fields.insert_field(UnknownField(), before="excluded_stances")
		fields.insert_field(UnknownField(), before="required_target")
		fields.append_fields(
			FloatField("multiplier_effect_1"),
			FloatField("multiplier_effect_2"),
			FloatField("multiplier_effect_3"),
			ForeignKey("descriptionvars", "SpellDescriptionVariables"),
		)

	def changed_10522(self, fields):
		self.changed_10026(fields)
		fields.append_fields(
			ForeignKey("spell_difficulty", "SpellDifficulty"),
		)
	
	def changed_11573(self, fields):
		self.changed_10522(fields)
		fields.delete_fields(
			"dice_base_effect_1",
			"dice_base_effect_2",
			"dice_base_effect_3",
			"dice_per_level_effect_1",
			"dice_per_level_effect_2",
			"dice_per_level_effect_3",
		)


class SpellAuraNames(Structure):
	"""
	SpellAuraNames.dbc
	Removed shortly after release
	"""
	DEAD = True
	fields = Skeleton(
		IDField(),
		UnknownField(),
		StringField("internal_name"),
		LocalizedFields("name", locales=OLD_LOCALES),
	)


class SpellCastTimes(Structure):
	"""
	SpellCastTimes.dbc
	Spell cast time info
	"""
	fields = Skeleton(
		IDField(),
		DurationField("cast_time", unit="milliseconds"),
		IntegerField("modifier"),
		DurationField("cast_time_max", unit="milliseconds"),
	)


class SpellCategory(Structure):
	"""
	SpellCategory.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
	)


class SpellChainEffects(Structure):
	"""
	SpellChainEffects.dbc
	"""
	fields = Skeleton(
		IDField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		IntegerField(),
		IntegerField(),
		FilePathField("texture")
	)


class SpellDescriptionVariables(Structure):
	"""
	SpellDescriptionVariables.dbc
	Used in spellstrings
	"""
	fields = Skeleton(
		IDField(),
		StringField("variables"),
	)


class SpellDifficulty(Structure):
	"""
	SpellDifficulty.dbc
	Spell heroic modes/raid sizes
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("10_man", "Spell"),
		ForeignKey("25_man", "Spell"),
		ForeignKey("10_man_heroic", "Spell"),
		ForeignKey("25_man_heroic", "Spell"),
	)


class SpellDispelType(Structure):
	"""
	SpellDispelType.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		UnknownField(),
		BooleanField("shown"), # in debuff tooltip
		StringField(), # same as name for magic/curse/disease/poison, used where?
	)


class SpellDuration(Structure):
	"""
	SpellDuration.dbc
	Spell duration data
	"""
	fields = Skeleton(
		IDField(),
		DurationField("duration_1", unit="milliseconds"),
		DurationField("duration_2", unit="milliseconds"),
		DurationField("duration_3", unit="milliseconds"),
	)


class SpellEffectCameraShakes(Structure):
	"""
	SpellEffectCameraShakes.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class SpellEffectNames(Structure):
	"""
	SpellEffectNames.dbc
	Removed shortly after release
	"""
	DEAD = True
	fields = Skeleton(
		IDField(),
		LocalizedFields("name", locales=OLD_LOCALES),
	)


class SpellFocusObject(Structure):
	"""
	SpellFocusObject.dbc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class SpellIcon(Structure):
	"""
	SpellIcon.dbc
	Spell icons
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("path"),
	)


class SpellItemEnchantment(Structure):
	"""
	SpellItemEnchantment.dbc
	Item enchants (Including temporary
	enchants and socketbonuses)
	"""
	fields = Skeleton(
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
		ForeignKey("glow", "ItemVisuals"),
		IntegerField(),
		ForeignKey("gem", "Item"), # added 5610
		ForeignKey("conditions", "SpellItemEnchantmentCondition"), # added 5610
		ForeignKey("required_skill", "SkillLine"), # added 3.x
		IntegerField("required_skill_level"), # added 3.x
	)
	
	def changed_9637(self, fields):
		fields.append_fields(
			IntegerField("required_level"),
		)


class SpellItemEnchantmentCondition(Structure):
	"""
	SpellItemEnchantmentCondition.dbc
	"""
	fields = Skeleton(
		IDField(),
		ByteField("gem_color_1"),
		ByteField("gem_color_2"),
		ByteField("gem_color_3"),
		ByteField("gem_color_4"),
		ByteField("gem_color_5"),
		IntegerField("operand_1"),
		IntegerField("operand_2"),
		IntegerField("operand_3"),
		IntegerField("operand_4"),
		IntegerField("operand_5"),
		ByteField("comparator_1"),
		ByteField("comparator_2"),
		ByteField("comparator_3"),
		ByteField("comparator_4"),
		ByteField("comparator_5"),
		ByteField("compare_color_1"),
		ByteField("compare_color_2"),
		ByteField("compare_color_3"),
		ByteField("compare_color_4"),
		ByteField("compare_color_5"),
		IntegerField("value_1"),
		IntegerField("value_2"),
		IntegerField("value_3"),
		IntegerField("value_4"),
		IntegerField("value_5"),
		ByteField("logic_1"),
		ByteField("logic_2"),
		ByteField("logic_3"),
		ByteField("logic_4"),
		ByteField("logic_5"),
	)


class SpellMechanic(Structure):
	"""
	SpellMechanic.dbc
	Spell mechanic names
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
	)


class SpellRadius(Structure):
	"""
	SpellRadius.dbc
	Spell radius data
	"""
	fields = Skeleton(
		IDField(),
		FloatField("radius_min"),
		IntegerField(),
		FloatField("radius_max"),
	)


class SpellRange(Structure):
	"""
	SpellRange.dbc
	Spell range data
	"""
	fields = Skeleton(
		IDField(),
		FloatField("range_min"),
		FloatField("range_min_friendly"),
		FloatField("range_max"),
		FloatField("range_max_friendly"),
		BitMaskField("flags"),
		LocalizedFields("name"),
		LocalizedFields("tooltip_name"),
	)


class SpellRuneCost(Structure):
	"""
	SpellRunecost.dbc
	Death Knight abilities' rune costs
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("blood"),
		IntegerField("unholy"),
		IntegerField("frost"),
		IntegerField("runic_power"),
	)


class SpellShapeshiftForm(Structure):
	"""
	SpellShapeshiftForm.dbc
	Different shapeshifts/stances for spells
	"""
	fields = Skeleton(
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


class SpellVisual(Structure):
	"""
	SpellVisual.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("precast_effect", "SpellVisualKit"),
		ForeignKey("casting_effect", "SpellVisualKit"),
		ForeignKey("target_effect", "SpellVisualKit"),
		ForeignKey("buff_effect", "SpellVisualKit"),
		IntegerField("shapeshift"),
		ForeignKey("channel_effect", "SpellVisualKit"),
		BooleanField("has_missile"),
		ForeignKey("missile_effect", "SpellVisualKit"),
		BitMaskField("flags"),
		UnknownField(),
		ForeignKey("sound", "SoundEntries"),
		UnknownField(),
		ForeignKey("center_effect", "SpellVisualKit"),
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
		ForeignKey("aoe_effect", "SpellVisualKit"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class SpellVisualKit(Structure):
	"""
	SpellVisualKit.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("caster_animation_1", "AnimationData"),
		ForeignKey("caster_animation_2", "AnimationData"),
		ForeignKey("caster_animation_3", "AnimationData"),
		ForeignKey("visual_head", "SpellVisualEffectName"),
		ForeignKey("visual_chest", "SpellVisualEffectName"),
		ForeignKey("visual_base", "SpellVisualEffectName"),
		ForeignKey("visual_right", "SpellVisualEffectName"),
		ForeignKey("visual_left", "SpellVisualEffectName"),
		ForeignKey("visual_aoe", "SpellVisualEffectName"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		ForeignKey("visual_unk", "SpellVisualEffectName"),
		ForeignKey("sound", "SoundEntries"),
		ForeignKey("camera_effect", "SpellEffectCameraShakes"),
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
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		BitMaskField(),
	)
	
	def changed_9637(self, fields):
		fields.delete_fields("caster_animation_3")


class SpellVisualEffectName(Structure):
	"""
	SpellVisualEffectName.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		FilePathField("path"),
		FloatField(),
		FloatField("scale"),
		FloatField(), #scale?
		FloatField(), #alpha?
	)

class SpellVisualPrecastTransitions(Structure):
	"""
	SpellVisualPrecastTransitions.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("load"),
		StringField("hold"),
	)


class StableSlotPrices(Structure):
	"""
	StableSlotPrices.dbc
	"""
	fields = Skeleton(
		IDField(),
		MoneyField("price"),
	)


class Startup_Strings(Structure):
	"""
	Startup_Strings.dbc
	Runtime messages and warnings
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		LocalizedFields("message"),
	)


class Stationery(Structure):
	"""
	Stationery.dbc
	In-game mail background
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("item", "Item"),
		StringField("name"),
		UnknownField(),
	)


class StringLookups(Structure):
	"""
	StringLookups.dbc
	"""
	fields = Skeleton(
		IDField(),
		FilePathField("path"),
	)


class SummonProperties(Structure):
	"""
	SummonProperties.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("category"),
		IntegerField("faction"), # doesn't seem to be Faction.dbc
		IntegerField("type"),
		IntegerField("slot"),
		BitMaskField("flags"),
	)


class Talent(Structure):
	"""
	Talent.dbc
	Player/pet talents
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("tab", "TalentTab"),
		UnsignedIntegerField("row"),
		UnsignedIntegerField("column"),
		ForeignKey("rank_1", "Spell"),
		ForeignKey("rank_2", "Spell"),
		ForeignKey("rank_3", "Spell"),
		ForeignKey("rank_4", "Spell"),
		ForeignKey("rank_5", "Spell"),
		ForeignKey("rank_6", "Spell"),
		ForeignKey("rank_7", "Spell"),
		ForeignKey("rank_8", "Spell"),
		ForeignKey("rank_9", "Spell"),
		ForeignKey("depends_1", "Talent"),
		ForeignKey("depends_2", "Talent"),
		ForeignKey("depends_3", "Talent"),
		IntegerField("depends_count_1"),
		IntegerField("depends_count_2"),
		IntegerField("depends_count_3"),
		BooleanField("single_point"), # More like "teaches spell"
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class TalentTab(Structure):
	"""
	TalentTab.dbc
	Talent panel tabs
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		ForeignKey("icon", "SpellIcon"),
		UnknownField(),
		BitMaskField("class_mask"),
		IntegerField("pet_mask"),
		IntegerField("page"),
		StringField("internal_name"),
	)


class TaxiNodes(Structure):
	"""
	TaxiNodes.dbc
	Flight paths, teleports, etc.
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("map", "Map"),
		FloatField("x"),
		FloatField("y"),
		FloatField("z"),
		LocalizedFields("name"),
		ForeignKey("mount_horde", "creaturecache"),
		ForeignKey("mount_alliance", "creaturecache"),
	)


class TaxiPath(Structure):
	"""
	TaxiPath.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("taxi_from", "TaxiNodes"),
		ForeignKey("taxi_to", "TaxiNodes"),
		MoneyField("price"),
	)


class TaxiPathNode(Structure):
	"""
	TaxiPathNode.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("taxi", "TaxiPath"),
		IntegerField("index"),
		ForeignKey("map", "Map"),
		FloatField("x"),
		FloatField("y"),
		FloatField("z"),
		UnknownField(),
		DurationField("delay", unit="seconds"), # Delay before moving to next point (used on boats / trams / zepplins) 
		IntegerField("arrival_event"),
		IntegerField("departure_event"),
	)


class TeamContributionPoints(Structure):
	"""
	TeamContributionPoints.dbc
	"""
	fields = Skeleton(
		IDField(),
		FloatField("points"),
	)


class TerrainType(Structure):
	"""
	TerrainType.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("type"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class TerrainTypeSounds(Structure):
	"""
	TerrainTypeSounds.dbc
	"""
	fields = Skeleton(
		IDField(),
	)


class TotemCategory(Structure):
	"""
	TotemCategory.dbc
	Item tools, totems etc
	"""
	fields = Skeleton(
		IDField(),
		LocalizedFields("name"),
		IntegerField("category"),
		BitMaskField("flags"),
	)


class TransportAnimation(Structure):
	"""
	TransportAnimation.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		ForeignKey("animation_data", "AnimationData")
	)


class TransportPhysics(Structure):
	"""
	TransportPhysics.dbc
	"""
	fields = Skeleton(
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


class UISoundLookups(Structure):
	"""
	UISoundLookups.dbc
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("sound", "SoundEntries"),
		StringField("name"),
	)


class UnitBlood(Structure):
	"""
	UnitBlood.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FilePathField("texture_1"),
		FilePathField("texture_2"),
		FilePathField("texture_3"),
		FilePathField("texture_4"),
		UnknownField(),
	)


class UnitBloodLevels(Structure):
	"""
	UnitBloodLevels.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class Vehicle(Structure):
	"""
	Vehicle.dbc
	"""
	fields = Skeleton(
		IDField(),
		BitMaskField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
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
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FloatField(),
		FilePathField("texture_1"),
		FilePathField("texture_2"),
		FilePathField("model_1"),
		FilePathField("model_2"),
		FloatField(),
		UnknownField(),
		FloatField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class VehicleSeat(Structure):
	"""
	VehicleSeat.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(),
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
		UnknownField(),
		UnknownField(),
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
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		FloatField(),
		FloatField(),
		UnknownField(),
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


class VehicleUIIndicator(Structure):
	"""
	VehicleUIIndicator.dbc
	"""
	fields = Skeleton(
		IDField(), # id seems shared between VehicleUIInd*
		UnknownField(),
	)


class VehicleUIIndSeat(Structure):
	"""
	VehicleUIIndSeat.dbc
	"""
	fields = Skeleton(
		IDField(), # id seems shared between VehicleUIInd*
		UnknownField(), # id seems shared between VehicleUIInd*
		UnknownField(),
		FloatField(),
		FloatField(),
	)


class VideoHardware(Structure):
	"""
	VideoHardware.dbc
	"""
	fields = Skeleton(
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
		StringField(),
		StringField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class VocalUISounds(Structure):
	"""
	VocalUISounds.dbc
	Contains UI error sounds for all the different races and genders,
	eg "Already in a group", "Not Enough Mana", etc.
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		ForeignKey("race", "ChrRaces"),
		ForeignKey("sound_male", "SoundEntries"),
		ForeignKey("sound_female", "SoundEntries"),
		UnknownField(),
		UnknownField(),
	)


class WeaponImpactSounds(Structure):
	"""
	WeaponImpactSounds.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		UnknownField(), # boolean? for crits maybe?
		ForeignKey("sound_1", "SoundEntries"),
		ForeignKey("sound_2", "SoundEntries"),
		ForeignKey("sound_3", "SoundEntries"),
		ForeignKey("sound_4", "SoundEntries"),
		ForeignKey("sound_5", "SoundEntries"),
		ForeignKey("sound_6", "SoundEntries"),
		ForeignKey("sound_7", "SoundEntries"),
		ForeignKey("sound_8", "SoundEntries"),
		ForeignKey("sound_9", "SoundEntries"),
		ForeignKey("sound_10", "SoundEntries"),
		ForeignKey("sound_11", "SoundEntries"),
		ForeignKey("sound_12", "SoundEntries"),
		ForeignKey("sound_13", "SoundEntries"),
		ForeignKey("sound_14", "SoundEntries"),
		ForeignKey("sound_15", "SoundEntries"),
		ForeignKey("sound_16", "SoundEntries"),
		ForeignKey("sound_17", "SoundEntries"),
		ForeignKey("sound_18", "SoundEntries"),
		ForeignKey("sound_19", "SoundEntries"),
		ForeignKey("sound_20", "SoundEntries"),
	)


class WeaponSwingSounds2(Structure):
	"""
	WeaponSwingSounds2.dbc
	"""
	fields = Skeleton(
		IDField(),
		UnknownField(),
		BooleanField("critical"),
		ForeignKey("sound", "SoundEntries")
	)


class Weather(Structure):
	"""
	Weather.dbc
	Weather lookups
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("sound", "SoundEntries"),
		IntegerField("type"), #	 1 = Rain, 2 = Snow, 3 = Sandstorm
		FloatField(), # cmyk?
		FloatField(),
		FloatField(),
		FilePathField("texture"),
	)
	
	def changed_10522(self, fields):
		fields.insert_field(FloatField(), before="texture")


class WMOAreaTable(Structure):
	"""
	WMOAreaTable.dbc
	"""
	fields = Skeleton(
		IDField(),
		IntegerField("root"),
		IntegerField("nameset"),
		IntegerField("group"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		ForeignKey("zone", "AreaTable"),
		LocalizedFields("name"),
	)


class WorldChunkSounds(Structure):
	"""
	WorldChunkSounds.dbc
	"""
	DEAD = True
	fields = Skeleton(
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


class WorldMapArea(Structure):
	"""
	WorldMapArea.dbc
	Map data for each "zone" (instance)
	"""
	fields = Skeleton(
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
	
	def changed_10116(self, fields):
		fields.append_fields(
			ForeignKey("parent_area", "WorldMapArea"), # Not for all?!
		)


class WorldMapContinent(Structure):
	"""
	WorldMapContinent.dbc
	"""
	fields = Skeleton(
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
	
	def changed_9901(self, fields):
		"""
		XXX Unknown build!
		"""
		fields.append_fields(
			UnknownField(),
		)


class WorldMapOverlay(Structure):
	"""
	WorldMapOverlay.dbc
	"""
	fields = Skeleton(
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


class WorldMapTransforms(Structure):
	"""
	WorldMapTransforms.dbc
	Coordinate transformations from one
	instance to another - Example:
	Expansion01 -> Azuremyst Isles
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("map", "Map"),
		FloatField("x1"),
		FloatField("x2"),
		FloatField("y1"),
		FloatField("y2"),
		ForeignKey("target_map", "Map"),
		FloatField("target_x"),
		FloatField("target_y"),
	)
	
	def changed_9658(self, fields):
		"""
		XXX When was this added? 6080->9658
		"""
		fields.append_fields(UnknownField())


class WorldStateUI(Structure):
	"""
	WorldStateUI.dbc
	Used for drawing icons on the world map (eg naxx/wotlk event)
	"""
	fields = Skeleton(
		IDField(),
		ForeignKey("map", "Map"),
		UnknownField(),
		UnknownField(),
		FilePathField("path"),
		LocalizedFields("name"),
		LocalizedFields("description"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		LocalizedFields("battleground"),
		StringField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
	)


class WorldStateZoneSounds(Structure):
	"""
	WorldStateZoneSounds.dbc
	"""
	implicit_id = True
	fields = Skeleton(
		IntegerField("world_state"),
		IntegerField("value"),
		ForeignKey("area", "AreaTable"),
		ForeignKey("area_wmo", "WMOAreaTable"),
		ForeignKey("intro_music", "ZoneIntroMusicTable"),
		ForeignKey("music", "ZoneMusic"),
		ForeignKey("sound_ambience", "SoundAmbience"),
		ForeignKey("preferences", "SoundProviderPreferences"),
	)


class WowError_Strings(Structure):
	"""
	WowError_Strings.dbc
	Localization called by WowError.exe when the game crashes.
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		LocalizedFields("description"),
	)


class ZoneIntroMusicTable(Structure):
	"""
	ZoneIntroMusicTable.dbc
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		ForeignKey("sound", "SoundEntries"),
		BooleanField(),
		DurationField(unit="seconds"),
	)


class ZoneMusic(Structure):
	"""
	ZoneMusic.dbc
	Music played in a zone
	"""
	fields = Skeleton(
		IDField(),
		StringField("name"),
		DurationField("duration_day", unit="milliseconds"),
		DurationField("duration_night", unit="milliseconds"),
		DurationField("loop_wait_day", unit="milliseconds"), # How long until it plays again
		DurationField("loop_wait_night", unit="milliseconds"),
		ForeignKey("music_day", "SoundEntries"),
		ForeignKey("music_night", "SoundEntries"),
	)
