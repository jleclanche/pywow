"""
game.items.sockets
 Socket class for items
"""

from .. import globalstrings

class Socket(object):
	SOCKET_META      = 1
	SOCKET_RED       = 2
	SOCKET_YELLOW    = 4
	SOCKET_BLUE      = 8
	SOCKET_HYDRAULIC = 16
	SOCKET_COGWHEEL  = 32
	
	strings = {
		SOCKET_META:      globalstrings.EMPTY_SOCKET_META,
		SOCKET_RED:       globalstrings.EMPTY_SOCKET_RED,
		SOCKET_YELLOW:    globalstrings.EMPTY_SOCKET_YELLOW,
		SOCKET_BLUE:      globalstrings.EMPTY_SOCKET_BLUE,
		SOCKET_HYDRAULIC: globalstrings.EMPTY_SOCKET_HYDRAULIC,
		SOCKET_COGWHEEL:  globalstrings.EMPTY_SOCKET_COGWHEEL,
	}
	
	def __init__(self, color):
		self.color = color
		self.text = self.strings[color]
	
	def getText(self):
		return self.text
