# -*- coding: utf-8 -*-
"""
Game module
Contains model logic for the game
"""

from .colors import *


class Model(object):
	"""
	Base Model class for all the game models:
	Items, Spells, Quests, Talents, ...
	"""

	class DoesNotExist(Exception):
		pass

	@classmethod
	def initProxy(cls, proxy):
		cls.proxy = proxy(cls)

	def __init__(self, id, build=-1, locale="enUS"):
		if not hasattr(self, "proxy"):
			raise RuntimeError("%s.proxy needs to be initialized with initProxy(proxy)" % (self.__class__.__name__))
		self.id = id
		self.proxy.build = build
		self.proxy.locale = locale
		try:
			self.obj = self.proxy.get(id)
		except KeyError:
			raise self.DoesNotExist(id)

	def __getattr__(self, attr):
		if attr != "obj" and hasattr(self.obj, attr):
			return getattr(self.obj, attr)

		if attr != "proxy" and hasattr(self.proxy, attr):
			func = getattr(self.proxy, attr)
			return lambda: func(self.obj)

		return super(Model, self).__getattribute__(attr)

	def __repr__(self):
		return "%s(%i)" % (self.__class__.__name__, self.id)

	def __str__(self):
		if hasattr(self, "getName"):
			return self.getName()
		return self.__repr__()

	def tooltip(self, renderer):
		return self.Tooltip(self).render(renderer)

class Tooltip(object):
	def __init__(self, obj):
		self.obj = obj
		self.values = []

	def append(self, name, text, color=WHITE, side=LEFT):
		if text:
			node = TooltipNode(name, text, color, side)
			if side == RIGHT:
				previousLine = self.values[-1]
				if len(previousLine) < 2:
					previousLine.append(node)
			else:
				self.values.append([node])

	def appendEmptyLine(self):
		self.values.append([TooltipNode("__separator", "", WHITE, 0)])

	def flush(self):
		ret = self.values
		self.values = []
		return ret

	def formatAppend(self, name, text, value, color=WHITE):
		if value:
			self.append(name, text % (value), color)

	def render(self, renderer):
		return renderer(self.tooltip())

class TooltipNode(object):
	LEFT = LEFT
	RIGHT = RIGHT

	def __init__(self, name, content, color, side):
		self.name = name
		if isinstance(content, Tooltip):
			self._tooltip = content
		else:
			self._text = content
			self._color = color
			self._side = side

	def __repr__(self):
		return repr(self.getText())

	def __str__(self):
		return self.getText()

	def color(self):
		if self.isTooltip():
			return 0
		return self._color

	def isEmpty(self):
		return self.name == "__separator"

	def isTooltip(self):
		return hasattr(self, "_tooltip")

	def side(self):
		if self.isTooltip():
			return self.LEFT
		return self._side

	def text(self):
		if self.isTooltip():
			return ""
		return str(self._text)

	def tooltip(self):
		return self._tooltip
