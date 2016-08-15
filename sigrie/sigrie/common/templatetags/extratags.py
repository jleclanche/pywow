import re
from datetime import timedelta
from django import template
from django.utils import html, safestring
from django.template.defaultfilters import stringfilter
from math import ceil

register = template.Library()


@register.simple_tag
def sitenav():
	return """<ul id="sitenav">
	<li><a href="/" rel="sigrie" class="">Database</a></li>
	<li>&raquo; <a href="/items" rel="items">Items</a></li>
	<li>&raquo; <a href="/items/9" rel="items_9" class="">Recipe</a></li>
	<li>&raquo; <a href="/items/9/2" rel="items_9_2">Tailoring</a></li>
</ul>
"""





def esc(text, autoescape):
	if autoescape:
		return html.conditional_escape(text)
	return text


@register.filter
def colorinline(value, autoescape=None):
	pattern = r"\|c([0-9a-f]{8})(.+)\|r"
	sre = re.search(pattern, value, re.IGNORECASE)
	if not sre:
		return value
	color, text = sre.groups()
	output = '<span style="color:#%s;">%s</span>' % (color[2:], esc(text, autoescape))
	output = "".join([value[:sre.start()], output, value[sre.end():]])
	return safestring.mark_safe(output)
colorinline.needs_autoescape = True

@register.filter
def genderinline(value, autoescape=None):
	if not value.find("$"):
		return value
	pattern = r"\$(G|g)\s?([^:]+):([^;]+);"
	sre = re.search(pattern, value)
	if not sre:
		return value
	char, male, female = sre.groups()
	output = '&lt;%s/%s&gt;' % (esc(male.strip(), autoescape), esc(female.strip(), autoescape))
	output = "".join([esc(value[:sre.start()], autoescape), output, esc(value[sre.end():], autoescape)])
	return safestring.mark_safe(output)
genderinline.needs_autoescape = True


DURATIONS_DEFAULT = {
	"second":  "second",
	"seconds": "seconds",
	"minute":  "minute",
	"minutes": "minutes",
	"hour":    "hour",
	"hours":   "hours",
	"day":     "day",
	"days":    "days",
}
DURATIONS_SHORT = {
	"second":  "sec",
	"seconds": "sec",
	"minute":  "min",
	"minutes": "min",
	"hour":    "hour",
	"hours":   "hrs",
	"day":     "day",
	"days":    "days",
}

DURATIONS_SHORTCAP = {
	"second":  "Sec",
	"seconds": "Sec",
	"minute":  "Min",
	"minutes": "Min",
	"hour":    "Hr",
	"hours":   "Hr",
	"day":     "Day",
	"days":    "Days",
}

@register.filter
def duration(value, locales=DURATIONS_DEFAULT):
	if not isinstance(value, timedelta):
		if value < 0: value = 0
		value = timedelta(microseconds=value)
	if value == timedelta(seconds=1):
		return "1 %s" % (locales["second"])
	elif value < timedelta(minutes=1):
		return "%.3g %s" % (value.seconds+float(value.microseconds)/1000000, locales["seconds"])
	elif value < timedelta(hours=1):
		return "%.3g %s" % (value.seconds / 60, value.seconds >= 120 and locales["minutes"] or locales["minute"])
	elif value < timedelta(days=1):
		return "%d %s" % (ceil(value.seconds / 3600.0), value.seconds > 3600 and locales["hours"] or locales["hour"])
	else:
		return "%.3g %s" % (value.days, value.days > 1 and locales["days"] or locales["day"])
duration.is_safe = True

@register.filter
def duration_short(value):
	return duration(value, DURATIONS_SHORT)

@register.filter
def duration_shortcap(value):
	return duration(value, DURATIONS_SHORTCAP)


PRICE_TEMPLATE = '<span class="%(letter)s">%(amt)i<span class="price-hidden">%(letter)s</span></span>'
@register.filter
def price(value, autoescape=None):
	value = int(value)
	if not value:
		g, s, c = 0, 0, 0
	else:
		g = divmod(value, 10000)[0]
		s = divmod(value, 100)[0] % 100
		c = value % 100

	output = '<span class="price">%s %s %s</span>' % (
		g and PRICE_TEMPLATE % {"amt": g, "letter": "g", "alt": "Gold"} or "",
		s and PRICE_TEMPLATE % {"amt": s, "letter": "s", "alt": "Silver"} or "",
		c and PRICE_TEMPLATE % {"amt": c, "letter": "c", "alt": "Copper"} or "",
	)

	return safestring.mark_safe(output)
price.needs_autoescape = True

@register.filter
def mapify(locations, autoescape=None):
	locations = locations.filter(x__gt=0, y__gt=0).select_related()
	if not locations.count():
		return ""
	html_base = """
	<div id="map-container"></div>
	<script type="text/javascript">
	%s
	maplib.renderMaps([%s])
	</script>
	"""
	html_vars = """
	var %s = {
		name: %r,
		file: %r,
		nodes: %r
	}
	"""
	ret = {}
	for location in locations.all():
		key = "map_%i_%i" % (location.zone_id, abs(hash(location.zone.map)))
		if key not in ret:
			map = str(location.zone.map)
			if location.floor:
				map += str(location.floor)
			ret[key] = (str(location.zone.name), map, [])
		ret[key][2].append([location.x, location.y])
	vars_list = []
	for k in ret:
		vars_list.append(html_vars % (k, ret[k][0], ret[k][1], ret[k][2]))
	vars_html = "\n".join(vars_list)
	return html_base % (vars_html, ",".join(ret.keys()))
mapify.needs_autoescape = True


@register.filter
def supermark(value):
	if isinstance(value, float):
		return "%+f" % value
	else:
		return "%+i" % int(value)
supermark.is_safe = True


@register.filter
def url(value, text="", autoescape=None):
	url = hasattr(value, "get_absolute_url") and value.get_absolute_url()
	if url:
		classes = (hasattr(value, "get_htclasses") and ' class="%s"' % (value.get_htclasses())) or ""
		html = '<a href="%s"%s>%s</a>' % (url, classes, esc(str(text or value), autoescape=True))
		return safestring.mark_safe(html)
	text = text or value
	try:
		return esc(str(text), autoescape=True)
	except UnicodeError:
		return text.encode("ascii", "ignore")
url.needs_autoescape = True

@register.filter
def icon(value, arg=64, autoescape=None):
	try:
		arg = int(arg)
	except ValueError: # Invalid literal for int()
		return value # Fail silently
	BASE_URL = "http://db.mmo-champion.com"
	url = hasattr(value, "get_absolute_url") and value.get_absolute_url()
	if not url:
		return safestring.mark_safe(value)
	else:
		icon = value.icon or "temp"
		value = esc(str(value), autoescape)
		return safestring.mark_safe('<a href="%s" class="iconinline"><img src="http://static.mmo-champion.com/db/img/icons/%s.png" alt="%s" width="%i" height="%i"/></a>' % (url, icon, value, arg, arg))
icon.needs_autoescape = True

@register.filter
def iconize(value, arg="small", autoescape=None):
	if arg == "large":
		size = 40
	else:
		size = 16
	_icon = icon(value, size)
	_url = url(value)
	return safestring.mark_safe('<div class="iconized-%s"><div class="icon">%s</div> <span>%s</span></div>' % (arg, _icon, _url))
iconize.needs_autoescape = True

@register.filter
def screenshot(value, autoescape=None):
	if not value:
		return ""

	screenshot = value[0]
	url = screenshot.get_absolute_url()

	# Don't give it a size as its dynamic
	return safestring.mark_safe('<a id="screenshot-thumbnail" href="%s.jpg"><img src="%s.thumbnail.jpg" alt="%s"/></a>' % (url, url, screenshot.caption))
icon.needs_autoescape = True

@register.filter
def tooltip(obj, paperdoll, autoescape=None):
	return safestring.mark_safe(obj.tooltip(paperdoll))
tooltip.needs_autoescape = True


@register.filter
def str_repr(value):
	value = str(value)
	return repr(value)

@register.filter
def verbose_name(cls):
	return cls()._meta.verbose_name

@register.filter
def verbose_name_plural(cls):
	return cls()._meta.verbose_name_plural

@register.filter
@stringfilter
def truncate(value, arg):
	try:
		length = int(arg)
	except ValueError: # Invalid literal for int().
		return value # Fail silently.
	if len(value) > arg:
		value = value[:arg]
		if not value.endswith("..."):
			value += "..."
	return value


@register.tag
def sigrielisting(parser, token):
	try:
		cls, iterable = token.split_contents()[1:]
		iterable = parser.compile_filter(iterable)
	except ValueError:
		raise template.TemplateSyntaxError("%s tag requires two arguments" % token.contents[0])
	return SigrieListing(cls, iterable)

class SigrieListing(template.Node):
	def __init__(self, cls, iterable):
		self.cls = cls
		self.iterable = iterable

	def render(self, context):
		from sigrie.owdb import listings
		cls = getattr(listings, self.cls)
		iterable = self.iterable.resolve(context)
		return cls(iterable).render()
