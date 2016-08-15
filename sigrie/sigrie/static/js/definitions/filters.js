sigrieDefinitions = {};

var fields = {
	"integer": function(custom) {
		if (typeof(custom) != "object") custom = {};
		var result = {
			"type": "integer",
			"size": 7,
			"default": "",
			"validator": function(type, value, modifier) {
				if ((modifier != "in") && (isNaN(value))) return false;
				if (typeof(type.min) == "number") {
					if (value < type.min) return false;
				}
				if (typeof(type.max) == "number") {
					if (value > type.max) return false;
				}
				return true
			}
		}
		for (var key in custom) {
			result[key] = custom[key]
		}
		return result
	},
	"string": function(custom) {
		if (typeof(custom) != "object") custom = {};
		var result = {
			"type": "string",
			"default": "",
			"size": 30,
			"validator": function(type, value, modifier) {
				if (typeof(type.maxLength) == "number") {
					if (value.length > type.maxLength) return false;
				}
				return true;
			}
		}
		for (var key in custom) {
			result[key] = custom[key]
		}
		return result
	},
	"foreignKey": function(name, custom) {
		if (typeof(custom) != "object") custom = {};
		var result = {
			"type": "foreignKey",
			"key": name
		}
		for (var key in custom) {
			result[key] = custom[key]
		}
		return result
	}
}
var choices = {
	"binds": [
		{"value": 0, "name": "None"},
		{"value": 1, "name": "Binds when picked up"},
		{"value": 2, "name": "Binds when equipped"},
		{"value": 3, "name": "Binds when used"},
		{"value": 4, "name": "Quest Item"},
		{"value": 5, "name": "Binds to account"}
	],
	"classes": [
		{"value": 1, "name": "Warrior"},
		{"value": 2, "name": "Paladin"},
		{"value": 3, "name": "Hunter"},
		{"value": 4, "name": "Rogue"},
		{"value": 5, "name": "Priest"},
		{"value": 6, "name": "Death Knight"},
		{"value": 7, "name": "Shaman"},
		{"value": 8, "name": "Mage"},
		{"value": 9, "name": "Warlock"},
		{"value": 11, "name": "Druid"}
	],
	"creatureCategories": [
		{"value": 0, "name": "Not Specified"},
		{"value": 1, "name": "Beast"},
		{"value": 2, "name": "Dragonkin"},
		{"value": 3, "name": "Demon"},
		{"value": 4, "name": "Elemental"},
		{"value": 5, "name": "Giant"},
		{"value": 6, "name": "Undead"},
		{"value": 7, "name": "Humanoid"},
		{"value": 8, "name": "Critter"},
		{"value": 9, "name": "Mechanical"},
		{"value": 10, "name": "Uncategorized"},
		{"value": 11, "name": "Totem"},
		{"value": 12, "name": "Non-combat Pet"},
		{"value": 13, "name": "Gas Cloud"}
	],
	"creatureTypes": [
		{"value": 0, "name": "Normal"},
		{"value": 1, "name": "Elite"},
		{"value": 2, "name": "Rare-Elite"},
		{"value": 3, "name": "Boss"},
		{"value": 4, "name": "Rare"}
	],
	"dispelTypes":
	[
		{"value": 1, "name": "Magic"},
		{"value": 2, "name": "Curse"},
		{"value": 3, "name": "Disease"},
		{"value": 4, "name": "Poison"},
		{"value": 9, "name": "Enrage"}
	],
	"gemColors": [
		{"value": 1, "name": "Meta"},
		{"value": 2, "name": "Red"},
		{"value": 4, "name": "Yellow"},
		{"value": 8, "name": "Blue"}
	],
	"itemCategories": [
		{"value": 0, "name": "Consumable"},
		{"value": 1, "name": "Bags"},
		{"value": 2, "name": "Weapons"},
		{"value": 3, "name": "Gems"},
		{"value": 4, "name": "Armor"},
		{"value": 6, "name": "Projectiles"},
		{"value": 7, "name": "Trade Goods"},
		{"value": 9, "name": "Recipes"},
		{"value": 10, "name": "Currency"},
		{"value": 11, "name": "Quivers"},
		{"value": 12, "name": "Quest Items"},
		{"value": 13, "name": "Keys"},
		{"value": 15, "name": "Miscellaneous"},
		{"value": 16, "name": "Glyphs"}
	],
	"itemQualities": [
		{"value": 0, "name": "Poor"},
		{"value": 1, "name": "Common"},
		{"value": 2, "name": "Uncommon"},
		{"value": 3, "name": "Rare"},
		{"value": 4, "name": "Epic"},
		{"value": 5, "name": "Legendary"},
		{"value": 6, "name": "Artifact"},
		{"value": 7, "name": "Heirloom"}
	],
	"races": [
		{"value": 1, "name": "Human"},
		{"value": 2, "name": "Orc"},
		{"value": 3, "name": "Dwarf"},
		{"value": 4, "name": "Night Elf"},
		{"value": 5, "name": "Undead"},
		{"value": 6, "name": "Tauren"},
		{"value": 7, "name": "Gnome"},
		{"value": 8, "name": "Troll"},
		{"value": 10, "name": "Blood Elf"},
		{"value": 11, "name": "Draenei"}
	],
	"schools": [
		{"value": 0, "name": "Physical"},
		{"value": 1, "name": "Holy"},
		{"value": 2, "name": "Fire"},
		{"value": 3, "name": "Nature"},
		{"value": 4, "name": "Frost"},
		{"value": 5, "name": "Shadow"},
		{"value": 6, "name": "Arcane"}
	],
	"slots": [
		{"value": 0, "name": "None"},
		{"value": 1, "name": "Head"},
		{"value": 2, "name": "Neck"},
		{"value": 3, "name": "Shoulder"},
		{"value": 4, "name": "Shirt"},
		{"value": 5, "name": "Chest"},
		{"value": 6, "name": "Waist"},
		{"value": 7, "name": "Legs"},
		{"value": 8, "name": "Feet"},
		{"value": 9, "name": "Wrist"},
		{"value": 10, "name": "Hands"},
		{"value": 11, "name": "Finger"},
		{"value": 12, "name": "Trinket"},
		{"value": 13, "name": "One-Hand"},
		{"value": 14, "name": "Shield"},
		{"value": 15, "name": "Ranged"},
		{"value": 16, "name": "Back"},
		{"value": 17, "name": "Two-Hand"},
		{"value": 18, "name": "Bag"},
		{"value": 19, "name": "Tabard"},
		{"value": 20, "name": "Chest"},
		{"value": 21, "name": "Main Hand"},
		{"value": 22, "name": "Off-Hand"},
		{"value": 23, "name": "Held In Off-hand"},
		{"value": 24, "name": "Projectile"},
		{"value": 25, "name": "Thrown"},
		{"value": 26, "name": "Ranged"},
		{"value": 28, "name": "Relic"}
	],
	"boolean": [
		{"value": 0, "name": "No"},
		{"value": 1, "name": "Yes"}
	],
	"faction": [
		{"value": -1, "name": "Both"},
		{"value": 0, "name": "Horde"},
		{"value": 1, "name": "Alliance"}
	],
	"pvpZoneType": [
		{"value": 0, "name": "Contested"},
		{"value": 2, "name": "Alliance"},
		{"value": 4, "name": "Horde"},
		{"value": 6, "name": "Sanctuary"}
	],
	"questTypes": [
		{"value": 1, "name": "Group"},
// 		{"value": 21, "name": "Life"},
		{"value": 41, "name": "PvP"},
		{"value": 62, "name": "Raid"},
		{"value": 81, "name": "Dungeon"},
		{"value": 82, "name": "World Event"},
// 		{"value": 83, "name": "Legendary"},
		{"value": 85, "name": "Heroic"},
		{"value": 88, "name": "Raid (10)"},
		{"value": 89, "name": "Raid (25)"}
	]
}

sigrieDefinitions.achievement = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"faction": fields.integer({"name": "Faction", "choices": choices.faction, "default": -1}),
	"Instance": fields.foreignKey("instance", {"name": "Instance"}),
	"parent": fields.foreignKey("achievement", {"name": "Parent Achievement"}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"points": fields.integer({"name": "Awards points"}),
	"statistic": fields.integer({"name": "Statistic", "choices": choices.boolean, "default": 1}),
	"serverfirst": fields.integer({"name": "Realm first", "choices": choices.boolean, "default": 1}),
	"icon": fields.string({"name": "Icon", "maxLength": 32}),
	"objective": fields.string({"name": "Objective"}),
	"reward": fields.string({"name": "Reward"}),
	"category": fields.foreignKey("achievementCategory", {"name": "Category"})
};

sigrieDefinitions.achievementCategory = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"parent": fields.foreignKey("achievementCategory", {"name": "Parent"}),
	"name": fields.string({"name": "Name", "maxLength": 64})
}

sigrieDefinitions.creature = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"title": fields.string({"name": "Title", "maxLength": 128}),
	"category":fields.integer({"name": "Category", "choices": choices.creatureCategories}),
	"family": fields.integer({"name": "Family"}),
	"type": fields.integer({"name": "Type", "choices": choices.creatureTypes}),
	"can_repair": fields.integer({"name": "Can repair", "choices": choices.boolean})
// 	"locations": fields.foreignKey("zone", {"name": "Located in zone..."})
}

sigrieDefinitions.enchant = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"charges": fields.integer({"name": "Charges"}),
	"name": fields.string({"name": "Name", "maxLength": 64}),
	"gem": fields.foreignKey("item", {"name": "Gem"}),
	"required_level": fields.integer({"name": "Required level"}),
	"required_skill": fields.foreignKey("skill", {"name": "Required skill"}),
	"required_skill_level": fields.integer({"name": "Required skill level"})
}

sigrieDefinitions.faction = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"description": fields.string({"name": "Description"})
}

sigrieDefinitions.glyph = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 64}),
	"icon": fields.string({"name": "Icon", "maxLength": 64})
}

sigrieDefinitions.holiday = {
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"description": fields.string({"name": "Description"}),
	"icon": fields.string({"name": "Icon", "maxLength": 64})
}

sigrieDefinitions.instance = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 256})
}

sigrieDefinitions.item = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"category": fields.integer({"name": "Category", "choices": choices.itemCategories}),
	"subcategory": fields.integer({"name": "Subcategory"}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"icon": fields.string({"name": "Icon", "maxLength": 64}),
	"quality": fields.integer({"name": "Quality", "choices": choices.itemQualities}),
	"conjured": fields.integer({"name": "Conjured", "choices": choices.boolean, "default": 1}),
	"openable": fields.integer({"name": "Openable", "choices": choices.boolean, "default": 1}),
	"heroic": fields.integer({"name": "Heroic", "choices": choices.boolean, "default": 1}),
	"unique_equipped": fields.integer({"name": "Unique-Equipped", "choices": choices.boolean, "default": 1}),
	"group_loot": fields.integer({"name": "Group loot", "choices": choices.boolean, "default": 1}),
	"refundable": fields.integer({"name": "Refundable", "choices": choices.boolean, "default": 1}),
	"chart": fields.integer({"name": "Chart", "choices": choices.boolean, "default": 1}),
	"prospecting": fields.integer({"name": "Prospectable at level"}),
	"usable_in_arena": fields.integer({"name": "Usable in arenas", "choices": choices.boolean, "default": 1}),
	"milling": fields.integer({"name": "Millable at level"}),
	"buy_price": fields.integer({"name": "Sold for (copper)"}),
	"sell_price": fields.integer({"name": "Bought for (copper)"}),
	"slot": fields.integer({"name": "Slot", "choices": choices.slots}),
	"level": fields.integer({"name": "Level"}),
	"required_level": fields.integer({"name": "Required level"}),
	"required_skill": fields.foreignKey("skill", {"name": "Required skill"}),
	"required_skill_level": fields.integer({"name": "Required skill level"}),
	"required_spell": fields.foreignKey("spell", {"name": "Required spell"}),
	"required_faction": fields.foreignKey("faction", {"name": "Required faction"}),
	"unique": fields.integer({"name": "Unique count"}),
	"stack": fields.integer({"name": "Stack count"}),
	"bag_slots": fields.integer({"name": "Bag slots"}),
// 	"damage_min": fields.integer({"name": "Minimum damage"}),
// 	"damage_max": fields.integer({"name": "Maximum damage"}),
	"damage_type": fields.integer({"name": "Damage type", "choices": choices.schools}),
	"armor": fields.integer({"name": "Armor"}),
	"fire_resist": fields.integer({"name": "Fire resistance"}),
	"nature_resist": fields.integer({"name": "Nature resistance"}),
	"frost_resist": fields.integer({"name": "Frost resistance"}),
	"shadow_resist": fields.integer({"name": "Shadow resistance"}),
	"arcane_resist": fields.integer({"name": "Arcane resistance"}),
	"speed": fields.integer({"name": "Attack speed"}),
	"teaches_spell": fields.foreignKey("spell", {"name": "Teaches spell"}),
	"bind": fields.integer({"name": "Binding", "choices": choices.binds}),
	"note": fields.string({"name": "Note", "maxLength": 1024}),
	"starts_quest": fields.foreignKey("quest", {"name": "Starts quest"}),
	"lockpicking": fields.integer({"name": "Requires Lockpicking"}),
	"random_enchantment": fields.integer({"name": "Random properties", "choices": choices.boolean, "default": 1}),
	"block": fields.integer({"name": "Block"}),
	"itemset": fields.foreignKey("itemset", {"name": "Part of item set"}),
	"durability": fields.integer({"name": "Durability"}),
	"zone_bind": fields.foreignKey("zone", {"name": "Bound to zone"}),
	"instance_bind": fields.foreignKey("instance", {"name": "Bound to instance"}),
	"socket_bonus": fields.foreignKey("enchant", {"name": "Socket bonus"}),
	"gem_properties": fields.foreignKey("enchant", {"name": "Gem properties"}),
	"gem_color": fields.integer({"name": "Matches socket", "choices": choices.gemColors}),
	"disenchanting": fields.integer({"name": "Disenchantable at level"}),
	"bonus_armor": fields.integer({"name": "Bonus armor"}),
	"unique_category": fields.foreignKey("itemUniqueCategory", {"name": "Unique category"}),
	"required_holiday": fields.foreignKey("holiday", {"name": "Required holiday"})
}

sigrieDefinitions.itemUniqueCategory = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"amount": fields.integer({"name": "Amount"}),
	"equipped": fields.integer({"name": "Unique-Equipped", "choices": choices.boolean, "default": 1})
}

sigrieDefinitions.itemset = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"required_skill": fields.foreignKey("skill", {"name": "Required skill"}),
	"required_skill_level": fields.integer({"name": "Required skill level"})
}

sigrieDefinitions.object = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 64}),
	"type": fields.integer({"name": "Type"})
}

sigrieDefinitions.page = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 64}),
	"text": fields.string({"name": "Text"}),
	"next_page": fields.foreignKey("page", {"name": "Next page"})
}

sigrieDefinitions.quest = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"level": fields.integer({"name": "Level"}),
	"category": fields.integer({"name": "Category Id"}),
	"zone": fields.foreignKey("zone", {"name": "Zone"}),
	"type": fields.integer({"name": "Type", "choices": choices.questTypes}),
	"suggested_players": fields.integer({"name": "Suggested players"}),
	"followup": fields.foreignKey("quest", {"name": "Follow up"}),
	"required_money": fields.integer({"name": "Required money"}),
	"money_reward": fields.integer({"name": "Money reward"}),
	"money_reward_cap": fields.integer({"name": "Money reward at level 80"}),
	"spell_reward": fields.foreignKey("spell", {"name": "Rewards spell"}),
	"spell_trigger": fields.foreignKey("spell", {"name": "Triggers spell"}),
	"raid": fields.integer({"name": "Completable in raid", "choices": choices.boolean, "default": 1}),
	"daily": fields.integer({"name": "Daily", "choices": choices.boolean, "default": 1}),
	"flags_pvp": fields.integer({"name": "Flags PvP", "choices": choices.boolean, "default": 1}),
	"talents_reward": fields.integer({"name": "Talents rewarded"}),
	"name": fields.string({"name": "Name", "maxLength": 512}),
	"objective": fields.string({"name": "Objective"}),
	"description": fields.string({"name": "Description"}),
	"summary": fields.string({"name": "Summary"}),
	"quick_summary": fields.string({"name": "Quick summary"})
}

sigrieDefinitions.skill = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"name": fields.string({"name": "Name", "maxLength": 256}),
	"description": fields.string({"name": "Description"}),
	"is_tradeskill": fields.integer({"name": "Is a tradeskill", "choices": choices.boolean, "default": 1})
}

sigrieDefinitions.spell = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"dispel_type": fields.integer({"name": "Dispel Type", "choices": choices.dispelTypes}),
	"cast_time": fields.integer({"name": "Cast Time (seconds)"}),
	"power_cost_type": fields.integer({"name": "Power cost type"}),
	"power_cost_amount": fields.integer({"name": "Power cost amount"}),
	"min_range": fields.integer({"name": "Minimum range"}),
	"max_range": fields.integer({"name": "Maximum range"}),
	"max_stack": fields.integer({"name": "Maximum stack"}),
	"created_item": fields.foreignKey("item", {"name": "Creates Item"}),
	"icon": fields.string({"name": "Icon", "maxLength": 64}),
	"buff_icon": fields.string({"name": "Buff icon", "maxLength": 64}),
	"name": fields.string({"name": "Name", "maxLength": 512}),
	"rank": fields.string({"name": "Rank", "maxLength": 32}),
	"description": fields.string({"name": "Description"}),
	"buff_description": fields.string({"name": "Buff description"}),
	"power_percent": fields.integer({"name": "Power cost (%)"}),
	"max_target_level": fields.integer({"name": "Maximum target level"}),
	"runic_power_gain": fields.integer({"name": "Runic power gain"}),
	"primary_skill": fields.foreignKey("skill", {"name": "Skill Category"}),
	"passive": fields.integer({"name": "Passive", "choices": choices.boolean, "default": 1}),
	"not_usable_in_combat": fields.integer({"name": "Not usable in combat", "choices": choices.boolean, "default": 1}),
	"channeled": fields.integer({"name": "Channeled", "choices": choices.boolean, "default": 1})
}

sigrieDefinitions.zone = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"level": fields.integer({"name": "Level"}),
	"parent_area": fields.foreignKey("zone", {"name": "Parent area"}),
	"name": fields.string({"name": "Name", "maxLength": 128}),
	"pvp": fields.integer({"name": "Territory", "choices": choices.pvpZoneType})
}

sigrieDefinitions.talent = {
	"id": fields.integer({"name": "Id", "primaryKey": true}),
	"depends": fields.foreignKey("talent", {"name": "Depends on"})
}