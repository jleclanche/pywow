CREATURE_TYPES = {
	0: "",
	1: "Elite",
	2: "Rare-Elite",
	3: "Boss",
	4: "Rare",
	5: ""
}

CREATURE_CATEGORIES = {
	 0: "Not Specified",
	 1: "Beast",
	 2: "Dragonkin",
	 3: "Demon",
	 4: "Elemental",
	 5: "Giant",
	 6: "Undead",
	 7: "Humanoid",
	 8: "Critter",
	 9: "Mechanical",
	10: "",
	11: "Totem",
	12: "Non-combat Pet",
	13: "Gas Cloud"
}

CREATURE_FAMILIES = {
	 0: "",
	 1: "Wolf",
	 2: "Cat",
	 3: "Spider",
	 4: "Bear",
	 5: "Boar",
	 6: "Crocolisk",
	 7: "Carrion Bird",
	 8: "Crab",
	 9: "Gorilla",
	10: "Stag",
	11: "Raptor",
	12: "Tallstrider",
	20: "Scorpid",
	21: "Turtle",
	24: "Bat",
	25: "Hyena",
	26: "Bird of Prey",
	27: "Wind Serpent",
	30: "Dragonhawk",
	31: "Ravager",
	32: "Warp Stalker",
	33: "Sporebat",
	34: "Nether Ray",
	35: "Serpent",
	37: "Moth",
	38: "Chimaera",
	39: "Devilsaur",
	41: "Silithid",
	42: "Worm",
	43: "Rhino",
	44: "Wasp",
	45: "Core Hound",
	46: "Spirit Beast"
}

DISPEL_TYPES = {
	0: "",
	1: "Magic",
	2: "Curse",
	3: "Disease",
	4: "Poison",
	5: "Stealth",
	6: "Invisibility",
	9: "Enrage"
}

FACTIONS = {
	0: "Both",
	1: "Horde",
	2: "Alliance"
}

POWER_TYPES = { // Negative values from PowerDisplay.dbc
// 	-142: "Wrath", // POWER_TYPE_WRATH
// 	-141: "Blood Power", // POWER_TYPE_BLOOD_POWER
// 	-121: "Ooze", // POWER_TYPE_OOZE
// 	-101: "Heat", // POWER_TYPE_HEAT
// 	 -61: "Steam Pressure", // POWER_TYPE_STEAM
// 	 -41: "Pyrite", // POWER_TYPE_PYRITE
// 	  -2: "Health",
// 	  -1: "Ammo", // AMMOSLOT
	   0: "Mana",
	   1: "Rage",
	   2: "Focus",
	   3: "Energy",
	   4: "Consumable",
	   5: "Runes",
	   6: "Runic Power"
}

ZONE_PVP_TYPES = {
	0: "Contested",
	2: "Alliance",
	4: "Horde",
	6: "Sanctuary"
}

SLOTS = {
	 0: "",
	 1: "Head",
	 2: "Neck",
	 3: "Shoulder",
	 4: "Shirt",
	 5: "Chest",
	 6: "Waist",
	 7: "Legs",
	 8: "Feet",
	 9: "Wrist",
	10: "Hands",
	11: "Finger",
	12: "Trinket",
	13: "One-Hand",
	14: "Shield",
	15: "Ranged",
	16: "Back",
	17: "Two-Hand",
	18: "Bag",
	19: "Tabard",
	20: "Chest",
	21: "Main Hand",
	22: "Off-Hand",
	23: "Held In Off-hand",
	24: "Projectile",
	25: "Thrown",
	26: "Ranged",
	28: "Relic"
}

SKILL_CATEGORIES = {
	 0: "",
	 5: "Attributes",
	 6: "Weapon Skills",
	 7: "Class Skills",
	 8: "Armor Proficiencies",
	 9: "Secondary Skills",
	10: "Languages",
	11: "Professions",
	12: "Not Displayed"
}

ITEM_SUBCLASSES = {
        0: {0: 'Consumable', 1: 'Potion', 2: 'Elixir', 3: 'Flask', 4: 'Scroll', 5: 'Food & Drink', 6: 'Item Enhancement', 7: 'Bandage', 8: 'Other'},
        1: {0: 'Bag', 1: 'Soul Bag', 2: 'Herb Bag', 3: 'Enchanting Bag', 4: 'Engineering Bag', 5: 'Gem Bag', 6: 'Mining Bag', 7: 'Leatherworking Bag', 8: 'Inscription Bag'},
        2: {0: 'Axe', 1: 'Axe', 2: 'Bow', 3: 'Gun', 4: 'Mace', 5: 'Mace', 6: 'Polearm', 7: 'Sword', 8: 'Sword', 9: 'Obsolete', 10: 'Staff', 11: 'Exotic', 12: 'Exotic', 13: 'Fist Weapon', 14: 'Miscellaneous', 15: 'Dagger', 16: 'Thrown', 17: 'Spear', 18: 'Crossbow', 19: 'Wand', 20: 'Fishing Pole'},
        3: {0: 'Red', 1: 'Blue', 2: 'Yellow', 3: 'Purple', 4: 'Green', 5: 'Orange', 6: 'Meta', 7: 'Simple', 8: 'Prismatic'},
        4: {0: 'Miscellaneous', 1: 'Cloth', 2: 'Leather', 3: 'Mail', 4: 'Plate', 5: 'Buckler(OBSOLETE)', 6: 'Shield', 7: 'Libram', 8: 'Idol', 9: 'Totem', 10: 'Sigil'},
        5: {0: 'Reagent'},
        6: {0: 'Wand(OBSOLETE)', 1: 'Bolt(OBSOLETE)', 2: 'Arrow', 3: 'Bullet', 4: 'Thrown(OBSOLETE)'},
        7: {0: 'Trade Goods', 1: 'Parts', 2: 'Explosives', 3: 'Devices', 4: 'Jewelcrafting', 5: 'Cloth', 6: 'Leather', 7: 'Metal & Stone', 8: 'Meat', 9: 'Herb', 10: 'Elemental', 11: 'Other', 12: 'Enchanting', 13: 'Materials', 14: 'Armor Enchantment', 15: 'Weapon Enchantment'},
        8: {0: 'Generic(OBSOLETE)'},
        9: {0: 'Book', 1: 'Leatherworking', 2: 'Tailoring', 3: 'Engineering', 4: 'Blacksmithing', 5: 'Cooking', 6: 'Alchemy', 7: 'First Aid', 8: 'Enchanting', 9: 'Fishing', 10: 'Jewelcrafting', 11: 'Inscription'},
        10: {0: 'Currency', 7: 'Unknown'},
        11: {0: 'Quiver(OBSOLETE)', 1: 'Quiver(OBSOLETE)', 2: 'Quiver', 3: 'Ammo Pouch'},
        12: {0: 'Quest', 8: 'Unknown', 3: 'Unknown'},
        13: {0: 'Key', 1: 'Lockpick'},
        14: {0: 'Permanent'},
        15: {0: 'Junk', 1: 'Reagent', 2: 'Pet', 3: 'Holiday', 4: 'Other', 5: 'Mount', 12: 'Unknown'},
        16: {1: 'Warrior', 2: 'Paladin', 3: 'Hunter', 4: 'Rogue', 5: 'Priest', 6: 'Death Knight', 7: 'Shaman', 8: 'Mage', 9: 'Warlock', 11: 'Druid'}
}
