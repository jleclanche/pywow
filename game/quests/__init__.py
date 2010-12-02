# -*- coding: utf-8 -*-
"""
Quests
 - questcache.wdb
"""

from .. import *


class Quest(Model):
	def getTooltip(self):
		return QuestTooltip(self)

class QuestTooltip(Tooltip):
	def tooltip(self):
		
		self.append("name", self.obj.getName(), color=YELLOW)
		
		ret = self.values
		self.values = []
		return ret

class QuestProxy(object):
	"""
	WDBC proxy for quests
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("questcache.wdb", build=-1)
	
	def get(self, id):
		return self.__file[id]
	
	def getName(self, row):
		return row.name

Quest.initProxy(QuestProxy)
