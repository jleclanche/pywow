# -*- coding: utf-8 -*-
"""
Base logging for wdbc, all messages redirecting to stdout by default
"""

import logging
import sys

LOG_CONFIG = {
	"stream": sys.stdout,
	"format": "%(levelname)s: %(message)s"
}

class LazyLogger(object):
	log = None
	
	@classmethod
	def get_logger(cls):
		if not cls.log:
			logging.basicConfig(**LOG_CONFIG)
			cls.log = logging.getLogger("wdbc")
			cls.log.setLevel(logging.WARN)
		return cls.log

log = LazyLogger.get_logger()
