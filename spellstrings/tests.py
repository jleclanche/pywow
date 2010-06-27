#!/usr/bin/python
# -*- coding: utf-8 -*-

BUILD = 12266
TESTS = {}

TESTS[11723] = {
	 1010: "Curse the target with idiocy, reducing Intellect and Spirit by 6 every 3 seconds until each is reduced by a total of 90.  Only one Curse per Warlock can be active on any one target.",
	 2687: "Generates 20 rage at the cost of health, and then generates an additional 10 rage over 10 sec.",
	 8024: "Imbue the Shaman's weapon with fire, increasing total spell damage by 7. Each hit causes 4.2 to 13.0 additional Fire damage, based on the speed of the weapon.  Slower weapons cause more fire damage per swing.  Lasts 30 minutes.",
	10390: "Causes an explosion of arcane magic around the caster, causing 0 damage to all targets within 0 yards.",
	11213: "Gives you a 2% chance of entering a Clearcasting state after any damage spell hits a target.  The Clearcasting state reduces the mana cost of your next damage spell by 100%.",
	14253: "Attempts to cure 1 poison effect on the target, and 1 more poison effect every 2 seconds for 8 sec.",
	16190: "Summons a Mana Tide Totem with 10% of the caster's health at the feet of the caster for 12 sec that restores 6% of total mana every 3 seconds to group members within 30 yards.",
	21228: "Increases the duration of your Arcane Missiles by 1 sec.",
	23025: "Reduces the cooldown of your Blink spell by 2 sec.",
	29907: "Hits an enemy with an anti-mana bolt that consumes up to 255 to 295 mana. For each point of mana consumed by the bolt, the target takes 1.0 damage.",
	29977: "When activated, this spell causes each of your Fire damage spell hits to increase your critical strike chance with Fire damage spells by 10%.  This effect lasts until you have caused 3 critical strikes with Fire spells.",
	31687: "Summon a Water Elemental to fight for the caster for 45 sec.",
	33127: "Gives the Paladin a chance to deal additional Holy damage equal to 36% of normal weapon damage.  Only one Seal can be active on the Paladin at any one time.  Lasts 30 sec.\r\n\r\nUnleashing this Seal's energy will judge an enemy, instantly causing $s1 Holy damage, $s1 if the target is stunned or incapacitated.",
	36459: "Summon a Water Elemental to fight for the caster for until cancelled.",
	36950: "Causes up to 5 nearby enemies to flee for 6 sec.",
	37360: "Imbue your weapon with power, increasing attack power against undead and demons by 150.  Lasts 5 min.  Cannot be used on items level 138 and higher.",
	39758: "Soothes the target, reducing the range at which it will attack you by 1000 yards.  Only affects Humanoid targets level 200 or lower.  Lasts 1 hour.",
	39794: "Brings a dead player back to life with 1 health and 0 mana.  Cannot be cast when in combat.",
	47471: "Attempt to finish off a wounded foe, causing [1456+AP*0.2] damage and converting each extra point of rage into 38 additional damage (up to a maximum cost of 30 rage).  Only usable on enemies that have less than 20% health.",
	48677: "Throw burning oil at your pursuers slowing them down and inflicting 21336 to 42664 Fire damage over 8 sec.",
	49628: "Your auto attacks have a 30% chance to cause a Blood-Caked Strike, which hits for 25% weapon damage plus 12.5% for each of your diseases on the target.",
	53717: "Cause a corpse to explode for 60 Nature damage modified by attack power to all enemies within 20 yards.  Will use a nearby corpse if none is targeted.  Does not affect mechanical or elemental corpses.",
	57861: "Lets loose a roar, Increaseing damage taken by 20% for $.",
	58425: "Your finishing moves have a 20% chance per combo point to restore 25 energy.",
	58644: "Reduces the cost of your Frost Strike by -5864.",
	58645: "Restores 18480 health and 12840 mana over 30 sec.  Must remain seated while eating.",
	61905: "Summons a Magma Totem with 5000 health at the feet of the caster for -1 sec that causes 371 Fire damage to creatures within 8 yards every 2 seconds.",
	64936: "Shield Block also grants you $s1% reduction to magical damage taken.",
	66188: "A deadly attack that deals 150% offhand weapon damage plus a bonus and heals the Death Knight for 5.0% of <his/her> maximum health for each of <his/her> diseases on the target.",
	69561: "Restores 19200 mana over 30 sec.  Must remain seated while drinking.  If you spend at least 10 seconds drinking you will become \"well fed\" and gain 40 critical strike rating for 1 hour. Standard alcohol.",
	71180: "Reduces the cast time of your next Frostbolt or Frostfire Bolt by $/1000S1 sec.  Lasts 10 sec.",
	72930: "Chills a random target, reducing movement speed by 50% and dealing significant Frost damage after 14 sec.",
	75878: "Deals 75000 to 85000 Fire damage to enemies within 0 yards and spawns a Living Inferno.",
}

_ = TESTS[12266] = TESTS[11723].copy()
del _[1010], _[37360], _[47471], _[57861], _[75878]
_[14253] = "Attempts to cure 1 poison effect on the target, and $s1 more poison effect every 2 seconds for 8 sec."
_[15349] = "Increases your critical healing effect chance by 2% for each harmful damage-over-time effect on your target up to 2 effects or -20% increased critical healing effect chance."
_[16190] = "Summons a Mana Tide Totem with 10% of the caster's health at the feet of the caster for 12 sec that restores 6% of total mana every 3 seconds to group members within 10 yards." # scaling
_[61905] = "Summons a Magma Totem with 5000 health at the feet of the caster for -1 sec that causes $s1 Fire damage to creatures within $a1 yards every $t1 seconds."
_[78273] = "Imbue the Shaman's weapon with fire, increasing total spell damage by 7. Each hit causes $/78275m1 to 1 additional Fire damage. Lasts 30 minutes."

def main():
	from pywow.wdbc.environment import Environment
	from pywow.spellstrings import SpellString, WDBCProxy
	
	f = Environment(BUILD)["Spell.dbc"]
	
	fail, success = 0, 0
	for id, expected in sorted(TESTS[BUILD].items()):
		print "Testing %i..." % (id),
		if id not in f:
			print "PASS"
			continue
		
		spell = f[id]
		description = SpellString(spell.description_enus).format(spell, proxy=WDBCProxy)
		
		if description != expected:
			print "FAIL"
			print "Returned:", repr(description)
			print "Expected:", repr(expected)
			print "Original:", repr(spell.description_enus)
			fail += 1
		else:
			print "OK"
			success += 1
	
	print "%i/%i tests passed, %i failure" % (success, fail+success, fail)

if __name__ == "__main__":
	main()
