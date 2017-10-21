"""
Enemy board:
Sylvanas

Your board:
Cult Master

Your turn.
Destroy Sylvanas.
-> Sylvanas dies.
-> Sylvanas steals CM.
-> Sylvanas does not draw.


Tracking at zero card does not increase fatigue counter.


20140817 trumpsc (arena vs Xpand):
- player1 plays haunted creeper
- player2 plays abom
- player1 plays abom (faceless on abom)
- player2 hits abom into abom
-> aboms both explode; kills haunted creeper, haunted creeper "dies" after both deathrattles have procced
"""



# At turn 10 by default in tests
def test_deathrattle_ordering_sylv(board):
	swdeath = board.player1.addToHand("Shadow Word: Death")
	sylvanas = board.player1.addToField("Sylvanas Windrunner")
	cultmaster = board.player2.addToField("Cult Master")
	board.player1.beginTurn()
	board.player1.playCard(swdeath, target=sylvanas)
	board.commit()

	# Check player2 did not draw any cards
	assert len(board.player2.cards) == 0


def test_tracking_zero_cards(board):
	tracking = board.player1.addToDeck("Tracking")
	board.player1.beginTurn()

	assert board.player1.hand == [tracking]
	board.player1.playCard(tracking)
	board.commit()

	assert board.player1.fatigueCounter == 0


