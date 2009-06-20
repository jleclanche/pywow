#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Common hardcoded database values"""

STATS = {
	 1: { "name": 'Health', "text": '%+i Health', "special": False },
	 2: { "name": 'Mana', "text": '%+i Mana', "special": False },
	 3: { "name": 'Agility', "text": '%+i Agility', "special": False },
	 4: { "name": 'Strength', "text": '%+i Strength', "special": False },
	 5: { "name": 'Intellect', "text": '%+i Intellect', "special": False },
	 6: { "name": 'Spirit', "text": '%+i Spirit', "special": False },
	 7: { "name": 'Stamina', "text": '%+i Stamina', "special": False },
	12: { "name": 'Defense Rating', "text": 'Equip: Increases defense rating by %i.', "special": True },
	13: { "name": 'Dodge Rating', "text": 'Equip: Increases your dodge rating by %i.', "special": True },
	14: { "name": 'Parry Rating', "text": 'Equip: Increases your parry rating by %i.', "special": True },
	15: { "name": 'Shield Block Rating', "text": 'Equip: Increases your shield block rating by %i.', "special": True },
	16: { "name": 'Melee Hit Rating', "text": 'Equip: Improves melee hit rating by %i.', "special": True },
	17: { "name": 'Ranged Hit Rating', "text": 'Equip: Improves ranged hit rating by %i.', "special": True }, # TODO check text
	18: { "name": 'Spell Hit Rating', "text": 'Equip: Improves spell hit rating by %i.', "special": True },
	19: { "name": 'Melee Critical Strike Rating', "text": 'Equip: Improves melee critical strike rating by %i.', "special": True }, # TODO check text
	20: { "name": 'Ranged Critical Strike Rating', "text": 'Equip: Improves ranged critical strike rating by %i.', "special": True },
	21: { "name": 'Spell Critical Strike Rating', "text": 'Equip: Improves spell critical strike rating by %i.', "special": True },
	22: { "name": 'Melee Hit Avoidance Rating', "text": 'Equip: Improves melee hit avoidance rating by %i.', "special": True },
	23: { "name": 'Ranged Hit Avoidance Rating', "text": 'Equip: Improves ranged hit avoidance rating by %i.', "special": True },
	24: { "name": 'Spell Hit Avoidance Rating', "text": 'Equip: Improves spell hit avoidance rating by %i.', "special": True },
	25: { "name": 'Melee Crit Avoidance Rating', "text": 'Equip: Improves melee critical avoidance rating by %i.', "special": True },
	26: { "name": 'Ranged Crit Avoidance Rating', "text": 'Equip: Improves ranged critical avoidance rating by %i.', "special": True },
	27: { "name": 'Spell Crit Avoidance Rating', "text": 'Equip: Improves spell critical avoidance rating by %i.', "special": True },
	28: { "name": 'Melee Haste Rating', "text": 'Equip: Improves melee haste rating by %i.', "special": True },
	29: { "name": 'Ranged Haste Rating', "text": 'Equip: Improves haste rating by %i.', "special": True }, # TODO check text
	30: { "name": 'Haste Rating', "text": 'Equip: Improves haste rating by %i.', "special": True },
	31: { "name": 'Hit Rating', "text": 'Equip: Improves hit rating by %i.', "special": True },
	32: { "name": 'Critical Strike Rating', "text": 'Equip: Improves critical strike rating by %i.', "special": True },
	33: { "name": 'Hit Avoidance Rating', "text": 'Equip: Improves hit avoidance rating by %i.', "special": True },
	34: { "name": 'Crit Avoidance Rating', "text": 'Equip: Improves critical avoidance rating by %i.', "special": True },
	35: { "name": 'Resilience Rating', "text": 'Equip: Improves your resilience rating by %i.', "special": True },
	36: { "name": 'Haste Rating', "text": 'Equip: Improves haste rating by %i.', "special": True },
	37: { "name": 'Expertise Rating', "text": 'Equip: Increases your expertise rating by %i.', "special": True },
	38: { "name": 'Attack Power', "text": 'Equip: Increases attack power by %i.', "special": True },
	39: { "name": 'Ranged Attack Power', "text": 'Equip: Increases ranged attack power by %i.', "special": True }, # TODO check text
	40: { "name": 'Feral Attack Power', "text": 'Increases attack power by %i in Cat, Bear, Dire Bear, and Moonkin forms only.', "special": True }, # Druid Only
	41: { "name": 'Spell Damage and Healing', "text": 'Equip: Increases healing done by magical spells and effects by up to %i.', "special": True }, # OLD
	42: { "name": 'Spell Damage', "text": 'Equip: Increases damage done by magical spells and effects by up to %i.', "special": True }, # OLD
	43: { "name": 'Mana Per 5', "text": 'Equip: Restores %i mana per 5 sec.', "special": True },
	44: { "name": 'Armor Penetration Rating', "text": 'Equip: Increases your armor penetration rating by %i.', "special": True },
	45: { "name": 'Spell Power', "text": 'Equip: Increases spell power by %i.', "special": True },
}