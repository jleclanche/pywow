# -*- coding: utf-8 -*-
"""
gameobjectcache.wdb data structures
"""

from ..base import DBStructure, Skeleton
from ..fields import *

class GameObject_Door(DBStructure):
	"""
	GAMEOBJECT_TYPE_DOOR (0)
	"""
	
	base = Skeleton(
		BooleanField("start_open"),
		ForeignKey("lock", "Lock"),
		DurationField("auto_close_timer", unit="milliseconds"),
		BooleanField("no_damage_immune"),
		IntegerField("open_text"),
		IntegerField("close_text"),
		BooleanField("ignore_los"),
	)

class GameObject_Button(DBStructure):
	"""
	GAMEOBJECT_TYPE_BUTTON (1)
	"""
	
	base = Skeleton(
		BooleanField("start_open"),
		ForeignKey("lock", "Lock"),
		DurationField("auto_close_timer", unit="milliseconds"),
		ForeignKey("trap", "gameobjectcache"),
		BooleanField("no_damage_immune"),
		BooleanField("large"),
		IntegerField("open_text"),
		IntegerField("close_text"),
		BooleanField("ignore_los"),
	)

class GameObject_QuestGiver(DBStructure):
	"""
	GAMEOBJECT_TYPE_QUESTGIVER (2)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("quest_list"),
		ForeignKey("material", "Material"),
		ForeignKey("gossip", "npccache"),
		IntegerField("custom_animation"),
		IntegerField("open_text"),
		BooleanField("ignore_los"),
		BooleanField("usable_mounted"),
		BooleanField("large"),
	)

class GameObject_Chest(DBStructure):
	"""
	GAMEOBJECT_TYPE_CHEST (3)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("loot"),
		IntegerField("restock_timer"),
		BooleanField("consumable"),
		IntegerField("min_openings"),
		IntegerField("max_openings"),
		IntegerField("event"),
		ForeignKey("trap", "gameobjectcache"),
		ForeignKey("quest", "Quest"),
		IntegerField("level"),
		BooleanField("ignore_los"),
		BooleanField("leave_loot"),
		BooleanField("not_in_combat"),
		BooleanField("log_loot"),
		IntegerField("open_text"),
		IntegerField("group_loot_rules"),
		BooleanField("floating_tooltip"),
	)

class GameObject_Binder(DBStructure):
	"""
	GAMEOBJECT_TYPE_BINDER (4)
	"""
	base = Skeleton() # empty

class GameObject_Generic(DBStructure):
	"""
	GAMEOBJECT_TYPE_GENERIC (5)
	"""
	
	base = Skeleton(
		BooleanField("floating_tooltip"),
		BooleanField("highlight"),
		BooleanField("server_only"),
		BooleanField("large"),
		BooleanField("float_on_water"),
		ForeignKey("quest", "Quest"),
	)

class GameObject_Trap(DBStructure):
	"""
	GAMEOBJECT_TYPE_TRAP (6)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("level"),
		IntegerField("radius"),
		ForeignKey("spell", "Spell"),
		IntegerField("charges"),
		DurationField("cooldown", unit="seconds"),
		DurationField("auto_close_timer", unit="milliseconds"),
		IntegerField("start_delay"),
		BooleanField("server_only"),
		BooleanField("stealthed"),
		BooleanField("large"),
		BooleanField("stealth_affected"),
		IntegerField("open_text"),
		IntegerField("close_text"),
		BooleanField("ignore_totems"),
	)


class GameObject_Chair(DBStructure):
	"""
	GAMEOBJECT_TYPE_CHAIR (7)
	"""
	
	base = Skeleton(
		IntegerField("slots"),
		IntegerField("height"),
		BooleanField("only_creator_use"),
		IntegerField("event"),
	)

class GameObject_SpellFocus(DBStructure):
	"""
	GAMEOBJECT_TYPE_SPELLFOCUS (8)
	"""
	
	base = Skeleton(
		IntegerField("focus"),
		IntegerField("range"),
		ForeignKey("trap", "gameobjectcache"),
		BooleanField("server_only"),
		ForeignKey("quest", "Quest"),
		BooleanField("large"),
		BooleanField("floating_tooltip"),
	)

class GameObject_Text(DBStructure):
	"""
	GAMEOBJECT_TYPE_SPELLFOCUS (9)
	"""
	
	base = Skeleton(
		ForeignKey("page", "pagetextcache"),
		ForeignKey("language", "Languages"),
		ForeignKey("material", "Material"),
		BooleanField("usable_mounted"),
	)

class GameObject_Goober(DBStructure):
	"""
	GAMEOBJECT_TYPE_GOOBER (10)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		ForeignKey("quest", "Quest"),
		IntegerField("event"),
		DurationField("auto_close_timer", unit="milliseconds"),
		IntegerField("custom_animation"),
		BooleanField("consumable"),
		DurationField("cooldown", unit="seconds"),
		ForeignKey("page", "pagetextcache"),
		ForeignKey("language", "Languages"),
		ForeignKey("material", "Material"),
		ForeignKey("spell", "Spell"),
		BooleanField("no_damage_immune"),
		ForeignKey("trap", "gameobjectcache"),
		BooleanField("large"),
		IntegerField("open_text"),
		IntegerField("close_text"),
		BooleanField("ignore_los"),
		BooleanField("usable_mounted"),
		BooleanField("floating_tooltip"),
		ForeignKey("gossip", "npccache"),
		IntegerField("world_state_sets_state"),
	)

class GameObject_Transport(DBStructure):
	"""
	GAMEOBJECT_TYPE_TRANSPORT (11)
	"""
	
	base = Skeleton(
		IntegerField("pause"),
		BooleanField("start_open"),
		DurationField("auto_close_timer", unit="milliseconds"),
		IntegerField("pause_event_1"),
		IntegerField("pause_event_2"),
	)

class GameObject_AreaDamage(DBStructure):
	"""
	GAMEOBJECT_TYPE_AREADAMAGE (12)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("radius"),
		IntegerField("damage_min"),
		IntegerField("damage_max"),
		IntegerField("damage_school"),
		IntegerField("open_text"),
		IntegerField("close_text"),
	)


class GameObject_Camera(DBStructure):
	"""
	GAMEOBJECT_TYPE_CAMERA (13)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("cinematic"),
		IntegerField("event"),
		IntegerField("open_text"),
	)

class GameObject_MapObject(DBStructure):
	"""
	GAMEOBJECT_TYPE_MAPOBJECT (14)
	"""
	base = Skeleton() # empty

class GameObject_MOTransport(DBStructure):
	"""
	GAMEOBJECT_TYPE_MO_TRANSPORT (15)
	"""
	
	base = Skeleton(
		IntegerField("taxi_path"),
		IntegerField("move_speed"),
		IntegerField("acceleration"),
		IntegerField("start_event"),
		IntegerField("stop_event"),
		IntegerField("transport_physics"),
		ForeignKey("map", "Map"),
		IntegerField("world_state")
	)

class GameObject_DuelFlag(DBStructure):
	"""
	GAMEOBJECT_TYPE_DUELFLAG (16)
	"""
	base = Skeleton() # empty

class GameObject_FishingNode(DBStructure):
	"""
	GAMEOBJECT_TYPE_FISHINGNODE (17)
	"""
	base = Skeleton() # empty

class GameObject_SummoningRitual(DBStructure):
	"""
	GAMEOBJECT_TYPE_SUMMONING_RITUAL (18)
	"""
	
	base = Skeleton(
		IntegerField("required_players"),
		ForeignKey("spell", "Spell"),
		IntegerField("animation_spell"),
		IntegerField("persistent"),
		ForeignKey("caster_target_spell", "Spell"),
		IntegerField("caster_target_spell_targets"),
		BooleanField("party_only"),
		BooleanField("no_target_check"),
	)

class GameObject_Mailbox(DBStructure):
	"""
	GAMEOBJECT_TYPE_MAILBOX (19)
	"""
	base = Skeleton() # empty

class GameObject_DoNotUse(DBStructure):
	"""
	GAMEOBJECT_TYPE_DONOTUSE (20)
	"""
	base = Skeleton() # empty

class GameObject_GuardPost(DBStructure):
	"""
	GAMEOBJECT_TYPE_GUARDPOST (21)
	"""
	
	base = Skeleton(
		ForeignKey("creature", "creaturecache"),
		IntegerField("charges"),
	)

class GameObject_SpellCaster(DBStructure):
	"""
	GAMEOBJECT_TYPE_SPELLCASTER (22)
	"""
	
	base = Skeleton(
		ForeignKey("spell", "Spell"),
		IntegerField("charges"),
		BooleanField("party_only"),
		BooleanField("usable_mounted"),
		BooleanField("large"),
	)

class GameObject_MeetingStone(DBStructure):
	"""
	GAMEOBJECT_TYPE_MEETINGSTONE (23)
	"""
	
	base = Skeleton(
		IntegerField("min_level"),
		IntegerField("max_level"),
		IntegerField("zone", "AreaTable"),
	)

class GameObject_FlagStand(DBStructure):
	"""
	GAMEOBJECT_TYPE_FLAGSTAND (24)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		ForeignKey("spell", "Spell"),
		IntegerField("radius"),
		ForeignKey("return_aura", "Spell"),
		ForeignKey("return_spell", "Spell"),
		BooleanField("no_damage_immune"),
		IntegerField("close_text"),
		IntegerField("ignore_los"),
	)

class GameObject_FishingHole(DBStructure):
	"""
	GAMEOBJECT_TYPE_FISHINGHOLE (25)
	"""
	
	base = Skeleton(
		IntegerField("radius"),
		IntegerField("loot"),
		IntegerField("min_openings"),
		IntegerField("max_openings"),
		ForeignKey("lock", "Lock"),
	)

class GameObject_FlagDrop(DBStructure):
	"""
	GAMEOBJECT_TYPE_AURA_FLAGDROP (26)
	"""
	
	base = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("event"),
		ForeignKey("spell", "Spell"),
		BooleanField("no_damage_immune"),
		IntegerField("close_text"),
	)

class GameObject_MiniGame(DBStructure):
	"""
	GAMEOBJECT_TYPE_AURA_MINI_GAME (27)
	"""
	
	base = Skeleton(
		IntegerField("game_type"),
	)

class GameObject_CapturePoint(DBStructure):
	"""
	GAMEOBJECT_TYPE_AURA_CAPTURE_POINT (29)
	"""
	
	base = Skeleton(
		IntegerField("radius"),
		ForeignKey("spell", "Spell"),
		IntegerField("world_state_1"),
		IntegerField("world_state_2"),
		IntegerField("win_event_1"),
		IntegerField("win_event_2"),
		IntegerField("contested_event_1"),
		IntegerField("contested_event_2"),
		IntegerField("neutral_event_1"),
		IntegerField("neutral_event_2"),
		IntegerField("neutral_percent"),
		IntegerField("world_state_3"),
		IntegerField("min_superiority"),
		IntegerField("max_superiority"),
		IntegerField("min_time"),
		IntegerField("max_time"),
		BooleanField("large"),
		IntegerField("highlight"),
		IntegerField("starting_value"),
		IntegerField("unidirectional"),
	)

class GameObject_AuraGenerator(DBStructure):
	"""
	GAMEOBJECT_TYPE_AURA_GENERATOR (30)
	"""
	
	base = Skeleton(
		BooleanField("start_open"),
		IntegerField("radius"),
		ForeignKey("aura_1", "Spell"),
		IntegerField("condition_1"),
		ForeignKey("aura_2", "Spell"),
		IntegerField("condition_2"),
		BooleanField("server_only"),
	)

class GameObject_DungeonDifficulty(DBStructure):
	"""
	GAMEOBJECT_TYPE_DUNGEON_DIFFICULTY (31)
	"""
	
	base = Skeleton(
		ForeignKey("instance", "Map"),
		IntegerField("difficulty"),
	)

class GameObject_BarberChair(DBStructure):
	"""
	GAMEOBJECT_TYPE_BARBER_CHAIR (32)
	"""
	
	base = Skeleton(
		IntegerField("height"),
		IntegerField("offset"),
	)

class GameObject_DestructibleBuilding(DBStructure):
	"""
	GAMEOBJECT_TYPE_DESTRUCTIBLE_BUILDING (33)
	"""
	
	base = Skeleton(
		IntegerField("intact_health"),
		IntegerField("credit_proxy_creature"),
		UnknownField(),
		IntegerField("intact_event"),
		UnknownField(),
		IntegerField("damaged_health"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		IntegerField("damaged_event"),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		UnknownField(),
		IntegerField("destroyed_event"),
		UnknownField(),
		DurationField("debuilding_time", unit="seconds"),
		UnknownField(),
		IntegerField("destructible_data"),
		IntegerField("rebuilding_event"),
		UnknownField(),
		UnknownField(),
		IntegerField("damage_event"),
		UnknownField(),
	)

class GameObject_GuildBank(DBStructure):
	"""
	GAMEOBJECT_TYPE_GUILDBANK (34)
	"""
	base = Skeleton() # empty

class GameObject_TrapDoor(DBStructure):
	"""
	GAMEOBJECT_TYPE_TRAPDOOR (35)
	"""
	
	base = Skeleton(
		IntegerField("when_to_pause"),
		BooleanField("start_open"),
		BooleanField("auto_close"),
	)

GAME_OBJECT_TYPES = {
	 0: GameObject_Door,
	 1: GameObject_Button,
	 2: GameObject_QuestGiver,
	 3: GameObject_Chest,
	 4: GameObject_Binder,
	 5: GameObject_Generic,
	 6: GameObject_Trap,
	 7: GameObject_Chair,
	 8: GameObject_SpellFocus,
	 9: GameObject_Text,
	10: GameObject_Goober,
	11: GameObject_Transport,
	12: GameObject_AreaDamage,
	13: GameObject_Camera,
	14: GameObject_MapObject,
	15: GameObject_MOTransport,
	16: GameObject_DuelFlag,
	17: GameObject_FishingNode,
	18: GameObject_SummoningRitual,
	19: GameObject_Mailbox,
	20: GameObject_DoNotUse,
	21: GameObject_GuardPost,
	22: GameObject_SpellCaster,
	23: GameObject_MeetingStone,
	24: GameObject_FlagStand,
	25: GameObject_FishingHole,
	26: GameObject_FlagDrop,
	27: GameObject_MiniGame,
	29: GameObject_CapturePoint,
	30: GameObject_AuraGenerator,
	31: GameObject_DungeonDifficulty,
	32: GameObject_BarberChair,
	33: GameObject_DestructibleBuilding,
	34: GameObject_GuildBank,
	35: GameObject_TrapDoor,
}
