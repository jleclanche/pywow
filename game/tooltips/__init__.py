"""
Tooltip generators
Usage:
 Item(12345).tooltip(game.tooltips.renderer)
=>
 game.tooltips.renderer(ItemTooltip(Item(12345)))
"""

from ..colors import *

def PlainTextRenderer(tooltip):
	"""
	A simple renderer that does not implement colors/sides
	"""
	ret = []
	for node in tooltip:
		ret.append(node.getText())

	return "\n".join(ret)

def TerminalRenderer(tooltip):
	"""
	A renderer that implements colors through termcolor.
	Meant for printing on terminals.
	"""
	from termcolor import colored
	colorMatch = {
		BLUE    : ("blue", None),
		CYAN    : ("cyan", None),
		DARKCYAN: ("cyan", "dark"),
		GOLD    : ("yellow", "dark"),
		GREEN   : ("green", None),
		GREY    : ("grey", None),
		ORANGE  : ("yellow", "dark"),
		PURPLE  : ("blue", "dark"),
		RED     : ("red", None),
		YELLOW  : ("yellow", None),
		WHITE   : ("white", None),
	}
	ret = []

	for idx, node in enumerate(tooltip):
		attributes = []
		if idx == 0:
			# First line is always larger; we can't control that so we make it bold
			attributes.append("bold")

		text = node.getText()
		color, attribute = colorMatch[node.getColor()]
		if attribute:
			attributes.append(attribute)

		text = colored(text, color, attrs=attributes)
		ret.append(text)

	return "\n".join(ret)
