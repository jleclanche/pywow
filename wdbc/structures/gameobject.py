# -*- coding: utf-8 -*-
"""
gameobjectcache.wdb data structures
"""

from pywow.structures import Structure, Skeleton
from pywow.structures import *

class GameObject_Door(Structure):
	"""
	GAMEOBJECT_TYPE_DOOR (0)
	"""
	
	fields = Skeleton(
		BooleanField("start_open"),
		ForeignKey("lock", "Lock"),
		DurationField("auto_close_timer", unit="milliseconds"),
		BooleanField("no_damage_immune"),
		IntegerField("open_text"),
		IntegerField("close_text"),
		BooleanField("ignore_los"),
	)

class GameObject_Button(Structure):
	"""
	GAMEOBJECT_TYPE_BUTTON (1)
	"""
	
	fields = Skeleton(
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

class GameObject_QuestGiver(Structure):
	"""
	GAMEOBJECT_TYPE_QUESTGIVER (2)
	"""
	
	fields = Skeleton(
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

class GameObject_Chest(Structure):
	"""
	GAMEOBJECT_TYPE_CHEST (3)
	"""
	
	fields = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("loot"),
		IntegerField("restock_time"),
		BooleanField("consumable"),
		IntegerField("min_openings"),
		IntegerField("max_openings"),
		IntegerField("loot_event"),
		ForeignKey("trap", "gameobjectcache"),
		ForeignKey("quest", "Quest"),
		IntegerField("level"),
		BooleanField("ignore_los"),
		BooleanField("leave_loot"),
		BooleanField("unusable_in_combat"),
		BooleanField("log_loot"),
		IntegerField("open_text"),
		IntegerField("group_loot_rules"),
		BooleanField("floating_tooltip"),
	)

class GameObject_Binder(Structure):
	"""
	GAMEOBJECT_TYPE_BINDER (4)
	"""
	fields = Skeleton() # empty

class GameObject_Generic(Structure):
	"""
	GAMEOBJECT_TYPE_GENERIC (5)
	"""
	
	fields = Skeleton(
		BooleanField("floating_tooltip"),
		BooleanField("highlight"),
		BooleanField("server_only"),
		BooleanField("large"),
		BooleanField("float_on_water"),
		ForeignKey("quest", "Quest"),
	)

class GameObject_Trap(Structure):
	"""
	GAMEOBJECT_TYPE_TRAP (6)
	"""
	
	fields = Skeleton(
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


class GameObject_Chair(Structure):
	"""
	GAMEOBJECT_TYPE_CHAIR (7)
	"""
	
	fields = Skeleton(
		IntegerField("slots"),
		IntegerField("height"),
		BooleanField("creator_use_only"),
		IntegerField("event"),
	)

class GameObject_SpellFocus(Structure):
	"""
	GAMEOBJECT_TYPE_SPELLFOCUS (8)
	"""
	
	fields = Skeleton(
		IntegerField("focus"),
		IntegerField("range"),
		ForeignKey("trap", "gameobjectcache"),
		BooleanField("server_only"),
		ForeignKey("quest", "Quest"),
		BooleanField("large"),
		BooleanField("floating_tooltip"),
	)

class GameObject_Text(Structure):
	"""
	GAMEOBJECT_TYPE_SPELLFOCUS (9)
	"""
	
	fields = Skeleton(
		ForeignKey("page", "pagetextcache"),
		ForeignKey("language", "Languages"),
		ForeignKey("material", "Material"),
		BooleanField("usable_mounted"),
	)

class GameObject_Goober(Structure):
	"""
	GAMEOBJECT_TYPE_GOOBER (10)
	"""
	
	fields = Skeleton(
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

class GameObject_Transport(Structure):
	"""
	GAMEOBJECT_TYPE_TRANSPORT (11)
	"""
	
	fields = Skeleton(
		IntegerField("pause"),
		BooleanField("start_open"),
		DurationField("auto_close_timer", unit="milliseconds"),
		IntegerField("pause_event_1"),
		IntegerField("pause_event_2"),
	)

class GameObject_AreaDamage(Structure):
	"""
	GAMEOBJECT_TYPE_AREADAMAGE (12)
	"""
	
	fields = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("radius"),
		IntegerField("damage_min"),
		IntegerField("damage_max"),
		IntegerField("damage_school"),
		IntegerField("open_text"),
		IntegerField("close_text"),
	)


class GameObject_Camera(Structure):
	"""
	GAMEOBJECT_TYPE_CAMERA (13)
	"""
	
	fields = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("cinematic"),
		IntegerField("event"),
		IntegerField("open_text"),
	)

class GameObject_MapObject(Structure):
	"""
	GAMEOBJECT_TYPE_MAPOBJECT (14)
	"""
	fields = Skeleton() # empty

class GameObject_MOTransport(Structure):
	"""
	GAMEOBJECT_TYPE_MO_TRANSPORT (15)
	"""
	
	fields = Skeleton(
		IntegerField("taxi"),
		IntegerField("move_speed"),
		IntegerField("acceleration"),
		IntegerField("start_event"),
		IntegerField("stop_event"),
		IntegerField("transport_physics"),
		ForeignKey("map", "Map"),
		IntegerField("world_state")
	)

class GameObject_DuelFlag(Structure):
	"""
	GAMEOBJECT_TYPE_DUELFLAG (16)
	"""
	fields = Skeleton() # empty

class GameObject_FishingNode(Structure):
	"""
	GAMEOBJECT_TYPE_FISHINGNODE (17)
	"""
	fields = Skeleton() # empty

class GameObject_SummoningRitual(Structure):
	"""
	GAMEOBJECT_TYPE_SUMMONING_RITUAL (18)
	"""
	
	fields = Skeleton(
		IntegerField("required_players"),
		ForeignKey("spell", "Spell"),
		IntegerField("animation_spell"),
		IntegerField("persistent"),
		ForeignKey("caster_target_spell", "Spell"),
		IntegerField("caster_target_spell_targets"),
		BooleanField("party_only"),
		BooleanField("no_target_check"),
	)

class GameObject_Mailbox(Structure):
	"""
	GAMEOBJECT_TYPE_MAILBOX (19)
	"""
	fields = Skeleton() # empty

class GameObject_DoNotUse(Structure):
	"""
	GAMEOBJECT_TYPE_DONOTUSE (20)
	"""
	fields = Skeleton() # empty

class GameObject_GuardPost(Structure):
	"""
	GAMEOBJECT_TYPE_GUARDPOST (21)
	"""
	
	fields = Skeleton(
		ForeignKey("creature", "creaturecache"),
		IntegerField("charges"),
	)

class GameObject_SpellCaster(Structure):
	"""
	GAMEOBJECT_TYPE_SPELLCASTER (22)
	"""
	
	fields = Skeleton(
		ForeignKey("spell", "Spell"),
		IntegerField("charges"),
		BooleanField("party_only"),
		BooleanField("usable_mounted"),
		BooleanField("large"),
	)

class GameObject_MeetingStone(Structure):
	"""
	GAMEOBJECT_TYPE_MEETINGSTONE (23)
	"""
	
	fields = Skeleton(
		IntegerField("min_level"),
		IntegerField("max_level"),
		ForeignKey("zone", "AreaTable"),
	)

class GameObject_FlagStand(Structure):
	"""
	GAMEOBJECT_TYPE_FLAGSTAND (24)
	"""
	
	fields = Skeleton(
		ForeignKey("lock", "Lock"),
		ForeignKey("spell", "Spell"),
		IntegerField("radius"),
		ForeignKey("return_aura", "Spell"),
		ForeignKey("return_spell", "Spell"),
		BooleanField("no_damage_immune"),
		IntegerField("close_text"),
		IntegerField("ignore_los"),
	)

class GameObject_FishingHole(Structure):
	"""
	GAMEOBJECT_TYPE_FISHINGHOLE (25)
	"""
	
	fields = Skeleton(
		IntegerField("radius"),
		IntegerField("loot"),
		IntegerField("min_openings"),
		IntegerField("max_openings"),
		ForeignKey("lock", "Lock"),
	)

class GameObject_FlagDrop(Structure):
	"""
	GAMEOBJECT_TYPE_AURA_FLAGDROP (26)
	"""
	
	fields = Skeleton(
		ForeignKey("lock", "Lock"),
		IntegerField("event"),
		ForeignKey("spell", "Spell"),
		BooleanField("no_damage_immune"),
		IntegerField("close_text"),
	)

class GameObject_MiniGame(Structure):
	"""
	GAMEOBJECT_TYPE_AURA_MINI_GAME (27)
	"""
	
	fields = Skeleton(
		IntegerField("game_type"),
	)

class GameObject_CapturePoint(Structure):
	"""
	GAMEOBJECT_TYPE_AURA_CAPTURE_POINT (29)
	"""
	
	fields = Skeleton(
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

class GameObject_AuraGenerator(Structure):
	"""
	GAMEOBJECT_TYPE_AURA_GENERATOR (30)
	"""
	
	fields = Skeleton(
		BooleanField("start_open"),
		IntegerField("radius"),
		ForeignKey("aura_1", "Spell"),
		IntegerField("condition_1"),
		ForeignKey("aura_2", "Spell"),
		IntegerField("condition_2"),
		BooleanField("server_only"),
	)

class GameObject_DungeonDifficulty(Structure):
	"""
	GAMEOBJECT_TYPE_DUNGEON_DIFFICULTY (31)
	"""
	
	fields = Skeleton(
		ForeignKey("instance", "Map"),
		IntegerField("difficulty"),
	)

class GameObject_BarberChair(Structure):
	"""
	GAMEOBJECT_TYPE_BARBER_CHAIR (32)
	"""
	
	fields = Skeleton(
		IntegerField("height"),
		IntegerField("offset"),
	)

class GameObject_DestructibleBuilding(Structure):
	"""
	GAMEOBJECT_TYPE_DESTRUCTIBLE_BUILDING (33)
	"""
	
	fields = Skeleton(
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

class GameObject_GuildBank(Structure):
	"""
	GAMEOBJECT_TYPE_GUILDBANK (34)
	"""
	fields = Skeleton() # empty

class GameObject_TrapDoor(Structure):
	"""
	GAMEOBJECT_TYPE_TRAPDOOR (35)
	"""
	
	fields = Skeleton(
		IntegerField("pause"),
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
