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
		self.appendEmptyLine()

		self.append("objective", self.obj.getObjective())
		self.appendEmptyLine()

		return self.flush()
Quest.Tooltip = QuestTooltip

class QuestProxy(object):
	"""
	WDBC proxy for quests
	"""
	def __init__(self, cls):
		from pywow import wdbc
		self.__file = wdbc.get("questcache.wdb", build=-1)

	def get(self, id):
		return self.__file[id]

	def getCompleteSummary(self, row):
		return row.complete_summary

	def getDescription(self, row):
		return row.description.replace("$B", "\n")

	def getName(self, row):
		return row.name

	def getObjective(self, row):
		return row.objective

	def getSummary(self, row):
		return row.summary

Quest.initProxy(QuestProxy)
