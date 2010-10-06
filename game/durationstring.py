# -*- coding: utf-8 -*-

from datetime import timedelta
from math import ceil

DEFAULT = {
	"second":  "second",
	"seconds": "seconds",
	"minute":  "minute",
	"minutes": "minutes",
	"hour":    "hour",
	"hours":   "hours",
	"day":     "day",
	"days":    "days",
}

SHORT = {
	"second":  "sec",
	"seconds": "sec",
	"minute":  "min",
	"minutes": "min",
	"hour":    "hour",
	"hours":   "hrs",
	"day":     "day",
	"days":    "days",
}

SHORTCAP = {
	"second":  "Sec",
	"seconds": "Sec",
	"minute":  "Min",
	"minutes": "Min",
	"hour":    "Hr",
	"hours":   "Hr",
	"day":     "Day",
	"days":    "Days",
}

def duration(value, locales=DEFAULT):
	if not isinstance(value, timedelta):
		value = timedelta(microseconds=max(0, value))
	
	if value == timedelta(seconds=1):
		return "1 %s" % (locales["second"])
	
	if value < timedelta(minutes=1):
		return "%.3g %s" % (value.seconds+float(value.microseconds) / 1000000, locales["seconds"])
	
	if value < timedelta(hours=1):
		return "%.3g %s" % (value.seconds / 60, value.seconds >= 120 and locales["minutes"] or locales["minute"])
	
	if value < timedelta(days=1):
		return "%d %s" % (ceil(value.seconds / 3600.0), value.seconds > 3600 and locales["hours"] or locales["hour"])
	
	return "%.3g %s" % (value.days, value.days > 1 and locales["days"] or locales["day"])
