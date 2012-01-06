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
		ret.append(node.text())

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

		text = node.text()
		color, attribute = colorMatch[node.color()]
		if attribute:
			attributes.append(attribute)

		text = colored(text, color, attrs=attributes)
		ret.append(text)

	return "\n".join(ret)

def HtmlRenderer(tooltip):
	"""
	A renderer that implements all tooltip features
	in html.
	"""
	ret = []
	USE_STYLE = True

	lineTpl = '<div style="%s">%s</div>'
	sideTpl = '<span style="%s">%s</span>'

	for idx, line in enumerate(tooltip):
		lineHtml = []
		lineStyle = []
		if idx == 0:
			lineStyle.append("font-size: 110%;")

		for side in line:
			style = ["color: #%06x;" % (side.color())]

			if side.side() == side.RIGHT:
				style.append("float: right;")

			lineHtml.append(sideTpl % (" ".join(style), side.text()))

		text = lineTpl % (" ".join(lineStyle), " ".join(lineHtml))
		ret.append(text)

	return "\n".join(ret)
