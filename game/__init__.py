# -*- coding: utf-8 -*-
"""
Game module
Contains model logic for the game
"""

# Colors
BLUE     = 0x0080ff
CYAN     = 0x66bbff
DARKCYAN = 0x88aaff
GOLD     = 0xe5cc80
GREEN    = 0x1eff00
GREY     = 0x9d9d9d
ORANGE   = 0xff8000
PURPLE   = 0xb048f8
RED      = 0xff2020
YELLOW   = 0xffd100
WHITE    = 0xffffff

class Model(object):
	"""
	Base Model class for all the game models:
	Items, Spells, Quests, Talents, ...
	"""
	
	@classmethod
	def initProxy(cls, proxy):
		cls.proxy = proxy(cls)
	
	def __init__(self, id):
		if not hasattr(self, "proxy"):
			raise RuntimeError("%s.proxy needs to be initialized with initProxy(proxy)" % (self.__class__.__name__))
		self.id = id
		self.obj = self.proxy.get(id)
		#if not self.obj:
			#self = None
	
	def __getattr__(self, attr):
		if attr != "obj" and hasattr(self.obj, attr):
			return getattr(self.obj, attr)
		
		if attr != "proxy" and hasattr(self.proxy, attr):
			func = getattr(self.proxy, attr)
			return lambda: func(self.obj)
		
		return super(Model, self).__getattribute__(attr)
	
	def __repr__(self):
		if hasattr(self, "name"):
			return "<%s #%i: %s>" % (self.__class__.__name__, self.id, self.name)
		return "<%s #%i>" % (self.__class__.__name__, self.id)

class Tooltip(object):
	LEFT = 0
	RIGHT = 1
	def __init__(self, obj):
		self.obj = obj
		self.keys = []
		self.values = []
	
	def append(self, name, text, color=WHITE, side=LEFT):
		if text:
			self.keys.append(name)
			self.values.append(TooltipNode(name, text, color, side))
	
	def formatAppend(self, name, text, value, color=WHITE):
		if value:
			self.append(name, text % (value), color)
	
	def render(self, renderer):
		return renderer(self.tooltip())

class TooltipNode(object):
	def __init__(self, name, content, color, side):
		self.name = name
		if isinstance(content, Tooltip):
			self.tooltip = content
		else:
			self.text = content
			self.color = color
			self.side = side
	
	def __repr__(self):
		return repr(self.getText())
	
	def __str__(self):
		return self.getText()
	
	def getColor(self):
		if self.isTooltip():
			return 0
		return self.color
	
	def getText(self):
		if self.isTooltip():
			return ""
		return str(self.text)
	
	def isTooltip(self):
		return hasattr(self, "tooltip")
