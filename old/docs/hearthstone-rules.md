[//]: # (md)
===========
Hearthstone
===========

Hearthstone is a card game. By Blizzard.


Basic mechanics
===============

Each player starts at maximum health. The game ends when there is only N(..1) hero still alive.
The winner is the player with the most heroes alive. The game is a draw if no hero is left alive.

Each player has a deck of N(30) sequenced cards. Additionally, each player starts with N(1) Hero
and N(1) Hero Power in their respective slots (see below).

At the beginning of the game, the first N(3) cards of the player's Deck are transferred to the
player's Hand. More details in the Beginning of Game section.
A randomly chosen player then starts a Turn.


Turn
----

A Turn is a time during which only one Player is able to perform Actions.
During their Turn, the Player is able to play any playable card currently in their Hand.

Each player is given N(90) seconds for their turn and may end the Turn at any time. If they have
not ended the Turn when the counter ends, the turn immediately ends. There is no time limit if it
has not been defined.

Each Card played during a Turn adds N(1) to a counter. The counter resets to N(0) whenever a Turn
starts.


Mana
----

Each player starts with N(0) Mana Crystals. Whenever the Player's Turn starts, the Player gains
N(1) Mana Crystal. Each player may have a total of up to N(10) Mana Crystals.

Each Card has a Cost. For the Card to be playable, the Player must have an amount of Active Mana
Crystals greater than or equal to the Card's Cost.
When a Card is played, N(n) of the player's Mana Crystals become inactive, where n is equal to the
Card's Cost.

Mana Crystals may be in Overload. See the Overload section for more details.


Board
-----

The Board is composed of N(1) Side per Player. Each Player is in Control of N(1) Side. Each Side is
composed of the following elements:

* Hero
* Hero Power
* Deck
* Hand
* Secrets
* Field

Each of those elements are Slots where a defined maximum amount of Cards can be held. Different
rules come into play when the Slot is full, these are defined in their respective sections.


Attack
------

Minions and Heroes with an Attack value of N(1) or greater are able to Attack any chosen Enemy
target, with defined restrictions.
An Attack reduces the targeted opponent's Health by an amount equal to the Attack of the Attacking
Player or Minion.
Whenever a Player or Minion attacks a Minion, the Attacking Player or Minion's Health is reduced by
an amount equal to the Attack of the targeted Minion.
Unless it has Summoning Sickness or is Unable to Attack, a Minion is able to Attack any chosen
target on another Side of the Board.

Special rules:
* Taunt: If there is at least one Minion with Taunt on the targeted enemy Side of the Board, all
enemy Minions and Heroes are unable to attack any target that does not have Taunt until there
remains no Taunt effect on the Board.
* Stealth: Any Minion that has Stealth is unable to be targeted by any Attack or Spell by any
Player.
* Chromatic: A Creature that has Chromatic is exempt from targeting by any Spells or Hero Powers.
* Immune: All Damage dealt to a Creature with Immune is negated.
* Divine Shield: All Damage dealt to a Creature with Divine Shield is negated. The Divine Shield
effect disappears when any damage is negated by the Creature.
* Charge: Any Minion with Charge ignores Summoning Sickness.
* Frozen: Any Frozen Creature is unable to Attack.
* Can't Attack: Any Minion that Can't Attack cannot Attack.
* Poisonous: If any Damage is dealt by an Attack by a Poisonous Creature to a Minion, the targeted
Minion dies.
* Windfury: Any Creature with Windfury is able to Attack N(2) times instead of N(1) time.


Health
------

Creatures all have N(n) Health. In addition to its Health, Damage on the Creature is tracked
through the Creature's Current Health. The Creature's Current Health may never exceed the
Creature's Health. Whenever the Current Health is reduced to N(0) or below, the Creature dies.


Card Draw
---------

A Card Draw moves N(1) Card from the top of a select Player's Deck to the top of the Player's Hand.
When there are N(0) Cards left in the Player's Deck, the Draw is replaced by a Fatigue effect. See
below for details.

Fatigue
----

At the Beginning of Game, each Player gets a Fatigue Counter set to N(0). Whenever a Fatigue effect
is triggered, the Counter increases by N(1) and the Player receives N(n) Damage, where n is equal
to the Fatigue Counter.

When the Fatigue Counter reaches N(20), the Game immediately ends in a Draw.


Card types
==========

Cards can be of the following types:

* Hero
* Hero Power
* Weapon
* Spell
* Minion

Each Card type is described below.


Minion
------

A Minion card can only be played on the Field. A Minion that is on the Field may be targeted by
Spells that target Minions as well as by other Minions and Heroes for Attack.
Minions have an Attack value, a Health value and a Current Health value. For more details on these,
see the Attack and Health sections.

When a Minion is first summoned, it gets Summoning Sickness. All Summoning Sickness is cleared when
the Turn ends. For details on how Minions Attack, see the Attack section.

Whenever a Minion is played, it triggers its Battlecry (if it has one). Similarly, whenever a
Minion dies, it triggers its Deathrattle (if it has one).
While a Minion is on the Field, it may affect the variables of the game in some defined way.


Spell
-----

A Spell is a type of Card which produces a defined Action through a scripted effect. Some Spells
have a Target.


Secret
------

A Secret is a special type of Spell card which is hidden from anyone who is not the Player. When a
Secret is played, other Players are notified that the Player has played a Secret.
Secrets are the equivalent of face-down Cards. They trigger upon a defined Event and may intercept
the performed Action. When triggered, Secrets perform their Action and are Destroyed.


Weapon
------

A Weapon is a card that, when played, is equipped into the Weapon slot. If a Weapon is already
equipped, the equipped Weapon is Destroyed.
During their Owner's turn, equipped Weapons increase the Hero's Attack value by N(n) where n is
equal to the Weapon's Attack value. During the Opponent's turn, equipped Weapons are Sheathed and
do not increase Attack value.

Weapons, like Creatures, have a defined amount of Health (known as Durability for Weapons). They
also have a Current Health which is decreased by N(1) every time the Hero Attacks while the Weapon
is in the Weapon slot. When the Weapon's Current Health reaches N(0), the Weapon is Destroyed.

Whenever a Weapon is played, it triggers its Battlecry (if it has one).
Whenever a Weapon is Destroyed, it triggers its Deathrattle (if it has one).


Hero
----

The Hero card determines the character the player is represented by.
Only Hero type cards can go in this slot. The Hero retains the following attributes:

* Max health
* Current health
* Attack
* Attack counter
* Armor

Armor is a Hero-specific attribute. Whenever damage is dealt to the hero, the armor is reduced
before the health.

A Hero may bear a Weapon. All Attack from the currently-worn Weapon is added to the Hero's Attack.
Other Weapon attributes are defined in the Weapon section.

All other attributes are defined in the Minion section.


Hero Power
----------

The Hero Power slot can only contain Hero Power cards. This card is determined at the beginning
of the game by the Hero the player is playing as.
Each Hero card defines which Hero Power Card it comes with.

There are two kind of Hero Power cards: Active and Passive.

Active Hero Power cards are activated on the Player's Turn. When they are activated, they can no
longer be activated until the next Player's Turn.
If the Hero Power card is replaced, its activation status is reset and it can once again be
activated during the Turn.

Active Hero Powers trigger a scripted Action. They may have a Target and behave like Spells
regarding Targeting.

Passive Hero Power cards cannot be activated. Instead, they provide a permanent Buff.


Mechanics
=========

Buffs
-----

Select Actions may create a Buff on a Minion. The Buff may change the Health or Attack amounts,
add Mechanics to the Minion, or apply a running scripted Action on the Minion.


Battlecry
---------

Minions and Weapons may have a Battlecry capability. A Battlecry is an Action which happens
immediately after a Minion is Summoned on the Field iff it has been played directly from the
Owner's Hand. The Battlecry happens *before* the Summon Event is sent.


Deathrattle
-----------

Minions and Weapons may have a Deathrattle capability. A Deathrattle is an Action which happens
immediately after the Card is Destroyed while it is on the Field.


Silence
-------

Silence is a Mechanic which can be applied on a Minion on the Field. When Active, Silence changes
the Card by removing all active Buffs and Mechanics from the Minion.


Overload
--------

Overload is a Mechanic which triggers when the Card is played. At the Beginning of Turn, N(n) of
the Player's Mana Crystals are placed in Overload where n is the Overload Counter. The Overload
Counter is then reset to N(0).
Whenever a Card with Overload is played, the Overload Counter increases by N(n) where n is the
Overload of the Card.


Bounce
------

Bounce is a Mechanic which can be applied on a Minion on the Field. When Activated, the targeted
Minion is returned to its current Owner's hand. The Card may be modified in some way, such as in
Mana cost, by other Effects.
Iff the Owner's hand is Full, instead of being returned, the Minion will be Destroyed. See
Mechanics -> Destroy for more information.


Choose One
----------

When a Choose One Card is played, a set of Cards defined by the Card is suggested to the Player.
The Player chooses one of the Cards. The original Card is played and the Action or the Minion of
the original Card is replaced by the one of the chosen Card.


Summon
------

A Summon creates a Minion on the Owner's side of the Field. Immediately after the Summon, iff
the Minion has a Battlecry and iff the Minion has been played directly from the Owner's Hand, the
Battlecry is then triggered.
This is then followed by a Summon Event.


Destroy
-------

A Destroy will remove a Character from the board.
This is followed by a Death event. Iff the Character in question has an active (non-Silenced)
Deathrattle, the Deathrattle is then triggered.


Actions and Resolutions
=======================

Whenever any type of Action is performed, a Stack is opened. The stack controls the order upon
which simulations are resolved.


Attack
------

An Attack is an Action which Characters can perform while it is the Owner's Turn.
See Basic Mechanics -> Attack for more information.




